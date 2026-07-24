from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch, MagicMock

User = get_user_model()

class UsersViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create users with correct roles and staff status if needed
        self.admin = User.objects.create_superuser(username="ADMIN", password="password123", email="admin@test.com")
        self.admin.role = "ADMIN"
        self.admin.save()
        
        self.supervisor = User.objects.create_user(username="SUPERVISOR", password="password123", role="SUPERVISOR")
        self.pg = User.objects.create_user(username="RESIDENT", password="password123", role="RESIDENT")
        self.pg.supervisor = self.supervisor
        self.pg.save()

    def test_login_view_get(self):
        response = self.client.get(reverse("users:login"))
        self.assertEqual(response.status_code, 200)

    def test_login_view_post_success_admin(self):
        response = self.client.post(reverse("users:login"), {"username": "ADMIN", "password": "password123"}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/admin_dashboard.html")

    def test_login_view_post_success_supervisor(self):
        response = self.client.post(reverse("users:login"), {"username": "SUPERVISOR", "password": "password123"}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/supervisor_dashboard.html")

    def test_login_view_post_success_pg(self):
        response = self.client.post(reverse("users:login"), {"username": "RESIDENT", "password": "password123"}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/pg_dashboard.html")

    def test_login_view_post_invalid(self):
        response = self.client.post(reverse("users:login"), {"username": "RESIDENT", "password": "wrongpassword"})
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        self.client.login(username="RESIDENT", password="password123")
        response = self.client.get(reverse("users:logout"))
        self.assertEqual(response.status_code, 200)

    def test_supervisor_dashboard_access(self):
        self.client.login(username="SUPERVISOR", password="password123")
        response = self.client.get(reverse("users:supervisor_dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_supervisor_dashboard_denied_for_pg(self):
        self.client.login(username="RESIDENT", password="password123")
        response = self.client.get(reverse("users:supervisor_dashboard"))
        self.assertEqual(response.status_code, 403)

    def test_pg_dashboard_access(self):
        self.client.login(username="RESIDENT", password="password123")
        response = self.client.get(reverse("users:resident_dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_redirect_view(self):
        self.client.login(username="ADMIN", password="password123")
        response = self.client.get(reverse("users:dashboard"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/admin_dashboard.html")

    def test_user_list_view_admin(self):
        self.client.login(username="ADMIN", password="password123")
        response = self.client.get(reverse("users:user_list"))
        self.assertEqual(response.status_code, 200)

    def test_user_create_view_post(self):
        self.client.login(username="ADMIN", password="password123")
        data = {
            "username": "newuser",
            "email": "new@test.com",
            "first_name": "New",
            "last_name": "User",
            "role": "RESIDENT",
            "password1": "password123",
            "password2": "password123",
            "specialty": "medicine",
            "year": "1",
            "supervisor_choice": self.supervisor.id
        }
        response = self.client.post(reverse("users:user_create"), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_user_activate_deactivate(self):
        self.client.login(username="ADMIN", password="password123")
        user = User.objects.create_user(username="temp", password="password123", is_active=True)
        self.client.post(reverse("users:user_deactivate", kwargs={"pk": user.pk}))
        user.refresh_from_db()
        self.assertFalse(user.is_active)
        self.client.post(reverse("users:user_activate", kwargs={"pk": user.pk}))
        user.refresh_from_db()
        self.assertTrue(user.is_active)

    def test_user_archive(self):
        self.client.login(username="ADMIN", password="password123")
        user = User.objects.create_user(username="temp_arch", password="password123")
        self.client.post(reverse("users:user_archive", kwargs={"pk": user.pk}))
        user.refresh_from_db()
        self.assertTrue(user.is_archived)

