from registration.signals import user_registered

from main.models import Profile

def create_profile(user, **kwargs):
    Profile.objects.create(user=user)

user_registered.connect(create_profile, dispatch_uid='main.signals.create_profile')
