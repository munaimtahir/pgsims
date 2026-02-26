"""Common permission classes shared across apps."""

from rest_framework import permissions


SAFE_METHODS = permissions.SAFE_METHODS


def _is_authenticated_user(user):
    return bool(user and user.is_authenticated)


def _role(user):
    return getattr(user, "role", None)


class IsPGUser(permissions.BasePermission):
    """Allows access only to users with the 'pg' role."""
    
    message = "Only PG users can access this resource."

    def has_permission(self, request, view):
        return _is_authenticated_user(request.user) and _role(request.user) == "pg"


class IsUTRMCAdminUser(permissions.BasePermission):
    """Allows access only to users with the 'utrmc_admin' role."""

    message = "Only UTRMC admins can access this resource."

    def has_permission(self, request, view):
        return _is_authenticated_user(request.user) and _role(request.user) == "utrmc_admin"


class CanViewPendingLogbookQueue(permissions.BasePermission):
    """Supervisors/admin/UTRMC oversight can view pending verification queue."""

    message = "Only supervisors, admins, and UTRMC oversight users can view pending entries."

    def has_permission(self, request, view):
        if not _is_authenticated_user(request.user):
            return False
        role = _role(request.user)
        return bool(request.user.is_superuser or role in {"supervisor", "admin", "utrmc_user", "utrmc_admin"})


class CanVerifyLogbookEntry(permissions.BasePermission):
    """Supervisors (assigned PG only) and admins can verify logbook entries."""

    message = "Only supervisors and admins can verify logbook entries."

    def has_permission(self, request, view):
        if not _is_authenticated_user(request.user):
            return False
        role = _role(request.user)
        return bool(request.user.is_superuser or role in {"supervisor", "admin"})

    def has_object_permission(self, request, view, obj):
        user = request.user
        if getattr(user, "is_superuser", False) or _role(user) == "admin":
            return True
        if _role(user) == "supervisor":
            return getattr(obj, "pg_id", None) and getattr(obj.pg, "supervisor_id", None) == user.id
        return False


class CanApproveRotationOverride(permissions.BasePermission):
    """Only UTRMC admins may approve inter-hospital rotation overrides."""

    message = "Only UTRMC admins can approve inter-hospital rotation overrides."

    def has_permission(self, request, view):
        return _is_authenticated_user(request.user) and _role(request.user) == "utrmc_admin"


class ReadAnyWriteAdminOrUTRMCAdmin(permissions.BasePermission):
    """Authenticated users may read; writes limited to admin/UTRMC admin."""

    message = "Write access is restricted to admin or UTRMC admin."

    def has_permission(self, request, view):
        if not _is_authenticated_user(request.user):
            return False
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user.is_superuser or _role(request.user) in {"admin", "utrmc_admin"})


class ReadAnyWriteAdminOnly(permissions.BasePermission):
    """Authenticated users may read; writes limited to admin."""

    message = "Write access is restricted to admin."

    def has_permission(self, request, view):
        if not _is_authenticated_user(request.user):
            return False
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user.is_superuser or _role(request.user) == "admin")


class ReadAnyWriteUTRMCAdmin(permissions.BasePermission):
    """Authenticated users may read; writes limited to UTRMC admin."""

    message = "Write access is restricted to UTRMC admin."

    def has_permission(self, request, view):
        if not _is_authenticated_user(request.user):
            return False
        if request.method in SAFE_METHODS:
            return True
        return _role(request.user) == "utrmc_admin"
