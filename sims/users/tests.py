import json

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class UserModelTestCase(TestCase):
    """
    Test cases for the custom User model in SIMS.

    Created: 2025-05-29 16:05:01 UTC
    Author: SMIB2012
    """

    def setUp(self):
        """Set up test data"""
        # Create test users for different roles
        self.admin_user = User.objects.create_user(
            username="admin_test",
            email="admin@sims.test",
            password="testpass123",
            role="admin",
            first_name="Admin",
            last_name="User",
        )

        self.supervisor_user = User.objects.create_user(
            username="supervisor_test",
            email="supervisor@sims.test",
            password="testpass123",
            role="supervisor",
            specialty="medicine",
            first_name="Super",
            last_name="Visor",
        )

        self.pg_user = User.objects.create_user(
            username="pg_test",
            email="pg@sims.test",
            password="testpass123",
            role="pg",
            specialty="medicine",
            year="1",
            supervisor=self.supervisor_user,
            first_name="Post",
            last_name="Graduate",
        )

    def test_user_creation_admin(self):
        """Test admin user creation"""
        self.assertEqual(self.admin_user.role, "admin")
        self.assertTrue(self.admin_user.is_admin())
        self.assertFalse(self.admin_user.is_supervisor())
        self.assertFalse(self.admin_user.is_pg())
        self.assertIsNone(self.admin_user.specialty)
        self.assertIsNone(self.admin_user.supervisor)

    def test_user_creation_supervisor(self):
        """Test supervisor user creation"""
        self.assertEqual(self.supervisor_user.role, "supervisor")
        self.assertFalse(self.supervisor_user.is_admin())
        self.assertTrue(self.supervisor_user.is_supervisor())
        self.assertFalse(self.supervisor_user.is_pg())
        self.assertEqual(self.supervisor_user.specialty, "medicine")
        self.assertIsNone(self.supervisor_user.supervisor)

    def test_user_creation_pg(self):
        """Test PG user creation"""
        self.assertEqual(self.pg_user.role, "pg")
        self.assertFalse(self.pg_user.is_admin())
        self.assertFalse(self.pg_user.is_supervisor())
        self.assertTrue(self.pg_user.is_pg())
        self.assertEqual(self.pg_user.specialty, "medicine")
        self.assertEqual(self.pg_user.year, "1")
        self.assertEqual(self.pg_user.supervisor, self.supervisor_user)

    def test_user_string_representation(self):
        """Test __str__ method"""
        expected = "Post Graduate (Postgraduate)"
        self.assertEqual(str(self.pg_user), expected)

        # Test with user without full name but with required fields for PG
        user_no_name = User.objects.create_user(
            username="testuser",
            password="testpass123",
            role="pg",
            specialty="medicine",
            year="1",
            supervisor=self.supervisor_user,
        )
        expected_no_name = "testuser (Postgraduate)"
        self.assertEqual(str(user_no_name), expected_no_name)

    def test_pg_validation_missing_specialty(self):
        """Test PG validation fails without specialty"""
        with self.assertRaises(ValidationError):
            user = User(
                username="invalid_pg",
                email="invalid@test.com",
                role="pg",
                year="1",
                supervisor=self.supervisor_user,
                # Missing specialty
            )
            user.full_clean()

    def test_pg_validation_missing_year(self):
        """Test PG validation fails without year"""
        with self.assertRaises(ValidationError):
            user = User(
                username="invalid_pg",
                email="invalid@test.com",
                role="pg",
                specialty="medicine",
                supervisor=self.supervisor_user,
                # Missing year
            )
            user.full_clean()

    def test_pg_validation_missing_supervisor(self):
        """Test PG validation fails without supervisor"""
        with self.assertRaises(ValidationError):
            user = User(
                username="invalid_pg",
                email="invalid@test.com",
                role="pg",
                specialty="medicine",
                year="1",
                # Missing supervisor
            )
            user.full_clean()

    def test_supervisor_validation_missing_specialty(self):
        """Test supervisor validation fails without specialty"""
        with self.assertRaises(ValidationError):
            user = User(
                username="invalid_supervisor",
                email="invalid@test.com",
                role="supervisor",
                # Missing specialty
            )
            user.full_clean()

    def test_admin_cannot_have_supervisor(self):
        """Test admin cannot have a supervisor"""
        with self.assertRaises(ValidationError):
            user = User(
                username="invalid_admin",
                email="invalid@test.com",
                role="admin",
                supervisor=self.supervisor_user,
            )
            user.full_clean()

    def test_self_supervision_prevention(self):
        """Test users cannot supervise themselves"""
        with self.assertRaises(ValidationError):
            self.supervisor_user.supervisor = self.supervisor_user
            self.supervisor_user.full_clean()

    def test_supervisor_relationship_methods(self):
        """Test supervisor-PG relationship methods"""
        assigned_pgs = self.supervisor_user.get_assigned_pgs()
        self.assertIn(self.pg_user, assigned_pgs)

        supervisor_name = self.pg_user.get_supervisor_name()
        self.assertEqual(supervisor_name, "Super Visor")

    def test_user_archiving(self):
        """Test user archiving functionality"""
        self.assertFalse(self.pg_user.is_archived)
        self.assertIsNone(self.pg_user.archived_date)

        self.pg_user.is_archived = True
        self.pg_user.save()

        self.assertTrue(self.pg_user.is_archived)
        self.assertIsNotNone(self.pg_user.archived_date)

    def test_dashboard_urls(self):
        """Test dashboard URL generation"""
        admin_url = self.admin_user.get_dashboard_url()
        self.assertEqual(admin_url, reverse("admin:index"))

        supervisor_url = self.supervisor_user.get_dashboard_url()
        self.assertEqual(supervisor_url, reverse("users:supervisor_dashboard"))

        pg_url = self.pg_user.get_dashboard_url()
        self.assertEqual(pg_url, reverse("users:pg_dashboard"))


