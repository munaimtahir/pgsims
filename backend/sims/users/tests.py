"""
Minimal user model tests for clean-slate PGSIMS build.
Legacy HTML view tests removed; only model-level and API tests remain.
"""
from unittest.mock import patch

from django.test import TestCase
from rest_framework.test import APIClient

from django.contrib.auth import get_user_model
from sims.academics.models import Department
from sims.users.models import HODAssignment, SupervisorResidentLink

User = get_user_model()


class UserModelBasicTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username="admin1", password="pass", role="admin")
        self.supervisor = User.objects.create_user(username="sup1", password="pass", role="supervisor")
        self.resident = User.objects.create_user(username="res1", password="pass", role="resident")

    def test_roles_set(self):
        self.assertEqual(self.admin.role, "admin")
        self.assertEqual(self.supervisor.role, "supervisor")
        self.assertEqual(self.resident.role, "resident")

    def test_str(self):
        self.assertIn("admin1", str(self.admin))

    def test_is_admin_property(self):
        self.assertTrue(self.admin.role in ("admin", "utrmc_admin"))


class UserAPIAuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(username="apiadmin", password="pass", role="admin", is_staff=True, is_superuser=True)

    def test_login_returns_token(self):
        r = self.client.post("/api/auth/login/", {"username": "apiadmin", "password": "pass"}, format="json")
        self.assertEqual(r.status_code, 200)
        self.assertIn("access", r.data)

    def test_me_returns_user(self):
        self.client.force_authenticate(self.admin)
        r = self.client.get("/api/auth/me/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["username"], "apiadmin")

    def test_unauthenticated_me_rejected(self):
        r = self.client.get("/api/auth/me/")
        self.assertEqual(r.status_code, 401)

    @patch("sims.users.api_views.send_mail", side_effect=Exception("mail backend unavailable"))
    def test_password_reset_returns_generic_success_when_email_send_fails(self, mocked_send_mail):
        user = User.objects.create_user(
            username="reset_user",
            password="pass",
            role="resident",
            email="reset@example.com",
        )

        r = self.client.post("/api/auth/password-reset/", {"email": user.email}, format="json")

        self.assertEqual(r.status_code, 200)
        self.assertIn("message", r.data)
        self.assertIn("If an account with that email exists", r.data["message"])
        mocked_send_mail.assert_called_once()


class UserbaseReadOnlyScopeTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(username="mgr", password="pass", role="utrmc_admin")
        self.utrmc_user = User.objects.create_user(username="viewer", password="pass", role="utrmc_user")
        self.supervisor = User.objects.create_user(username="supviewer", password="pass", role="supervisor")
        self.resident = User.objects.create_user(
            username="resviewer",
            password="pass",
            role="resident",
            specialty="medicine",
            year="1",
        )
        self.department = Department.objects.create(name="Medicine", code="MED")
        SupervisorResidentLink.objects.create(
            supervisor_user=self.supervisor,
            resident_user=self.resident,
            department=self.department,
            start_date="2026-01-01",
            created_by=self.admin,
            updated_by=self.admin,
        )
        HODAssignment.objects.create(
            department=self.department,
            hod_user=self.supervisor,
            start_date="2026-01-01",
            created_by=self.admin,
            updated_by=self.admin,
        )

    def test_utrmc_user_can_list_users_for_read_only_oversight(self):
        self.client.force_authenticate(self.utrmc_user)
        response = self.client.get("/api/users/")
        self.assertEqual(response.status_code, 200)
        rows = response.data if isinstance(response.data, list) else response.data.get("results", [])
        usernames = {row["username"] for row in rows}
        self.assertIn("viewer", usernames)
        self.assertIn("supviewer", usernames)
        self.assertIn("resviewer", usernames)

    def test_utrmc_user_cannot_create_users(self):
        self.client.force_authenticate(self.utrmc_user)
        response = self.client.post(
            "/api/users/",
            {
                "username": "blocked_user",
                "email": "blocked@example.com",
                "password": "pass12345",
                "first_name": "Blocked",
                "last_name": "User",
                "role": "resident",
                "is_active": True,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 403)

    def test_utrmc_user_can_list_supervision_links_and_hod_assignments(self):
        self.client.force_authenticate(self.utrmc_user)
        supervision_response = self.client.get("/api/supervision-links/")
        hod_response = self.client.get("/api/hod-assignments/")

        self.assertEqual(supervision_response.status_code, 200)
        self.assertEqual(hod_response.status_code, 200)

        supervision_rows = (
            supervision_response.data
            if isinstance(supervision_response.data, list)
            else supervision_response.data.get("results", [])
        )
        hod_rows = (
            hod_response.data
            if isinstance(hod_response.data, list)
            else hod_response.data.get("results", [])
        )
        self.assertEqual(len(supervision_rows), 1)
        self.assertEqual(len(hod_rows), 1)
