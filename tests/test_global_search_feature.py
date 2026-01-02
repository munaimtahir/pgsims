import datetime
import os

import django
import pytest
from django.urls import reverse


pytestmark = pytest.mark.django_db


@pytest.fixture
def admin_user(django_user_model):
    return django_user_model.objects.create_superuser(
        username="admin",
        password="adminpass",
        email="admin@example.com",
        role="admin",
        first_name="System",
        last_name="Admin",
    )


@pytest.fixture
def supervisor_user(django_user_model):
    return django_user_model.objects.create_user(
        username="sup",
        password="password",
        email="sup@example.com",
        role="supervisor",
        first_name="Super",
        last_name="Visor",
        specialty="medicine",
    )


@pytest.fixture
def pg_user(django_user_model, supervisor_user):
    user = django_user_model.objects.create_user(
        username="pguser",
        password="password",
        email="pg@example.com",
        role="pg",
        first_name="Pat",
        last_name="Graduate",
        specialty="medicine",
        year="1",
        supervisor=supervisor_user,
    )
    return user


@pytest.fixture
def sample_rotation(pg_user, supervisor_user):
    from sims.rotations.models import Department, Hospital, Rotation

    hospital = Hospital.objects.create(name="City Hospital")
    department = Department.objects.create(name="General Medicine", hospital=hospital)
    rotation = Rotation.objects.create(
        pg=pg_user,
        department=department,
        hospital=hospital,
        supervisor=supervisor_user,
        start_date=datetime.date.today() - datetime.timedelta(days=30),
        end_date=datetime.date.today() + datetime.timedelta(days=30),
        status="ongoing",
    )
    return rotation


def test_search_service_returns_results(admin_user, pg_user, sample_rotation):
    from sims.search.services import SearchService

    service = SearchService(admin_user)
    results = service.search(pg_user.first_name)
    assert any(
        result.module == "users" and result.object_id == pg_user.pk
        for result in results
    )


def test_search_api_logs_queries(client, admin_user, pg_user, sample_rotation):
    from sims.search.models import SavedSearchSuggestion, SearchQueryLog

    client.force_login(admin_user)
    SavedSearchSuggestion.objects.create(label="rotation")
    url = reverse("search:global_search")
    response = client.get(url, {"q": pg_user.first_name})
    assert response.status_code == 200
    payload = response.json()
    assert payload["count"] >= 1
    assert SearchQueryLog.objects.filter(
        user=admin_user, query__icontains=pg_user.first_name
    ).exists()
    assert "suggestions" in payload


def test_audit_report_generation(admin_user):
    from sims.audit.models import ActivityLog, AuditReport

    ActivityLog.log(actor=admin_user, action="view", verb="unit-test")
    start = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=1)
    end = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1)
    report = AuditReport.generate(start=start, end=end, created_by=admin_user)
    assert report.payload["total"] >= 1
    assert report.payload["by_action"]["view"] >= 1
