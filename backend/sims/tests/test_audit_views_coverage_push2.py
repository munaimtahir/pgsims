"""Coverage for sims/audit/views.py (ActivityLogViewSet, AuditReportViewSet) — untested
before this file. Uses APIClient against the router-registered /api/audit/ routes.
"""
import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from sims.audit.models import ActivityLog, AuditReport

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_user():
    return User.objects.create_superuser(
        username="audit_push2_admin", password="password123", role="ADMIN"
    )


@pytest.fixture
def plain_user():
    return User.objects.create_user(
        username="audit_push2_plain", password="password123", role="RESIDENT"
    )


@pytest.mark.django_db
class TestActivityLogViewSet:
    def test_non_admin_forbidden(self, api_client, plain_user):
        api_client.force_authenticate(user=plain_user)
        url = reverse("activity-log-list")
        response = api_client.get(url)
        assert response.status_code in (status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED)

    def test_admin_list_and_export(self, api_client, admin_user):
        ActivityLog.objects.create(
            actor=admin_user,
            action="create",
            verb="TEST_VERB",
            target_repr="Something",
        )
        api_client.force_authenticate(user=admin_user)
        url = reverse("activity-log-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

        export_url = reverse("activity-log-export-csv")
        response = api_client.get(export_url)
        assert response.status_code == status.HTTP_200_OK
        assert response["Content-Type"] == "text/csv"
        content = response.content.decode("utf-8")
        assert "timestamp,actor,action,verb,target,ip" in content
        assert "TEST_VERB" in content


@pytest.mark.django_db
class TestAuditReportViewSet:
    def test_non_admin_forbidden(self, api_client, plain_user):
        api_client.force_authenticate(user=plain_user)
        url = reverse("audit-report-list")
        response = api_client.get(url)
        assert response.status_code in (status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED)

    def test_create_missing_start_end(self, api_client, admin_user):
        api_client.force_authenticate(user=admin_user)
        url = reverse("audit-report-list")
        response = api_client.post(url, {}, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_invalid_datetime_format(self, api_client, admin_user):
        api_client.force_authenticate(user=admin_user)
        url = reverse("audit-report-list")
        response = api_client.post(
            url, {"start": "not-a-date", "end": "also-not-a-date"}, format="json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_start_after_end(self, api_client, admin_user):
        api_client.force_authenticate(user=admin_user)
        url = reverse("audit-report-list")
        response = api_client.post(
            url,
            {"start": "2026-08-01T00:00:00", "end": "2026-01-01T00:00:00"},
            format="json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_success(self, api_client, admin_user):
        ActivityLog.objects.create(
            actor=admin_user,
            action="create",
            verb="REPORT_TEST_VERB",
            target_repr="Thing",
        )
        api_client.force_authenticate(user=admin_user)
        url = reverse("audit-report-list")
        response = api_client.post(
            url,
            {"start": "2020-01-01T00:00:00", "end": "2030-01-01T00:00:00"},
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert AuditReport.objects.count() == 1

    def test_latest_no_reports(self, api_client, admin_user):
        api_client.force_authenticate(user=admin_user)
        url = reverse("audit-report-latest")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_latest_with_reports(self, api_client, admin_user):
        AuditReport.generate(
            start=__import__("datetime").datetime(2020, 1, 1),
            end=__import__("datetime").datetime(2030, 1, 1),
            created_by=admin_user,
        )
        api_client.force_authenticate(user=admin_user)
        url = reverse("audit-report-latest")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
