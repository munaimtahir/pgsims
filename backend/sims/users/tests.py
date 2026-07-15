"""
Minimal user model tests for clean-slate PGSIMS build.
Legacy HTML view tests removed; only model-level and API tests remain.
"""
from unittest.mock import patch

from django.test import TestCase
from rest_framework.test import APIClient

from django.contrib.auth import get_user_model
from sims.academics.models import Department
from sims.supervision.models import ResidentSupervisorAssignment
from sims.training.models import ResidentTrainingRecord
from sims.users.models import ResidentProfile, SupervisorProfile

User = get_user_model()


class UserModelBasicTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username="admin1", password="pass", role="ADMIN")
        self.supervisor = User.objects.create_user(username="sup1", password="pass", role="SUPERVISOR")
        self.resident = User.objects.create_user(username="res1", password="pass", role="RESIDENT")

    def test_roles_set(self):
        self.assertEqual(self.admin.role, "ADMIN")
        self.assertEqual(self.supervisor.role, "SUPERVISOR")
        self.assertEqual(self.resident.role, "RESIDENT")

    def test_str(self):
        self.assertIn("admin1", str(self.admin))

    def test_is_admin_property(self):
        self.assertTrue(self.admin.role in ("ADMIN", "ADMIN"))

    def test_pilot_pg_bootstrap_creates_active_training_record(self):
        pilot = User.objects.create_user(
            username="pilot_pg",
            password="pass",
            role="RESIDENT",
        )

        records = ResidentTrainingRecord.objects.filter(resident_user=pilot, active=True)

        self.assertEqual(records.count(), 1)
        self.assertEqual(records.first().program.code, "PILOT-BASELINE")
        self.assertEqual(records.first().status, ResidentTrainingRecord.STATUS_ACTIVE)


class UserAPIAuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(username="apiadmin", password="pass", role="ADMIN", is_staff=True, is_superuser=True)

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
            role="RESIDENT",
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
        self.admin = User.objects.create_user(username="mgr", password="pass", role="ADMIN")
        self.utrmc_user = User.objects.create_user(username="viewer", password="pass", role="SUPPORT_STAFF")
        self.supervisor = User.objects.create_user(username="supviewer", password="pass", role="SUPERVISOR")
        self.resident = User.objects.create_user(
            username="resviewer",
            password="pass",
            role="RESIDENT",
            specialty="medicine",
            year="1",
        )
        self.department = Department.objects.create(name="Medicine", code="MED")
        SupervisorProfile.objects.create(
            user=self.supervisor,
            designation_ref="HOD",
            department_ref=self.department,
        )
        resident_profile = ResidentProfile.objects.create(
            user=self.resident,
            department_ref=self.department,
        )
        supervisor_profile = self.supervisor.supervisor_profile
        ResidentSupervisorAssignment.objects.create(
            supervisor=supervisor_profile,
            resident=resident_profile,
            assignment_type=ResidentSupervisorAssignment.ASSIGNMENT_PRIMARY,
            start_date="2026-01-01",
            is_active=True,
            status=ResidentSupervisorAssignment.STATUS_ACTIVE,
            created_by=self.admin,
            updated_by=self.admin,
        )

    def test_support_staff_user_list_is_self_scoped(self):
        self.client.force_authenticate(self.utrmc_user)
        response = self.client.get("/api/users/")
        self.assertEqual(response.status_code, 200)
        rows = response.data if isinstance(response.data, list) else response.data.get("results", [])
        usernames = {row["username"] for row in rows}
        self.assertEqual(usernames, {"viewer"})

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
                "role": "RESIDENT",
                "is_active": True,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 403)

    def test_support_staff_cannot_list_supervision_assignments(self):
        self.client.force_authenticate(self.utrmc_user)
        supervision_response = self.client.get("/api/supervision/assignments/")

        self.assertEqual(supervision_response.status_code, 403)
