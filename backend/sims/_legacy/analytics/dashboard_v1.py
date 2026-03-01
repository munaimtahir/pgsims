"""Admin analytics v1 query helpers."""

from __future__ import annotations

import csv
import io
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from typing import Any

from django.conf import settings
from django.core.cache import cache
from django.db.models import Count, Q, Sum
from django.db.models.functions import TruncDate
from django.utils import timezone

from sims.academics.models import Department
from sims.analytics.models import AnalyticsDailyRollup, AnalyticsEvent
from sims.rotations.models import Hospital

ANALYTICS_CACHE_TTL = int(getattr(settings, "ANALYTICS_CACHE_TTL", 60))
ANALYTICS_ROLLUP_RANGE_DAYS = int(getattr(settings, "ANALYTICS_ROLLUP_RANGE_DAYS", 60))

TAB_KEYS = {
    "overview",
    "adoption",
    "logbook",
    "review-sla",
    "departments",
    "rotations",
    "research",
    "data-ops",
    "system",
    "security",
    "live",
}

ROLE_OPTIONS = ["pg", "supervisor", "admin", "utrmc_user", "utrmc_admin"]


@dataclass(frozen=True)
class AnalyticsFilters:
    start_date: date
    end_date: date
    department_id: int | None = None
    hospital_id: int | None = None
    role: str | None = None

    def cache_key(self) -> str:
        return (
            f"{self.start_date.isoformat()}:{self.end_date.isoformat()}:"
            f"d{self.department_id or 'all'}:h{self.hospital_id or 'all'}:r{self.role or 'all'}"
        )


def _parse_date(raw_value: str | None) -> date | None:
    if not raw_value:
        return None
    try:
        return date.fromisoformat(str(raw_value))
    except ValueError:
        return None


def _parse_int(raw_value: str | None) -> int | None:
    if raw_value in (None, ""):
        return None
    try:
        return int(raw_value)
    except (TypeError, ValueError):
        return None


def resolve_filters(query_params: Any) -> AnalyticsFilters:
    end_date = _parse_date(query_params.get("end_date")) or timezone.now().date()
    start_date = _parse_date(query_params.get("start_date")) or (end_date - timedelta(days=13))
    if start_date > end_date:
        start_date, end_date = end_date, start_date
    role = (query_params.get("role") or "").strip() or None
    if role and role not in ROLE_OPTIONS:
        role = None
    return AnalyticsFilters(
        start_date=start_date,
        end_date=end_date,
        department_id=_parse_int(query_params.get("department_id")),
        hospital_id=_parse_int(query_params.get("hospital_id")),
        role=role,
    )


def _range_bounds(filters: AnalyticsFilters):
    start_dt = timezone.make_aware(datetime.combine(filters.start_date, time.min))
    end_dt = timezone.make_aware(datetime.combine(filters.end_date + timedelta(days=1), time.min))
    return start_dt, end_dt


def _range_days(filters: AnalyticsFilters) -> int:
    return (filters.end_date - filters.start_date).days + 1


def event_queryset(filters: AnalyticsFilters):
    start_dt, end_dt = _range_bounds(filters)
    queryset = AnalyticsEvent.objects.filter(occurred_at__gte=start_dt, occurred_at__lt=end_dt)
    if filters.department_id:
        queryset = queryset.filter(department_id=filters.department_id)
    if filters.hospital_id:
        queryset = queryset.filter(hospital_id=filters.hospital_id)
    if filters.role:
        queryset = queryset.filter(actor_role=filters.role)
    return queryset


def _event_counts(filters: AnalyticsFilters, event_types: list[str]) -> dict[str, int]:
    if not event_types:
        return {}
    if not filters.role and _range_days(filters) > ANALYTICS_ROLLUP_RANGE_DAYS:
        rollup_qs = AnalyticsDailyRollup.objects.filter(
            day__gte=filters.start_date,
            day__lte=filters.end_date,
            event_type__in=event_types,
        )
        if filters.department_id:
            rollup_qs = rollup_qs.filter(department_id=filters.department_id)
        if filters.hospital_id:
            rollup_qs = rollup_qs.filter(hospital_id=filters.hospital_id)
        rollup_data = {
            row["event_type"]: int(row["total"])
            for row in rollup_qs.values("event_type").annotate(total=Sum("count"))
        }
        return {event_type: rollup_data.get(event_type, 0) for event_type in event_types}

    event_data = {
        row["event_type"]: int(row["total"])
        for row in event_queryset(filters)
        .filter(event_type__in=event_types)
        .values("event_type")
        .annotate(total=Count("id"))
    }
    return {event_type: event_data.get(event_type, 0) for event_type in event_types}


