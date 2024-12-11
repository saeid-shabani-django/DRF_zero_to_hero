import copy
from rest_framework import permissions

SAFE_METHODS = ("GET", "HEAD", "OPTIONS")


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or (request.user and request.user.is_staff)
        )


class SendPrivateEmail(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.has_perm("store.send_email"))
    

class CustomDjangoModelPermission(permissions.DjangoModelPermissions):
    def __init__(self):
        self.perms_map = copy.deepcopy(self.perms_map)
        self.perms_map['GET']=['%(app_label)s.view_%(model_name)s']






