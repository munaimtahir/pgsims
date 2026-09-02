"""
Role-based access control decorators and mixins for SIMS
"""

from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


def _track_rbac_denied(request, required_roles: str, reason: str):
    pass  # analytics module removed


def admin_required(view_func):
    """Decorator to require admin role"""

    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_admin():
            messages.error(request, "You don't have permission to access this page.")
            _track_rbac_denied(request, "ADMIN", "admin_required")
            raise PermissionDenied("Admin access required")
        return view_func(request, *args, **kwargs)

    return wrapper


def supervisor_required(view_func):
    """Decorator to require supervisor role"""

    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_supervisor():
            messages.error(request, "You don't have permission to access this page.")
            _track_rbac_denied(request, "SUPERVISOR", "supervisor_required")
            raise PermissionDenied("Supervisor access required")
        return view_func(request, *args, **kwargs)

    return wrapper


def resident_required(view_func):
    """Decorator to require Resident role"""

    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_resident():
            messages.error(request, "You don't have permission to access this page.")
            _track_rbac_denied(request, "RESIDENT", "resident_required")
            raise PermissionDenied("Resident access required")
        return view_func(request, *args, **kwargs)

    return wrapper


def supervisor_or_admin_required(view_func):
    """
    Decorator for views that require either supervisor or admin role.
    """

    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not (request.user.is_supervisor() or request.user.is_admin()):
            messages.error(request, "You don't have permission to access this page.")
            _track_rbac_denied(request, "supervisor|admin", "supervisor_or_admin_required")
            raise PermissionDenied("Supervisor or Admin access required")
        return view_func(request, *args, **kwargs)

    return wrapper


class AdminRequiredMixin(LoginRequiredMixin):
    """Mixin to require admin role for class-based views"""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not request.user.is_admin():
            messages.error(request, "You don't have permission to access this page.")
            _track_rbac_denied(request, "ADMIN", "admin_mixin_required")
            raise PermissionDenied("Admin access required")

        return super().dispatch(request, *args, **kwargs)


class SupervisorRequiredMixin(LoginRequiredMixin):
    """Mixin to require supervisor role for class-based views"""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not request.user.is_supervisor():
            messages.error(request, "You don't have permission to access this page.")
            _track_rbac_denied(request, "SUPERVISOR", "supervisor_mixin_required")
            raise PermissionDenied("Supervisor access required")

        return super().dispatch(request, *args, **kwargs)


class ResidentRequiredMixin(LoginRequiredMixin):
    """Mixin to require Resident role for class-based views"""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not request.user.is_resident():
            messages.error(request, "You don't have permission to access this page.")
            _track_rbac_denied(request, "RESIDENT", "resident_mixin_required")
            raise PermissionDenied("Resident access required")

        return super().dispatch(request, *args, **kwargs)


class SupervisorOrAdminRequiredMixin(LoginRequiredMixin):
    """Mixin to require supervisor or admin role for class-based views"""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not (request.user.is_supervisor() or request.user.is_admin()):
            messages.error(request, "You don't have permission to access this page.")
            _track_rbac_denied(request, "supervisor|admin", "supervisor_or_admin_mixin_required")
            raise PermissionDenied("Supervisor or Admin access required")

        return super().dispatch(request, *args, **kwargs)


class RoleBasedAccessMixin(LoginRequiredMixin):
    """Mixin that allows specifying allowed roles"""

    allowed_roles = []  # Should be overridden in the view

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if self.allowed_roles and request.user.role not in self.allowed_roles:
            messages.error(request, "You don't have permission to access this page.")
            _track_rbac_denied(
                request,
                "|".join(self.allowed_roles),
                "role_based_mixin_required",
            )
            raise PermissionDenied(f"Access restricted to: {', '.join(self.allowed_roles)}")

        return super().dispatch(request, *args, **kwargs)
