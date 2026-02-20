import pytest
from django.test import Client
from django.test.utils import override_settings

@pytest.mark.django_db
def test_login_logout_and_password_pages(admin_user):
    client = Client()

    # Login page loads
    resp = client.get("/users/login/")
    assert resp.status_code in (200, 302)

    # Login works
    assert client.login(username="admin_test", password="testpass123")

    # Password change page loads (authenticated)
    resp = client.get("/users/password-change/")
    assert resp.status_code in (200, 302)

    # Logout works (should redirect)
    resp = client.get("/users/logout/")
    assert resp.status_code in (200, 302)

@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
@pytest.mark.django_db
def test_password_reset_flow_pages():
    client = Client()
    for path in (
        "/users/password-reset/",
        "/users/password-reset/done/",
    ):
        resp = client.get(path)
        assert resp.status_code in (200, 302)

@pytest.mark.django_db
def test_admin_site_access(admin_user):
    client = Client()
    assert client.login(username="admin_test", password="testpass123")
    resp = client.get("/admin/")
    # 200 when logged in, or 302 to admin index/dashboard
    assert resp.status_code in (200, 302)

@pytest.mark.django_db
def test_role_based_dashboard_access(admin_user, supervisor_user, pg_user):
    client = Client()

    # Admin
    assert client.login(username="admin_test", password="testpass123")
    resp = client.get("/users/dashboard/")
    assert resp.status_code in (200, 302)
    client.logout()

    # Supervisor
    assert client.login(username="supervisor_test", password="testpass123")
    resp = client.get("/users/dashboard/")
    assert resp.status_code in (200, 302)
    client.logout()

    # PG
    assert client.login(username="pg_test", password="testpass123")
    resp = client.get("/users/dashboard/")
    assert resp.status_code in (200, 302)

import pytest
from django.test import Client

@pytest.mark.parametrize("base_path", [
    "/logbook/",
    "/cases/",
    "/certificates/",
    "/rotations/",
])
@pytest.mark.django_db
def test_app_includes_are_mounted(base_path):
    client = Client()
    resp = client.get(base_path)
    # Allow 200 (ok) or 302 (redirect to a list or login), but not 404
    assert resp.status_code in (200, 302), f"{base_path} not reachable"
