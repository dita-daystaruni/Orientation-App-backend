from rest_framework.permissions import BasePermission, SAFE_METHODS

from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to only allow admins or parents to edit or delete an object.
    """

    def has_permission(self, request, view):
        # Allow any user to view (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True
        
        return request.user.is_authenticated and (request.user.user_type == 'admin' or request.user.user_type == 'parent')

class IsAuthenticatedReadOnly(BasePermission):
    """
    Custom permission to allow authenticated users to view.
    """

    def has_permission(self, request, view):
        # Allow any authenticated user to view (GET, HEAD, OPTIONS)
        return request.user.is_authenticated and request.method in SAFE_METHODS