def _daily_series(filters: AnalyticsFilters, event_types: list[str]):
    if not filters.role and _range_days(filters) > ANALYTICS_ROLLUP_RANGE_DAYS:
        rollup_qs = AnalyticsDailyRollup.objects.filter(
            day__gte=filters.start_date,
            day__lte=filters.end_date,
            event_type__in=event_types,
        )
        if filters.department_id:
            rollup_qs = rollup_qs.filter(department_id=filters.department_id)
        if filters.hospital_id:
            rollup_qs = rollup_qs.filter(hospital_id=filters.hospital_id)
        return [
            {
                "day": row["day"].isoformat() if row["day"] else None,
                "event_type": row["event_type"],
                "count": int(row["count"]),
            }
            for row in rollup_qs.values("day", "event_type", "count").order_by("day", "event_type")
        ]

    queryset = (
        event_queryset(filters)
        .filter(event_type__in=event_types)
        .annotate(day=TruncDate("occurred_at"))
        .values("day", "event_type")
        .annotate(count=Count("id"))
        .order_by("day", "event_type")
    )
    return [
        {
            "day": row["day"].isoformat() if row["day"] else None,
            "event_type": row["event_type"],
            "count": int(row["count"]),
        }
        for row in queryset
    ]


def _table_from_counts(counts: dict[str, int]):
    return {
        "columns": ["event_type", "count"],
        "rows": [{"event_type": key, "count": value} for key, value in counts.items()],
    }


def _build_common_payload(filters: AnalyticsFilters, title: str, counts: dict[str, int], series=None):
    total_events = sum(counts.values())
    cards = [
        {"key": "total_events", "title": "Total Events", "value": total_events},
        {"key": "unique_event_types", "title": "Event Types", "value": len([v for v in counts.values() if v > 0])},
    ]
    return {
        "title": title,
        "date_range": {
            "start_date": filters.start_date.isoformat(),
            "end_date": filters.end_date.isoformat(),
        },
        "cards": cards,
        "table": _table_from_counts(counts),
        "series": series or [],
    }


def _review_sla_payload(filters: AnalyticsFilters):
    submissions = (
        event_queryset(filters)
        .filter(event_type__in=["logbook.case.submitted", "logbook.case.resubmitted"])
        .exclude(entity_id__isnull=True)
        .values("entity_id", "occurred_at")
        .order_by("entity_id", "occurred_at")
    )
    reviews = (
        event_queryset(filters)
        .filter(event_type__in=["logbook.case.verified", "logbook.case.sent_back", "logbook.case.rejected"])
        .exclude(entity_id__isnull=True)
        .values("entity_id", "event_type", "occurred_at")
        .order_by("entity_id", "occurred_at")
    )

    first_submission: dict[str, datetime] = {}
    for row in submissions:
        entity_id = str(row["entity_id"])
        first_submission.setdefault(entity_id, row["occurred_at"])

    durations: list[float] = []
    rows = []
    for row in reviews:
        entity_id = str(row["entity_id"])
        submitted_at = first_submission.get(entity_id)
        if submitted_at is None:
            continue
        duration_hours = max(0.0, (row["occurred_at"] - submitted_at).total_seconds() / 3600)
        durations.append(duration_hours)
        rows.append(
            {
                "entity_id": entity_id,
                "review_event": row["event_type"],
                "submitted_at": submitted_at.isoformat(),
                "reviewed_at": row["occurred_at"].isoformat(),
                "hours_to_review": round(duration_hours, 2),
            }
        )
        first_submission.pop(entity_id, None)

    average_hours = round(sum(durations) / len(durations), 2) if durations else 0.0
    return {
        "title": "Review / SLA",
        "date_range": {
            "start_date": filters.start_date.isoformat(),
            "end_date": filters.end_date.isoformat(),
        },
        "cards": [
            {"key": "avg_review_hours", "title": "Avg Review Time (hours)", "value": average_hours},
            {"key": "reviewed_items", "title": "Reviewed Items", "value": len(rows)},
        ],
        "table": {
            "columns": ["entity_id", "review_event", "submitted_at", "reviewed_at", "hours_to_review"],
            "rows": rows,
        },
        "series": [],
    }


