"""Custom permission classes for user-related API views."""

from rest_framework import permissions


class IsSupervisor(permissions.BasePermission):
    """Allows access only to users with the 'supervisor' role."""
    
    message = "Only supervisors can access this resource."

    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            getattr(request.user, "role", None) == "supervisor"
        )
