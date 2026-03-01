"""API URL routing for certificate endpoints."""

from django.urls import path
from sims.certificates.api_views import PGCertificatesListView, PGCertificateDownloadView

app_name = "certificates_api"

urlpatterns = [
    path("my/", PGCertificatesListView.as_view(), name="my_certificates"),
    path("my/<int:pk>/download/", PGCertificateDownloadView.as_view(), name="my_certificate_download"),
]
