from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from sims.users.models import User, ResidentProfile, SupervisorProfile, AdminProfile
from sims.supervision.models import ResidentSupervisorAssignment
from sims.training.models import TrainingProgram, ResidentTrainingRecord, ResidentSubmission, SubmissionRequirementTemplate
from sims.academics.models import Department, Specialty
import uuid

class AuditWorkflowTests(APITestCase):
    def setUp(self):
        self.dept = Department.objects.create(code="TEST", name="Test Dept", active=True)
        self.specialty = Specialty.objects.create(code="MED", name="Medicine")
        self.prog = TrainingProgram.objects.create(code="TEST_PROG", name="Test Program", duration_months=12)

        self.res_a = User.objects.create_user(username="res_a", password="password", role="RESIDENT", specialty=self.specialty)
        self.res_prof_a = ResidentProfile.objects.create(user=self.res_a)

        self.training_record = ResidentTrainingRecord.objects.create(
            resident_user=self.res_a, program=self.prog, current_level="y1",
            status="ACTIVE", start_date="2023-01-01", expected_end_date="2024-01-01"
        )

        self.sup_a = User.objects.create_user(username="sup_a", password="password", role="SUPERVISOR", specialty=self.specialty)
        self.sup_prof_a = SupervisorProfile.objects.create(user=self.sup_a)

        self.assignment = ResidentSupervisorAssignment.objects.create(
            resident=self.res_prof_a, supervisor=self.sup_prof_a, assignment_type="PRIMARY",
            start_date="2023-01-01", is_active=True
        )

        self.submission = ResidentSubmission.objects.create(
            resident_training_record=self.training_record,
            submission_type=ResidentSubmission.TYPE_SYNOPSIS,
            status=ResidentSubmission.STATUS_DRAFT,
            feedback="Test Synopsis"
        )

    def test_synopsis_submit_invalid_state(self):
        self.submission.status = ResidentSubmission.STATUS_UNDER_REVIEW
        self.submission.save()

        self.client.force_authenticate(user=self.res_a)
        url = reverse("synopsis-submission-submit")
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Cannot submit from status", resp.data["detail"])

    def test_synopsis_review_invalid_state(self):
        self.submission.status = ResidentSubmission.STATUS_DRAFT
        self.submission.save()

        self.client.force_authenticate(user=self.sup_a)
        url = reverse("synopsis-review-action", args=[self.submission.id])
        resp = self.client.post(url, {"action": "start-review"})
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Cannot start review from status", resp.data["detail"])

    def test_cross_supervisor_unauthorized_review(self):
        self.res_b = User.objects.create_user(username="res_b", password="password", role="RESIDENT", specialty=self.specialty)
        self.res_prof_b = ResidentProfile.objects.create(user=self.res_b)

        self.training_record_b = ResidentTrainingRecord.objects.create(
            resident_user=self.res_b, program=self.prog, current_level="y1",
            status="ACTIVE", start_date="2023-01-01", expected_end_date="2024-01-01"
        )

        self.sup_b = User.objects.create_user(username="sup_b", password="password", role="SUPERVISOR", specialty=self.specialty)
        self.sup_prof_b = SupervisorProfile.objects.create(user=self.sup_b)

        ResidentSupervisorAssignment.objects.create(
            resident=self.res_prof_b, supervisor=self.sup_prof_b, assignment_type="PRIMARY",
            start_date="2023-01-01", is_active=True
        )

        submission_b = ResidentSubmission.objects.create(
            resident_training_record=self.training_record_b,
            submission_type=ResidentSubmission.TYPE_SYNOPSIS,
            status=ResidentSubmission.STATUS_SUBMITTED,
            feedback="Test Synopsis B"
        )

        # Attempt to review Resident B's submission as Supervisor A
        self.client.force_authenticate(user=self.sup_a)
        url = reverse("synopsis-review-action", args=[submission_b.id])
        resp = self.client.post(url, {"action": "start-review"})

        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        submission_b.refresh_from_db()
        self.assertEqual(submission_b.status, ResidentSubmission.STATUS_SUBMITTED)