def _group_payload(filters: AnalyticsFilters, group_type: str):
    if group_type == "departments":
        rows = (
            event_queryset(filters)
            .values("department_id", "department__name")
            .annotate(count=Count("id"))
            .order_by("-count", "department__name")
        )
        table_rows = [
            {
                "department_id": row["department_id"],
                "department_name": row["department__name"] or "Unassigned",
                "count": int(row["count"]),
            }
            for row in rows
        ]
        return {
            "title": "Departments",
            "date_range": {
                "start_date": filters.start_date.isoformat(),
                "end_date": filters.end_date.isoformat(),
            },
            "cards": [
                {"key": "departments_active", "title": "Departments with Activity", "value": len(table_rows)},
            ],
            "table": {"columns": ["department_id", "department_name", "count"], "rows": table_rows},
            "series": [],
        }

    rows = (
        event_queryset(filters)
        .values("hospital_id", "hospital__name")
        .annotate(count=Count("id"))
        .order_by("-count", "hospital__name")
    )
    table_rows = [
        {
            "hospital_id": row["hospital_id"],
            "hospital_name": row["hospital__name"] or "Unassigned",
            "count": int(row["count"]),
        }
        for row in rows
    ]
    return {
        "title": "Rotations / Hospital Distribution",
        "date_range": {
            "start_date": filters.start_date.isoformat(),
            "end_date": filters.end_date.isoformat(),
        },
        "cards": [
            {"key": "hospitals_active", "title": "Hospitals with Activity", "value": len(table_rows)},
        ],
        "table": {"columns": ["hospital_id", "hospital_name", "count"], "rows": table_rows},
        "series": [],
    }


def build_tab_payload(tab: str, filters: AnalyticsFilters):
    if tab not in TAB_KEYS:
        raise ValueError(f"Unsupported analytics tab: {tab}")

    if tab == "overview":
        event_types = [
            "auth.login.succeeded",
            "auth.login.failed",
            "logbook.case.created",
            "logbook.case.submitted",
            "data.import.completed",
            "data.export.completed",
        ]
        counts = _event_counts(filters, event_types)
        payload = _build_common_payload(filters, "Overview", counts, _daily_series(filters, event_types[:3]))
        payload["cards"].extend(
            [
                {"key": "successful_logins", "title": "Login Success", "value": counts["auth.login.succeeded"]},
                {"key": "logbook_submissions", "title": "Logbook Submissions", "value": counts["logbook.case.submitted"]},
            ]
        )
        return payload

    if tab == "adoption":
        event_types = ["ui.page.view", "ui.feature.used"]
        counts = _event_counts(filters, event_types)
        payload = _build_common_payload(filters, "Adoption", counts, _daily_series(filters, event_types))
        payload["cards"].append({"key": "feature_usage", "title": "Feature Usage", "value": counts["ui.feature.used"]})
        return payload

    if tab == "logbook":
        event_types = [
            "logbook.case.created",
            "logbook.case.submitted",
            "logbook.case.sent_back",
            "logbook.case.resubmitted",
            "logbook.case.verified",
            "logbook.case.rejected",
            "logbook.status.transitioned",
        ]
        return _build_common_payload(filters, "Logbook", _event_counts(filters, event_types), _daily_series(filters, event_types[:4]))

    if tab == "review-sla":
        return _review_sla_payload(filters)

    if tab == "departments":
        return _group_payload(filters, "departments")

    if tab == "rotations":
        return _group_payload(filters, "rotations")

    if tab == "research":
        event_types = ["research.project.created", "research.project.submitted"]
        return _build_common_payload(filters, "Research", _event_counts(filters, event_types), [])

    if tab == "data-ops":
        event_types = [
            "data.import.started",
            "data.import.completed",
            "data.import.failed",
            "data.export.started",
            "data.export.completed",
            "data.export.failed",
        ]
        return _build_common_payload(filters, "Data Ops", _event_counts(filters, event_types), _daily_series(filters, event_types))

    if tab == "system":
        event_types = ["system.api.error", "system.job.started", "system.job.completed", "system.job.failed"]
        return _build_common_payload(filters, "System", _event_counts(filters, event_types), _daily_series(filters, event_types))

    if tab == "security":
        event_types = ["auth.login.failed", "auth.rbac.denied"]
        return _build_common_payload(filters, "Security", _event_counts(filters, event_types), _daily_series(filters, event_types))

    if tab == "live":
        live_payload = build_live_payload(filters, limit=200)
        return {
            "title": "Live",
            "date_range": live_payload["date_range"],
            "cards": [
                {"key": "live_events", "title": "Events (Latest Window)", "value": len(live_payload["events"])},
            ],
            "table": {
                "columns": ["occurred_at", "event_type", "actor_role", "department_id", "hospital_id", "entity_id"],
                "rows": live_payload["events"],
            },
            "series": [],
        }

    return _build_common_payload(filters, "Overview", {}, [])


