"""Analytics event tracking helpers."""

from __future__ import annotations

import hashlib
import json
import logging
import random
import re
from typing import Any

from django.conf import settings
from django.db import IntegrityError
from django.utils import timezone

from sims.analytics.dimensions import get_current_hospital_id, resolve_department_id
from sims.analytics.event_catalog import (
    BLOCKED_METADATA_KEY_TOKENS,
    EVENT_CATALOG,
    MAX_METADATA_BYTES,
    MAX_STRING_VALUE_LEN,
    UI_EVENT_MAP,
    get_event_spec,
    is_ui_ingest_allowed,
)
from sims.analytics.models import AnalyticsEvent
from sims.analytics.models import AnalyticsValidationRejection

logger = logging.getLogger(__name__)

EVENT_TYPE_RE = re.compile(r"^[a-z]+(?:\.[a-z0-9_]+){2,}$")


def analytics_enabled() -> bool:
    return bool(getattr(settings, "ANALYTICS_ENABLED", True))


def should_sample(rate: float | None = None) -> bool:
    sample_rate = getattr(settings, "ANALYTICS_REQUEST_SAMPLING", 1.0) if rate is None else rate
    sample_rate = max(0.0, min(float(sample_rate), 1.0))
    return random.random() <= sample_rate


def normalize_ui_event_type(event_type: str) -> str:
    normalized = str(event_type or "").strip().lower()
    mapped = UI_EVENT_MAP.get(normalized)
    if not mapped or not is_ui_ingest_allowed(mapped):
        raise ValueError("Unsupported analytics UI event type.")
    return mapped


def normalize_event_type(event_type: str) -> str:
    normalized = str(event_type or "").strip().lower()
    if not EVENT_TYPE_RE.match(normalized):
        raise ValueError("Event type must follow verb.noun.action format.")
    return normalized


def hash_ip(ip_value: str | None) -> str | None:
    if not ip_value:
        return None
    digest = hashlib.sha256(f"{settings.SECRET_KEY}:{ip_value}".encode("utf-8")).hexdigest()
    return digest[:24]


def extract_request_id(request: Any | None) -> str | None:
    if request is None:
        return None
    request_id = getattr(request, "request_id", None)
    if request_id:
        return str(request_id)
    headers = getattr(request, "headers", None)
    if headers:
        return headers.get("X-Request-ID") or headers.get("x-request-id")
    return None


def _clean_metadata(metadata: dict[str, Any] | None) -> dict[str, Any]:
    if metadata is None:
        return {}
    if not isinstance(metadata, dict):
        raise ValueError("Metadata must be an object.")
    cleaned: dict[str, Any] = {}
    for key, value in metadata.items():
        key_text = str(key).strip().lower()
        if not key_text:
            raise ValueError("Metadata keys cannot be empty.")
        if any(token in key_text for token in BLOCKED_METADATA_KEY_TOKENS):
            raise ValueError(f"PII-like metadata key '{key_text}' is blocked.")
        if isinstance(value, str):
            cleaned[key_text] = value.strip()[:MAX_STRING_VALUE_LEN]
        elif isinstance(value, (int, float, bool)) or value is None:
            cleaned[key_text] = value
        else:
            cleaned[key_text] = str(value)[:MAX_STRING_VALUE_LEN]
    serialized = json.dumps(cleaned, sort_keys=True).encode("utf-8")
    if len(serialized) > MAX_METADATA_BYTES:
        raise ValueError("Metadata exceeds maximum allowed size.")
    return cleaned


def _resolve_dimension(actor: Any | None, explicit_department: Any | None, explicit_hospital: Any | None):
    from sims.academics.models import Department
    from sims.rotations.models import Hospital

    department_id = resolve_department_id(actor=actor, explicit_department=explicit_department)
    hospital_id = get_current_hospital_id(actor=actor, explicit_hospital=explicit_hospital)
    department = Department.objects.filter(pk=department_id).first() if department_id else None
    hospital = Hospital.objects.filter(pk=hospital_id).first() if hospital_id else None
    return department, hospital


