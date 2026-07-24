from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from sims.training.models import (
    TrainingProgram, ResidentTrainingRecord,
    RotationAssignment, LeaveRequest, ResidentSubmission,
    ResidentWorkshopCompletion, Workshop
)
from sims.rotations.models import Hospital, HospitalDepartment
from sims.academics.models import Department
from sims.supervision.models import ResidentSupervisorAssignment
from sims.users.models import ResidentProfile, SupervisorProfile
from django.utils import timezone
from datetime import date, timedelta
import json

User = get_user_model()

class BackendCoveragePushTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(username="admin_push", password="password123", role="ADMIN")
        self.admin.role = "ADMIN"
        self.admin.save()
        
        self.supervisor = User.objects.create_user(username="sup_push", password="password123", role="SUPERVISOR")
        self.pg = User.objects.create_user(username="pg_push", password="password123", role="RESIDENT")
        
        self.program = TrainingProgram.objects.create(name="Push Program", code="PUSH", duration_months=48)
        self.rtr = ResidentTrainingRecord.objects.create(
            resident_user=self.pg, program=self.program, 
            start_date=date.today() - timedelta(days=100), 
            expected_end_date=date.today() + timedelta(days=365)
        )
        self.hospital = Hospital.objects.create(name="Push Hospital", code="PH", is_active=True)
        self.dept = Department.objects.create(name="Push Dept", code="PDEP")
        self.hdept = HospitalDepartment.objects.create(hospital=self.hospital, department=self.dept)
        self.resident_profile = ResidentProfile.objects.create(
            user=self.pg,
            hospital=self.hospital,
            department_ref=self.dept,
        )
        self.supervisor_profile = SupervisorProfile.objects.create(
            user=self.supervisor,
            hospital=self.hospital,
            department_ref=self.dept,
        )

    def test_rotation_assignment_full_cycle(self):
        self.client.login(username="admin_push", password="password123")
        assignment = RotationAssignment.objects.create(
            resident_training=self.rtr,
            hospital_department=self.hdept,
            start_date=date.today() + timedelta(days=1),
            end_date=date.today() + timedelta(days=31),
            status="DRAFT"
        )
        
        # Submit
        self.client.post(f"/api/rotations/{assignment.id}/submit/")
        
        # Review (Redirect action)
        hdept2 = HospitalDepartment.objects.create(
            hospital=self.hospital, 
            department=Department.objects.create(name="D2", code="D2")
        )
        response = self.client.post(f"/api/rotations/{assignment.id}/review-application/", 
                                   data=json.dumps({
                                       "action": "redirect", 
                                       "hospital_department": hdept2.id,
                                       "reason": "Changed"
                                   }),
                                   content_type="application/json")
        self.assertEqual(response.status_code, 200)
        assignment.refresh_from_db()
        self.assertEqual(assignment.hospital_department, hdept2)

    def test_leave_request_denials_and_actions(self):
        self.client.login(username="pg_push", password="password123")
        leave = LeaveRequest.objects.create(
            resident_training=self.rtr,
            leave_type="annual",
            start_date=date.today() + timedelta(days=5),
            end_date=date.today() + timedelta(days=10),
            status="DRAFT"
        )
        
        # Submit
        self.client.post(f"/api/leaves/{leave.id}/submit/")
        
        # Approve (as supervisor)
        self.client.login(username="sup_push", password="password123")
        ResidentSupervisorAssignment.objects.create(
            resident=self.resident_profile,
            supervisor=self.supervisor_profile,
            assignment_type=ResidentSupervisorAssignment.ASSIGNMENT_PRIMARY,
            start_date=date.today(),
            is_active=True,
            status=ResidentSupervisorAssignment.STATUS_ACTIVE,
        )
        
        response = self.client.post(f"/api/leaves/{leave.id}/approve/")
        self.assertEqual(response.status_code, 200)

    def test_resident_summary_structure(self):
        self.client.login(username="pg_push", password="password123")
        response = self.client.get("/api/residents/me/summary/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("training_record", response.data)
