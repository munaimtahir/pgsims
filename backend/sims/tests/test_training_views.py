from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from sims.training.models import (
    TrainingProgram, ResidentTrainingRecord, ProgramMilestone,
    ResidentResearchProject, LogbookEntry
)
from sims.rotations.models import Hospital, HospitalDepartment
from sims.academics.models import Department
from datetime import date, timedelta
from django.utils import timezone
import json

User = get_user_model()

class TrainingViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(username="ADMIN", password="password123", role="ADMIN")
        self.supervisor = User.objects.create_user(username="SUPERVISOR", password="password123", role="SUPERVISOR")
        self.pg = User.objects.create_user(username="RESIDENT", password="password123", role="RESIDENT")
        
        self.program = TrainingProgram.objects.create(name="Medicine", code="MED-FCPS", duration_months=48)
        self.rtr = ResidentTrainingRecord.objects.create(
            resident_user=self.pg, program=self.program, 
            start_date=date.today(), expected_end_date=date.today() + timedelta(days=365)
        )
        
        self.hospital = Hospital.objects.create(name="Allied Hospital", code="AH", is_active=True)
        self.dept = Department.objects.create(name="Medicine", code="MED")
        self.hdept = HospitalDepartment.objects.create(hospital=self.hospital, department=self.dept)

    def test_logbook_entry_workflow(self):
        # Create draft
        self.client.login(username="RESIDENT", password="password123")
        entry = LogbookEntry.objects.create(
            resident_training_record=self.rtr,
            patient_id_number="P100",
            patient_seen_at=timezone.now(),
            status="DRAFT"
        )
        
        # Submit
        response = self.client.post(f"/api/logbook/{entry.id}/submit/")
        self.assertEqual(response.status_code, 200)
        entry.refresh_from_db()
        self.assertEqual(entry.status, "SUBMITTED")
        
        # Review (Supervisor)
        self.client.login(username="SUPERVISOR", password="password123")
        # Ensure supervisor is linked or has HOD access to allow review
        from sims.users.models import SupervisorResidentLink
        SupervisorResidentLink.objects.create(
            supervisor_user=self.supervisor, resident_user=self.pg, start_date=date.today()
        )
        
        response = self.client.post(f"/api/logbook/{entry.id}/review/", 
                                   data=json.dumps({"action": "approved", "feedback": "Good job"}),
                                   content_type="application/json")
        self.assertEqual(response.status_code, 200)
        entry.refresh_from_db()
        self.assertEqual(entry.status, "APPROVED")

    def test_resident_summary_api(self):
        self.client.login(username="RESIDENT", password="password123")
        response = self.client.get(reverse("resident-summary"))
        self.assertEqual(response.status_code, 200)

    def test_resident_operational_dashboard_api(self):
        self.client.login(username="RESIDENT", password="password123")
        response = self.client.get(reverse("dashboard-resident"))
        self.assertEqual(response.status_code, 200)

    def test_supervisor_operational_dashboard_api(self):
        self.client.login(username="SUPERVISOR", password="password123")
        response = self.client.get(reverse("dashboard-supervisor"))
        self.assertEqual(response.status_code, 200)



    def test_utrmc_operational_dashboard_api(self):
        utrmc_admin = User.objects.create_user(username="utrmc", password="password123", role="ADMIN")
        self.client.login(username="utrmc", password="password123")
        response = self.client.get(reverse("dashboard-utrmc"))
        self.assertEqual(response.status_code, 200)

    def test_program_policy_api(self):
        self.client.login(username="ADMIN", password="password123")
        response = self.client.get(reverse("program-policy", kwargs={"program_id": self.program.id}))
        self.assertEqual(response.status_code, 200)

    def test_milestone_research_requirement_api(self):
        milestone = ProgramMilestone.objects.create(
            program=self.program, name="Year 1", code="IMM", recommended_month=12
        )
        self.client.login(username="ADMIN", password="password123")
        response = self.client.get(reverse("milestone-research-req", kwargs={"milestone_id": milestone.id}))
        self.assertEqual(response.status_code, 200)

    def test_resident_research_project_api(self):
        self.client.login(username="RESIDENT", password="password123")
        response = self.client.get(reverse("my-research"))
        self.assertEqual(response.status_code, 404)
        
        data = {"title": "My Research", "synopsis_status": "DRAFT"}
        response = self.client.post(reverse("my-research"), data=data)
        self.assertEqual(response.status_code, 201)

    def test_logbook_my_threshold_api(self):
        self.client.login(username="RESIDENT", password="password123")
        response = self.client.get(reverse("logbook-my-threshold"))
        self.assertEqual(response.status_code, 200)

    def test_my_workshop_completions_api(self):
        self.client.login(username="RESIDENT", password="password123")
        response = self.client.get(reverse("my-workshops"))
        self.assertEqual(response.status_code, 200)

    def test_my_eligibility_api(self):
        self.client.login(username="RESIDENT", password="password123")
        response = self.client.get(reverse("my-eligibility"))
        self.assertEqual(response.status_code, 200)

    def test_leave_approval_inbox_api(self):
        utrmc_admin = User.objects.create_user(username="utrmc_admin_p", password="password123", role="ADMIN")
        self.client.login(username="utrmc_admin_p", password="password123")
        response = self.client.get(reverse("leave-approvals-inbox"))
        self.assertEqual(response.status_code, 200)

    def test_rotation_approval_inbox_api(self):
        utrmc_admin = User.objects.create_user(username="utrmc_admin_q", password="password123", role="ADMIN")
        self.client.login(username="utrmc_admin_q", password="password123")
        response = self.client.get(reverse("rotation-approvals-inbox"))
        self.assertEqual(response.status_code, 200)