def _validate_catalog_payload(
    *,
    event_type: str,
    metadata: dict[str, Any],
    hospital_id: int | None,
    allow_unlisted: bool,
) -> None:
    spec = get_event_spec(event_type)
    if spec is None and not allow_unlisted:
        raise ValueError(f"Unsupported analytics event type: {event_type}")
    if spec is None:
        return
    missing_required = [key for key in spec.required_metadata_keys if key not in metadata]
    if missing_required:
        raise ValueError(f"Missing required metadata keys: {', '.join(sorted(missing_required))}")
    unexpected = [key for key in metadata.keys() if key not in spec.allowed_metadata_keys]
    if unexpected:
        raise ValueError(f"Unexpected metadata keys: {', '.join(sorted(unexpected))}")
    if hospital_id is None and not spec.allow_missing_hospital:
        raise ValueError("hospital_id is required for analytics events.")


def record_validation_rejection(
    *,
    source: str,
    event_type: str | None,
    reason: str,
    actor_role: str = "",
    department_id: int | None = None,
    hospital_id: int | None = None,
    metadata_keys: list[str] | None = None,
) -> None:
    AnalyticsValidationRejection.objects.create(
        source=source,
        event_type=(event_type or "")[:120],
        reason=reason[:200],
        actor_role=(actor_role or "")[:32],
        department_id=department_id,
        hospital_id=hospital_id,
        metadata_keys=metadata_keys or [],
    )


def track_event(
    *,
    event_type: str,
    actor: Any | None = None,
    request: Any | None = None,
    department: Any | None = None,
    hospital: Any | None = None,
    entity_type: str | None = None,
    entity_id: str | int | None = None,
    status_from: str | None = None,
    status_to: str | None = None,
    request_id: str | None = None,
    event_key: str | None = None,
    metadata: dict[str, Any] | None = None,
    occurred_at=None,
    allow_unlisted: bool = False,
) -> AnalyticsEvent | None:
    if not analytics_enabled():
        return None

    normalized_type = normalize_event_type(event_type)

    resolved_request_id = request_id or extract_request_id(request)
    actor_role = getattr(actor, "role", "") if actor is not None else "anonymous"
    resolved_department, resolved_hospital = _resolve_dimension(actor, department, hospital)
    safe_metadata = _clean_metadata(metadata)
    if request is not None and "ip_hash" not in safe_metadata:
        ip_hash = hash_ip(getattr(request, "META", {}).get("REMOTE_ADDR"))
        if ip_hash:
            safe_metadata["ip_hash"] = ip_hash
    _validate_catalog_payload(
        event_type=normalized_type,
        metadata=safe_metadata,
        hospital_id=getattr(resolved_hospital, "id", None),
        allow_unlisted=allow_unlisted,
    )

    defaults = {
        "occurred_at": occurred_at or timezone.now(),
        "actor_user": actor,
        "actor_role": actor_role or "",
        "department": resolved_department,
        "hospital": resolved_hospital,
        "entity_type": entity_type,
        "entity_id": str(entity_id) if entity_id is not None else None,
        "status_from": status_from,
        "status_to": status_to,
        "request_id": resolved_request_id,
        "event_key": event_key,
        "metadata": safe_metadata,
    }
    if resolved_request_id and event_key:
        event, _ = AnalyticsEvent.objects.get_or_create(
            request_id=resolved_request_id,
            event_type=normalized_type,
            event_key=event_key,
            defaults=defaults,
        )
        return event
    return AnalyticsEvent.objects.create(event_type=normalized_type, **defaults)


def safe_track_event(**kwargs) -> AnalyticsEvent | None:
    try:
        return track_event(**kwargs)
    except (IntegrityError, ValueError, TypeError) as exc:
        actor = kwargs.get("actor")
        record_validation_rejection(
            source="safe_track_event",
            event_type=kwargs.get("event_type"),
            reason=str(exc),
            actor_role=getattr(actor, "role", "") if actor is not None else "",
            department_id=getattr(kwargs.get("department"), "id", None),
            hospital_id=getattr(kwargs.get("hospital"), "id", None),
            metadata_keys=sorted(list((kwargs.get("metadata") or {}).keys()))
            if isinstance(kwargs.get("metadata"), dict)
            else [],
        )
        logger.warning("analytics_event_dropped", extra={"error": str(exc), "event_type": kwargs.get("event_type")})
        return None
