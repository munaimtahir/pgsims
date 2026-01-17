"""Custom permission classes for logbook-related API views."""

from rest_framework import permissions


class IsPGUser(permissions.BasePermission):
    """Allows access only to users with the 'pg' role."""
    
    message = "Only PG users can access this resource."

    def has_permission(self, request, view):
        return getattr(request.user, "role", None) == "pg"
