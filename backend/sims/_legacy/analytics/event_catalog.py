"""Canonical analytics event catalog and validation policy."""

from __future__ import annotations

from dataclasses import dataclass

MAX_METADATA_BYTES = 8192
MAX_STRING_VALUE_LEN = 200

BLOCKED_METADATA_KEY_TOKENS = {
    "name",
    "email",
    "phone",
    "mobile",
    "mrno",
    "address",
    "cnic",
    "dob",
    "patient",
    "password",
    "token",
}

DEFAULT_ALLOWED_METADATA_KEYS = {
    "source",
    "action",
    "reason",
    "error_code",
    "record_count",
    "failure_count",
    "resource",
    "path",
    "http_method",
    "status_code",
    "duration_ms",
    "tab",
    "feature",
    "sampled",
    "ip_hash",
    "event_source",
}


@dataclass(frozen=True)
class EventSpec:
    description: str
    required_metadata_keys: frozenset[str]
    allowed_metadata_keys: frozenset[str]
    allow_missing_hospital: bool = False
    ui_ingest_allowed: bool = False


def _spec(
    description: str,
    *,
    required_metadata_keys: set[str] | None = None,
    allowed_metadata_keys: set[str] | None = None,
    allow_missing_hospital: bool = False,
    ui_ingest_allowed: bool = False,
) -> EventSpec:
    merged_allowed = set(DEFAULT_ALLOWED_METADATA_KEYS)
    if allowed_metadata_keys:
        merged_allowed.update(allowed_metadata_keys)
    return EventSpec(
        description=description,
        required_metadata_keys=frozenset(required_metadata_keys or set()),
        allowed_metadata_keys=frozenset(merged_allowed),
        allow_missing_hospital=allow_missing_hospital,
        ui_ingest_allowed=ui_ingest_allowed,
    )


EVENT_CATALOG: dict[str, EventSpec] = {
    "auth.login.succeeded": _spec("Successful authentication event"),
    "auth.login.failed": _spec("Failed authentication event"),
    "auth.rbac.denied": _spec("Authorization denial"),
    "logbook.case.created": _spec("Logbook draft created"),
    "logbook.case.submitted": _spec("Logbook submitted for review"),
    "logbook.case.sent_back": _spec("Logbook returned by reviewer"),
    "logbook.case.resubmitted": _spec("Returned logbook resubmitted"),
    "logbook.case.verified": _spec("Logbook approved"),
    "logbook.case.rejected": _spec("Logbook rejected"),
    "logbook.status.transitioned": _spec("Logbook workflow state transition"),
    "data.import.started": _spec("Data import started"),
    "data.import.completed": _spec("Data import completed"),
    "data.import.failed": _spec("Data import failed"),
    "data.export.started": _spec("Data export started"),
    "data.export.completed": _spec("Data export completed"),
    "data.export.failed": _spec("Data export failed"),
    "system.job.started": _spec("Background job started"),
    "system.job.completed": _spec("Background job completed"),
    "system.job.failed": _spec("Background job failed"),
    "system.api.error": _spec(
        "API error sampled in middleware",
        allow_missing_hospital=True,
    ),
    "ui.page.view": _spec(
        "Analytics UI page view",
        required_metadata_keys={"tab"},
        ui_ingest_allowed=True,
    ),
    "ui.feature.used": _spec(
        "Analytics UI feature usage",
        required_metadata_keys={"feature"},
        ui_ingest_allowed=True,
    ),
    "research.project.created": _spec("Research project created"),
    "research.project.submitted": _spec("Research project submitted"),
}

UI_EVENT_MAP = {
    "page.view": "ui.page.view",
    "feature.used": "ui.feature.used",
    "ui.page.view": "ui.page.view",
    "ui.feature.used": "ui.feature.used",
}


def get_event_spec(event_type: str) -> EventSpec | None:
    return EVENT_CATALOG.get(event_type)


def is_ui_ingest_allowed(event_type: str) -> bool:
    spec = get_event_spec(event_type)
    return bool(spec and spec.ui_ingest_allowed)
