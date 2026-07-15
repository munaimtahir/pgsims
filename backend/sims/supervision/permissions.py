from rest_framework import permissions


class IsSupervisionAdminOrReadOnly(permissions.BasePermission):
    """
    Admin has full read/write access.
    Resident and Supervisor have scoped read-only access.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        # Admin role gets full read/write access
        if request.user.role == "ADMIN":
            return True

        # Safe read operations are limited to the directly involved roles.
        if request.method in permissions.SAFE_METHODS:
            return request.user.role in ["RESIDENT", "SUPERVISOR"]

        return False
