from django.urls import path

from . import views

app_name = "certificates"

urlpatterns = [
    # Main certificate views
    path("", views.CertificateListView.as_view(), name="list"),
    path("dashboard/", views.CertificateDashboardView.as_view(), name="dashboard"),
    path("create/", views.CertificateCreateView.as_view(), name="create"),
    path("<int:pk>/", views.CertificateDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", views.CertificateUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", views.CertificateDeleteView.as_view(), name="delete"),
    # Certificate review views
    path(
        "<int:certificate_pk>/review/", views.CertificateReviewCreateView.as_view(), name="review"
    ),
    path("review/<int:pk>/", views.CertificateReviewDetailView.as_view(), name="review_detail"),
    # Certificate management views
    path("bulk-approval/", views.BulkCertificateApprovalView.as_view(), name="bulk_approval"),
    path("compliance/", views.CertificateComplianceView.as_view(), name="compliance"),
    # File operations
    path("<int:pk>/download/", views.certificate_download, name="download"),
    # Export and reporting
    path("export/csv/", views.export_certificates_csv, name="export_csv"),
    # AJAX/API endpoints
    path("api/stats/", views.certificate_stats_api, name="stats_api"),
    path("api/quick-stats/", views.certificate_quick_stats, name="quick_stats_api"),
    path("api/<int:pk>/verify/", views.certificate_verification_api, name="verify_api"),
    path("api/update-statistics/", views.update_certificate_statistics, name="update_stats_api"),
]

# API URLs for mobile app and external integrations
api_urlpatterns = [
    # REST API endpoints would go here
    # These would be included in the main API routing
]
