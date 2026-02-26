from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIClient

from sims.users.models import User


class PublicRegistrationAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.supervisor = User.objects.create_user(
            username="sup_registration",
            email="sup@example.com",
            password="testpass123",
            role="supervisor",
            specialty="medicine",
        )
        self.url = reverse("auth_api:register")
        self.base_payload = {
            "username": "new_pg_user",
            "email": "newpg@example.com",
            "password": "SafePassword123!",
            "password2": "SafePassword123!",
            "first_name": "New",
            "last_name": "Resident",
            "role": "pg",
            "specialty": "medicine",
            "year": "1",
            "supervisor": self.supervisor.id,
        }

    @override_settings(ENABLE_PUBLIC_REGISTRATION=False)
    def test_public_registration_disabled_by_default(self):
        response = self.client.post(self.url, self.base_payload, format="json")
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data["error"], "Public registration is disabled.")

    @override_settings(ENABLE_PUBLIC_REGISTRATION=True)
    def test_public_registration_creates_pg_when_enabled(self):
        response = self.client.post(self.url, self.base_payload, format="json")
        self.assertEqual(response.status_code, 201)
        created = User.objects.get(username="new_pg_user")
        self.assertEqual(created.role, "pg")

    @override_settings(ENABLE_PUBLIC_REGISTRATION=True)
    def test_public_registration_rejects_privileged_roles(self):
        payload = {**self.base_payload, "username": "bad_role_user", "role": "admin"}
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("role", response.data)
