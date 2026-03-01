"""Routing for reports API."""

from django.urls import path

from sims.reports.views import (
    ReportCatalogView,
    ReportExportView,
    ReportGenerateView,
    ReportRunView,
    ReportTemplateListView,
    ScheduledReportDetailView,
    ScheduledReportListCreateView,
)

app_name = "reports_api"

urlpatterns = [
    path("templates/", ReportTemplateListView.as_view(), name="templates"),
    path("catalog/", ReportCatalogView.as_view(), name="catalog"),
    path("run/<str:key>/", ReportRunView.as_view(), name="run"),
    path("export/<str:key>/", ReportExportView.as_view(), name="export"),
    path("generate/", ReportGenerateView.as_view(), name="generate"),
    path("scheduled/", ScheduledReportListCreateView.as_view(), name="scheduled_list"),
    path(
        "scheduled/<int:pk>/",
        ScheduledReportDetailView.as_view(),
        name="scheduled_detail",
    ),
]
