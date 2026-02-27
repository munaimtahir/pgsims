"""API views for the analytics module."""

from __future__ import annotations

from typing import Iterable, List

from django.conf import settings
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
    safe_track_event,
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
        if getattr(user, "role", None) == "supervisor" and getattr(
            settings, "ANALYTICS_ALLOW_SUPERVISOR_ACCESS", False
        ):
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
        payload = get_cached_tab_payload(tab, filters)
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
        payload = get_cached_tab_payload(tab, filters)
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
        payload = build_live_payload(filters, limit=min(limit, 200))
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

        event = safe_track_event(
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
        return Response(
            {"accepted": True, "event_id": str(event.id) if event is not None else None},
            status=status.HTTP_202_ACCEPTED,
        )


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
]
