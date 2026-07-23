"""Tests for sims.bulk.services.BulkService import methods that had zero prior coverage:
import_hospital_departments, import_training_programs, import_rotation_templates, and
import_resident_training_records. These are exactly the entities wired into the /masters
bulk-import screen (see docs/AUDIT_2026-07-23_PILOT_READINESS.md Step 5) - the pilot roster
onboarding path this audit flagged as needing test coverage.
"""

import io
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase

from sims.academics.models import Department
from sims.bulk.services import BulkService
from sims.rotations.models import Hospital, HospitalDepartment
from sims.training.models import ProgramRotationTemplate, ResidentTrainingRecord, TrainingProgram
from sims.users.models import ResidentProfile

User = get_user_model()


def _csv_file(content: str, name: str = "upload.csv") -> io.BytesIO:
    file = io.BytesIO(content.encode("utf-8"))
    file.name = name
    return file


class BulkImportHospitalDepartmentsTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username="admin_hd", password="pw", role="ADMIN")
        self.service = BulkService(self.admin)
        self.hospital = Hospital.objects.create(name="Allied Hospital", code="AH", is_active=True)
        self.dept = Department.objects.create(name="Medicine", code="MED", active=True)

    def test_dry_run_does_not_create_matrix_row(self):
        file = _csv_file("hospital_code,department_code,active\nAH,MED,true\n")
        operation = self.service.import_hospital_departments(file, dry_run=True)
        self.assertEqual(operation.success_count, 1)
        self.assertFalse(HospitalDepartment.objects.filter(hospital=self.hospital, department=self.dept).exists())

    def test_apply_creates_matrix_row(self):
        file = _csv_file("hospital_code,department_code,active\nAH,MED,true\n")
        operation = self.service.import_hospital_departments(file, dry_run=False)
        self.assertEqual(operation.success_count, 1)
        self.assertTrue(HospitalDepartment.objects.filter(hospital=self.hospital, department=self.dept, is_active=True).exists())

    def test_unknown_hospital_code_fails_row(self):
        file = _csv_file("hospital_code,department_code,active\nNOPE,MED,true\n")
        operation = self.service.import_hospital_departments(file, dry_run=True)
        self.assertEqual(operation.success_count, 0)
        self.assertEqual(operation.failure_count, 1)

    def test_missing_required_columns_fails_row(self):
        file = _csv_file("hospital_code,department_code,active\n,MED,true\n")
        operation = self.service.import_hospital_departments(file, dry_run=True)
        self.assertEqual(operation.failure_count, 1)

    def test_apply_rolls_back_whole_batch_on_error_without_allow_partial(self):
        file = _csv_file(
            "hospital_code,department_code,active\nAH,MED,true\nNOPE,MED,true\n"
        )
        operation = self.service.import_hospital_departments(file, dry_run=False, allow_partial=False)
        self.assertEqual(operation.status, "failed")
        self.assertFalse(HospitalDepartment.objects.filter(hospital=self.hospital, department=self.dept).exists())


class BulkImportTrainingProgramsTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username="admin_tp", password="pw", role="ADMIN")
        self.service = BulkService(self.admin)

    def test_apply_creates_program(self):
        file = _csv_file("program_code,program_name,duration_months,active\nMED,MS Medicine,60,true\n")
        operation = self.service.import_training_programs(file, dry_run=False)
        self.assertEqual(operation.success_count, 1)
        program = TrainingProgram.objects.get(code="MED")
        self.assertEqual(program.name, "MS Medicine")
        self.assertEqual(program.duration_months, 60)
        self.assertTrue(program.active)

    def test_dry_run_does_not_create_program(self):
        file = _csv_file("program_code,program_name,duration_months,active\nMED,MS Medicine,60,true\n")
        operation = self.service.import_training_programs(file, dry_run=True)
        self.assertEqual(operation.success_count, 1)
        self.assertFalse(TrainingProgram.objects.filter(code="MED").exists())

    def test_apply_is_idempotent_update_or_create(self):
        file = _csv_file("program_code,program_name,duration_months,active\nMED,MS Medicine,60,true\n")
        self.service.import_training_programs(file, dry_run=False)
        file2 = _csv_file("program_code,program_name,duration_months,active\nMED,MS Medicine Updated,72,true\n")
        self.service.import_training_programs(file2, dry_run=False)
        self.assertEqual(TrainingProgram.objects.filter(code="MED").count(), 1)
        program = TrainingProgram.objects.get(code="MED")
        self.assertEqual(program.name, "MS Medicine Updated")
        self.assertEqual(program.duration_months, 72)

    def test_invalid_duration_months_fails_row(self):
        file = _csv_file("program_code,program_name,duration_months,active\nMED,MS Medicine,not-a-number,true\n")
        operation = self.service.import_training_programs(file, dry_run=False)
        self.assertEqual(operation.success_count, 0)
        self.assertEqual(operation.failure_count, 1)

    def test_missing_required_fields_fails_row(self):
        file = _csv_file("program_code,program_name,duration_months,active\n,MS Medicine,60,true\n")
        operation = self.service.import_training_programs(file, dry_run=False)
        self.assertEqual(operation.failure_count, 1)


class BulkImportRotationTemplatesTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username="admin_rt", password="pw", role="ADMIN")
        self.service = BulkService(self.admin)
        self.program = TrainingProgram.objects.create(name="Medicine", code="MED-FCPS", duration_months=48)
        self.dept = Department.objects.create(name="Medicine", code="MED", active=True)

    def test_apply_creates_rotation_template(self):
        file = _csv_file(
            "program_code,template_name,department_code,duration_weeks,required\n"
            "MED-FCPS,Core Medicine Rotation,MED,8,true\n"
        )
        operation = self.service.import_rotation_templates(file, dry_run=False)
        self.assertEqual(operation.success_count, 1)
        template = ProgramRotationTemplate.objects.get(program=self.program, name="Core Medicine Rotation")
        self.assertEqual(template.department, self.dept)
        self.assertEqual(template.duration_weeks, 8)
        self.assertTrue(template.required)

    def test_unknown_program_code_fails_row(self):
        file = _csv_file(
            "program_code,template_name,department_code,duration_weeks,required\n"
            "NOPE,Core Medicine Rotation,MED,8,true\n"
        )
        operation = self.service.import_rotation_templates(file, dry_run=False)
        self.assertEqual(operation.success_count, 0)
        self.assertEqual(operation.failure_count, 1)

    def test_invalid_duration_weeks_fails_row(self):
        file = _csv_file(
            "program_code,template_name,department_code,duration_weeks,required\n"
            "MED-FCPS,Core Medicine Rotation,MED,not-a-number,true\n"
        )
        operation = self.service.import_rotation_templates(file, dry_run=False)
        self.assertEqual(operation.failure_count, 1)


class BulkImportResidentTrainingRecordsTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username="admin_rtr", password="pw", role="ADMIN")
        self.service = BulkService(self.admin)
        self.resident = User.objects.create_user(
            username="resident_rtr", password="pw", role="RESIDENT", email="resident_rtr@example.com"
        )
        ResidentProfile.objects.create(user=self.resident)
        self.program = TrainingProgram.objects.create(name="Medicine", code="MED-FCPS", duration_months=48)

    def test_apply_creates_training_record(self):
        file = _csv_file(
            "resident_email,program_code,start_date,expected_end_date,current_level\n"
            "resident_rtr@example.com,MED-FCPS,2026-01-01,2029-01-01,Y1\n"
        )
        operation = self.service.import_resident_training_records(file, dry_run=False)
        self.assertEqual(operation.success_count, 1)
        record = ResidentTrainingRecord.objects.get(resident_user=self.resident, program=self.program)
        self.assertEqual(str(record.start_date), "2026-01-01")
        self.assertTrue(record.active)

    def test_unknown_resident_email_fails_row(self):
        file = _csv_file(
            "resident_email,program_code,start_date\n"
            "nobody@example.com,MED-FCPS,2026-01-01\n"
        )
        operation = self.service.import_resident_training_records(file, dry_run=False)
        self.assertEqual(operation.success_count, 0)
        self.assertEqual(operation.failure_count, 1)

    def test_unknown_program_code_fails_row(self):
        file = _csv_file(
            "resident_email,program_code,start_date\n"
            "resident_rtr@example.com,NOPE,2026-01-01\n"
        )
        operation = self.service.import_resident_training_records(file, dry_run=False)
        self.assertEqual(operation.failure_count, 1)

    def test_missing_required_fields_fails_row(self):
        file = _csv_file(
            "resident_email,program_code,start_date\n"
            ",MED-FCPS,2026-01-01\n"
        )
        operation = self.service.import_resident_training_records(file, dry_run=False)
        self.assertEqual(operation.failure_count, 1)
