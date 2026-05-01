from django.test import TestCase
from django.contrib.auth import get_user_model
from sims.training.models import (
    TrainingProgram, ResidentTrainingRecord, RotationAssignment,
    LeaveRequest, LogbookEntry, LogbookReview
)
from sims.rotations.models import Hospital, HospitalDepartment
from sims.academics.models import Department
from datetime import date, timedelta
from django.utils import timezone

User = get_user_model()

class TrainingModelsTests(TestCase):
    def setUp(self):
        self.pg = User.objects.create_user(username="pg", role="pg")
        self.supervisor = User.objects.create_user(username="sup", role="supervisor")
        self.program = TrainingProgram.objects.create(name="Medicine", code="MED", duration_months=48)
        self.rtr = ResidentTrainingRecord.objects.create(
            resident_user=self.pg, program=self.program, 
            start_date=date.today(), expected_end_date=date.today() + timedelta(days=365)
        )
        self.hospital = Hospital.objects.create(name="Allied", code="AH", is_active=True)
        self.dept = Department.objects.create(name="Med", code="MED")
        self.hdept = HospitalDepartment.objects.create(hospital=self.hospital, department=self.dept)

    def test_rtr_active_logic(self):
        self.assertTrue(self.rtr.active)
        self.rtr.active = False
        self.rtr.save()
        self.assertFalse(self.rtr.active)

    def test_rotation_assignment_status(self):
        assignment = RotationAssignment.objects.create(
            resident_training=self.rtr, hospital_department=self.hdept,
            start_date=date.today(), end_date=date.today() + timedelta(days=30)
        )
        self.assertEqual(assignment.status, "DRAFT")

    def test_logbook_entry_review(self):
        entry = LogbookEntry.objects.create(
            resident_training_record=self.rtr,
            patient_id_number="P1",
            patient_seen_at=timezone.now(),
            status="SUBMITTED"
        )
        review = LogbookReview.objects.create(
            entry=entry, reviewer=self.supervisor, action="APPROVED"
        )
        self.assertEqual(review.action, "APPROVED")

    def test_leave_request(self):
        leave = LeaveRequest.objects.create(
            resident_training=self.rtr,
            leave_type="casual",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=2),
            reason="Sick"
        )
        self.assertEqual(leave.status, "DRAFT")
