from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from sims.training.models import (
    TrainingProgram, ResidentTrainingRecord, ProgramRotationTemplate,
    LogbookEntry, RotationAssignment, LeaveRequest
)
from sims.academics.models import Department
from datetime import date, timedelta
import json

User = get_user_model()

class TrainingViewsHeavyTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(username="admin_heavy", password="password123", role="admin")
        self.admin.role = "admin"
        self.admin.save()
        self.pg = User.objects.create_user(username="pg_heavy", password="password123", role="pg")
        self.client.login(username="admin_heavy", password="password123")
        self.dept = Department.objects.create(name="H Heavy", code="HHEAVY")

    def test_training_program_crud(self):
        # List
        response = self.client.get("/api/programs/")
        self.assertEqual(response.status_code, 200)
        
        # Create
        data = {"name": "H Program", "code": "HP", "duration_months": 24}
        response = self.client.post("/api/programs/", data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        program_id = response.data["id"]
        
        # Detail
        response = self.client.get(f"/api/programs/{program_id}/")
        self.assertEqual(response.status_code, 200)
        
        # Update
        response = self.client.patch(f"/api/programs/{program_id}/", data=json.dumps({"name": "Updated H"}), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_resident_training_record_crud(self):
        program = TrainingProgram.objects.create(name="P1", code="P1", duration_months=12)
        # Create
        data = {
            "resident_user": self.pg.id,
            "program": program.id,
            "start_date": str(date.today()),
            "expected_end_date": str(date.today() + timedelta(days=365)),
            "active": True
        }
        response = self.client.post("/api/resident-training/", data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        
        # List
        response = self.client.get("/api/resident-training/")
        self.assertEqual(response.status_code, 200)

    def test_program_rotation_template_crud(self):
        program = TrainingProgram.objects.create(name="P2", code="P2", duration_months=12)
        # Create - requires department in template
        data = {
            "program": program.id,
            "name": "Template 1",
            "duration_weeks": 4,
            "sequence_order": 1,
            "required": True,
            "department": self.dept.id
        }
        response = self.client.post("/api/program-templates/", data=json.dumps(data), content_type="application/json")
        if response.status_code != 201:
            print(f"DEBUG Template 400: {response.data}")
        self.assertEqual(response.status_code, 201)
        
    def test_milestones_crud(self):
        program = TrainingProgram.objects.create(name="P3", code="P3", duration_months=12)
        # List milestones for program
        url = f"/api/programs/{program.id}/milestones/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # Create milestone - explicitly include program if nested route doesn't handle it
        data = {"name": "M1", "code": "IMM", "recommended_month": 12, "program": program.id}
        response = self.client.post(url, data=json.dumps(data), content_type="application/json")
        if response.status_code != 201:
            print(f"DEBUG Milestone 400: {response.data}")
        self.assertEqual(response.status_code, 201)
