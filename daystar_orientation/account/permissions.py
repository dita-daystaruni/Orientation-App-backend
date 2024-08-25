from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    """Custom permission to only allow admins to access the view."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'admin'
