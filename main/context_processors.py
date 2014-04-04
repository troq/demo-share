from django.contrib.auth.forms import AuthenticationForm
from registration.forms import RegistrationForm

def login_and_register_forms(request):
    return {
        'login_form': AuthenticationForm(),
        'registration_form': RegistrationForm(),
    }
