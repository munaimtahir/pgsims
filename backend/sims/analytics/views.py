"""API views for the analytics module."""

from __future__ import annotations

from typing import Iterable, List

from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from sims.analytics.serializers import (
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


__all__ = [
    "TrendAnalyticsView",
    "ComparativeAnalyticsView",
    "PerformanceMetricsView",
    "DashboardOverviewView",
    "DashboardTrendsView",
    "DashboardComplianceView",
]
