from __future__ import annotations

from typing import Optional

from django.http import HttpRequest

from .models import ActivityLog


def log_view(
    request: HttpRequest, verb: str, *, target=None, metadata=None, sensitive=False
) -> None:
    """Helper for logging read/view operations."""

    if not request:
        return

    ActivityLog.log(
        actor=(
            getattr(request, "user", None)
            if getattr(request, "user", None) and request.user.is_authenticated
            else None
        ),
        action="view",
        verb=verb,
        target=target,
        metadata=metadata or {},
        ip_address=_get_ip(request),
        is_sensitive=sensitive,
    )


def log_mutation(
    request: Optional[HttpRequest],
    verb: str,
    *,
    target=None,
    metadata=None,
    action: str = "update",
    sensitive: bool = False,
) -> None:
    """Helper for logging write operations."""

    ActivityLog.log(
        actor=(
            getattr(request, "user", None)
            if request and getattr(request, "user", None) and request.user.is_authenticated
            else None
        ),
        action=action,
        verb=verb,
        target=target,
        metadata=metadata or {},
        ip_address=_get_ip(request) if request else None,
        is_sensitive=sensitive,
    )


def _get_ip(request: Optional[HttpRequest]) -> Optional[str]:
    if not request:
        return None
    return request.META.get("HTTP_X_FORWARDED_FOR", request.META.get("REMOTE_ADDR"))
