import io
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from sims.academics.models import Department
from sims.rotations.models import Hospital
from sims.supervision.models import ResidentSupervisorAssignment
from sims.training.models import ResidentTrainingRecord, TrainingProgram
from sims.users.models import (
    AdminProfile,
    ResidentDocument,
    ResidentDocumentRequirement,
    ResidentProfile,
    SupervisorProfile,
    SupportStaffProfile,
    User,
)


class SecurityRemediationM1Tests(APITestCase):
    """Regression and authorization tests for the four M0 P0 security blockers and auth lifecycle."""

    def setUp(self):
        # Create department and hospital
        self.department = Department.objects.create(code="MED-SEC", name="Security Medicine", active=True)
        self.hospital = Hospital.objects.create(code="H-SEC", name="Security Hospital", is_active=True)
        self.program = TrainingProgram.objects.create(
            code="SEC-PROG",
            name="Security Training Program",
            duration_months=36,
            degree_type=TrainingProgram.DEGREE_FCPS,
            department=self.department,
            active=True,
        )

        # Admin User
        self.admin_user = User.objects.create_superuser(
            username="admin_sec",
            email="admin_sec@example.com",
            password="AdminPassword123!",
            role="ADMIN",
        )
        self.admin_profile = AdminProfile.objects.create(
            user=self.admin_user,
            designation="Security Director",
        )

        # Resident 1
        self.resident_1_user = User.objects.create_user(
            username="resident1_sec",
            email="resident1_sec@example.com",
            password="ResidentPass123!",
            role="RESIDENT",
            first_name="Resident",
            last_name="One",
        )
        self.resident_1_profile = ResidentProfile.objects.create(
            user=self.resident_1_user,
            department_ref=self.department,
            hospital=self.hospital,
            program_ref=self.program,
        )
        self.rtr_1 = ResidentTrainingRecord.objects.create(
            resident_user=self.resident_1_user,
            program=self.program,
            start_date="2026-01-01",
            active=True,
        )

        # Resident 2
        self.resident_2_user = User.objects.create_user(
            username="resident2_sec",
            email="resident2_sec@example.com",
            password="ResidentPass123!",
            role="RESIDENT",
            first_name="Resident",
            last_name="Two",
        )
        self.resident_2_profile = ResidentProfile.objects.create(
            user=self.resident_2_user,
            department_ref=self.department,
            hospital=self.hospital,
            program_ref=self.program,
        )
        self.rtr_2 = ResidentTrainingRecord.objects.create(
            resident_user=self.resident_2_user,
            program=self.program,
            start_date="2026-01-01",
            active=True,
        )

        # Supervisor 1 (Assigned to Resident 1)
        self.supervisor_1_user = User.objects.create_user(
            username="supervisor1_sec",
            email="supervisor1_sec@example.com",
            password="SupervisorPass123!",
            role="SUPERVISOR",
            first_name="Supervisor",
            last_name="One",
        )
        self.supervisor_1_profile = SupervisorProfile.objects.create(
            user=self.supervisor_1_user,
            department_ref=self.department,
            hospital=self.hospital,
        )

        # Supervisor 2 (Unassigned to Resident 1, assigned to Resident 2)
        self.supervisor_2_user = User.objects.create_user(
            username="supervisor2_sec",
            email="supervisor2_sec@example.com",
            password="SupervisorPass123!",
            role="SUPERVISOR",
            first_name="Supervisor",
            last_name="Two",
        )
        self.supervisor_2_profile = SupervisorProfile.objects.create(
            user=self.supervisor_2_user,
            department_ref=self.department,
            hospital=self.hospital,
        )

        # Canonical Assignments
        ResidentSupervisorAssignment.objects.create(
            resident=self.resident_1_profile,
            supervisor=self.supervisor_1_profile,
            assignment_type=ResidentSupervisorAssignment.ASSIGNMENT_PRIMARY,
            start_date="2026-01-01",
            status=ResidentSupervisorAssignment.STATUS_ACTIVE,
            is_active=True,
        )
        ResidentSupervisorAssignment.objects.create(
            resident=self.resident_2_profile,
            supervisor=self.supervisor_2_profile,
            assignment_type=ResidentSupervisorAssignment.ASSIGNMENT_PRIMARY,
            start_date="2026-01-01",
            status=ResidentSupervisorAssignment.STATUS_ACTIVE,
            is_active=True,
        )

        # Document requirement & Document for Resident 1
        self.req = ResidentDocumentRequirement.objects.create(
            document_type="pmdc_registration",
            display_name="PMDC Certificate",
            stage=ResidentDocumentRequirement.STAGE_ONBOARDING,
            is_required=True,
            is_active=True,
        )
        dummy_file = SimpleUploadedFile("pmdc_cert.pdf", b"%PDF-1.4 dummy pdf content", content_type="application/pdf")
        self.doc_1 = ResidentDocument.objects.create(
            resident=self.resident_1_profile,
            requirement=self.req,
            document_type="pmdc_registration",
            title="PMDC Certificate",
            file=dummy_file,
            original_filename="pmdc_cert.pdf",
            status=ResidentDocument.STATUS_UPLOADED,
        )

    # =========================================================================
    # P0-1: Self-Profile Privilege Escalation Protection
    # =========================================================================

    def test_self_profile_update_cannot_elevate_role_to_admin(self):
        """Resident cannot escalate role to ADMIN via /api/auth/profile/update/."""
        self.client.force_authenticate(user=self.resident_1_user)
        response = self.client.patch(
            reverse("auth_api:profile_update"),
            {"role": "ADMIN"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.resident_1_user.refresh_from_db()
        self.assertEqual(self.resident_1_user.role, "RESIDENT")

    def test_self_profile_update_cannot_mutate_is_active(self):
        """Resident cannot deactivate/reactivate account via self profile update."""
        self.client.force_authenticate(user=self.resident_1_user)
        response = self.client.patch(
            reverse("auth_api:profile_update"),
            {"is_active": False},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.resident_1_user.refresh_from_db()
        self.assertTrue(self.resident_1_user.is_active)

    def test_self_profile_update_cannot_mutate_username(self):
        """Resident cannot change username via self profile update."""
        self.client.force_authenticate(user=self.resident_1_user)
        response = self.client.patch(
            reverse("auth_api:profile_update"),
            {"username": "new_admin_username"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.resident_1_user.refresh_from_db()
        self.assertEqual(self.resident_1_user.username, "resident1_sec")

    def test_self_profile_update_allows_safe_fields(self):
        """Resident can safely update first_name, last_name, and phone_number."""
        self.client.force_authenticate(user=self.resident_1_user)
        response = self.client.patch(
            reverse("auth_api:profile_update"),
            {
                "first_name": "UpdatedFirst",
                "last_name": "UpdatedLast",
                "phone_number": "+923001234567",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.resident_1_user.refresh_from_db()
        self.assertEqual(self.resident_1_user.first_name, "UpdatedFirst")
        self.assertEqual(self.resident_1_user.last_name, "UpdatedLast")
        self.assertEqual(self.resident_1_user.phone_number, "+923001234567")

    # =========================================================================
    # P0-2: Role Profile API Authorization & Scoping
    # =========================================================================

    def test_resident_cannot_list_admin_profiles(self):
        """Resident calling admin-profiles list receives empty list."""
        self.client.force_authenticate(user=self.resident_1_user)
        url = reverse("userbase-admins-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Non-admin sees 0 admin profiles
        results = response.data.get("results", response.data) if isinstance(response.data, dict) else response.data
        self.assertEqual(len(results), 0)

    def test_resident_cannot_retrieve_other_resident_profile(self):
        """Resident cannot view another resident's profile object."""
        self.client.force_authenticate(user=self.resident_1_user)
        url = reverse("userbase-residents-detail", kwargs={"user_id": self.resident_2_user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_resident_cannot_mutate_other_resident_profile(self):
        """Resident cannot patch another resident's profile."""
        self.client.force_authenticate(user=self.resident_1_user)
        url = reverse("userbase-residents-detail", kwargs={"user_id": self.resident_2_user.id})
        response = self.client.patch(url, {"registration_no": "HACKED"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unassigned_supervisor_cannot_view_resident_profile(self):
        """Supervisor 2 cannot view Resident 1's profile because there is no assignment."""
        self.client.force_authenticate(user=self.supervisor_2_user)
        url = reverse("userbase-residents-detail", kwargs={"user_id": self.resident_1_user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_assigned_supervisor_can_view_resident_profile(self):
        """Supervisor 1 can view Resident 1's profile because an active assignment exists."""
        self.client.force_authenticate(user=self.supervisor_1_user)
        url = reverse("userbase-residents-detail", kwargs={"user_id": self.resident_1_user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_view_any_resident_profile(self):
        """Admin can view any resident profile."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("userbase-residents-detail", kwargs={"user_id": self.resident_1_user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # =========================================================================
    # P0-3: Protected Resident Document Access
    # =========================================================================

    def test_unauthenticated_cannot_access_resident_document(self):
        """Unauthenticated request to download resident document is denied."""
        url = reverse("resident-documents-file", kwargs={"pk": self.doc_1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unrelated_resident_cannot_access_document(self):
        """Resident 2 cannot access Resident 1's uploaded document."""
        self.client.force_authenticate(user=self.resident_2_user)
        url = reverse("resident-documents-file", kwargs={"pk": self.doc_1.id})
        response = self.client.get(url)
        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND])

    def test_unassigned_supervisor_cannot_access_document(self):
        """Supervisor 2 (unassigned) cannot access Resident 1's document."""
        self.client.force_authenticate(user=self.supervisor_2_user)
        url = reverse("resident-documents-file", kwargs={"pk": self.doc_1.id})
        response = self.client.get(url)
        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND])

    def test_document_owner_can_access_document(self):
        """Resident 1 (owner) can download own document with private cache headers."""
        self.client.force_authenticate(user=self.resident_1_user)
        url = reverse("resident-documents-file", kwargs={"pk": self.doc_1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("private", response.headers.get("Cache-Control", ""))

    def test_assigned_supervisor_can_access_document(self):
        """Supervisor 1 (assigned) can access Resident 1's document."""
        self.client.force_authenticate(user=self.supervisor_1_user)
        url = reverse("resident-documents-file", kwargs={"pk": self.doc_1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_access_document(self):
        """Admin can access any resident's document."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("resident-documents-file", kwargs={"pk": self.doc_1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # =========================================================================
    # P0-4: Canonical Supervisor Assignment on Progress View
    # =========================================================================

    def test_unassigned_supervisor_cannot_access_resident_progress(self):
        """Supervisor 2 cannot access Resident 1's progress endpoint (IDOR prevention)."""
        self.client.force_authenticate(user=self.supervisor_2_user)
        url = reverse("supervisor-resident-progress", kwargs={"resident_id": self.resident_1_user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_assigned_supervisor_can_access_resident_progress(self):
        """Supervisor 1 can access Resident 1's progress endpoint."""
        self.client.force_authenticate(user=self.supervisor_1_user)
        url = reverse("supervisor-resident-progress", kwargs={"resident_id": self.resident_1_user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["RESIDENT"]["id"], self.resident_1_user.id)

    def test_admin_can_access_resident_progress(self):
        """Admin can access any resident's progress endpoint."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("supervisor-resident-progress", kwargs={"resident_id": self.resident_1_user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # =========================================================================
    # JWT Logout & Revocation & Password Validation
    # =========================================================================

    def test_jwt_logout_blacklists_refresh_token(self):
        """Logout endpoint blacklists refresh token, preventing subsequent refresh."""
        refresh = RefreshToken.for_user(self.resident_1_user)
        refresh_str = str(refresh)

        # Verify refresh works before logout
        refresh_url = reverse("auth_api:token_refresh")
        refresh_resp = self.client.post(refresh_url, {"refresh": refresh_str}, format="json")
        self.assertEqual(refresh_resp.status_code, status.HTTP_200_OK)

        # Get latest refresh token from rotation
        new_refresh = refresh_resp.data.get("refresh", refresh_str)

        # Call logout
        self.client.force_authenticate(user=self.resident_1_user)
        logout_url = reverse("auth_api:logout")
        logout_resp = self.client.post(logout_url, {"refresh": new_refresh}, format="json")
        self.assertEqual(logout_resp.status_code, status.HTTP_200_OK)

        # Try to refresh with blacklisted token
        self.client.logout()
        failed_refresh = self.client.post(refresh_url, {"refresh": new_refresh}, format="json")
        self.assertEqual(failed_refresh.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_change_password_validates_password_strength(self):
        """Password change rejects too short or common passwords."""
        self.client.force_authenticate(user=self.resident_1_user)
        url = reverse("auth_api:change_password")
        response = self.client.post(
            url,
            {
                "old_password": "ResidentPass123!",
                "new_password": "123",
                "new_password2": "123",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
