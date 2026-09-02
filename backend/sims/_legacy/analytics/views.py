"""API views for the analytics module."""

from __future__ import annotations

from typing import Iterable, List

from django.conf import settings
from django.db.models import Count
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework import status, throttling
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from sims.academics.models import Department
from sims.analytics.dashboard_v1 import (
    TAB_KEYS,
    build_live_payload,
    filter_options_payload,
    get_cached_tab_payload,
    resolve_filters,
    tab_payload_to_csv,
)
from sims.analytics.event_catalog import EVENT_CATALOG
from sims.analytics.event_tracking import record_validation_rejection, track_event
from sims.analytics.models import AnalyticsEvent, AnalyticsValidationRejection
from sims.analytics.serializers import (
    AnalyticsFiltersSerializer,
    AnalyticsLivePayloadSerializer,
    AnalyticsTabPayloadSerializer,
    AnalyticsUIEventIngestSerializer,
    ComparativeResponseSerializer,
    DashboardComplianceSerializer,
    DashboardOverviewSerializer,
    DashboardTrendsSerializer,
    PerformanceMetricsSerializer,
    TrendPointSerializer,
    TrendResponseSerializer,
)
from sims.analytics.services import (
    TrendRequest,
    comparative_summary,
    dashboard_compliance,
    dashboard_overview,
    dashboard_trends,
    get_accessible_users,
    performance_metrics,
    trend_for_user,
    validate_window,
)
from sims.rotations.models import Hospital

User = get_user_model()


class TrendPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = "page_size"
    max_page_size = 180


class TrendAnalyticsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        window = validate_window(request.query_params.get("window"))
        metric = request.query_params.get("metric", "entries")
        include_moving_average = request.query_params.get("moving_average", "true").lower() in {
            "1",
            "true",
            "yes",
        }
        params = TrendRequest(
            window=window, metric=metric, include_moving_average=include_moving_average
        )

        try:
            target_user = self._get_target_user(request)
        except PermissionError as exc:  # pragma: no cover - defensive branch
            raise PermissionDenied(str(exc)) from exc
        status_filter: List[str] = [s for s in request.query_params.getlist("status") if s]

        data = trend_for_user(
            request.user, target_user, params, status_filter=status_filter or None
        )

        paginator = TrendPagination()
        paginated = paginator.paginate_queryset(data["series"], request)
        if paginated is not None:
            serializer = TrendPointSerializer(paginated, many=True)
            payload = {
                "metric": data["metric"],
                "window": data["window"],
                "series": serializer.data,
                "count": paginator.page.paginator.count,
                "next": paginator.get_next_link(),
                "previous": paginator.get_previous_link(),
            }
            return Response(payload)

        serializer = TrendResponseSerializer(data)
        return Response(serializer.data)

    def _get_target_user(self, request: Request) -> User:
        target_param = request.query_params.get("user_id")
        if target_param:
            accessible = get_accessible_users(request.user)
            try:
                return accessible.get(pk=target_param)
            except accessible.model.DoesNotExist as exc:
                raise PermissionDenied("You cannot access this user's analytics") from exc
        return request.user


class ComparativeAnalyticsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        primary_users = self._resolve_users(request, "primary_users")
        secondary_users = self._resolve_users(request, "secondary_users")
        metric = request.query_params.get("metric", "entries")

        try:
            aggregates = comparative_summary(
                request.user, primary_users, secondary_users, metric=metric
            )
        except PermissionError as exc:
            raise PermissionDenied(str(exc)) from exc
        serializer = ComparativeResponseSerializer(aggregates)
        return Response(serializer.data)

    def _resolve_users(self, request: Request, param_name: str) -> Iterable[User]:
        ids = [pk for pk in request.query_params.get(param_name, "").split(",") if pk]
        if not ids:
            if param_name == "primary_users":
                return [request.user]
            return []
        accessible = get_accessible_users(request.user)
        return accessible.filter(pk__in=ids)


class PerformanceMetricsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        metrics = performance_metrics(request.user)
        serializer = PerformanceMetricsSerializer(metrics)
        return Response(serializer.data)


class DashboardOverviewView(APIView):
    """API endpoint for dashboard overview data."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        overview = dashboard_overview(request.user)
        serializer = DashboardOverviewSerializer(overview)
        return Response(serializer.data)


class DashboardTrendsView(APIView):
    """API endpoint for monthly trends data (last 12 months)."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        trends = dashboard_trends(request.user)
        serializer = DashboardTrendsSerializer(trends)
        return Response(serializer.data)


