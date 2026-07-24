from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
import json

User = get_user_model()

class UsersViewsFinalPushTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(username="admin_final", password="password123", role="ADMIN")
        self.client.login(username="admin_final", password="password123")
        self.pg = User.objects.create_user(username="pg_final", password="password123", role="RESIDENT")
        self.supervisor = User.objects.create_user(username="sup_final", password="password123", role="SUPERVISOR")

    def test_profile_detail_view(self):
        response = self.client.get(reverse("users:profile_detail", kwargs={"pk": self.pg.pk}))
        self.assertEqual(response.status_code, 200)

    def test_supervisor_pgs_view(self):
        self.client.login(username="admin_final", password="password123")
        response = self.client.get(reverse("users:supervisor_pgs", kwargs={"pk": self.supervisor.pk}))
        self.assertEqual(response.status_code, 200)
