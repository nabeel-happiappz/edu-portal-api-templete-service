from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or admins to access it
    """
    
    def has_object_permission(self, request, view, obj):
        # Admin permissions
        if request.user.is_staff:
            return True
        
        # Handle UserProfile objects
        if hasattr(obj, 'user'):
            return obj.user == request.user
            
        # Handle User objects
        return obj == request.user


class IsAdminUser(permissions.BasePermission):
    """
    Permission to only allow admin users
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_staff
