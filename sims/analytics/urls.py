"""URL routing for analytics APIs."""

from django.urls import path

from sims.analytics.views import (
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
]
