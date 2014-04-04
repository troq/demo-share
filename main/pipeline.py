def set_is_connected(user, **kwargs):
    user.profile.is_connected = True
    user.profile.save()
