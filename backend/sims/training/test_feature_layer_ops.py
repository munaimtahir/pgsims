from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from sims.academics.models import Department
from sims.rotations.models import Hospital, HospitalDepartment
from sims.training.models import (
    LeaveRequest,
    LogbookEntry,
    LogbookThresholdConfig,
    ResidentSubmission,
    RotationAssignment,
    RotationCompletion,
    SubmissionCertificate,
    SubmissionRequirementTemplate,
)
from sims.users.models import HODAssignment, SupervisorResidentLink

from .models import ResidentTrainingRecord, TrainingProgram

User = get_user_model()


def make_user(username, role, **kwargs):
    if role in {"pg", "resident"}:
        kwargs.setdefault("specialty", "medicine")
        kwargs.setdefault("year", "1")
    if role in {"supervisor", "faculty"}:
        kwargs.setdefault("specialty", "medicine")
    return User.objects.create_user(
        username=username,
        password="Test1234!",
        role=role,
        email=f"{username}@example.com",
        **kwargs,
    )


class FeatureLayerOperationalFlowTests(APITestCase):
    def setUp(self):
        self.department = Department.objects.create(name="Medicine", code="MED-FL")
        self.hospital = Hospital.objects.create(name="Teaching Hospital", code="TH-FL")
        self.hospital_department = HospitalDepartment.objects.create(
            hospital=self.hospital, department=self.department
        )

        self.program = TrainingProgram.objects.create(
            name="FCPS Medicine",
            code="FCPS-MED-FL",
            duration_months=48,
            department=self.department,
        )

        self.admin = make_user("fl_admin", "admin")
        self.utrmc_admin = make_user("fl_utrmc_admin", "utrmc_admin")
        self.utrmc_user = make_user("fl_utrmc_user", "utrmc_user")
        self.supervisor = make_user("fl_supervisor", "supervisor")
        self.resident = make_user(
            "fl_resident",
            "pg",
            supervisor=self.supervisor,
            home_department=self.department,
            home_hospital=self.hospital,
        )

        self.rtr = ResidentTrainingRecord.objects.create(
            resident_user=self.resident,
            program=self.program,
            start_date=date.today() - timedelta(days=120),
            active=True,
        )

        SupervisorResidentLink.objects.create(
            supervisor_user=self.supervisor,
            resident_user=self.resident,
            department=self.department,
            start_date=date.today() - timedelta(days=120),
            active=True,
        )
        HODAssignment.objects.create(
            department=self.department,
            hod_user=self.supervisor,
            start_date=date.today() - timedelta(days=30),
            active=True,
        )

    def test_logbook_submit_return_resubmit_approve_flow(self):
        self.client.force_authenticate(self.resident)
        create_resp = self.client.post(
            "/api/logbook/",
            {
                "patient_id_number": "P-001",
                "patient_name": "Jane Doe",
                "age": 32,
                "gender": "F",
                "disease_area": "Medicine",
                "diagnosis": "Hypertension",
                "clinical_presentation": "Headache",
                "management_plan": "Medication adjustment",
                "resident_reflection": "Need tighter follow-up",
                "patient_seen_at": "2026-01-10T10:30:00Z",
            },
            format="json",
        )
        self.assertEqual(create_resp.status_code, status.HTTP_201_CREATED)
        entry_id = create_resp.data["id"]

        submit_resp = self.client.post(f"/api/logbook/{entry_id}/submit/")
        self.assertEqual(submit_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(submit_resp.data["status"], LogbookEntry.STATUS_SUBMITTED)

        self.client.force_authenticate(self.supervisor)
        return_resp = self.client.post(
            f"/api/logbook/{entry_id}/review/",
            {"action": "returned", "feedback": "Please clarify management rationale."},
            format="json",
        )
        self.assertEqual(return_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(return_resp.data["status"], LogbookEntry.STATUS_RETURNED)

        self.client.force_authenticate(self.resident)
        patch_resp = self.client.patch(
            f"/api/logbook/{entry_id}/",
            {"management_plan": "Added guideline-based rationale."},
            format="json",
        )
        self.assertEqual(patch_resp.status_code, status.HTTP_200_OK)

        resubmit_resp = self.client.post(f"/api/logbook/{entry_id}/submit/")
        self.assertEqual(resubmit_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resubmit_resp.data["status"], LogbookEntry.STATUS_SUBMITTED)

        self.client.force_authenticate(self.supervisor)
        approve_resp = self.client.post(
            f"/api/logbook/{entry_id}/review/",
            {"action": "approved", "feedback": "Approved."},
            format="json",
        )
        self.assertEqual(approve_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(approve_resp.data["status"], LogbookEntry.STATUS_APPROVED)
        self.assertEqual(approve_resp.data["feedback"], "Approved.")

    def test_logbook_invalid_transitions_and_wrong_reviewer_are_blocked(self):
        self.client.force_authenticate(self.resident)
        create_resp = self.client.post(
            "/api/logbook/",
            {
                "patient_id_number": "P-INVALID-001",
                "patient_seen_at": "2026-01-10T10:30:00Z",
            },
            format="json",
        )
        self.assertEqual(create_resp.status_code, status.HTTP_201_CREATED)
        entry_id = create_resp.data["id"]

        self.client.force_authenticate(self.supervisor)
        draft_review = self.client.post(
            f"/api/logbook/{entry_id}/review/",
            {"action": "approved", "feedback": "Cannot approve draft."},
            format="json",
        )
        self.assertEqual(draft_review.status_code, status.HTTP_400_BAD_REQUEST)

        unrelated_supervisor = make_user("fl_unrelated_supervisor", "supervisor")
        self.client.force_authenticate(unrelated_supervisor)
        unrelated_review = self.client.post(
            f"/api/logbook/{entry_id}/review/",
            {"action": "approved", "feedback": "Not my resident."},
            format="json",
        )
        self.assertEqual(unrelated_review.status_code, status.HTTP_404_NOT_FOUND)

        self.client.force_authenticate(self.resident)
        submitted = self.client.post(f"/api/logbook/{entry_id}/submit/")
        self.assertEqual(submitted.status_code, status.HTTP_200_OK)

        self.client.force_authenticate(unrelated_supervisor)
        wrong_reviewer = self.client.post(
            f"/api/logbook/{entry_id}/review/",
            {"action": "approved", "feedback": "Not my resident."},
            format="json",
        )
        self.assertEqual(wrong_reviewer.status_code, status.HTTP_404_NOT_FOUND)

        self.client.force_authenticate(self.supervisor)
        bad_action = self.client.post(
            f"/api/logbook/{entry_id}/review/",
            {"action": "invalid", "feedback": "Bad action."},
            format="json",
        )
        self.assertEqual(bad_action.status_code, status.HTTP_400_BAD_REQUEST)

        approved = self.client.post(
            f"/api/logbook/{entry_id}/review/",
            {"action": "approved", "feedback": "Approved."},
            format="json",
        )
        self.assertEqual(approved.status_code, status.HTTP_200_OK)

        self.client.force_authenticate(self.resident)
        approved_resubmit = self.client.post(f"/api/logbook/{entry_id}/submit/")
        self.assertEqual(approved_resubmit.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logbook_threshold_per_rotation_and_period(self):
        rotation = RotationAssignment.objects.create(
            resident_training=self.rtr,
            hospital_department=self.hospital_department,
            start_date=date.today() - timedelta(days=40),
            end_date=date.today() + timedelta(days=5),
            status=RotationAssignment.STATUS_COMPLETED,
            requested_by=self.admin,
        )
        LogbookThresholdConfig.objects.create(
            name="Per rotation",
            mode=LogbookThresholdConfig.MODE_PER_ROTATION,
            min_approved_entries=1,
            program=self.program,
            department=self.department,
            configured_by=self.admin,
            is_active=True,
        )
        LogbookThresholdConfig.objects.create(
            name="Monthly minimum",
            mode=LogbookThresholdConfig.MODE_PER_PERIOD,
            min_approved_entries=2,
            period_days=30,
            program=self.program,
            department=self.department,
            configured_by=self.admin,
            is_active=True,
        )

        LogbookEntry.objects.create(
            resident_training_record=self.rtr,
            rotation_assignment=rotation,
            patient_id_number="P-100",
            patient_seen_at=timezone.now(),
            status=LogbookEntry.STATUS_APPROVED,
            approved_at=timezone.now(),
            created_by=self.resident,
        )

        self.client.force_authenticate(self.resident)
        first = self.client.get("/api/logbook/my-threshold/")
        self.assertEqual(first.status_code, status.HTTP_200_OK)
        self.assertFalse(first.data["overall_met"])

        LogbookEntry.objects.create(
            resident_training_record=self.rtr,
            rotation_assignment=rotation,
            patient_id_number="P-101",
            patient_seen_at=timezone.now(),
            status=LogbookEntry.STATUS_APPROVED,
            approved_at=timezone.now(),
            created_by=self.resident,
        )
        second = self.client.get("/api/logbook/my-threshold/")
        self.assertEqual(second.status_code, status.HTTP_200_OK)
        self.assertTrue(second.data["overall_met"])

    def test_synopsis_and_thesis_submission_completeness_certificate_flow(self):
        synopsis_requirement = SubmissionRequirementTemplate.objects.create(
            submission_type=SubmissionRequirementTemplate.TYPE_SYNOPSIS,
            code="SYN-1",
            title="Synopsis Proposal",
            is_required=True,
            active=True,
            program=self.program,
            department=self.department,
            created_by=self.admin,
        )
        thesis_requirement = SubmissionRequirementTemplate.objects.create(
            submission_type=SubmissionRequirementTemplate.TYPE_THESIS,
            code="THE-1",
            title="Thesis Document",
            is_required=True,
            active=True,
            program=self.program,
            department=self.department,
            created_by=self.admin,
        )

        self.client.force_authenticate(self.resident)
        synopsis_submit_without_docs = self.client.post("/api/submissions/synopsis/submit/")
        self.assertEqual(synopsis_submit_without_docs.status_code, status.HTTP_400_BAD_REQUEST)

        synopsis_file = SimpleUploadedFile("synopsis.pdf", b"synopsis-bytes", content_type="application/pdf")
        synopsis_upload = self.client.post(
            "/api/submissions/synopsis/documents/",
            {"file": synopsis_file, "requirement": synopsis_requirement.id},
            format="multipart",
        )
        self.assertEqual(synopsis_upload.status_code, status.HTTP_201_CREATED)
        synopsis_submit = self.client.post("/api/submissions/synopsis/submit/")
        self.assertEqual(synopsis_submit.status_code, status.HTTP_200_OK)
        self.assertEqual(synopsis_submit.data["status"], ResidentSubmission.STATUS_SUBMITTED)

        thesis_file = SimpleUploadedFile("thesis.pdf", b"thesis-bytes", content_type="application/pdf")
        thesis_upload = self.client.post(
            "/api/submissions/thesis/documents/",
            {"file": thesis_file, "requirement": thesis_requirement.id},
            format="multipart",
        )
        self.assertEqual(thesis_upload.status_code, status.HTTP_201_CREATED)
        thesis_submit = self.client.post("/api/submissions/thesis/submit/")
        self.assertEqual(thesis_submit.status_code, status.HTTP_200_OK)
        self.assertEqual(thesis_submit.data["status"], ResidentSubmission.STATUS_SUBMITTED)

        self.client.force_authenticate(self.utrmc_admin)
        synopsis_review = self.client.post(
            f"/api/submissions/synopsis/{synopsis_submit.data['id']}/review/",
            {"action": "verify", "comments": "Complete package."},
            format="json",
        )
        self.assertEqual(synopsis_review.status_code, status.HTTP_200_OK)
        self.assertEqual(synopsis_review.data["status"], ResidentSubmission.STATUS_CERTIFICATE_ISSUED)

        thesis_review = self.client.post(
            f"/api/submissions/thesis/{thesis_submit.data['id']}/review/",
            {"action": "verify", "comments": "Complete package."},
            format="json",
        )
        self.assertEqual(thesis_review.status_code, status.HTTP_200_OK)
        self.assertEqual(thesis_review.data["status"], ResidentSubmission.STATUS_CERTIFICATE_ISSUED)

        self.assertTrue(
            SubmissionCertificate.objects.filter(
                submission_id=synopsis_submit.data["id"],
            ).exists()
        )
        self.assertTrue(
            SubmissionCertificate.objects.filter(
                submission_id=thesis_submit.data["id"],
            ).exists()
        )

    def test_rotation_application_decision_activation_completion_verification_flow(self):
        self.client.force_authenticate(self.admin)
        create_resp = self.client.post(
            "/api/rotations/",
            {
                "resident_training": self.rtr.id,
                "hospital_department": self.hospital_department.id,
                "start_date": str(date.today() + timedelta(days=1)),
                "end_date": str(date.today() + timedelta(days=45)),
            },
            format="json",
        )
        self.assertEqual(create_resp.status_code, status.HTTP_201_CREATED)
        rotation_id = create_resp.data["id"]

        self.client.force_authenticate(self.resident)
        submit_resp = self.client.post(f"/api/rotations/{rotation_id}/submit/")
        self.assertEqual(submit_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(submit_resp.data["status"], RotationAssignment.STATUS_SUBMITTED)

        self.client.force_authenticate(self.supervisor)
        review_resp = self.client.post(
            f"/api/rotations/{rotation_id}/review-application/",
            {"action": "approve"},
            format="json",
        )
        self.assertEqual(review_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(review_resp.data["status"], RotationAssignment.STATUS_APPROVED)

        self.client.force_authenticate(self.admin)
        activate_resp = self.client.post(f"/api/rotations/{rotation_id}/activate/")
        self.assertEqual(activate_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(activate_resp.data["status"], RotationAssignment.STATUS_ACTIVE)

        self.client.force_authenticate(self.supervisor)
        confirm_resp = self.client.post(
            f"/api/rotations/{rotation_id}/confirm-completion/",
            {"notes": "Rotation completed successfully."},
            format="json",
        )
        self.assertEqual(confirm_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(
            confirm_resp.data["completion"]["status"],
            RotationCompletion.STATUS_PENDING_UTRMC_VERIFICATION,
        )
        completion_id = confirm_resp.data["completion"]["id"]

        self.client.force_authenticate(self.utrmc_admin)
        verify_resp = self.client.post(f"/api/rotations/completions/{completion_id}/verify/")
        self.assertEqual(verify_resp.status_code, status.HTTP_200_OK)
        self.assertEqual(verify_resp.data["status"], RotationCompletion.STATUS_VERIFIED)

    def test_leave_invalid_transitions_and_wrong_role_actions_are_blocked(self):
        leave = LeaveRequest.objects.create(
            resident_training=self.rtr,
            leave_type=LeaveRequest.TYPE_ANNUAL,
            start_date=date.today() + timedelta(days=10),
            end_date=date.today() + timedelta(days=12),
            reason="Transition coverage",
        )

        self.client.force_authenticate(self.resident)
        resident_approve = self.client.post(f"/api/leaves/{leave.id}/approve/")
        self.assertEqual(resident_approve.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(self.supervisor)
        draft_approve = self.client.post(f"/api/leaves/{leave.id}/approve/")
        self.assertEqual(draft_approve.status_code, status.HTTP_400_BAD_REQUEST)

        self.client.force_authenticate(self.resident)
        submit = self.client.post(f"/api/leaves/{leave.id}/submit/")
        self.assertEqual(submit.status_code, status.HTTP_200_OK)

        second_submit = self.client.post(f"/api/leaves/{leave.id}/submit/")
        self.assertEqual(second_submit.status_code, status.HTTP_400_BAD_REQUEST)

        unrelated_supervisor = make_user("fl_leave_unrelated_supervisor", "supervisor")
        self.client.force_authenticate(unrelated_supervisor)
        wrong_supervisor = self.client.post(f"/api/leaves/{leave.id}/approve/")
        self.assertEqual(wrong_supervisor.status_code, status.HTTP_404_NOT_FOUND)

        self.client.force_authenticate(self.supervisor)
        approve = self.client.post(f"/api/leaves/{leave.id}/approve/")
        self.assertEqual(approve.status_code, status.HTTP_200_OK)
        self.assertEqual(approve.data["status"], LeaveRequest.STATUS_APPROVED)

        reject_after_approval = self.client.post(
            f"/api/leaves/{leave.id}/reject/",
            {"reason": "Too late"},
            format="json",
        )
        self.assertEqual(reject_after_approval.status_code, status.HTTP_400_BAD_REQUEST)

    def test_role_aware_dashboard_endpoints_and_permissions(self):
        self.client.force_authenticate(self.resident)
        resident_dashboard = self.client.get("/api/dashboard/resident/")
        self.assertEqual(resident_dashboard.status_code, status.HTTP_200_OK)
        self.assertIn("readiness", resident_dashboard.data)
        resident_review_denied = self.client.get("/api/logbook/review-queue/")
        self.assertEqual(resident_review_denied.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(self.supervisor)
        supervisor_dashboard = self.client.get("/api/dashboard/supervisor/")
        self.assertEqual(supervisor_dashboard.status_code, status.HTTP_200_OK)
        self.assertIn("pending_logbook_reviews", supervisor_dashboard.data)
        hod_dashboard = self.client.get("/api/dashboard/hod/")
        self.assertEqual(hod_dashboard.status_code, status.HTTP_200_OK)
        self.assertIn("supervisor_lag", hod_dashboard.data)

        self.client.force_authenticate(self.utrmc_user)
        utrmc_dashboard = self.client.get("/api/dashboard/utrmc/")
        self.assertEqual(utrmc_dashboard.status_code, status.HTTP_200_OK)
        self.assertIn("cross_department_overview", utrmc_dashboard.data)

        verify_denied = self.client.post("/api/rotations/completions/999999/verify/")
        self.assertEqual(verify_denied.status_code, status.HTTP_403_FORBIDDEN)


class ActiveSurfaceBaselineTests(APITestCase):
    def test_seeded_baseline_resident_dashboard_and_leave_create_work(self):
        call_command("seed_org_data", verbosity=0)
        call_command("seed_active_surface_baseline", verbosity=0)
        resident = User.objects.get(username="pilot_pg")
        self.client.force_authenticate(resident)

        dashboard = self.client.get("/api/dashboard/resident/")
        self.assertEqual(dashboard.status_code, status.HTTP_200_OK)
        self.assertIn("training_record_id", dashboard.data)
        training_record_id = dashboard.data["training_record_id"]
        self.assertIsNotNone(training_record_id)
        self.assertEqual(dashboard.data["logbook"]["total"], 0)

        leave = self.client.post(
            "/api/leaves/",
            {
                "resident_training": training_record_id,
                "leave_type": "annual",
                "start_date": str(date.today() + timedelta(days=10)),
                "end_date": str(date.today() + timedelta(days=12)),
                "reason": "Baseline verification",
            },
            format="json",
        )
        self.assertEqual(leave.status_code, status.HTTP_201_CREATED)
        self.assertEqual(leave.data["status"], "DRAFT")
        self.assertEqual(
            leave.data["resident_training"],
            ResidentTrainingRecord.objects.get(resident_user=resident, active=True).id,
        )

    def test_resident_cannot_create_leave_for_another_training_record(self):
        other = make_user("other_resident", "pg")
        other_rtr = ResidentTrainingRecord.objects.create(
            resident_user=other,
            program=self.program if hasattr(self, "program") else TrainingProgram.objects.create(
                name="Other Program",
                code="OTHER-ACTIVE",
                duration_months=48,
            ),
            start_date=date.today(),
            active=True,
        )
        resident = make_user("own_resident", "pg")
        own_program = TrainingProgram.objects.create(
            name="Own Program",
            code="OWN-ACTIVE",
            duration_months=48,
        )
        ResidentTrainingRecord.objects.create(
            resident_user=resident,
            program=own_program,
            start_date=date.today(),
            active=True,
        )
        self.client.force_authenticate(resident)
        response = self.client.post(
            "/api/leaves/",
            {
                "resident_training": other_rtr.id,
                "leave_type": "annual",
                "start_date": str(date.today() + timedelta(days=10)),
                "end_date": str(date.today() + timedelta(days=12)),
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
