from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
import json

User = get_user_model()

class UsersViewsFinalPushTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(username="admin_final", password="password123", role="admin")
        self.client.login(username="admin_final", password="password123")
        self.pg = User.objects.create_user(username="pg_final", password="password123", role="pg")
        self.supervisor = User.objects.create_user(username="sup_final", password="password123", role="supervisor")

    def test_profile_detail_view(self):
        response = self.client.get(reverse("users:profile_detail", kwargs={"pk": self.pg.pk}))
        self.assertEqual(response.status_code, 200)

    def test_user_list_api_and_stats(self):
        # Stats API
        response = self.client.get(reverse("users:user_list_stats_api"))
        self.assertEqual(response.status_code, 200)
        
        # User statistics
        response = self.client.get(reverse("users:api_user_statistics"))
        self.assertEqual(response.status_code, 200)

    def test_analytics_views(self):
        # Admin analytics
        response = self.client.get(reverse("users:admin_analytics"))
        self.assertEqual(response.status_code, 200)
        
        # Supervisor analytics
        self.client.login(username="sup_final", password="password123")
        response = self.client.get(reverse("users:supervisor_analytics"))
        self.assertEqual(response.status_code, 200)
        
        # PG analytics
        self.client.login(username="pg_final", password="password123")
        response = self.client.get(reverse("users:pg_analytics"))
        self.assertEqual(response.status_code, 200)

    def test_supervisor_pgs_view(self):
        self.client.login(username="admin_final", password="password123")
        response = self.client.get(reverse("users:supervisor_pgs", kwargs={"pk": self.supervisor.pk}))
        self.assertEqual(response.status_code, 200)

    def test_user_stats_api(self):
        response = self.client.get(reverse("users:user_stats_api", kwargs={"pk": self.pg.pk}))
        self.assertEqual(response.status_code, 200)
