"""URL routing for analytics APIs."""

from django.urls import path

from sims.analytics.views import (
    AnalyticsEventIngestView,
    AnalyticsFiltersView,
    AnalyticsLiveView,
    AnalyticsTabExportView,
    AnalyticsTabView,
    ComparativeAnalyticsView,
    DashboardComplianceView,
    DashboardOverviewView,
    DashboardTrendsView,
    PerformanceMetricsView,
    TrendAnalyticsView,
)

app_name = "analytics_api"

urlpatterns = [
    path("trends/", TrendAnalyticsView.as_view(), name="trends"),
    path("comparative/", ComparativeAnalyticsView.as_view(), name="comparative"),
    path("performance/", PerformanceMetricsView.as_view(), name="performance"),
    path("dashboard/overview/", DashboardOverviewView.as_view(), name="dashboard-overview"),
    path("dashboard/trends/", DashboardTrendsView.as_view(), name="dashboard-trends"),
    path("dashboard/compliance/", DashboardComplianceView.as_view(), name="dashboard-compliance"),
    path("events/", AnalyticsEventIngestView.as_view(), name="events-ingest"),
    path("v1/filters/", AnalyticsFiltersView.as_view(), name="v1-filters"),
    path("v1/tabs/<str:tab>/", AnalyticsTabView.as_view(), name="v1-tab"),
    path("v1/tabs/<str:tab>/export/", AnalyticsTabExportView.as_view(), name="v1-tab-export"),
    path("v1/live/", AnalyticsLiveView.as_view(), name="v1-live"),
]
