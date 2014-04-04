from rest_framework.permissions import BasePermission

class IsAdminOrAjax(BasePermission):
    """
    Allows browseable api access only to admin users,
    but allows api access if request is ajax.
    """

    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return True

        return request.is_ajax()

class IsProfileUser(BasePermission):
    """
    Allows profile to be updated only if the profile is the user's
    """

    def has_object_permission(self, request, view, obj):
        return obj is None or request.user.profile == obj
