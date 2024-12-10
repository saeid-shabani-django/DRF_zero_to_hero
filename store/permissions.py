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
