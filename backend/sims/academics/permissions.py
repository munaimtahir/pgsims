from __future__ import annotations

from rest_framework import permissions

from sims.supervision.models import ResidentSupervisorAssignment


class IsAcademicAdminOrReadOnly(permissions.BasePermission):
    message = "Academic mutations are restricted to admins."

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(user.is_superuser or user.role == "ADMIN")


def can_view_resident_profile(user, resident_profile) -> bool:
    if not user or not user.is_authenticated:
        return False
    if user.is_superuser or user.role == "ADMIN":
        return True
    if user.role == "RESIDENT":
        return getattr(user, "resident_profile", None) and user.resident_profile.id == resident_profile.id
    if user.role == "SUPERVISOR":
        supervisor_profile = getattr(user, "supervisor_profile", None)
        if not supervisor_profile:
            return False
        return ResidentSupervisorAssignment.objects.filter(
            resident=resident_profile,
            supervisor=supervisor_profile,
            is_active=True,
        ).exists()
    return user.role == "SUPPORT_STAFF"


def can_view_supervisor_profile(user, supervisor_profile) -> bool:
    if not user or not user.is_authenticated:
        return False
    if user.is_superuser or user.role == "ADMIN":
        return True
    if user.role == "SUPERVISOR":
        return getattr(user, "supervisor_profile", None) and user.supervisor_profile.id == supervisor_profile.id
    if user.role == "RESIDENT":
        resident_profile = getattr(user, "resident_profile", None)
        if not resident_profile:
            return False
        return ResidentSupervisorAssignment.objects.filter(
            resident=resident_profile,
            supervisor=supervisor_profile,
            is_active=True,
        ).exists()
    return user.role == "SUPPORT_STAFF"