class DashboardComplianceView(APIView):
    """API endpoint for compliance data by rotation."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        compliance = dashboard_compliance(request.user)
        serializer = DashboardComplianceSerializer(compliance)
        return Response(serializer.data)


class AnalyticsAccessPermission(permissions.BasePermission):
    message = "Analytics access is restricted to admin users."

    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated):
            return False
        if user.is_superuser or getattr(user, "role", None) == "admin":
            return True
        supervisor_enabled = getattr(
            settings,
            "ANALYTICS_SUPERVISOR_ACCESS_ENABLED",
            getattr(settings, "ANALYTICS_ALLOW_SUPERVISOR_ACCESS", False),
        )
        if getattr(user, "role", None) == "supervisor" and supervisor_enabled:
            return True
        return False


class AnalyticsUIIngestRateThrottle(throttling.UserRateThrottle):
    rate = getattr(settings, "ANALYTICS_UI_INGEST_RATE", "120/min")


class AnalyticsFiltersView(APIView):
    permission_classes = [permissions.IsAuthenticated, AnalyticsAccessPermission]

    def get(self, request: Request) -> Response:
        if not getattr(settings, "ANALYTICS_ENABLED", True):
            return Response({"detail": "Analytics is disabled."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        payload = filter_options_payload()
        serializer = AnalyticsFiltersSerializer(payload)
        return Response(serializer.data)


class AnalyticsTabView(APIView):
    permission_classes = [permissions.IsAuthenticated, AnalyticsAccessPermission]

    def get(self, request: Request, tab: str) -> Response:
        if not getattr(settings, "ANALYTICS_ENABLED", True):
            return Response({"detail": "Analytics is disabled."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        if tab not in TAB_KEYS:
            return Response({"detail": "Unknown analytics tab."}, status=status.HTTP_404_NOT_FOUND)
        filters = resolve_filters(request.query_params)
        payload = get_cached_tab_payload(
            tab,
            filters,
            cache_scope=f"user:{request.user.id}:role:{getattr(request.user, 'role', '')}",
        )
        serializer = AnalyticsTabPayloadSerializer(payload)
        return Response(serializer.data)


class AnalyticsTabExportView(APIView):
    permission_classes = [permissions.IsAuthenticated, AnalyticsAccessPermission]

    def get(self, request: Request, tab: str) -> Response:
        if not getattr(settings, "ANALYTICS_ENABLED", True):
            return Response({"detail": "Analytics is disabled."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        if tab not in TAB_KEYS:
            return Response({"detail": "Unknown analytics tab."}, status=status.HTTP_404_NOT_FOUND)
        filters = resolve_filters(request.query_params)
        payload = get_cached_tab_payload(
            tab,
            filters,
            cache_scope=f"user:{request.user.id}:role:{getattr(request.user, 'role', '')}",
        )
        csv_text = tab_payload_to_csv(payload)
        response = HttpResponse(csv_text, content_type="text/csv")
        response["Content-Disposition"] = f'attachment; filename="analytics-{tab}.csv"'
        return response


class AnalyticsLiveView(APIView):
    permission_classes = [permissions.IsAuthenticated, AnalyticsAccessPermission]

    def get(self, request: Request) -> Response:
        if not getattr(settings, "ANALYTICS_ENABLED", True):
            return Response({"detail": "Analytics is disabled."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        filters = resolve_filters(request.query_params)
        limit = int(request.query_params.get("limit", 200))
        payload = build_live_payload(
            filters,
            limit=min(limit, 200),
            cursor=request.query_params.get("cursor"),
            event_type_prefix=request.query_params.get("event_type_prefix"),
            entity_type=request.query_params.get("entity_type"),
        )
        serializer = AnalyticsLivePayloadSerializer(payload)
        return Response(serializer.data)


class AnalyticsEventIngestView(APIView):
    permission_classes = [permissions.IsAuthenticated, AnalyticsAccessPermission]
    throttle_classes = [AnalyticsUIIngestRateThrottle]

    def post(self, request: Request) -> Response:
        if not getattr(settings, "ANALYTICS_ENABLED", True):
            return Response({"detail": "Analytics is disabled."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        if not getattr(settings, "ANALYTICS_UI_INGEST_ENABLED", False):
            return Response({"detail": "Analytics UI ingest is disabled."}, status=status.HTTP_403_FORBIDDEN)

        serializer = AnalyticsUIEventIngestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated = serializer.validated_data

        department = None
        if validated.get("department_id"):
            department = Department.objects.filter(pk=validated["department_id"], active=True).first()
            if department is None:
                return Response({"detail": "Invalid department_id"}, status=status.HTTP_400_BAD_REQUEST)

        hospital = None
        if validated.get("hospital_id"):
            hospital = Hospital.objects.filter(pk=validated["hospital_id"], is_active=True).first()
            if hospital is None:
                return Response({"detail": "Invalid hospital_id"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            event = track_event(
                event_type=validated["event_type"],
                actor=request.user,
                request=request,
                department=department,
                hospital=hospital,
                entity_type=validated.get("entity_type") or None,
                entity_id=validated.get("entity_id") or None,
                event_key=validated.get("event_key") or validated["event_type"],
                metadata={
                    **(validated.get("metadata") or {}),
                    "event_source": "ui_ingest",
                },
                occurred_at=validated.get("occurred_at"),
            )
        except ValueError as exc:
            record_validation_rejection(
                source="ui_ingest",
                event_type=validated.get("event_type"),
                reason=str(exc),
                actor_role=getattr(request.user, "role", ""),
                department_id=getattr(department, "id", None),
                hospital_id=getattr(hospital, "id", None),
                metadata_keys=sorted(list((validated.get("metadata") or {}).keys())),
            )
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"accepted": True, "event_id": str(event.id) if event is not None else None},
            status=status.HTTP_202_ACCEPTED,
        )


class AnalyticsQualityView(APIView):
    permission_classes = [permissions.IsAuthenticated, AnalyticsAccessPermission]

    def get(self, request: Request) -> Response:
        if not getattr(settings, "ANALYTICS_ENABLED", True):
            return Response({"detail": "Analytics is disabled."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        filters = resolve_filters(request.query_params)
        range_days = max((filters.end_date - filters.start_date).days + 1, 1)
        start_dt, end_dt = _bounds(filters.start_date, filters.end_date)
        baseline_start = start_dt - (end_dt - start_dt)
        baseline_end = start_dt

        current_total = AnalyticsEvent.objects.filter(occurred_at__gte=start_dt, occurred_at__lt=end_dt).count()
        baseline_total = AnalyticsEvent.objects.filter(
            occurred_at__gte=baseline_start, occurred_at__lt=baseline_end
        ).count()
        baseline_per_day = baseline_total / range_days if baseline_total else 0.0
        current_per_day = current_total / range_days
        anomaly = "stable"
        if baseline_per_day > 0 and current_per_day >= baseline_per_day * 2:
            anomaly = "spike"
        elif baseline_per_day > 0 and current_per_day <= baseline_per_day * 0.5:
            anomaly = "drop"

        rejections = list(
            AnalyticsValidationRejection.objects.filter(created_at__gte=start_dt, created_at__lt=end_dt)
            .values("event_type", "reason")
            .annotate(total=Count("id"))
            .order_by("-total")[:10]
        )
        missing_hospital = AnalyticsEvent.objects.filter(
            occurred_at__gte=start_dt, occurred_at__lt=end_dt, hospital__isnull=True
        ).count()
        missing_department = AnalyticsEvent.objects.filter(
            occurred_at__gte=start_dt, occurred_at__lt=end_dt, department__isnull=True
        ).count()

        drift_counts: dict[str, int] = {}
        for event in AnalyticsEvent.objects.filter(occurred_at__gte=start_dt, occurred_at__lt=end_dt).only(
            "event_type", "metadata"
        )[:1000]:
            spec = EVENT_CATALOG.get(event.event_type)
            if not spec or not isinstance(event.metadata, dict):
                continue
            for key in event.metadata.keys():
                if key not in spec.allowed_metadata_keys:
                    drift_counts[key] = drift_counts.get(key, 0) + 1

        payload = {
            "anomaly": {
                "status": anomaly,
                "current_events": current_total,
                "baseline_events": baseline_total,
                "current_per_day": round(current_per_day, 2),
                "baseline_per_day": round(baseline_per_day, 2),
            },
            "top_rejections": rejections,
            "missing_dimensions": {
                "missing_hospital": missing_hospital,
                "missing_department": missing_department,
            },
            "schema_drift": [
                {"metadata_key": key, "count": value}
                for key, value in sorted(drift_counts.items(), key=lambda item: item[1], reverse=True)[:20]
            ],
        }
        return Response(payload)


def _bounds(start_date, end_date):
    from datetime import datetime, time, timedelta
    from django.utils import timezone

    start_dt = timezone.make_aware(datetime.combine(start_date, time.min))
    end_dt = timezone.make_aware(datetime.combine(end_date + timedelta(days=1), time.min))
    return start_dt, end_dt


__all__ = [
    "TrendAnalyticsView",
    "ComparativeAnalyticsView",
    "PerformanceMetricsView",
    "DashboardOverviewView",
    "DashboardTrendsView",
    "DashboardComplianceView",
    "AnalyticsFiltersView",
    "AnalyticsTabView",
    "AnalyticsTabExportView",
    "AnalyticsLiveView",
    "AnalyticsEventIngestView",
    "AnalyticsQualityView",
]
