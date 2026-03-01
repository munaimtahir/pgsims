"""Dimension resolver helpers for analytics entities."""

from __future__ import annotations

from typing import Any

from django.conf import settings


def _as_id(value: Any | None) -> int | None:
    if value is None:
        return None
    if isinstance(value, int):
        return value
    return int(getattr(value, "id", value))


def get_current_hospital_id(
    *,
    actor: Any | None = None,
    request: Any | None = None,
    explicit_hospital: Any | None = None,
) -> int | None:
    """Resolve canonical hospital_id in single-hospital mode (future switchable)."""

    explicit_id = _as_id(explicit_hospital)
    if explicit_id:
        return explicit_id

    if actor is not None:
        actor_hospital_id = getattr(actor, "home_hospital_id", None)
        if actor_hospital_id:
            return int(actor_hospital_id)

    if request is not None and getattr(request, "user", None) is not None:
        request_hospital_id = getattr(request.user, "home_hospital_id", None)
        if request_hospital_id:
            return int(request_hospital_id)

    default_hospital = getattr(settings, "ANALYTICS_DEFAULT_HOSPITAL_ID", None)
    if default_hospital:
        return int(default_hospital)

    from sims.rotations.models import Hospital

    fallback = Hospital.objects.filter(is_active=True).order_by("id").values_list("id", flat=True).first()
    return int(fallback) if fallback else None


def resolve_department_id(*, actor: Any | None = None, explicit_department: Any | None = None) -> int | None:
    explicit_id = _as_id(explicit_department)
    if explicit_id:
        return explicit_id
    if actor is not None and getattr(actor, "home_department_id", None):
        return int(actor.home_department_id)
    return None
