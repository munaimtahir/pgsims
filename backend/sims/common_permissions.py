"""Common permission classes shared across apps."""

from rest_framework import permissions


SAFE_METHODS = permissions.SAFE_METHODS


def _is_authenticated_user(user):
    return bool(user and user.is_authenticated)


def _role(user):
    return getattr(user, "role", None)


def _track_rbac_denied(request, required_roles: str, reason: str):
    from sims.analytics.services import safe_track_event

    actor = request.user if _is_authenticated_user(request.user) else None
    safe_track_event(
        event_type="auth.rbac.denied",
        actor=actor,
        request=request,
        event_key=f"rbac:{request.method}:{request.path}:{required_roles}",
        metadata={
            "source": "permissions",
            "reason": reason,
            "action": required_roles,
            "path": request.path,
            "http_method": request.method,
        },
    )


class IsPGUser(permissions.BasePermission):
    """Allows access only to users with the 'pg' role."""

    message = "Only PG users can access this resource."

    def has_permission(self, request, view):
        allowed = _is_authenticated_user(request.user) and _role(request.user) == "pg"
        if not allowed:
            _track_rbac_denied(request, "pg", "pg_role_required")
        return allowed


class IsUTRMCAdminUser(permissions.BasePermission):
    """Allows access only to users with the 'utrmc_admin' role."""

    message = "Only UTRMC admins can access this resource."

    def has_permission(self, request, view):
        allowed = _is_authenticated_user(request.user) and _role(request.user) == "utrmc_admin"
        if not allowed:
            _track_rbac_denied(request, "utrmc_admin", "utrmc_admin_required")
        return allowed


class CanViewPendingLogbookQueue(permissions.BasePermission):
    """Supervisors/admin/UTRMC oversight can view pending verification queue."""

    message = "Only supervisors, admins, and UTRMC oversight users can view pending entries."

    def has_permission(self, request, view):
        if not _is_authenticated_user(request.user):
            _track_rbac_denied(request, "supervisor|admin|utrmc_user|utrmc_admin", "not_authenticated")
            return False
        role = _role(request.user)
        allowed = bool(
            request.user.is_superuser or role in {"supervisor", "admin", "utrmc_user", "utrmc_admin"}
        )
        if not allowed:
            _track_rbac_denied(request, "supervisor|admin|utrmc_user|utrmc_admin", "role_not_allowed")
        return allowed


class CanVerifyLogbookEntry(permissions.BasePermission):
    """Supervisors (assigned PG only) and admins can verify logbook entries."""

    message = "Only supervisors and admins can verify logbook entries."

    def has_permission(self, request, view):
        if not _is_authenticated_user(request.user):
            _track_rbac_denied(request, "supervisor|admin", "not_authenticated")
            return False
        role = _role(request.user)
        allowed = bool(request.user.is_superuser or role in {"supervisor", "admin"})
        if not allowed:
            _track_rbac_denied(request, "supervisor|admin", "role_not_allowed")
        return allowed

    def has_object_permission(self, request, view, obj):
        user = request.user
        if getattr(user, "is_superuser", False) or _role(user) == "admin":
            return True
        if _role(user) == "supervisor":
            allowed = getattr(obj, "pg_id", None) and getattr(obj.pg, "supervisor_id", None) == user.id
            if not allowed:
                _track_rbac_denied(request, "supervisor_assigned_pg", "object_scope_denied")
            return allowed
        _track_rbac_denied(request, "supervisor|admin", "object_role_not_allowed")
        return False


class CanApproveRotationOverride(permissions.BasePermission):
    """Only UTRMC admins may approve inter-hospital rotation overrides."""

    message = "Only UTRMC admins can approve inter-hospital rotation overrides."

    def has_permission(self, request, view):
        allowed = _is_authenticated_user(request.user) and _role(request.user) == "utrmc_admin"
        if not allowed:
            _track_rbac_denied(request, "utrmc_admin", "utrmc_admin_required")
        return allowed


class ReadAnyWriteAdminOrUTRMCAdmin(permissions.BasePermission):
    """Authenticated users may read; writes limited to admin/UTRMC admin."""

    message = "Write access is restricted to admin or UTRMC admin."

    def has_permission(self, request, view):
        if not _is_authenticated_user(request.user):
            _track_rbac_denied(request, "authenticated", "not_authenticated")
            return False
        if request.method in SAFE_METHODS:
            return True
        allowed = bool(request.user.is_superuser or _role(request.user) in {"admin", "utrmc_admin"})
        if not allowed:
            _track_rbac_denied(request, "admin|utrmc_admin", "write_denied")
        return allowed


class ReadAnyWriteAdminOnly(permissions.BasePermission):
    """Authenticated users may read; writes limited to admin."""

    message = "Write access is restricted to admin."

    def has_permission(self, request, view):
        if not _is_authenticated_user(request.user):
            _track_rbac_denied(request, "authenticated", "not_authenticated")
            return False
        if request.method in SAFE_METHODS:
            return True
        allowed = bool(request.user.is_superuser or _role(request.user) == "admin")
        if not allowed:
            _track_rbac_denied(request, "admin", "write_denied")
        return allowed


class ReadAnyWriteUTRMCAdmin(permissions.BasePermission):
    """Authenticated users may read; writes limited to UTRMC admin."""

    message = "Write access is restricted to UTRMC admin."

    def has_permission(self, request, view):
        if not _is_authenticated_user(request.user):
            _track_rbac_denied(request, "authenticated", "not_authenticated")
            return False
        if request.method in SAFE_METHODS:
            return True
        allowed = _role(request.user) == "utrmc_admin"
        if not allowed:
            _track_rbac_denied(request, "utrmc_admin", "write_denied")
        return allowed
