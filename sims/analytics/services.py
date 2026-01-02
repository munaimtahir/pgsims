"""Service layer for advanced analytics computations."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from typing import Dict, Iterable, List, Optional, Sequence

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db import models
from django.db.models import Avg, Count, DurationField, ExpressionWrapper, F, Max, QuerySet

from sims.logbook.models import LogbookEntry

User = get_user_model()

ALLOWED_WINDOWS: Sequence[int] = (7, 30, 90)
CACHE_TIMEOUT_SECONDS = 300


@dataclass(frozen=True)
class TrendRequest:
    """Parameters for building trend analytics."""

    window: int
    metric: str = "entries"
    include_moving_average: bool = True

    def cache_key(self, user_id: int, extra_filters: Optional[str] = None) -> str:
        suffix = f"::{extra_filters}" if extra_filters else ""
        return f"analytics:trend:{user_id}:{self.metric}:{self.window}{suffix}"


def validate_window(raw_window: Optional[str]) -> int:
    """Validate and normalise the rolling window parameter."""

    window = 30 if raw_window is None else int(raw_window)
    if window not in ALLOWED_WINDOWS:
        raise ValueError(f"Window must be one of {', '.join(map(str, ALLOWED_WINDOWS))}")
    return window


def get_accessible_users(user: User) -> QuerySet[User]:
    """Return a queryset of users visible to the acting user."""

    if user.is_superuser or getattr(user, "role", None) == "admin":
        return User.objects.all()
    if getattr(user, "role", None) == "supervisor":
        return User.objects.filter(models.Q(id=user.id) | models.Q(supervisor=user))
    return User.objects.filter(id=user.id)


def _base_logbook_queryset() -> QuerySet[LogbookEntry]:
    return (
        LogbookEntry.objects.select_related("pg", "supervisor", "rotation")
        .prefetch_related("procedures", "skills")
        .all()
    )


def trend_for_user(
    acting_user: User,
    target_user: User,
    params: TrendRequest,
    status_filter: Optional[Sequence[str]] = None,
) -> Dict[str, List[Dict[str, Optional[float]]]]:
    """Compute a rolling trend for a user with caching."""

    from django.db.models import Q

    if target_user not in get_accessible_users(acting_user):
        raise PermissionError("You do not have permission to view this user's analytics.")

    cache_key = params.cache_key(
        target_user.pk, extra_filters="|".join(status_filter) if status_filter else None
    )
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    window_delta = params.window - 1
    queryset = _base_logbook_queryset().filter(pg=target_user)
    if status_filter:
        queryset = queryset.filter(status__in=status_filter)

    latest_entry_date = queryset.aggregate(max_date=Max("date"))["max_date"]
    if latest_entry_date is None:
        payload = {"series": [], "window": params.window, "metric": params.metric}
        cache.set(cache_key, payload, CACHE_TIMEOUT_SECONDS)
        return payload

    start_date = latest_entry_date - timedelta(days=window_delta)
    queryset = queryset.filter(date__gte=start_date)

    daily_counts = (
        queryset.values("date")
        .annotate(
            value=Count("id"),
            approved=Count("id", filter=Q(status="approved")),
            avg_score=Avg("supervisor_assessment_score"),
        )
        .order_by("date")
    )

    series: List[Dict[str, Optional[float]]] = []
    rolling_window: List[int] = []

    for bucket in daily_counts:
        bucket_date = bucket["date"]
        count = int(bucket["value"])
        rolling_window.append(count)
        if len(rolling_window) > params.window:
            rolling_window.pop(0)
        moving_average = (
            sum(rolling_window) / len(rolling_window) if params.include_moving_average else None
        )
        series.append(
            {
                "date": bucket_date.isoformat(),
                "count": count,
                "approved": int(bucket["approved"]),
                "avg_score": (
                    float(bucket["avg_score"]) if bucket["avg_score"] is not None else None
                ),
                "moving_average": (
                    round(moving_average, 2) if moving_average is not None else None
                ),
            }
        )

    payload: Dict[str, List[Dict[str, Optional[float]]]] = {
        "series": series,
        "window": params.window,
        "metric": params.metric,
    }
    cache.set(cache_key, payload, CACHE_TIMEOUT_SECONDS)
    return payload


def comparative_summary(
    acting_user: User,
    primary_users: Iterable[User],
    secondary_users: Iterable[User],
    metric: str = "entries",
) -> Dict[str, Dict[str, float]]:
    """Build comparative analytics between two groups of users."""

    allowed_users = get_accessible_users(acting_user)
    allowed_ids = set(allowed_users.values_list("id", flat=True))
    primary_ids = [user.pk for user in primary_users if user.pk in allowed_ids]
    secondary_ids = [user.pk for user in secondary_users if user.pk in allowed_ids]

    if not primary_ids:
        raise PermissionError("No primary users available with your permissions.")
    if not secondary_ids:
        raise PermissionError("No secondary users available with your permissions.")

    queryset = _base_logbook_queryset()

    aggregates = {
        "primary": _comparative_block(queryset, primary_ids, metric),
        "secondary": _comparative_block(queryset, secondary_ids, metric),
    }
    return aggregates


def _comparative_block(
    queryset: QuerySet[LogbookEntry], user_ids: Sequence[int], metric: str
) -> Dict[str, float]:
    subset = queryset.filter(pg_id__in=user_ids)
    total_entries = subset.count()
    approved_count = subset.filter(status="approved").count()
    average_score = subset.aggregate(avg=Avg("supervisor_assessment_score"))["avg"] or 0.0
    if metric == "approval_rate":
        value: float = approved_count / total_entries if total_entries else 0.0
    elif metric == "avg_score":
        value = float(average_score)
    else:
        value = float(total_entries)

    return {
        "value": round(value, 2),
        "total_entries": total_entries,
        "approved": approved_count,
        "average_score": round(float(average_score), 2) if average_score else 0.0,
    }


def performance_metrics(
    acting_user: User, queryset: Optional[QuerySet[LogbookEntry]] = None
) -> Dict[str, float]:
    """Return KPI style metrics for the performance dashboard."""

    if queryset is None:
        accessible_users = get_accessible_users(acting_user)
        queryset = _base_logbook_queryset().filter(pg__in=accessible_users)

    total_entries = queryset.count()
    pending = queryset.filter(status="pending").count()
    approved = queryset.filter(status="approved").count()
    rejected = queryset.filter(status="rejected").count()

    review_durations = queryset.filter(
        submitted_to_supervisor_at__isnull=False, supervisor_action_at__isnull=False
    ).annotate(
        review_duration=ExpressionWrapper(
            F("supervisor_action_at") - F("submitted_to_supervisor_at"),
            output_field=DurationField(),
        )
    )
    average_review_hours = 0.0
    if review_durations.exists():
        total_seconds = sum(
            duration["review_duration"].total_seconds()
            for duration in review_durations.values("review_duration")
        )
        average_review_hours = round(total_seconds / (len(review_durations) * 3600), 2)

    approval_rate = round(approved / total_entries, 2) if total_entries else 0.0
    rejection_rate = round(rejected / total_entries, 2) if total_entries else 0.0
    pending_rate = round(pending / total_entries, 2) if total_entries else 0.0

    return {
        "total_entries": float(total_entries),
        "pending": float(pending),
        "approved": float(approved),
        "approval_rate": approval_rate,
        "rejection_rate": rejection_rate,
        "pending_rate": pending_rate,
        "average_review_hours": average_review_hours,
    }


def dashboard_overview(user: User) -> Dict:
    """
    Get dashboard overview with totals and recent activity.

    Returns:
        - total_residents: count of PG users
        - active_rotations: count of active rotations
        - pending_certificates: count of pending certificates
        - last_30d_logs: count of logbook entries in last 30 days
        - last_30d_cases: count of cases in last 30 days
        - unverified_logs: count of unverified logbook entries
    """
    from datetime import datetime, timedelta
    from sims.rotations.models import Rotation
    from sims.certificates.models import Certificate
    from sims.cases.models import ClinicalCase

    thirty_days_ago = datetime.now() - timedelta(days=30)

    # Base queries - scope by user role
    if user.is_superuser or getattr(user, "role", None) == "admin":
        users_qs = User.objects.all()
        rotations_qs = Rotation.objects.all()
        certificates_qs = Certificate.objects.all()
        logs_qs = LogbookEntry.objects.all()
        cases_qs = ClinicalCase.objects.all()
    elif getattr(user, "role", None) == "supervisor":
        supervised_users = User.objects.filter(supervisor=user)
        users_qs = supervised_users
        rotations_qs = Rotation.objects.filter(pg__in=supervised_users)
        certificates_qs = Certificate.objects.filter(resident__in=supervised_users)
        logs_qs = LogbookEntry.objects.filter(user__in=supervised_users)
        cases_qs = ClinicalCase.objects.filter(pg__in=supervised_users)
    else:
        # PG user - own data only
        users_qs = User.objects.filter(id=user.id)
        rotations_qs = Rotation.objects.filter(pg=user)
        certificates_qs = Certificate.objects.filter(resident=user)
        logs_qs = LogbookEntry.objects.filter(user=user)
        cases_qs = ClinicalCase.objects.filter(pg=user)

    return {
        "total_residents": users_qs.filter(role="pg").count(),
        "active_rotations": rotations_qs.filter(status="ongoing").count(),
        "pending_certificates": certificates_qs.filter(status="pending").count(),
        "last_30d_logs": logs_qs.filter(date__gte=thirty_days_ago).count(),
        "last_30d_cases": cases_qs.filter(created_at__gte=thirty_days_ago).count(),
        "unverified_logs": logs_qs.filter(verified_by__isnull=True).count(),
    }


def dashboard_trends(user: User) -> Dict:
    """
    Get monthly trends for last 12 months by department.

    Returns data grouped by month and department with case/log counts.
    """
    from datetime import datetime, timedelta
    from django.db.models import Count
    from django.db.models.functions import TruncMonth
    from sims.cases.models import ClinicalCase

    twelve_months_ago = datetime.now() - timedelta(days=365)

    # Scope by user role
    if user.is_superuser or getattr(user, "role", None) == "admin":
        logs_qs = LogbookEntry.objects.all()
        cases_qs = ClinicalCase.objects.all()
    elif getattr(user, "role", None) == "supervisor":
        supervised_users = User.objects.filter(supervisor=user)
        logs_qs = LogbookEntry.objects.filter(user__in=supervised_users)
        cases_qs = ClinicalCase.objects.filter(pg__in=supervised_users)
    else:
        logs_qs = LogbookEntry.objects.filter(user=user)
        cases_qs = ClinicalCase.objects.filter(pg=user)

    # Get log counts by month and rotation department
    log_trends = (
        logs_qs.filter(date__gte=twelve_months_ago)
        .select_related("rotation__department")
        .annotate(month=TruncMonth("date"))
        .values("month", "rotation__department__name")
        .annotate(log_count=Count("id"))
        .order_by("month", "rotation__department__name")
    )

    # Get case counts by month and category
    case_trends = (
        cases_qs.filter(created_at__gte=twelve_months_ago)
        .select_related("category")
        .annotate(month=TruncMonth("created_at"))
        .values("month", "category__name")
        .annotate(case_count=Count("id"))
        .order_by("month", "category__name")
    )

    # Merge trends
    trends_dict = {}
    for item in log_trends:
        month_str = item["month"].strftime("%Y-%m") if item["month"] else "N/A"
        dept = item["rotation__department__name"] or "Unassigned"
        key = (month_str, dept)
        if key not in trends_dict:
            trends_dict[key] = {
                "month": month_str,
                "department": dept,
                "log_count": 0,
                "case_count": 0,
            }
        trends_dict[key]["log_count"] = item["log_count"]

    for item in case_trends:
        month_str = item["month"].strftime("%Y-%m") if item["month"] else "N/A"
        dept = item["category__name"] or "Unassigned"
        key = (month_str, dept)
        if key not in trends_dict:
            trends_dict[key] = {
                "month": month_str,
                "department": dept,
                "log_count": 0,
                "case_count": 0,
            }
        trends_dict[key]["case_count"] = item["case_count"]

    return {"trends": list(trends_dict.values())}


def dashboard_compliance(user: User) -> Dict:
    """
    Get compliance data showing % verified vs unverified logs by rotation.
    """
    from sims.rotations.models import Rotation

    # Scope by user role
    if user.is_superuser or getattr(user, "role", None) == "admin":
        rotations = Rotation.objects.all()
    elif getattr(user, "role", None) == "supervisor":
        supervised_users = User.objects.filter(supervisor=user)
        rotations = Rotation.objects.filter(pg__in=supervised_users)
    else:
        rotations = Rotation.objects.filter(pg=user)

    compliance_data = []
    for rotation in rotations:
        logs = LogbookEntry.objects.filter(rotation=rotation)
        total = logs.count()
        verified = logs.filter(verified_by__isnull=False).count()

        if total > 0:
            percentage = round((verified / total) * 100, 2)
        else:
            percentage = 0.0

        # Create a descriptive name for the rotation
        rotation_desc = f"{rotation.department.name} - {rotation.hospital.name}"

        compliance_data.append(
            {
                "rotation_name": rotation_desc,
                "total_logs": total,
                "verified_logs": verified,
                "verification_percentage": percentage,
            }
        )

    return {"compliance": compliance_data}


__all__ = [
    "TrendRequest",
    "trend_for_user",
    "comparative_summary",
    "performance_metrics",
    "validate_window",
    "get_accessible_users",
    "dashboard_overview",
    "dashboard_trends",
    "dashboard_compliance",
]
