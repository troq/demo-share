from registration.backends.simple.views import RegistrationView as SimpleRegistrationView
from django.http import HttpResponse
from django.template.loader import render_to_string
import simplejson as json

class RegistrationView(SimpleRegistrationView):
    def form_valid(self, request, form):
        #returns the json reponse for when the registration is successful
        new_user = self.register(request, **form.cleaned_data)
        
        response = {'success': True, 'logged_in_nav': render_to_string('main/snippets/logged_in_nav.html', {'user': new_user})}
        return self.json_response(response)

    def form_invalid(self, form, request=None):
        #returns the json reponse for when the registration is unsuccessful
        response = {'success': False, 'form': render_to_string('main/snippets/form.html', {'form': form})}
        return self.json_response(response)

    def json_response(self, response):
        #returns an http response of the response as a json
        return HttpResponse(json.dumps(response), content_type='application/json')
