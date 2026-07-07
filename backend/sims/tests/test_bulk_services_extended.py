from django.test import TestCase
from django.contrib.auth import get_user_model
from sims.bulk.services import BulkService
from sims.training.models import (
    LogbookEntry, TrainingProgram, ResidentTrainingRecord, RotationAssignment
)
from sims.rotations.models import Hospital, HospitalDepartment
from sims.academics.models import Department
from django.utils import timezone
from datetime import date, timedelta
import io

User = get_user_model()

class BulkServicesExtendedTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username="admin_ext", password="password123", role="ADMIN")
        self.supervisor = User.objects.create_user(username="sup_ext", password="password123", role="SUPERVISOR", email="sup_ext@test.com")
        self.pg = User.objects.create_user(username="pg_ext", password="password123", role="RESIDENT", email="pg_ext@test.com")
        self.service = BulkService(self.admin)
        
        self.hospital = Hospital.objects.create(name="Allied Hospital", code="AH", is_active=True)
        self.dept = Department.objects.create(name="Medicine", code="MED", active=True)
        self.hdept = HospitalDepartment.objects.create(hospital=self.hospital, department=self.dept, is_active=True)
        self.program = TrainingProgram.objects.create(name="Medicine", code="MED-FCPS", duration_months=48)
        self.rtr = ResidentTrainingRecord.objects.create(
            resident_user=self.pg, program=self.program, 
            start_date=date.today(), expected_end_date=date.today() + timedelta(days=365)
        )

    def test_import_userbase_hospitals(self):
        csv_content = "hospital_code,hospital_name,active\nH-USER,User Hospital,true\n"
        file = io.BytesIO(csv_content.encode('utf-8'))
        file.name = "hospitals.csv"
        op = self.service.import_userbase_hospitals(file, dry_run=False)
        self.assertEqual(op.success_count, 1)

    def test_import_userbase_departments(self):
        csv_content = "department_code,department_name,active\nD-USER,User Dept,true\n"
        file = io.BytesIO(csv_content.encode('utf-8'))
        file.name = "depts.csv"
        op = self.service.import_userbase_departments(file, dry_run=False)
        self.assertEqual(op.success_count, 1)

    def test_import_userbase_matrix(self):
        csv_content = "hospital_code,department_code,active\nAH,MED,false\n"
        file = io.BytesIO(csv_content.encode('utf-8'))
        file.name = "matrix.csv"
        op = self.service.import_userbase_matrix(file, dry_run=False)
        self.assertEqual(op.success_count, 1)

    def test_import_userbase_faculty_supervisors(self):
        # expects full_name, email, specialty, role, department_code, hospital_code
        csv_content = "full_name,email,specialty,role,department_code,hospital_code\nAlice Faculty,alice.fac@test.com,urology,faculty,MED,AH\n"
        file = io.BytesIO(csv_content.encode('utf-8'))
        file.name = "faculty.csv"
        op = self.service.import_userbase_faculty_supervisors(file, dry_run=False)
        self.assertEqual(op.success_count, 1)

    def test_import_userbase_residents(self):
        # expects full_name, email, specialty, year, training_start, department_code, hospital_code
        csv_content = f"full_name,email,specialty,year,training_start,department_code,hospital_code,supervisor_email\nBob Resident,bob.res@test.com,urology,1,2025-01-01,MED,AH,{self.supervisor.email}\n"
        file = io.BytesIO(csv_content.encode('utf-8'))
        file.name = "residents.csv"
        op = self.service.import_userbase_residents(file, dry_run=False)
        self.assertEqual(op.success_count, 1)

    def test_import_trainees_full(self):
        csv_content = "Name of Trainee,Date of Joining,MS/FCPS,Supervisor Name\nJane Dilly,2025-01-01,FCPS,Dr. Smithy\n"
        file = io.BytesIO(csv_content.encode('utf-8'))
        file.name = "trainees.csv"
        op = self.service.import_trainees(file, dry_run=False)
        self.assertEqual(op.success_count, 1)

    def test_import_supervisors_extended(self):
        csv_content = "Name,Email,Specialty,Department\nAlice Babs,alice.babs@test.com,urology,Medicine\n"
        file = io.BytesIO(csv_content.encode('utf-8'))
        file.name = "sups.csv"
        op = self.service.import_supervisors(file, dry_run=False)
        self.assertEqual(op.success_count, 1)

    def test_assign_supervisor_extended(self):
        entry = LogbookEntry.objects.create(
            resident_training_record=self.rtr,
            patient_id_number="P999-EXT",
            patient_seen_at=timezone.now(),
            status="DRAFT"
        )
        op = self.service.assign_supervisor([entry.id], self.supervisor)
        self.assertEqual(op.success_count, 1)
