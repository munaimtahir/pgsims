from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from sims.training.models import (
    TrainingProgram, ResidentTrainingRecord,
    RotationAssignment, LeaveRequest, ResidentSubmission,
    ResidentWorkshopCompletion, Workshop, ProgramMilestone,
    ProgramMilestoneResearchRequirement,
    RotationCompletion
)
from sims.rotations.models import Hospital, HospitalDepartment
from sims.academics.models import Department
from sims.users.models import ResidentProfile, SupervisorProfile
from django.utils import timezone
from datetime import date, timedelta
from django.core.files.uploadedfile import SimpleUploadedFile
import json

User = get_user_model()

class BackendMegaCoverageTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(username="admin_mega_v2", password="password123", role="ADMIN")
        self.admin.role = "ADMIN"
        self.admin.save()
        
        self.supervisor = User.objects.create_user(username="sup_mega_v2", password="password123", role="SUPERVISOR")
        self.pg = User.objects.create_user(username="pg_mega_v2", password="password123", role="RESIDENT")
        
        self.program = TrainingProgram.objects.create(name="Mega Program V2", code="MEGAV2", duration_months=48)
        self.rtr = ResidentTrainingRecord.objects.create(
            resident_user=self.pg, program=self.program, 
            start_date=date.today() - timedelta(days=100), 
            expected_end_date=date.today() + timedelta(days=365)
        )
        self.hospital = Hospital.objects.create(name="Mega Hospital V2", code="MHV2", is_active=True)
        self.dept = Department.objects.create(name="Mega Dept V2", code="MDEV2")
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
        self.client.login(username="admin_mega_v2", password="password123")

    def test_milestone_viewset_extended(self):
        url = f"/api/programs/{self.program.id}/milestones/"
        data = {"name": "Phase 1", "code": "IMM", "recommended_month": 24, "program": self.program.id}
        response = self.client.post(url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 201)

    def test_resident_submission_workflow(self):
        self.client.login(username="pg_mega_v2", password="password123")
        url = reverse("synopsis-submission")
        self.client.post(url, data=json.dumps({"feedback": "Init"}), content_type="application/json")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_rotation_completion_verification_flow(self):
        assignment = RotationAssignment.objects.create(
            resident_training=self.rtr, hospital_department=self.hdept,
            start_date=date.today() - timedelta(days=40),
            end_date=date.today() - timedelta(days=10),
            status="ACTIVE"
        )
        self.client.login(username="admin_mega_v2", password="password123")
        self.client.post(f"/api/rotations/{assignment.id}/complete/")
        
        comp = RotationCompletion.objects.get(rotation=assignment)
        verify_url = reverse("rotation-completion-verify", kwargs={"completion_id": comp.id})
        response = self.client.post(verify_url)
        self.assertEqual(response.status_code, 200)
