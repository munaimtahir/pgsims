from django.test import TestCase
from django.contrib.auth import get_user_model
from sims.bulk.services import BulkService
from sims.training.models import (
    LogbookEntry, TrainingProgram, ResidentTrainingRecord, ProgramRotationTemplate
)
from sims.rotations.models import Hospital, HospitalDepartment
from sims.academics.models import Department
from django.utils import timezone
from datetime import date, timedelta
import io

User = get_user_model()

class BulkServicesTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username="admin_srv", password="password123", role="admin")
        self.supervisor = User.objects.create_user(username="sup_srv", password="password123", role="supervisor", email="sup@test.com")
        self.pg = User.objects.create_user(username="pg_srv", password="password123", role="pg", email="pg@test.com")
        self.service = BulkService(self.admin)
        
        self.hospital = Hospital.objects.create(name="Allied Hospital", code="AH", is_active=True)
        self.dept = Department.objects.create(name="Medicine", code="MED", active=True)
        self.hdept = HospitalDepartment.objects.create(hospital=self.hospital, department=self.dept, is_active=True)
        self.program = TrainingProgram.objects.create(name="Medicine", code="MED-FCPS", duration_months=48)
        self.rtr = ResidentTrainingRecord.objects.create(
            resident_user=self.pg, program=self.program, 
            start_date=date.today(), expected_end_date=date.today() + timedelta(days=365)
        )

    def test_import_trainees_srv(self):
        # import_trainees uses _parse_trainee_rows which might expect specific columns
        csv_content = "Name of Trainee,Date of Joining,MS/FCPS,Supervisor Name\nJohn Doe,2026-01-01,FCPS,Dr. Smith\n"
        file = io.BytesIO(csv_content.encode('utf-8'))
        file.name = "trainees.csv"
        operation = self.service.import_trainees(file, dry_run=False)
        self.assertEqual(operation.success_count, 1)
        self.assertTrue(User.objects.filter(first_name="John", last_name="Doe").exists())

    def test_import_hospitals_srv(self):
        csv_content = "hospital_code,hospital_name,active\nH2,Hospital Two,true\n"
        file = io.BytesIO(csv_content.encode('utf-8'))
        file.name = "hospitals.csv"
        operation = self.service.import_hospitals(file, dry_run=False)
        self.assertEqual(operation.success_count, 1)

    def test_import_departments_srv(self):
        csv_content = "code,name,description,active\nSURG,Surgery,Surgery Dept,true\n"
        file = io.BytesIO(csv_content.encode('utf-8'))
        file.name = "depts.csv"
        operation = self.service.import_departments(file, dry_run=False)
        self.assertEqual(operation.success_count, 1)

    def test_import_supervision_links_srv(self):
        csv_content = f"supervisor_email,resident_email,department_code,start_date,active\n{self.supervisor.email},{self.pg.email},MED,2026-01-01,true\n"
        file = io.BytesIO(csv_content.encode('utf-8'))
        file.name = "links.csv"
        operation = self.service.import_supervision_links(file, dry_run=False)
        self.assertEqual(operation.success_count, 1)

    def test_import_supervisors_srv(self):
        csv_content = "name,email,specialty,department\nDr. New Supervisor,newsup@test.com,urology,Medicine\n"
        file = io.BytesIO(csv_content.encode('utf-8'))
        file.name = "sups.csv"
        operation = self.service.import_supervisors(file, dry_run=False)
        self.assertEqual(operation.success_count, 1)

    def test_import_residents_srv(self):
        csv_content = f"name,year,specialty,supervisor_username,email\nNew Resident,1,urology,{self.supervisor.username},newres@test.com\n"
        file = io.BytesIO(csv_content.encode('utf-8'))
        file.name = "residents.csv"
        operation = self.service.import_residents(file, dry_run=False)
        self.assertEqual(operation.success_count, 1)

    def test_import_logbook_entries_csv(self):
        csv_content = f"pg_username,case_title,date,status\n{self.pg.username},New Case,2026-01-01,submitted\n"
        file = io.BytesIO(csv_content.encode('utf-8'))
        file.name = "logbook.csv"
        operation = self.service.import_logbook_entries(file, dry_run=False)
        self.assertEqual(operation.success_count, 1)
