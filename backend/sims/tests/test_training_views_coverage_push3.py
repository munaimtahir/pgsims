"""Coverage for the small dashboard and read-only training endpoints."""

from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from sims.academics.models import Department
from sims.rotations.models import Hospital, HospitalDepartment
from sims.training.models import (
    ResidentSubmission,
    ResidentTrainingRecord,
    SubmissionRequirementTemplate,
    TrainingProgram,
)
from sims.users.models import ResidentProfile, SupervisorProfile
from sims.supervision.models import ResidentSupervisorAssignment

User = get_user_model()


class TrainingDashboardEndpointCoverageTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.department = Department.objects.create(name="Coverage Medicine", code="CV-MED")
        self.hospital = Hospital.objects.create(name="Coverage Hospital", code="CV-H")
        HospitalDepartment.objects.create(hospital=self.hospital, department=self.department)
        self.program = TrainingProgram.objects.create(
            name="Coverage Programme", code="CV-PROG", duration_months=36
        )
        self.admin = User.objects.create_user(
            username="cv3_admin", password="pw", role="ADMIN", email="a@cv.test",
            first_name="Coverage", last_name="Admin",
        )
        self.supervisor = User.objects.create_user(
            username="cv3_supervisor", password="pw", role="SUPERVISOR", email="s@cv.test",
            first_name="Coverage", last_name="Supervisor",
        )
        self.resident = User.objects.create_user(
            username="cv3_resident", password="pw", role="RESIDENT", email="r@cv.test",
            first_name="Coverage", last_name="Resident", supervisor=self.supervisor,
        )
        ResidentProfile.objects.create(
            user=self.resident, hospital=self.hospital, department_ref=self.department,
            program_ref=self.program,
        )
        SupervisorProfile.objects.create(
            user=self.supervisor, hospital=self.hospital, department_ref=self.department,
        )
        ResidentSupervisorAssignment.objects.create(
            resident=ResidentProfile.objects.get(user=self.resident),
            supervisor=SupervisorProfile.objects.get(user=self.supervisor),
            assignment_type=ResidentSupervisorAssignment.ASSIGNMENT_PRIMARY,
            is_active=True,
            status=ResidentSupervisorAssignment.STATUS_ACTIVE,
            start_date=date.today(),
        )
        self.rtr = ResidentTrainingRecord.objects.create(
            resident_user=self.resident, program=self.program,
            start_date=date.today(), expected_end_date=date.today() + timedelta(days=365),
            active=True,
        )

    def auth(self, user):
        self.client.force_authenticate(user=user)

    def test_resident_dashboard_reads(self):
        self.auth(self.resident)
        for path in (
            "/api/my/rotations/",
            "/api/my/leaves/",
            "/api/my/workshops/",
            "/api/my/eligibility/",
            "/api/residents/me/summary/",
        ):
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200, path)
        self.assertEqual(self.client.get("/api/my/research/").status_code, 404)
        self.assertEqual(self.client.get("/api/my/thesis/").status_code, 404)

    def test_non_resident_is_denied_from_resident_only_reads(self):
        self.auth(self.supervisor)
        self.assertEqual(self.client.get("/api/my/rotations/").status_code, 403)
        self.assertEqual(self.client.get("/api/my/leaves/").status_code, 403)

    def test_admin_and_supervisor_inboxes_and_settings(self):
        self.auth(self.admin)
        for path in (
            "/api/utrmc/approvals/rotations/",
            "/api/utrmc/approvals/leaves/",
            "/api/utrmc/eligibility/",
            "/api/supervisor/rotations/pending/",
            "/api/supervisor/research-approvals/",
            "/api/system/settings/",
        ):
            self.assertEqual(self.client.get(path).status_code, 200, path)

        self.auth(self.supervisor)
        self.assertEqual(self.client.get("/api/supervisor/rotations/pending/").status_code, 200)
        self.assertEqual(self.client.get("/api/supervisor/research-approvals/").status_code, 200)
        self.assertEqual(self.client.get("/api/supervisors/me/summary/").status_code, 200)

    def test_inbox_permission_denials(self):
        self.auth(self.resident)
        for path in (
            "/api/utrmc/approvals/rotations/",
            "/api/utrmc/approvals/leaves/",
            "/api/utrmc/eligibility/",
            "/api/supervisor/rotations/pending/",
            "/api/supervisor/research-approvals/",
        ):
            self.assertEqual(self.client.get(path).status_code, 403, path)

    def test_policy_and_milestone_requirement_read_write(self):
        self.auth(self.admin)
        policy = self.client.get(f"/api/programs/{self.program.id}/policy/")
        self.assertEqual(policy.status_code, 200)
        self.assertEqual(
            self.client.put(
                f"/api/programs/{self.program.id}/policy/",
                {"max_leave_days": 30}, format="json",
            ).status_code,
            200,
        )

        from sims.training.models import ProgramMilestone
        milestone = ProgramMilestone.objects.create(
            program=self.program, name="Coverage IMM", code="CV-IMM", recommended_month=12,
        )
        path = f"/api/milestones/{milestone.id}/requirements/research/"
        self.assertEqual(self.client.get(path).status_code, 200)
        self.assertEqual(
            self.client.put(path, {"requires_synopsis_approved": True}, format="json").status_code,
            200,
        )

    def test_workshop_listing_and_supervisor_resident_progress(self):
        self.auth(self.resident)
        self.assertEqual(self.client.get("/api/workshops/").status_code, 200)
        self.auth(self.supervisor)
        response = self.client.get(f"/api/supervisors/residents/{self.resident.id}/progress/")
        self.assertIn(response.status_code, (200, 404))

    def test_submission_lifecycle_and_review_branches(self):
        self.auth(self.resident)
        base = "/api/submissions/synopsis/"
        self.assertEqual(self.client.get(base).status_code, 404)
        created = self.client.post(base, {"title": "draft"}, format="json")
        self.assertEqual(created.status_code, 201)
        self.assertEqual(self.client.post(base, {}, format="json").status_code, 400)
        self.assertEqual(self.client.patch(base, {"feedback": "draft"}, format="json").status_code, 200)
        self.assertEqual(self.client.post(base + "submit/", {}, format="json").status_code, 200)
        self.assertEqual(self.client.post(base + "submit/", {}, format="json").status_code, 400)

        self.auth(self.admin)
        self.assertEqual(self.client.get(base + "review-queue/").status_code, 200)
        submission = ResidentSubmission.objects.get(resident_training_record=self.rtr)
        for action in ("start-review", "return", "start-review", "verify"):
            submission.refresh_from_db()
            if action == "start-review" and submission.status == ResidentSubmission.STATUS_RETURNED:
                submission.status = ResidentSubmission.STATUS_SUBMITTED
                submission.save(update_fields=["status"])
            response = self.client.post(
                f"{base}{submission.id}/review/", {"action": action, "comments": "ok"}, format="json"
            )
            self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(self.client.get("/api/submissions/certificates/").status_code, 200)

    def test_submission_required_document_and_denial_paths(self):
        requirement = SubmissionRequirementTemplate.objects.create(
            submission_type=SubmissionRequirementTemplate.TYPE_SYNOPSIS,
            code="SYN-1", title="Synopsis PDF", program=self.program,
        )
        self.auth(self.resident)
        self.assertEqual(self.client.post("/api/submissions/synopsis/submit/", {}, format="json").status_code, 400)
        submission = ResidentSubmission.objects.create(
            resident_training_record=self.rtr,
            submission_type=ResidentSubmission.TYPE_SYNOPSIS,
        )
        self.assertEqual(self.client.post("/api/submissions/synopsis/", {}, format="json").status_code, 400)
        self.assertEqual(self.client.post("/api/submissions/synopsis/documents/", {}, format="multipart").status_code, 400)
        self.auth(self.resident)
        self.assertEqual(self.client.get("/api/submissions/synopsis/review-queue/").status_code, 403)
        self.assertEqual(self.client.post(f"/api/submissions/synopsis/{submission.id}/review/", {"action": "verify"}, format="json").status_code, 403)
