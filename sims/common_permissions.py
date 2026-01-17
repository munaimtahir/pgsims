"""Common permission classes shared across apps."""

from rest_framework import permissions


class IsPGUser(permissions.BasePermission):
    """Allows access only to users with the 'pg' role."""
    
    message = "Only PG users can access this resource."

    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            getattr(request.user, "role", None) == "pg"
        )
