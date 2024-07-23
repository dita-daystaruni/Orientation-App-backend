from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to only allow admins to edit or delete an object.
    """

    def has_permission(self, request, view):
        # Allow any user to view (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True
        
        # Only allow admins to create, update, or delete
        return request.user.is_authenticated and request.user.user_type == 'admin'

class IsAuthenticatedReadOnly(BasePermission):
    """
    Custom permission to allow authenticated users to view.
    """

    def has_permission(self, request, view):
        # Allow any authenticated user to view (GET, HEAD, OPTIONS)
        return request.user.is_authenticated and request.method in SAFE_METHODS