def get_cached_tab_payload(tab: str, filters: AnalyticsFilters, cache_scope: str = "global"):
    cache_key = f"analytics:v1:tab:{tab}:{cache_scope}:{filters.cache_key()}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached
    payload = build_tab_payload(tab, filters)
    cache.set(cache_key, payload, ANALYTICS_CACHE_TTL)
    return payload


def build_live_payload(
    filters: AnalyticsFilters,
    *,
    limit: int = 200,
    cursor: str | None = None,
    event_type_prefix: str | None = None,
    entity_type: str | None = None,
):
    bounded_limit = max(1, min(int(limit), 200))
    queryset = event_queryset(filters).select_related("department", "hospital")
    if event_type_prefix:
        queryset = queryset.filter(event_type__startswith=event_type_prefix.strip().lower())
    if entity_type:
        queryset = queryset.filter(entity_type=entity_type.strip().lower())
    if cursor:
        try:
            raw_occurred_at, raw_id = cursor.split("|", 1)
            cursor_at = datetime.fromisoformat(raw_occurred_at)
            if timezone.is_naive(cursor_at):
                cursor_at = timezone.make_aware(cursor_at)
            queryset = queryset.filter(
                Q(occurred_at__gt=cursor_at) | (Q(occurred_at=cursor_at) & Q(id__gt=raw_id))
            )
        except (TypeError, ValueError):
            pass
    queryset = queryset.order_by("-occurred_at", "-id")[:bounded_limit]
    events = [
        {
            "id": str(event.id),
            "occurred_at": event.occurred_at.isoformat(),
            "event_type": event.event_type,
            "actor_role": event.actor_role,
            "department_id": event.department_id,
            "hospital_id": event.hospital_id,
            "entity_type": event.entity_type,
            "entity_id": event.entity_id,
            "drilldown_url": _entity_drilldown_url(event),
            "status_from": event.status_from,
            "status_to": event.status_to,
            "metadata": event.metadata,
        }
        for event in queryset
    ]
    return {
        "date_range": {
            "start_date": filters.start_date.isoformat(),
            "end_date": filters.end_date.isoformat(),
        },
        "cursor": f"{events[0]['occurred_at']}|{events[0]['id']}" if events else (cursor or None),
        "events": events,
    }


def _entity_drilldown_url(event: AnalyticsEvent) -> str | None:
    if not event.entity_id:
        return None
    if event.entity_type == "logbook_entry":
        return f"/dashboard/supervisor/logbooks?entry_id={event.entity_id}"
    if event.entity_type == "clinical_case":
        return f"/dashboard/supervisor/cases?case_id={event.entity_id}"
    return None


def filter_options_payload():
    cache_key = "analytics:v1:filter-options"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached
    payload = {
        "roles": ROLE_OPTIONS,
        "departments": [
            {"id": dept.id, "name": dept.name}
            for dept in Department.objects.filter(active=True).order_by("name")
        ],
        "hospitals": [
            {"id": hospital.id, "name": hospital.name}
            for hospital in Hospital.objects.filter(is_active=True).order_by("name")
        ],
    }
    cache.set(cache_key, payload, ANALYTICS_CACHE_TTL)
    return payload


def tab_payload_to_csv(tab_payload: dict[str, Any]) -> str:
    table = tab_payload.get("table", {})
    columns = table.get("columns", [])
    rows = table.get("rows", [])
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(columns)
    for row in rows:
        writer.writerow([row.get(column, "") if isinstance(row, dict) else "" for column in columns])
    return output.getvalue()
