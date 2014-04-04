"""    !!!!!!!!!!!!!!!"""
"""    there are todos"""
"""    !!!!!!!!!!!!!!!"""

""" gotcha:
when a new tshirt is created the image temporarily isn't valid for a few secs,
so tshirts w/o images must be filtered
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.views.generic.base import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse
from django.conf import settings

import stripe
import easypost
import simplejson as json
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from endless_pagination.decorators import page_template

from main.models import Tshirt, BaseTshirt, Profile
from main.forms import TshirtForm, PaymentForm
from main.serializers import BaseTshirtSerializer, ProfileSerializer
from main.permissions import IsProfileUser
from main.utils import base_price
from main.tasks import complete_campaign

easypost.api_key = settings.EASYPOST_SECRET

from_address = easypost.Address.retrieve(settings.EASYPOST_FROM_ADDRESS_ID)

class ProfileUpdate(generics.UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsProfileUser,)

class BaseTshirtList(generics.ListAPIView):
    queryset = BaseTshirt.objects.order_by('white_price')
    serializer_class = BaseTshirtSerializer

@api_view(['GET'])
def base_price_view(request):
    #calculates base price from canvas json
    num_orders = int(request.QUERY_PARAMS.get('num_orders'))
    num_colors = int(request.QUERY_PARAMS.get('num_colors'))
    base_tshirt_id = request.QUERY_PARAMS.get('base_tshirt_id')
    base_tshirt_color = request.QUERY_PARAMS.get('base_tshirt_color')
    if num_orders >= 1 and num_colors >= 0 and base_tshirt_id and base_tshirt_color:
        price = base_price(num_orders, num_colors, base_tshirt_id, base_tshirt_color)
        return Response({'base_price': price})
    else:
        return Response({'Please don\'t edit the website': 'A required field(s) was not included'}, status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def shipping_cost_view(request):
    #calculates shipping cost given the shipping address
    street = request.QUERY_PARAMS.get('street')
    zipcode = request.QUERY_PARAMS.get('zip')
    to_address = easypost.Address.create(
        street1=street,
        zip=zipcode,
    )
    try:
        to_address = to_address.verify()
    except:
        return Response({'success': False})
    parcel = easypost.Parcel.create(
        predefined_package='flat',
        weight=7,
    )
    shipment = easypost.Shipment.create(
        to_address=to_address,
        from_address=from_address,
        parcel=parcel,
    )
    rates = []
    for r in shipment.rates:
        r_dict = r.to_dict()
        rates.append({'est': r_dict.est_delivery_days, 'service': r_dict.service, 'rate': r_dict.rate})
    return Response({'success': True, 'rates': rates})

@api_view(['GET'])
def popular_tags_view(request):
    #returns a list of the 100 most popular tshirt tags
    tags = Tshirt.tags.most_common().values('name', 'num_times')

    query = request.QUERY_PARAMS.get('q')
    if query:
        tags = tags.filter(name__istartswith=query)

    num_tags = int(request.QUERY_PARAMS.get('num', 0))
    if 0 < num_tags <= 100:
        tags = tags[:num_tags]
    else:
        tags = tags[:100]

    return Response(tags)
    

def ajax_login(request):
    if request.method == 'POST':
        request.session.set_test_cookie()
        login_form = AuthenticationForm(request, request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            response = {'success': True, 'logged_in_nav': render_to_string('main/snippets/logged_in_nav.html', {'user': user})}
        else:
            response = {'success': False, 'form': render_to_string('main/snippets/form.html', {'form': login_form})}
        return HttpResponse(json.dumps(response), content_type='application/json')


class TshirtPage(View):
    """this provides the custom tshirt page and handles the tshirt payment"""

    def get(self, request, tshirt_pk, slug=None):
        tshirt = get_object_or_404(Tshirt, pk=tshirt_pk)
        if tshirt.slug != slug:
            return redirect('main:tshirt_page', permanent=True, tshirt_pk=tshirt.pk, slug=tshirt.slug)

        
        similar_tshirts = []
        completed_tshirts = 0
        for similar_tshirt in tshirt.tags.similar_objects():
            if similar_tshirt.image:
                similar_tshirts.append(similar_tshirt)
                completed_tshirts += 1
                if completed_tshirts == 4:
                    break

        context = {
            'tshirt': tshirt,
            'similar_tshirts': similar_tshirts,
            'firebase_tshirt_url': settings.FIREBASE_URL+str(tshirt.pk),
            'pub_key': settings.STRIPE_PUB_KEY,
            'form': PaymentForm(),
        }

        return render(request, 'main/tshirt.html', context)

    def post(self, request, tshirt_pk, slug=None):
        tshirt = get_object_or_404(Tshirt, pk=tshirt_pk)

        form = PaymentForm(tshirt, request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(json.dumps({'success': True}), content_type='application/json')
        return HttpResponse(json.dumps({'success': False}), content_type='application/json')


    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, *args, **kwargs):
        return super(TshirtPage, self).dispatch(*args, **kwargs)

class Designer(View):
    """this provides the designer page and handles the creation of new tshirts"""

    def get(self, request):
        """this renders the designer page"""
        form = TshirtForm()
        return render(request, 'main/designer.html', {'form': form})

    def post(self, request):
        """this handles the tshirt form submission to create a new Tshirt"""
        form = TshirtForm(request.user, request.POST)
        if form.is_valid():
            new_tshirt = form.save()
            complete_campaign.apply_async((new_tshirt.pk,), countdown=new_tshirt.days_left*86400)

            response = {
                'success': True, 
                'tshirt_page_url': reverse('main:tshirt_page', kwargs={'tshirt_pk':new_tshirt.pk, 'slug':new_tshirt.slug}),
            }
        else:
            response = {
                'success' : False,
                'form_part_1': render_to_string('main/snippets/tshirt_form.html', {'form': form, 'part': 1}),
                'form_part_2': render_to_string('main/snippets/tshirt_form.html', {'form': form, 'part': 2}),
            }

        return HttpResponse(json.dumps(response), content_type='application/json')

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, *args, **kwargs):
        return super(Designer, self).dispatch(*args, **kwargs)

@page_template('main/snippets/tshirt_showcase_pagination.html')
@page_template('main/snippets/tshirt_detailed_pagination.html', key='detailed_pagination')
@ensure_csrf_cookie
def profile(request, user_pk, template='main/profile.html', extra_context=None):
    user = get_object_or_404(User, pk=user_pk)

    if request.user == user:
        private_profile = True
    else:
        private_profile = False

    context = {
        'private_profile': private_profile,
        'profile_user': user,
        'tshirts': Tshirt.objects.filter(user=user).order_by('-date_created'),
    }

    if extra_context is not None:
        context.update(extra_context)

    return render(request, template, context)

@page_template('main/snippets/tshirt_shop_pagination.html')
@ensure_csrf_cookie
def shop(request, extra_context=None):
    tag_filter = request.GET.get('filter')
    tshirts = Tshirt.objects.exclude(image='').order_by('-date_created')
    if tag_filter:
        tshirts = tshirts.filter(tags__name__in=[tag_filter])
    context = {
        'tshirts': tshirts,
        'TSHIRT_SHOP_PAGINATION_PER_PAGE': settings.TSHIRT_SHOP_PAGINATION_PER_PAGE,
    }

    if extra_context is not None:
        context.update(extra_context)

    return render(request, 'main/shop.html', context)

@ensure_csrf_cookie
def howitworks(request):
    return render(request, 'main/howitworks.html')

@ensure_csrf_cookie
def about(request):
    return render(request, 'main/about.html')

@ensure_csrf_cookie
def home(request):
    return redirect('main:designer', permanent=True)
