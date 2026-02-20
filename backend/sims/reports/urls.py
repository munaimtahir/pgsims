"""Routing for reports API."""

from django.urls import path

from sims.reports.views import (
    ReportGenerateView,
    ReportTemplateListView,
    ScheduledReportDetailView,
    ScheduledReportListCreateView,
)

app_name = "reports_api"

urlpatterns = [
    path("templates/", ReportTemplateListView.as_view(), name="templates"),
    path("generate/", ReportGenerateView.as_view(), name="generate"),
    path("scheduled/", ScheduledReportListCreateView.as_view(), name="scheduled_list"),
    path(
        "scheduled/<int:pk>/",
        ScheduledReportDetailView.as_view(),
        name="scheduled_detail",
    ),
]