class UserViewsTestCase(TestCase):
    """Test cases for user views"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()

        self.admin_user = User.objects.create_user(
            username="admin_test",
            email="admin@sims.test",
            password="testpass123",
            role="admin",
            first_name="Admin",
            last_name="User",
        )

        self.supervisor_user = User.objects.create_user(
            username="supervisor_test",
            email="supervisor@sims.test",
            password="testpass123",
            role="supervisor",
            specialty="medicine",
            first_name="Super",
            last_name="Visor",
        )

        self.pg_user = User.objects.create_user(
            username="pg_test",
            email="pg@sims.test",
            password="testpass123",
            role="pg",
            specialty="medicine",
            year="1",
            supervisor=self.supervisor_user,
            first_name="Post",
            last_name="Graduate",
        )

    def test_login_view(self):
        """Test login functionality"""
        response = self.client.get(reverse("users:login"))
        self.assertEqual(response.status_code, 200)

        # Test successful login
        response = self.client.post(
            reverse("users:login"), {"username": "admin_test", "password": "testpass123"}
        )
        self.assertEqual(response.status_code, 302)  # Redirect after login

    def test_dashboard_redirect(self):
        """Test dashboard redirects to correct role-based dashboard"""
        # Test admin dashboard redirect
        self.client.login(username="admin_test", password="testpass123")
        response = self.client.get(reverse("users:dashboard"))
        self.assertRedirects(response, reverse("admin:index"), fetch_redirect_response=False)

        # Test supervisor dashboard redirect
        self.client.login(username="supervisor_test", password="testpass123")
        response = self.client.get(reverse("users:dashboard"))
        self.assertRedirects(response, reverse("users:supervisor_dashboard"))

        # Test PG dashboard redirect
        self.client.login(username="pg_test", password="testpass123")
        response = self.client.get(reverse("users:dashboard"))
        self.assertRedirects(response, reverse("users:pg_dashboard"))

    def test_admin_dashboard_access(self):
        """Test admin dashboard access control"""
        # Admin should have access (admin_dashboard redirects to admin:index)
        self.client.login(username="admin_test", password="testpass123")
        response = self.client.get(reverse("users:admin_dashboard"))
        self.assertEqual(response.status_code, 302)  # Redirects to admin:index

        # Non-admin should not have access
        self.client.login(username="pg_test", password="testpass123")
        response = self.client.get(reverse("users:admin_dashboard"))
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_supervisor_dashboard_access(self):
        """Test supervisor dashboard access control"""
        # Supervisor should have access
        self.client.login(username="supervisor_test", password="testpass123")
        response = self.client.get(reverse("users:supervisor_dashboard"))
        self.assertEqual(response.status_code, 200)

        # PG should not have access
        self.client.login(username="pg_test", password="testpass123")
        response = self.client.get(reverse("users:supervisor_dashboard"))
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_pg_dashboard_access(self):
        """Test PG dashboard access control"""
        # PG should have access
        self.client.login(username="pg_test", password="testpass123")
        response = self.client.get(reverse("users:pg_dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_profile_view(self):
        """Test profile view"""
        self.client.login(username="pg_test", password="testpass123")
        response = self.client.get(reverse("users:profile"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Post Graduate")

    def test_user_list_admin_only(self):
        """Test user list is only accessible by admins"""
        # Admin should have access
        self.client.login(username="admin_test", password="testpass123")
        response = self.client.get(reverse("users:user_list"))
        self.assertEqual(response.status_code, 200)

        # Non-admin should not have access
        self.client.login(username="pg_test", password="testpass123")
        response = self.client.get(reverse("users:user_list"))
        self.assertEqual(response.status_code, 403)

    def test_user_creation_admin_only(self):
        """Test user creation is only accessible by admins"""
        # Admin should have access
        self.client.login(username="admin_test", password="testpass123")
        response = self.client.get(reverse("users:user_create"))
        self.assertEqual(response.status_code, 200)

        # Test user creation POST
        response = self.client.post(
            reverse("users:user_create"),
            {
                "username": "new_pg",
                "email": "newpg@sims.test",
                "first_name": "New",
                "last_name": "PG",
                "password1": "newpassword123",
                "password2": "newpassword123",
                "role": "pg",
                "specialty": "surgery",
                "year": "1",
                "supervisor": self.supervisor_user.id,
            },
        )
        self.assertEqual(response.status_code, 302)  # Redirect after creation

        # Verify user was created
        new_user = User.objects.get(username="new_pg")
        self.assertEqual(new_user.role, "pg")
        self.assertEqual(new_user.specialty, "surgery")


class UserFormsTestCase(TestCase):
    """Test cases for user forms"""

    def setUp(self):
        """Set up test data"""
        self.supervisor_user = User.objects.create_user(
            username="supervisor_test",
            email="supervisor@sims.test",
            password="testpass123",
            role="supervisor",
            specialty="medicine",
            first_name="Super",
            last_name="Visor",
        )

    def test_user_creation_form_valid(self):
        """Test valid user creation form"""
        form_data = {
            "username": "test_pg",
            "email": "testpg@sims.test",
            "first_name": "Test",
            "last_name": "PG",
            "password1": "testpassword123",
            "password2": "testpassword123",
            "role": "pg",
            "specialty": "medicine",
            "year": "1",
            "supervisor": self.supervisor_user.id,
        }

        from .forms import CustomUserCreationForm

        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_creation_form_pg_missing_supervisor(self):
        """Test user creation form validation for PG without supervisor"""
        form_data = {
            "username": "test_pg",
            "email": "testpg@sims.test",
            "first_name": "Test",
            "last_name": "PG",
            "password1": "testpassword123",
            "password2": "testpassword123",
            "role": "pg",
            "specialty": "medicine",
            "year": "1",
            # Missing supervisor
        }

        from .forms import CustomUserCreationForm

        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("supervisor", form.errors)

    def test_profile_edit_form(self):
        """Test profile edit form"""
        user = User.objects.create_user(
            username="test_user",
            email="test@sims.test",
            password="testpass123",
            role="pg",
            specialty="medicine",
            year="1",
            supervisor=self.supervisor_user,
            first_name="Test",
            last_name="User",
        )

        form_data = {
            "first_name": "Updated",
            "last_name": "Name",
            "email": "updated@sims.test",
            "phone_number": "1234567890",
        }

        from .forms import ProfileEditForm

        form = ProfileEditForm(data=form_data, instance=user)
        self.assertTrue(form.is_valid())

        updated_user = form.save()
        self.assertEqual(updated_user.first_name, "Updated")
        self.assertEqual(updated_user.email, "updated@sims.test")


class UserPermissionsTestCase(TestCase):
    """Test cases for user permissions and access control"""

    def setUp(self):
        """Set up test data"""
        self.admin_user = User.objects.create_user(
            username="admin_test", password="testpass123", role="admin"
        )

        self.supervisor1 = User.objects.create_user(
            username="supervisor1", password="testpass123", role="supervisor", specialty="medicine"
        )

        self.supervisor2 = User.objects.create_user(
            username="supervisor2", password="testpass123", role="supervisor", specialty="surgery"
        )

        self.pg1 = User.objects.create_user(
            username="pg1",
            password="testpass123",
            role="pg",
            specialty="medicine",
            year="1",
            supervisor=self.supervisor1,
        )

        self.pg2 = User.objects.create_user(
            username="pg2",
            password="testpass123",
            role="pg",
            specialty="surgery",
            year="2",
            supervisor=self.supervisor2,
        )

    def test_supervisor_can_only_see_assigned_pgs(self):
        """Test supervisors can only access their assigned PGs"""
        # Supervisor1 should see PG1 but not PG2
        assigned_pgs = self.supervisor1.get_assigned_pgs()
        self.assertIn(self.pg1, assigned_pgs)
        self.assertNotIn(self.pg2, assigned_pgs)

        # Supervisor2 should see PG2 but not PG1
        assigned_pgs = self.supervisor2.get_assigned_pgs()
        self.assertIn(self.pg2, assigned_pgs)
        self.assertNotIn(self.pg1, assigned_pgs)

    def test_admin_can_see_all_users(self):
        """Test admins can access all users"""
        # This would be tested in view tests with proper queryset filtering
        all_users = User.objects.all()
        self.assertIn(self.admin_user, all_users)
        self.assertIn(self.supervisor1, all_users)
        self.assertIn(self.pg1, all_users)
        self.assertIn(self.pg2, all_users)


class UserAPITestCase(TestCase):
    """Test cases for user API endpoints"""

    def setUp(self):
        """Set up test data"""
        self.admin_user = User.objects.create_user(
            username="admin_test", password="testpass123", role="admin"
        )

        self.supervisor_user = User.objects.create_user(
            username="supervisor_test",
            password="testpass123",
            role="supervisor",
            specialty="medicine",
        )

        self.client = Client()

    def test_user_search_api_authenticated(self):
        """Test user search API requires authentication"""
        response = self.client.get(reverse("users:user_search_api"))
        self.assertEqual(response.status_code, 302)  # Redirect to login

        # Test with authentication
        self.client.login(username="admin_test", password="testpass123")
        response = self.client.get(reverse("users:user_search_api"))
        self.assertEqual(response.status_code, 200)

    def test_supervisors_by_specialty_api(self):
        """Test supervisors by specialty API"""
        self.client.login(username="admin_test", password="testpass123")

        response = self.client.get(
            reverse("users:supervisors_by_specialty", kwargs={"specialty": "medicine"})
        )
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertIn("supervisors", data)
        self.assertIsInstance(data["supervisors"], list)

        # Should contain supervisor_test
        supervisor_found = any(
            supervisor["id"] == self.supervisor_user.id for supervisor in data["supervisors"]
        )
        self.assertTrue(supervisor_found)


class UserStatisticsTestCase(TestCase):
    """Test cases for user statistics and analytics"""

    def setUp(self):
        """Set up test data"""
        self.supervisor_user = User.objects.create_user(
            username="supervisor_test",
            password="testpass123",
            role="supervisor",
            specialty="medicine",
        )

        self.pg_user = User.objects.create_user(
            username="pg_test",
            password="testpass123",
            role="pg",
            specialty="medicine",
            year="1",
            supervisor=self.supervisor_user,
        )

    def test_get_documents_pending_count(self):
        """Test documents pending count for supervisors"""
        # This test would require models from other apps
        # For now, test the method exists and returns integer
        count = self.supervisor_user.get_documents_pending_count()
        self.assertIsInstance(count, int)
        self.assertEqual(count, 0)  # No documents created yet

    def test_get_documents_submitted_count(self):
        """Test documents submitted count for PGs"""
        # This test would require models from other apps
        # For now, test the method exists and returns integer
        count = self.pg_user.get_documents_submitted_count()
        self.assertIsInstance(count, int)
        self.assertEqual(count, 0)  # No documents created yet
