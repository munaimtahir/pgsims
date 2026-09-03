from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIClient

from sims.academics.models import AcademicSession, Department
from sims.rotations.models import Hospital
from sims.training.models import TrainingProgram
from sims.users.models import ResidentDocumentRequirement, ResidentProfile, SupervisorProfile, User
from sims.users.onboarding_api import get_resident_onboarding_state
from sims.users.services import create_user_with_profile, recalculate_profile_completion
from sims.supervision.models import PendingSupervisorAssignment, ResidentSupervisorAssignment


class ResidentOnboardingConsolidationTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username="onboard_admin", password="x", role="ADMIN")
        self.program = TrainingProgram.objects.create(code="ONB", name="Onboarding Program", duration_months=60)

    def test_missing_supervisor_creates_pending_record_not_fake_identity(self):
        resident = create_user_with_profile(
            role="RESIDENT", full_name="Dr Pending Resident", actor=self.admin,
            profile_payload={"program_ref": self.program, "supervisor_name": "Prof. Dr. ABC"},
        )
        self.assertTrue(ResidentProfile.objects.filter(user=resident).exists())
        pending = PendingSupervisorAssignment.objects.get(resident__user=resident)
        self.assertEqual(pending.supervisor_name_text, "Prof. Dr. ABC")
        self.assertFalse(User.objects.filter(role="SUPERVISOR", first_name="Prof.").exists())

    def test_existing_supervisor_creates_canonical_assignment(self):
        supervisor = create_user_with_profile(role="SUPERVISOR", full_name="Dr Existing Supervisor", actor=self.admin)
        supervisor_profile = supervisor.supervisor_profile
        resident = create_user_with_profile(
            role="RESIDENT", full_name="Dr Linked Resident", actor=self.admin,
            profile_payload={"program_ref": self.program, "supervisor_profile": supervisor_profile},
        )
        self.assertTrue(ResidentSupervisorAssignment.objects.filter(resident__user=resident, supervisor=supervisor_profile).exists())
        self.assertFalse(PendingSupervisorAssignment.objects.filter(resident__user=resident).exists())

    def test_deferred_document_is_specific_and_upload_clears_reminder(self):
        resident = create_user_with_profile(role="RESIDENT", full_name="Dr Document Resident", actor=self.admin, profile_payload={"program_ref": self.program})
        requirement = ResidentDocumentRequirement.objects.create(document_type="CNIC", display_name="CNIC Copy", stage="ONBOARDING")
        state = get_resident_onboarding_state(resident)
        self.assertEqual(state["pending_uploads"], [])
        client = APIClient()
        client.force_authenticate(resident)
        document_id = resident.resident_profile.documents.get(requirement=requirement).id
        deferred = client.post(f"/api/resident-documents/{document_id}/defer/")
        self.assertEqual(deferred.status_code, 200)
        self.assertEqual(deferred.data["status"], "DEFERRED")
        self.assertEqual(client.get("/api/auth/me/").data["pending_uploads"][0]["display_name"], "CNIC Copy")
        uploaded = client.post(f"/api/resident-documents/{document_id}/upload/", {"file": SimpleUploadedFile("cnic.pdf", b"pdf")}, format="multipart")
        self.assertEqual(uploaded.status_code, 200)
        self.assertEqual(client.get("/api/auth/me/").data["pending_upload_count"], 0)

    def test_resident_cannot_review_document(self):
        resident = create_user_with_profile(role="RESIDENT", full_name="Dr Secure Resident", actor=self.admin, profile_payload={"program_ref": self.program})
        requirement = ResidentDocumentRequirement.objects.create(document_type="CNIC", display_name="CNIC Copy")
        get_resident_onboarding_state(resident)
        document = resident.resident_profile.documents.get(requirement=requirement)
        client = APIClient(); client.force_authenticate(resident)
        response = client.post(f"/api/resident-documents/{document.id}/review/", {"status": "VERIFIED"})
        self.assertIn(response.status_code, (403, 404))

    def test_non_resident_cannot_access_resident_onboarding_api(self):
        client = APIClient()
        client.force_authenticate(self.admin)

        self.assertEqual(client.get("/api/auth/onboarding/").status_code, 403)
        self.assertEqual(client.get("/api/resident-onboarding/state/").status_code, 403)
        self.assertEqual(
            client.post("/api/resident-onboarding/state/", {"accepted": True}, format="json").status_code,
            403,
        )

    def test_auth_me_requires_declaration_before_dashboard(self):
        resident = create_user_with_profile(
            role="RESIDENT",
            full_name="Dr Declaration Pending",
            actor=self.admin,
            profile_payload={"program_ref": self.program},
        )
        resident.must_change_password = False
        resident.save(update_fields=["must_change_password"])
        client = APIClient()
        client.force_authenticate(resident)

        onboarding_state = {"required_onboarding_fields": [], "onboarding_complete": False}
        with (
            patch("sims.users.userbase_views.recalculate_profile_completion"),
            patch("sims.users.userbase_views.get_missing_profile_fields", return_value=[]),
            patch("sims.users.onboarding_api.get_resident_onboarding_state", return_value=onboarding_state),
        ):
            response = client.get("/api/auth/me/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["allowed_next_route"], "/complete-profile")


class ResidentOnboardingReviewGateTests(TestCase):
    """Wave 1 addition: admin approve / request-correction review gate on ResidentProfile."""

    def setUp(self):
        self.admin = User.objects.create_user(username="review_admin", password="x", role="ADMIN")
        self.other_resident = User.objects.create_user(username="review_other_resident", password="x", role="RESIDENT")
        self.department = Department.objects.create(code="REV-DEPT", name="Review Department", active=True)
        self.hospital = Hospital.objects.create(code="REV-H", name="Review Hospital", is_active=True)
        self.session = AcademicSession.objects.create(code="REV-2026", name="Review Session 2026")
        self.program = TrainingProgram.objects.create(code="REV-PROG", name="Review Program", duration_months=48)

    def _make_resident(self, complete=True):
        resident = create_user_with_profile(
            role="RESIDENT",
            full_name="Dr Review Resident",
            actor=self.admin,
            profile_payload={"program_ref": self.program},
        )
        resident.must_change_password = False
        resident.phone_number = "+923001234567"
        resident.email = "review.resident@example.com"
        resident.save(update_fields=["must_change_password", "phone_number", "email"])
        if complete:
            profile = resident.resident_profile
            profile.hospital = self.hospital
            profile.department_ref = self.department
            profile.academic_session_ref = self.session
            profile.save(update_fields=["hospital", "department_ref", "academic_session_ref"])
        recalculate_profile_completion(resident)
        resident.refresh_from_db()
        return resident

    def _approve_url(self, resident):
        return f"/api/residents/{resident.id}/approve-onboarding/"

    def _correction_url(self, resident):
        return f"/api/residents/{resident.id}/request-onboarding-correction/"

    def test_incomplete_profile_cannot_be_submitted(self):
        resident = self._make_resident(complete=False)
        self.assertFalse(resident.is_profile_complete)
        client = APIClient()
        client.force_authenticate(resident)
        response = client.post("/api/resident-onboarding/state/", {"accepted": True}, format="json")
        self.assertEqual(response.status_code, 400)
        resident.resident_profile.refresh_from_db()
        self.assertEqual(resident.resident_profile.review_status, ResidentProfile.REVIEW_NOT_SUBMITTED)

    def test_complete_profile_submission_moves_to_pending_review(self):
        resident = self._make_resident(complete=True)
        self.assertTrue(resident.is_profile_complete)
        client = APIClient()
        client.force_authenticate(resident)
        response = client.post("/api/resident-onboarding/state/", {"accepted": True}, format="json")
        self.assertEqual(response.status_code, 200)
        resident.resident_profile.refresh_from_db()
        self.assertEqual(resident.resident_profile.review_status, ResidentProfile.REVIEW_PENDING_REVIEW)
        self.assertIsNotNone(resident.resident_profile.submitted_at)

    def test_resident_cannot_approve_own_onboarding(self):
        resident = self._make_resident(complete=True)
        client = APIClient()
        client.force_authenticate(resident)
        client.post("/api/resident-onboarding/state/", {"accepted": True}, format="json")
        response = client.post(self._approve_url(resident))
        self.assertEqual(response.status_code, 403)

    def test_unrelated_resident_cannot_approve_another_residents_onboarding(self):
        resident = self._make_resident(complete=True)
        client = APIClient()
        client.force_authenticate(resident)
        client.post("/api/resident-onboarding/state/", {"accepted": True}, format="json")
        other_client = APIClient()
        other_client.force_authenticate(self.other_resident)
        response = other_client.post(self._approve_url(resident))
        self.assertEqual(response.status_code, 403)

    def test_admin_cannot_approve_unsubmitted_profile(self):
        resident = self._make_resident(complete=True)
        client = APIClient()
        client.force_authenticate(self.admin)
        response = client.post(self._approve_url(resident))
        self.assertEqual(response.status_code, 409)

    def test_admin_can_approve_pending_review_profile(self):
        resident = self._make_resident(complete=True)
        resident_client = APIClient()
        resident_client.force_authenticate(resident)
        resident_client.post("/api/resident-onboarding/state/", {"accepted": True}, format="json")

        admin_client = APIClient()
        admin_client.force_authenticate(self.admin)
        response = admin_client.post(self._approve_url(resident))
        self.assertEqual(response.status_code, 200)
        resident.resident_profile.refresh_from_db()
        self.assertEqual(resident.resident_profile.review_status, ResidentProfile.REVIEW_APPROVED)
        self.assertEqual(resident.resident_profile.reviewed_by_id, self.admin.id)
        self.assertIsNotNone(resident.resident_profile.reviewed_at)

    def test_cannot_resubmit_after_approval(self):
        resident = self._make_resident(complete=True)
        resident_client = APIClient()
        resident_client.force_authenticate(resident)
        resident_client.post("/api/resident-onboarding/state/", {"accepted": True}, format="json")
        admin_client = APIClient()
        admin_client.force_authenticate(self.admin)
        admin_client.post(self._approve_url(resident))

        response = resident_client.post("/api/resident-onboarding/state/", {"accepted": True}, format="json")
        self.assertEqual(response.status_code, 409)

    def test_correction_request_requires_reason(self):
        resident = self._make_resident(complete=True)
        resident_client = APIClient()
        resident_client.force_authenticate(resident)
        resident_client.post("/api/resident-onboarding/state/", {"accepted": True}, format="json")

        admin_client = APIClient()
        admin_client.force_authenticate(self.admin)
        response = admin_client.post(self._correction_url(resident), {}, format="json")
        self.assertEqual(response.status_code, 400)

    def test_correction_request_and_resubmission_flow(self):
        resident = self._make_resident(complete=True)
        resident_client = APIClient()
        resident_client.force_authenticate(resident)
        resident_client.post("/api/resident-onboarding/state/", {"accepted": True}, format="json")

        admin_client = APIClient()
        admin_client.force_authenticate(self.admin)
        correction = admin_client.post(
            self._correction_url(resident), {"reason": "Registration number looks wrong."}, format="json"
        )
        self.assertEqual(correction.status_code, 200)
        resident.resident_profile.refresh_from_db()
        self.assertEqual(resident.resident_profile.review_status, ResidentProfile.REVIEW_CORRECTION_REQUIRED)
        self.assertEqual(resident.resident_profile.review_note, "Registration number looks wrong.")
        self.assertFalse(resident.resident_profile.declaration_accepted)

        me_response = resident_client.get("/api/auth/me/")
        self.assertEqual(me_response.data["onboarding_review_status"], "CORRECTION_REQUIRED")
        self.assertEqual(me_response.data["onboarding_review_note"], "Registration number looks wrong.")

        resubmit = resident_client.post("/api/resident-onboarding/state/", {"accepted": True}, format="json")
        self.assertEqual(resubmit.status_code, 200)
        resident.resident_profile.refresh_from_db()
        self.assertEqual(resident.resident_profile.review_status, ResidentProfile.REVIEW_PENDING_REVIEW)

    def test_supervisor_cannot_request_correction(self):
        supervisor = create_user_with_profile(role="SUPERVISOR", full_name="Dr Review Supervisor", actor=self.admin)
        resident = self._make_resident(complete=True)
        resident_client = APIClient()
        resident_client.force_authenticate(resident)
        resident_client.post("/api/resident-onboarding/state/", {"accepted": True}, format="json")

        supervisor_client = APIClient()
        supervisor_client.force_authenticate(supervisor)
        response = supervisor_client.post(self._correction_url(resident), {"reason": "x"}, format="json")
        self.assertEqual(response.status_code, 403)

    def test_patch_personal_info_updates_user_and_profile(self):
        resident = self._make_resident(complete=False)
        client = APIClient()
        client.force_authenticate(resident)
        response = client.patch(
            "/api/auth/onboarding/",
            {"fields": {"phone": "03009876543", "email": "updated@example.com", "full_name": "Updated Resident"}},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        resident.refresh_from_db()
        resident.resident_profile.refresh_from_db()
        self.assertEqual(resident.phone_number, "03009876543")
        self.assertEqual(resident.email, "updated@example.com")
        self.assertEqual(resident.first_name, "Updated")
        self.assertEqual(resident.last_name, "Resident")
        self.assertEqual(resident.resident_profile.phone, "03009876543")
        self.assertEqual(resident.resident_profile.email, "updated@example.com")
