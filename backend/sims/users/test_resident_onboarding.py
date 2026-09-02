from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIClient

from sims.training.models import TrainingProgram
from sims.users.models import ResidentDocumentRequirement, ResidentProfile, SupervisorProfile, User
from sims.users.onboarding_api import get_resident_onboarding_state
from sims.users.services import create_user_with_profile
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
