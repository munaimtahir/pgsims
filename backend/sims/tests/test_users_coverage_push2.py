"""
Additional coverage push for sims/users/views.py and sims/users/userbase_views.py.

Focus: views/endpoints not already exercised by test_users_views*.py,
test_userbase_api.py, test_demo_data_reset.py, test_registration_api.py,
or test_seed_demo_data.py (checked via --cov-report=term-missing before
writing these).
"""
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.test.utils import override_settings
from django.urls import reverse
from rest_framework.test import APIClient

from sims.academics.models import Department, Specialty
from sims.rotations.models import Hospital, HospitalDepartment
from sims.users.models import DepartmentMembership, ResidentProfile, SupervisorProfile

User = get_user_model()


class LegacyViewsExtraCoverageTests(TestCase):
    """Covers legacy dashboard/report views in sims/users/views.py that were
    still at 0% after the existing test_users_views* suite."""

    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(
            username="cov_admin", password="password123", email="cov_admin@test.com"
        )
        self.admin.role = "ADMIN"
        self.admin.save()

        self.supervisor = User.objects.create_user(
            username="cov_supervisor", password="password123", role="SUPERVISOR"
        )
        self.resident = User.objects.create_user(
            username="cov_resident", password="password123", role="RESIDENT"
        )
        self.resident.supervisor = self.supervisor
        self.resident.save()

    def test_supervisor_list_view(self):
        self.client.login(username="cov_admin", password="password123")
        response = self.client.get(reverse("users:supervisor_list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.supervisor, response.context["supervisors"])

    def test_supervisor_list_view_denied_for_resident(self):
        self.client.login(username="cov_resident", password="password123")
        response = self.client.get(reverse("users:supervisor_list"))
        self.assertEqual(response.status_code, 403)

    def test_pg_list_view_admin_with_search(self):
        self.client.login(username="cov_admin", password="password123")
        response = self.client.get(reverse("users:pg_list"), {"search": "cov_resident"})
        self.assertEqual(response.status_code, 200)

    def test_pg_list_view_supervisor_scope(self):
        self.client.login(username="cov_supervisor", password="password123")
        response = self.client.get(reverse("users:pg_list"))
        self.assertEqual(response.status_code, 200)

    def test_pg_list_view_denied_for_resident(self):
        self.client.login(username="cov_resident", password="password123")
        response = self.client.get(reverse("users:pg_list"))
        self.assertEqual(response.status_code, 403)

    def test_pg_progress_view_self_access(self):
        self.client.login(username="cov_resident", password="password123")
        response = self.client.get(reverse("users:pg_progress", kwargs={"pk": self.resident.pk}))
        self.assertEqual(response.status_code, 200)

    def test_pg_progress_view_denied_for_other_resident(self):
        other_resident = User.objects.create_user(
            username="cov_other_resident", password="password123", role="RESIDENT"
        )
        self.client.login(username="cov_other_resident", password="password123")
        response = self.client.get(reverse("users:pg_progress", kwargs={"pk": self.resident.pk}))
        self.assertEqual(response.status_code, 403)

    def test_pg_progress_view_admin_access(self):
        self.client.login(username="cov_admin", password="password123")
        response = self.client.get(reverse("users:pg_progress", kwargs={"pk": self.resident.pk}))
        self.assertEqual(response.status_code, 200)

    def test_user_reports_view(self):
        self.client.login(username="cov_admin", password="password123")
        response = self.client.get(reverse("users:user_reports"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("total_users", response.context)

    def test_user_export_view(self):
        self.client.login(username="cov_admin", password="password123")
        response = self.client.get(reverse("users:user_export"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "success"})

    def test_activity_log_view(self):
        self.client.login(username="cov_admin", password="password123")
        response = self.client.get(reverse("users:activity_log"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["activities"]), [])

    def test_trainee_template_download_view(self):
        self.client.login(username="cov_admin", password="password123")
        response = self.client.get(reverse("users:trainee_template_download"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("spreadsheetml", response["Content-Type"])

    def test_excel_converter_view_no_file(self):
        self.client.login(username="cov_admin", password="password123")
        response = self.client.post(reverse("users:excel_converter"), {})
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json()["success"])

    def test_pg_bulk_upload_view_get(self):
        self.client.login(username="cov_admin", password="password123")
        response = self.client.get(reverse("users:pg_bulk_upload"))
        self.assertEqual(response.status_code, 200)

    def test_pg_bulk_upload_view_no_file(self):
        self.client.login(username="cov_admin", password="password123")
        response = self.client.post(reverse("users:pg_bulk_upload"), {})
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json()["success"])

    def test_assign_supervisor_view_get(self):
        self.client.login(username="cov_admin", password="password123")
        response = self.client.get(reverse("users:assign_supervisor"))
        self.assertEqual(response.status_code, 200)

    def test_assign_supervisor_view_post_invalid(self):
        self.client.login(username="cov_admin", password="password123")
        response = self.client.post(reverse("users:assign_supervisor"), {})
        self.assertEqual(response.status_code, 200)

    def test_profile_view_self(self):
        self.client.login(username="cov_resident", password="password123")
        response = self.client.get(reverse("users:profile"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["profile_user"], self.resident)

    def test_logout_view_get_authenticated(self):
        self.client.login(username="cov_resident", password="password123")
        response = self.client.get(reverse("users:logout"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("user_name", response.context)

    def test_login_view_inactive_account(self):
        self.resident.is_active = False
        self.resident.save()
        response = self.client.post(
            reverse("users:login"),
            {"username": "cov_resident", "password": "password123"},
        )
        self.assertEqual(response.status_code, 200)

    def test_login_view_archived_account(self):
        archived = User.objects.create_user(
            username="cov_archived", password="password123", role="RESIDENT"
        )
        # Keep the fixture explicit: UserManager implementations in supported
        # Django versions may not forward status-only kwargs consistently.
        User.objects.filter(pk=archived.pk).update(is_archived=True)
        response = self.client.post(
            reverse("users:login"),
            {"username": "cov_archived", "password": "password123"},
        )
        # ``users:login`` resolves to Django's LoginView; the legacy custom
        # login_view is not wired to that URL.  The archived flag is not part
        # of ModelBackend authentication, so a valid active user redirects.
        self.assertEqual(response.status_code, 302)


class UserCreateViewValidationTests(TestCase):
    """UserCreateView.post exercises a lot of manual validation branches
    that weren't covered by the happy-path test in test_users_views.py."""

    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(
            username="cov_admin2", password="password123", email="cov_admin2@test.com"
        )
        self.admin.role = "ADMIN"
        self.admin.save()
        self.client.login(username="cov_admin2", password="password123")
        self.supervisor = User.objects.create_user(
            username="cov_sup2", password="password123", role="SUPERVISOR"
        )
        Specialty.objects.create(name="Medicine Push2", code="MED-PUSH2")

    def _base_payload(self, **overrides):
        payload = {
            "username": "newresident",
            "email": "newresident@test.com",
            "first_name": "New",
            "last_name": "Resident",
            "role": "RESIDENT",
            "specialty": "MED-PUSH2",
            "year": "1",
            "password1": "longpassword123",
            "password2": "longpassword123",
            "supervisor_choice": str(self.supervisor.pk),
        }
        payload.update(overrides)
        return payload

    def test_missing_required_fields(self):
        response = self.client.post(reverse("users:user_create"), {})
        self.assertEqual(response.status_code, 200)

    def test_duplicate_username(self):
        response = self.client.post(
            reverse("users:user_create"), self._base_payload(username="cov_admin2")
        )
        self.assertEqual(response.status_code, 200)

    def test_duplicate_email(self):
        response = self.client.post(
            reverse("users:user_create"), self._base_payload(email="cov_admin2@test.com")
        )
        self.assertEqual(response.status_code, 200)

    def test_password_mismatch(self):
        response = self.client.post(
            reverse("users:user_create"), self._base_payload(password2="different123")
        )
        self.assertEqual(response.status_code, 200)

    def test_password_too_short(self):
        response = self.client.post(
            reverse("users:user_create"),
            self._base_payload(password1="short", password2="short"),
        )
        self.assertEqual(response.status_code, 200)

    def test_resident_missing_year_and_supervisor(self):
        response = self.client.post(
            reverse("users:user_create"),
            self._base_payload(year="", supervisor_choice=""),
        )
        self.assertEqual(response.status_code, 200)

    def test_resident_missing_specialty(self):
        response = self.client.post(
            reverse("users:user_create"), self._base_payload(specialty="")
        )
        self.assertEqual(response.status_code, 200)

    def test_resident_supervisor_not_found(self):
        response = self.client.post(
            reverse("users:user_create"), self._base_payload(supervisor_choice="999999")
        )
        self.assertEqual(response.status_code, 200)

    def test_valid_resident_creation(self):
        response = self.client.post(reverse("users:user_create"), self._base_payload())
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newresident").exists())

    def test_valid_admin_creation_no_specialty_required(self):
        response = self.client.post(
            reverse("users:user_create"),
            self._base_payload(
                username="newadmin",
                email="newadmin@test.com",
                role="ADMIN",
                specialty="",
                year="",
                supervisor_choice="",
            ),
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newadmin").exists())


class UserbaseAuthMeAndCompleteProfileTests(TestCase):
    """AuthMeView + CompleteProfileView branch coverage."""

    def setUp(self):
        self.client = APIClient()
        self.hospital = Hospital.objects.create(name="Push2 Hospital", code="PUSH2-H")
        self.department = Department.objects.create(name="Push2 Dept", code="PUSH2-D")
        HospitalDepartment.objects.create(hospital=self.hospital, department=self.department)

        self.resident = User.objects.create_user(
            username="push2_resident",
            password="pass12345",
            role="RESIDENT",
            must_change_password=True,
        )
        self.resident_profile = ResidentProfile.objects.create(user=self.resident)

        self.admin = User.objects.create_user(
            username="push2_admin", password="pass12345", role="ADMIN"
        )

    def test_auth_me_must_change_password(self):
        self.client.force_authenticate(self.resident)
        response = self.client.get(reverse("auth_api:me"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["allowed_next_route"], "/change-password")

    def test_auth_me_missing_fields_routes_to_complete_profile(self):
        self.resident.must_change_password = False
        self.resident.save()
        self.client.force_authenticate(self.resident)
        response = self.client.get(reverse("auth_api:me"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["allowed_next_route"], "/complete-profile")
        self.assertIn("hospital", response.data["missing_required_fields"])

    def test_auth_me_no_profile_relation_role(self):
        # Give the resident a role that has no completion requirements to
        # exercise the "role not in PROFILE_COMPLETION_REQUIREMENTS" path is
        # not hit for a normal role; instead test admin with complete profile.
        from sims.users.models import AdminProfile

        AdminProfile.objects.create(
            user=self.admin,
            profile_status="COMPLETE",
        )
        self.admin.first_name = "Admin"
        self.admin.last_name = "User"
        self.admin.phone_number = "12345"
        self.admin.email = "push2_admin@test.com"
        self.admin.must_change_password = False
        self.admin.save()
        self.client.force_authenticate(self.admin)
        response = self.client.get(reverse("auth_api:me"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["profile_type"], "AdminProfile")

    def test_complete_profile_get(self):
        self.client.force_authenticate(self.resident)
        response = self.client.get(reverse("auth_api:complete_profile"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("missing_fields", response.data)

    def test_complete_profile_post_role_not_requiring(self):
        support = User.objects.create_user(
            username="push2_support_no_profile",
            password="pass12345",
            role="SUPPORT_STAFF",
        )
        self.client.force_authenticate(support)
        response = self.client.post(reverse("auth_api:complete_profile"), {}, format="json")
        # SUPPORT_STAFF is in PROFILE_COMPLETION_REQUIREMENTS but has no
        # profile row created here, so this hits the "profile does not exist"
        # branch instead.
        self.assertEqual(response.status_code, 400)

    def test_complete_profile_post_full_flow(self):
        self.client.force_authenticate(self.resident)
        payload = {
            "full_name": "Push Two Resident",
            "phone": "03001234567",
            "email": "push2_resident@test.com",
            "hospital": self.hospital.id,
            "department_ref": self.department.id,
        }
        response = self.client.post(reverse("auth_api:complete_profile"), payload, format="json")
        self.assertEqual(response.status_code, 200)
        self.resident.refresh_from_db()
        self.assertEqual(self.resident.first_name, "Push")

    def test_complete_profile_post_invalid_hospital(self):
        self.client.force_authenticate(self.resident)
        payload = {"hospital": 999999}
        response = self.client.post(reverse("auth_api:complete_profile"), payload, format="json")
        self.assertEqual(response.status_code, 400)

    def test_complete_profile_post_invalid_department(self):
        self.client.force_authenticate(self.resident)
        payload = {"department_ref": 999999}
        response = self.client.post(reverse("auth_api:complete_profile"), payload, format="json")
        self.assertEqual(response.status_code, 400)


class UserbaseIdentityOptionsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="push2_identity", password="pass12345", role="RESIDENT"
        )

    def test_identity_options_fallback_lists(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(reverse("identity_options"))
        self.assertEqual(response.status_code, 200)
        # No Designation/AcademicSession rows exist yet -> fallback branches.
        codes = {d["code"] for d in response.data["designations"]}
        self.assertIn("HOD", codes)
        session_codes = {s["code"] for s in response.data["academic_sessions"]}
        self.assertIn("2025-2026", session_codes)


class UserbaseDataQualityTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(
            username="push2_dq_admin", password="pass12345", role="ADMIN"
        )
        self.resident = User.objects.create_user(
            username="push2_dq_resident",
            password="pass12345",
            role="RESIDENT",
            has_placeholder_email=True,
        )

    def test_summary_denied_for_non_manager(self):
        self.client.force_authenticate(self.resident)
        response = self.client.get(reverse("data-quality-summary"))
        self.assertEqual(response.status_code, 403)

    def test_summary_disabled_layer(self):
        self.client.force_authenticate(self.admin)
        with override_settings(ENABLE_DATA_CORRECTION_LAYER=False):
            response = self.client.get(reverse("data-quality-summary"))
        self.assertEqual(response.status_code, 503)

    def test_summary_ok(self):
        self.client.force_authenticate(self.admin)
        response = self.client.get(reverse("data-quality-summary"))
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(response.data["users_with_placeholder_email"], 1)

    def test_users_view_filters(self):
        self.client.force_authenticate(self.admin)
        for filt in ["placeholder_email", "incomplete_profile", "missing_dates", "missing_email", ""]:
            response = self.client.get(reverse("data-quality-users"), {"filter": filt})
            self.assertEqual(response.status_code, 200, filt)

    def test_users_view_denied_for_non_manager(self):
        self.client.force_authenticate(self.resident)
        response = self.client.get(reverse("data-quality-users"))
        self.assertEqual(response.status_code, 403)

    def test_recompute_denied_for_non_manager(self):
        self.client.force_authenticate(self.resident)
        response = self.client.post(reverse("data-quality-recompute"))
        self.assertEqual(response.status_code, 403)

    def test_recompute_ok(self):
        self.client.force_authenticate(self.admin)
        response = self.client.post(reverse("data-quality-recompute"))
        self.assertEqual(response.status_code, 200)

    def test_audit_denied_for_non_manager(self):
        self.client.force_authenticate(self.resident)
        response = self.client.get(reverse("data-quality-audit"))
        self.assertEqual(response.status_code, 403)

    def test_audit_ok(self):
        self.client.force_authenticate(self.admin)
        response = self.client.get(reverse("data-quality-audit"))
        self.assertEqual(response.status_code, 200)

    def test_data_quality_view_denied_for_non_manager(self):
        self.client.force_authenticate(self.resident)
        response = self.client.get(reverse("data-quality"))
        self.assertEqual(response.status_code, 403)

    def test_data_quality_view_ok(self):
        self.client.force_authenticate(self.admin)
        response = self.client.get(reverse("data-quality"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("summary", response.data)
        self.assertIn("sections", response.data)


class UserbaseHospitalDepartmentActionsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(
            username="push2_action_admin", password="pass12345", role="ADMIN"
        )
        self.hospital = Hospital.objects.create(name="Action Hospital", code="ACT-H")
        self.department = Department.objects.create(name="Action Dept", code="ACT-D")
        HospitalDepartment.objects.create(
            hospital=self.hospital, department=self.department, is_active=True
        )

    def test_hospital_departments_action(self):
        self.client.force_authenticate(self.admin)
        url = reverse("userbase-hospitals-departments", kwargs={"pk": self.hospital.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["department"]["code"], "ACT-D")

    def test_department_roster_action_for_manager(self):
        self.client.force_authenticate(self.admin)
        url = reverse("userbase-departments-roster", kwargs={"pk": self.department.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["department"]["code"], "ACT-D")

    def test_department_roster_action_denied_without_membership(self):
        resident = User.objects.create_user(
            username="push2_roster_resident", password="pass12345", role="RESIDENT"
        )
        self.client.force_authenticate(resident)
        url = reverse("userbase-departments-roster", kwargs={"pk": self.department.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_department_roster_action_allowed_with_membership(self):
        resident = User.objects.create_user(
            username="push2_roster_resident2", password="pass12345", role="RESIDENT"
        )
        DepartmentMembership.objects.create(
            user=resident,
            department=self.department,
            member_type="resident",
            active=True,
            start_date="2020-01-01",
        )
        self.client.force_authenticate(resident)
        url = reverse("userbase-departments-roster", kwargs={"pk": self.department.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["residents"]), 1)


class UserViewSetCreateTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(
            username="push2_uvs_admin", password="pass12345", role="ADMIN"
        )

    def test_create_invalid_role(self):
        self.client.force_authenticate(self.admin)
        response = self.client.post(
            reverse("users_api:users-list"), {"role": "BOGUS", "full_name": "Bad Role"}
        )
        self.assertEqual(response.status_code, 400)

    def test_create_missing_full_name(self):
        self.client.force_authenticate(self.admin)
        response = self.client.post(reverse("users_api:users-list"), {"role": "SUPPORT_STAFF"})
        self.assertEqual(response.status_code, 400)

    def test_create_denied_for_non_manager(self):
        resident = User.objects.create_user(
            username="push2_uvs_resident", password="pass12345", role="RESIDENT"
        )
        self.client.force_authenticate(resident)
        response = self.client.post(
            reverse("users_api:users-list"), {"role": "SUPPORT_STAFF", "full_name": "New Staff"}
        )
        self.assertEqual(response.status_code, 403)

    def test_create_support_staff_success(self):
        self.client.force_authenticate(self.admin)
        response = self.client.post(
            reverse("users_api:users-list"),
            {"role": "SUPPORT_STAFF", "full_name": "New Staff Member"},
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["role"], "SUPPORT_STAFF")
