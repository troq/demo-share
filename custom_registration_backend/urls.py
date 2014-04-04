"""
This is the same urlconf as the simple backend using the custom
registration view instead of using the simple backend registration view 
"""


from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url
from django.views.generic.base import TemplateView

#this is the only line thats differernt than the simple urls.py
from custom_registration_backend.views import RegistrationView


urlpatterns = patterns('',
                       url(r'^register/$',
                           RegistrationView.as_view(),
                           name='registration_register'),
                       url(r'^register/closed/$',
                           TemplateView.as_view(template_name='registration/registration_closed.html'),
                           name='registration_disallowed'),
                       (r'', include('registration.auth_urls')),
                       )
