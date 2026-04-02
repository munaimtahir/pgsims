"""
Minimal user model tests for clean-slate PGSIMS build.
Legacy HTML view tests removed; only model-level and API tests remain.
"""
from unittest.mock import patch

from django.test import TestCase
from rest_framework.test import APIClient

from django.contrib.auth import get_user_model

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
