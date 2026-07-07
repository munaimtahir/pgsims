from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from sims.training.models import (
    LogbookEntry, TrainingProgram, ResidentTrainingRecord,
    RotationAssignment, LeaveRequest
)
from sims.rotations.models import Hospital, HospitalDepartment
from sims.academics.models import Department
from django.utils import timezone
from datetime import date, timedelta
import json

User = get_user_model()

class TrainingViewsExtendedTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(username="admin_view", password="password123", email="admin_view@test.com")
        self.admin.role = "ADMIN"
        self.admin.save()
        
        self.supervisor = User.objects.create_user(username="sup_view", password="password123", role="SUPERVISOR")
        self.pg = User.objects.create_user(username="pg_view", password="password123", role="RESIDENT")
        
        self.program = TrainingProgram.objects.create(name="Medicine", code="MED-V", duration_months=48)
        self.rtr = ResidentTrainingRecord.objects.create(
            resident_user=self.pg, program=self.program, 
            start_date=date.today() - timedelta(days=100), 
            expected_end_date=date.today() + timedelta(days=365)
        )
        self.hospital = Hospital.objects.create(name="Hospital", code="H1", is_active=True)
        self.dept = Department.objects.create(name="Surgery", code="SURG")
        self.hdept = HospitalDepartment.objects.create(hospital=self.hospital, department=self.dept)

    def test_logbook_entry_actions(self):
        self.client.login(username="pg_view", password="password123")
        entry = LogbookEntry.objects.create(
            resident_training_record=self.rtr,
            patient_id_number="P-ACTION",
            patient_seen_at=timezone.now(),
            status="DRAFT"
        )
        
        # Test verify (should fail for PG)
        response = self.client.post(f"/api/logbook/{entry.id}/review/", {"action": "approved"})
        self.assertEqual(response.status_code, 403)
        
        # Test submit
        response = self.client.post(f"/api/logbook/{entry.id}/submit/")
        self.assertEqual(response.status_code, 200)
        
        # Test verify (admin)
        self.client.login(username="admin_view", password="password123")
        response = self.client.post(f"/api/logbook/{entry.id}/review/", 
                                   data=json.dumps({"action": "approved", "feedback": "OK"}),
                                   content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_rotation_assignment_actions(self):
        self.client.login(username="admin_view", password="password123")
        assignment = RotationAssignment.objects.create(
            resident_training=self.rtr,
            hospital_department=self.hdept,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30),
            status="DRAFT"
        )
        
        # Submit
        response = self.client.post(f"/api/rotations/{assignment.id}/submit/")
        self.assertEqual(response.status_code, 200)
        
        # Approve (HOD Approve)
        response = self.client.post(f"/api/rotations/{assignment.id}/hod-approve/")
        self.assertEqual(response.status_code, 200)

    def test_leave_request_actions(self):
        self.client.login(username="pg_view", password="password123")
        leave = LeaveRequest.objects.create(
            resident_training=self.rtr,
            leave_type="casual",
            start_date=date.today() + timedelta(days=10),
            end_date=date.today() + timedelta(days=12),
            status="DRAFT"
        )
        
        # Submit
        response = self.client.post(f"/api/leaves/{leave.id}/submit/")
        self.assertEqual(response.status_code, 200)
        
        # Approve (Admin)
        self.client.login(username="admin_view", password="password123")
        response = self.client.post(f"/api/leaves/{leave.id}/approve/")
        self.assertEqual(response.status_code, 200)
