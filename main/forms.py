"""    !!!!!!!!!!!!!!!"""
"""    there are todos"""
"""    !!!!!!!!!!!!!!!"""
from django import forms
from django.template.defaultfilters import slugify

from main.models import Tshirt, Color, Payment
from main.tasks import set_tshirt_image, create_customer

class PaymentForm(forms.ModelForm):
    stripe_token = forms.CharField(widget=forms.HiddenInput(), max_length=255)
    class Meta:
        model = Payment
        fields = [
            'tshirt_size',
            'email',
            'shipping_name',
            'shipping_country',
            'shipping_city',
            'shipping_street',
            'shipping_state',
            'shipping_zip',
        ]
        widgets = {
            'email': forms.HiddenInput(),
            'shipping_name': forms.HiddenInput(),
            'shipping_country': forms.HiddenInput(),
            'shipping_city': forms.HiddenInput(),
            'shipping_street': forms.HiddenInput(),
            'shipping_state': forms.HiddenInput(),
            'shipping_zip': forms.HiddenInput(),
        }

    def __init__(self, tshirt=None, *args, **kwargs):
        self.tshirt = tshirt
        super(PaymentForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.instance.tshirt = self.tshirt
        new_payment = super(PaymentForm, self).save(*args, **kwargs) 
        create_customer.delay(new_payment.pk, self.cleaned_data['stripe_token'])
        return new_payment


class TshirtForm(forms.ModelForm):

    base_tshirt_id = forms.IntegerField(widget=forms.HiddenInput(), min_value=1)
    base_tshirt_color = forms.CharField(widget=forms.HiddenInput(), min_length='7', max_length='7')

    design = forms.CharField(widget=forms.HiddenInput())
    design_back = forms.CharField(widget=forms.HiddenInput())

    min_orders = forms.IntegerField(required=False, min_value=5, max_value=4999, initial=50, label="Minimum order",
        error_messages={
            'min_value': 'The minimum order goal must be at least 5.',
            'max_value': 'The maximum order goal must be at most 4999.',
        }
    )

    days_left = forms.IntegerField(required=False, min_value=5, max_value=100, label='Days left',
        error_messages={
            'min_value': 'The minimum days left must be at least 5.',
            'max_value': 'The maximum days left must be at most 100.',
        }
    )

    class Meta:
        model = Tshirt
        fields = [
            'title',
            'description',
            'tags',
            'selling_price',
            'min_orders',
            'days_left',
        ]

        widgets = {
            'description': forms.Textarea(attrs={'rows':3}),
        }

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(TshirtForm, self).__init__(*args, **kwargs)

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        if len(tags) > 10:
            raise forms.ValidationError("There is a 10 tag limit on each shirt.")
        for tag in tags:
            if len(tag) > 25:
                raise forms.ValidationError("Tags must be at most 25 characters long.")
        return tags

    def clean(self):
        cleaned_data = super(TshirtForm, self).clean()

        #checks if min_orders and days_left are provided 
        min_orders = cleaned_data.get('min_orders')
        days_left = cleaned_data.get('days_left')
        if not min_orders:
            msg = 'Min orders is required.'
            self._errors['min_orders'] = self.error_class([msg])
            del cleaned_data['min_orders']
        if not days_left:
            msg = 'Days left are required.'
            self._errors['days_left'] = self.error_class([msg])
            del cleaned_data['days_left']

        #checks if title can be converted to valid slug
        title = cleaned_data.get('title')
        if not slugify(title):
            msg = 'Title must contain at least one of the following: letters, numbers, underscores, or hyphens.'
            self._errors['title'] = self.error_class([msg])
            del cleaned_data['title']

        #sets cleaned_data['color'] to the Color object gotten from base_tshirt_id and base_tshirt_color
        base_tshirt_id = cleaned_data.get('base_tshirt_id')
        base_tshirt_color = cleaned_data.get('base_tshirt_color')
        try:
            #gets the Color from the base_tshirt_id and base_tshirt_color
            color = Color.objects.get(basetshirt__id=base_tshirt_id, code=base_tshirt_color)
        except Color.DoesNotExist:
            #error shouldn't occur unless user modifies website
            raise forms.ValidationError('Unexpected error (1). Please email support.')
        else:
            #puts the Color object into the cleaned_data
            cleaned_data['color'] = color

        return cleaned_data

    def save(self, *args, **kwargs):
        #sets the new tshirt user
        self.instance.user = self.user

        #todo: calculate the number of colors in the design somehow for base price
        #todo: sets the base price, right now just an arbitrary val of 10
        self.instance.base_price = 10

        #sets the new tshirt Color object
        self.instance.color = self.cleaned_data['color']

        #important! this assumes that commit=True is passed bc the pk is needed for the celery task set_tshirt_image
        new_tshirt = super(TshirtForm, self).save(*args, **kwargs) 

        #creates and sets the new tshirt image using celery
        #todo: change the background tshirt image depending on base tshirt type
        set_tshirt_image.delay(
            ('tshirt', self.cleaned_data['base_tshirt_color'], self.cleaned_data['design']),
            ('tshirt_back', self.cleaned_data['base_tshirt_color'], self.cleaned_data['design_back']),
            new_tshirt.pk) 

        return new_tshirt
