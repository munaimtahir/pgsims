"""Additional coverage for sims.bulk.services: export_dataset, review/assign, and the
validation / error / rollback branches of the various import_* methods that the existing
test_bulk_services*.py files only exercise on the happy path.
"""

import io
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied, ValidationError
from django.test import TestCase
from django.utils import timezone

from sims.academics.models import AcademicSession, Department
from sims.bulk.services import (
    BulkService,
    _generate_username,
    _infer_training_year,
    _parse_csv_rows,
    _parse_date,
    _parse_name,
    convert_excel_to_trainee_format,
    generate_trainee_template,
)
from sims.rotations.models import Hospital, HospitalDepartment
from sims.supervision.models import ResidentSupervisorAssignment
from sims.training.models import (
    LogbookEntry,
    ProgramRotationTemplate,
    ResidentTrainingRecord,
    RotationAssignment,
    TrainingProgram,
)
from sims.users.models import ResidentProfile, SupervisorProfile

User = get_user_model()


def _csv(content: str, name: str = "upload.csv") -> io.BytesIO:
    file = io.BytesIO(content.encode("utf-8"))
    file.name = name
    return file


class BulkServicePermissionsTests(TestCase):
    def test_resident_actor_denied(self):
        resident = User.objects.create_user(username="r1", password="pw", role="RESIDENT")
        with self.assertRaises(PermissionDenied):
            BulkService(resident)


class BulkServiceReviewAssignTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username="admin_rev", password="pw", role="ADMIN")
        self.supervisor = User.objects.create_user(
            username="sup_rev", password="pw", role="SUPERVISOR", email="sup_rev@test.com"
        )
        self.pg = User.objects.create_user(
            username="pg_rev", password="pw", role="RESIDENT", email="pg_rev@test.com"
        )
        self.service = BulkService(self.admin)
        self.program = TrainingProgram.objects.create(name="Medicine", code="MED-REV", duration_months=48)
        self.rtr = ResidentTrainingRecord.objects.create(
            resident_user=self.pg, program=self.program, start_date=date.today()
        )
        self.entry = LogbookEntry.objects.create(
            resident_training_record=self.rtr,
            patient_id_number="P-REV-1",
            patient_seen_at=timezone.now(),
            status="DRAFT",
        )

    def test_review_entries_updates_status(self):
        # BulkService.review_entries() (sims/bulk/services.py) used to do
        # entry.save(update_fields=["status", "verified_at"]), but sims.training.LogbookEntry has
        # no `verified_at` field (it only defines submitted_at/returned_at/approved_at -- that
        # field exists on the unrelated sims.academics.LogbookEntry model). Every call crashed
        # with ValueError instead of completing, so bulk logbook review was broken end-to-end.
        # Fixed by only updating the `status` field, which does exist.
        operation = self.service.review_entries([self.entry.id], "approved")
        self.assertEqual(operation.success_count, 1)
        self.entry.refresh_from_db()
        self.assertEqual(self.entry.status, "approved")

    def test_assign_supervisor_success_and_missing_id(self):
        operation = self.service.assign_supervisor([self.entry.id, 424242], self.supervisor)
        self.assertEqual(operation.success_count, 1)
        self.assertEqual(operation.failure_count, 1)
        self.entry.refresh_from_db()
        self.assertEqual(self.entry.reviewed_by_id, self.supervisor.id)


class BulkServiceLogbookImportTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username="admin_lb", password="pw", role="ADMIN")
        self.pg = User.objects.create_user(
            username="pg_lb", password="pw", role="RESIDENT", email="pg_lb@test.com"
        )
        self.service = BulkService(self.admin)
        self.program = TrainingProgram.objects.create(name="Medicine", code="MED-LB", duration_months=48)

    def test_invalid_pg_username_fails_row(self):
        file = _csv("pg_username,case_title,date,status\nnobody,Case,2026-01-01,submitted\n")
        operation = self.service.import_logbook_entries(file, dry_run=True)
        self.assertEqual(operation.failure_count, 1)
        self.assertEqual(operation.details["failures"][0]["error"], "invalid-pg")

    def test_invalid_date_fails_row(self):
        file = _csv(f"pg_username,case_title,date,status\n{self.pg.username},Case,not-a-date,submitted\n")
        operation = self.service.import_logbook_entries(file, dry_run=True)
        self.assertEqual(operation.failure_count, 1)
        self.assertEqual(operation.details["failures"][0]["error"], "invalid-date")

    def test_no_training_record_fails_row(self):
        file = _csv(f"pg_username,case_title,date,status\n{self.pg.username},Case,2026-01-01,submitted\n")
        operation = self.service.import_logbook_entries(file, dry_run=True)
        self.assertEqual(operation.failure_count, 1)
        self.assertEqual(operation.details["failures"][0]["error"], "no-training-record")

    def test_non_dry_run_rolls_back_whole_batch_on_error(self):
        ResidentTrainingRecord.objects.create(resident_user=self.pg, program=self.program, start_date=date.today())
        file = _csv(
            "pg_username,case_title,date,status\n"
            f"{self.pg.username},Good Case,2026-01-01,submitted\n"
            "nobody,Bad Case,2026-01-01,submitted\n"
        )
        operation = self.service.import_logbook_entries(file, dry_run=False, allow_partial=False)
        self.assertEqual(operation.status, "failed")
        self.assertFalse(LogbookEntry.objects.filter(diagnosis="Good Case").exists())

    def test_allow_partial_keeps_successful_rows(self):
        ResidentTrainingRecord.objects.create(resident_user=self.pg, program=self.program, start_date=date.today())
        file = _csv(
            "pg_username,case_title,date,status\n"
            f"{self.pg.username},Good Case 2,2026-01-01,submitted\n"
            "nobody,Bad Case,2026-01-01,submitted\n"
        )
        operation = self.service.import_logbook_entries(file, dry_run=False, allow_partial=True)
        self.assertEqual(operation.success_count, 1)
        self.assertEqual(operation.failure_count, 1)
        self.assertTrue(LogbookEntry.objects.filter(diagnosis="Good Case 2").exists())

    def test_missing_required_columns_propagates_validation_error(self):
        # import_logbook_entries does not catch ValidationError from _parse_rows itself;
        # it propagates to the caller (the view layer catches it as a 400).
        file = _csv("wrong_col\nvalue\n")
        with self.assertRaises(ValidationError):
            self.service.import_logbook_entries(file, dry_run=True)


class BulkServiceParseRowsTests(TestCase):
    def test_missing_columns_raise_validation_error(self):
        file = _csv("foo,bar\n1,2\n")
        with self.assertRaises(ValidationError):
            list(_parse_csv_rows(file, required_columns={"required_col"}))

    def test_unsupported_file_extension_raises(self):
        file = io.BytesIO(b"data")
        file.name = "upload.txt"
        with self.assertRaises(ValidationError):
            list(_parse_csv_rows(file))


class BulkServiceTraineeImportTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username="admin_tr", password="pw", role="ADMIN")
        self.service = BulkService(self.admin)

    def test_missing_name_fails_row(self):
        file = _csv("Name of Trainee,Date of Joining\n,2026-01-01\n")
        operation = self.service.import_trainees(file, dry_run=True)
        self.assertEqual(operation.failure_count, 1)
        self.assertIn("Name of Trainee", operation.details["failures"][0]["error"])

    def test_invalid_date_fails_row(self):
        file = _csv("Name of Trainee,Date of Joining\nJohn Doe,not-a-date\n")
        operation = self.service.import_trainees(file, dry_run=True)
        self.assertEqual(operation.failure_count, 1)

    def test_missing_supervisor_without_allow_partial_fails_row(self):
        file = _csv("Name of Trainee,Date of Joining\nJohn Doe,2026-01-01\n")
        operation = self.service.import_trainees(file, dry_run=True, allow_partial=False)
        self.assertEqual(operation.failure_count, 1)
        self.assertIn("Supervisor Name is required", operation.details["failures"][0]["error"])

    def test_missing_supervisor_with_allow_partial_creates_unlinked_resident(self):
        file = _csv("Name of Trainee,Date of Joining\nJane Roe,2026-01-01\n")
        operation = self.service.import_trainees(file, dry_run=False, allow_partial=True)
        self.assertEqual(operation.success_count, 1)
        self.assertTrue(User.objects.filter(first_name="Jane", last_name="Roe", supervisor__isnull=True).exists())


class BulkServiceDepartmentHospitalImportTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username="admin_dh", password="pw", role="ADMIN")
        self.service = BulkService(self.admin)
        self.hospital = Hospital.objects.create(name="Allied Hospital", code="AH", is_active=True)

    def test_import_departments_missing_name_and_code_fails_row(self):
        file = _csv("code,name,description,active\n,,,true\n")
        operation = self.service.import_departments(file, dry_run=True)
        self.assertEqual(operation.failure_count, 1)

    def test_import_departments_no_active_hospital_marks_failed(self):
        Hospital.objects.all().update(is_active=False)
        file = _csv("code,name,description,active\nSURG,Surgery,,true\n")
        operation = self.service.import_departments(file, dry_run=True)
        self.assertEqual(operation.status, "failed")

    def test_import_departments_rollback_on_error_without_allow_partial(self):
        file = _csv(
            "code,name,description,active\n"
            "SURG,Surgery,,true\n"
            ",,,\n"
        )
        operation = self.service.import_departments(file, dry_run=False, allow_partial=False)
        self.assertEqual(operation.status, "failed")
        self.assertFalse(Department.objects.filter(code="SURG").exists())

    def test_import_hospitals_missing_code_fails_row(self):
        file = _csv("hospital_code,hospital_name,active\n,Some Hospital,true\n")
        operation = self.service.import_hospitals(file, dry_run=True)
        self.assertEqual(operation.failure_count, 1)

    def test_import_hospitals_rollback_on_error_without_allow_partial(self):
        file = _csv(
            "hospital_code,hospital_name,active\n"
            "NEWH,New Hospital,true\n"
            ",Missing Code,true\n"
        )
        operation = self.service.import_hospitals(file, dry_run=False, allow_partial=False)
        self.assertEqual(operation.status, "failed")
        self.assertFalse(Hospital.objects.filter(code="NEWH").exists())


class BulkServiceSupervisionLinksTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username="admin_sl", password="pw", role="ADMIN")
        self.service = BulkService(self.admin)
        self.hospital = Hospital.objects.create(name="Allied Hospital", code="AH-SL", is_active=True)
        self.dept = Department.objects.create(name="Medicine", code="MED-SL", active=True)
        self.supervisor = User.objects.create_user(
            username="sup_sl", password="pw", role="SUPERVISOR", email="sup_sl@test.com"
        )
        self.resident = User.objects.create_user(
            username="res_sl", password="pw", role="RESIDENT", email="res_sl@test.com"
        )
        SupervisorProfile.objects.create(user=self.supervisor, hospital=self.hospital, department_ref=self.dept)
        ResidentProfile.objects.create(user=self.resident, hospital=self.hospital, department_ref=self.dept)

    def test_missing_emails_fails_row(self):
        file = _csv("supervisor_email,resident_email,department_code,active\n,,MED-SL,true\n")
        operation = self.service.import_supervision_links(file, dry_run=True)
        self.assertEqual(operation.failure_count, 1)

    def test_unknown_supervisor_fails_row(self):
        file = _csv(
            "supervisor_email,resident_email,department_code,active\n"
            f"nobody@test.com,{self.resident.email},MED-SL,true\n"
        )
        operation = self.service.import_supervision_links(file, dry_run=True)
        self.assertEqual(operation.failure_count, 1)
        self.assertIn("not found", operation.details["failures"][0]["error"])

    def test_unknown_resident_fails_row(self):
        file = _csv(
            "supervisor_email,resident_email,department_code,active\n"
            f"{self.supervisor.email},nobody@test.com,MED-SL,true\n"
        )
        operation = self.service.import_supervision_links(file, dry_run=True)
        self.assertEqual(operation.failure_count, 1)

    def test_apply_creates_and_can_end_assignment(self):
        file = _csv(
            "supervisor_email,resident_email,department_code,start_date,active\n"
            f"{self.supervisor.email},{self.resident.email},MED-SL,2026-01-01,false\n"
        )
        operation = self.service.import_supervision_links(file, dry_run=False)
        self.assertEqual(operation.success_count, 1)
        assignment = ResidentSupervisorAssignment.objects.get(
            supervisor=self.supervisor.supervisor_profile, resident=self.resident.resident_profile
        )
        self.assertFalse(assignment.is_active)
        self.assertEqual(assignment.status, ResidentSupervisorAssignment.STATUS_ENDED)


class BulkServiceTrainingSessionParseErrorTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username="admin_ts", password="pw", role="ADMIN")
        self.service = BulkService(self.admin)

    def test_import_training_programs_bad_file_marks_failed(self):
        file = io.BytesIO(b"not-a-table")
        file.name = "upload.txt"
        operation = self.service.import_training_programs(file, dry_run=True)
        self.assertEqual(operation.status, "failed")

    def test_import_academic_sessions_bad_file_marks_failed(self):
        file = io.BytesIO(b"not-a-table")
        file.name = "upload.txt"
        operation = self.service.import_academic_sessions(file, dry_run=True)
        self.assertEqual(operation.status, "failed")

    def test_import_rotation_templates_bad_file_marks_failed(self):
        file = io.BytesIO(b"not-a-table")
        file.name = "upload.txt"
        operation = self.service.import_rotation_templates(file, dry_run=True)
        self.assertEqual(operation.status, "failed")

    def test_import_resident_training_records_bad_file_marks_failed(self):
        file = io.BytesIO(b"not-a-table")
        file.name = "upload.txt"
        operation = self.service.import_resident_training_records(file, dry_run=True)
        self.assertEqual(operation.status, "failed")


class BulkServiceExportDatasetTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username="admin_exp", password="pw", role="ADMIN")
        self.service = BulkService(self.admin)
        self.hospital = Hospital.objects.create(name="Allied Hospital", code="AH", is_active=True)
        self.dept = Department.objects.create(name="Medicine", code="MED-EXP", active=True)
        self.hdept = HospitalDepartment.objects.create(hospital=self.hospital, department=self.dept, is_active=True)
        self.supervisor = User.objects.create_user(
            username="sup_exp", password="pw", role="SUPERVISOR", email="sup_exp@test.com",
            specialty="urology", phone_number="0300", registration_number="REG1",
        )
        self.resident = User.objects.create_user(
            username="res_exp", password="pw", role="RESIDENT", email="res_exp@test.com",
            specialty="urology", year="1", supervisor=self.supervisor, home_department=self.dept,
        )
        SupervisorProfile.objects.create(user=self.supervisor, hospital=self.hospital, department_ref=self.dept)
        ResidentProfile.objects.create(user=self.resident, hospital=self.hospital, department_ref=self.dept)
        self.program = TrainingProgram.objects.create(name="Medicine", code="MED-EXPPRG", duration_months=48)
        AcademicSession.objects.create(code="2026-EXP", name="Session 2026", active=True)
        ProgramRotationTemplate.objects.create(
            program=self.program, name="Core Rotation", department=self.dept, duration_weeks=8, required=True
        )
        self.rtr = ResidentTrainingRecord.objects.create(
            resident_user=self.resident, program=self.program, start_date=date.today()
        )

    def test_invalid_format_raises(self):
        with self.assertRaises(ValidationError):
            self.service.export_dataset(resource="residents", export_format="pdf")

    def test_unsupported_resource_raises(self):
        with self.assertRaises(ValidationError):
            self.service.export_dataset(resource="not-a-real-resource", export_format="csv")

    def test_export_residents_csv(self):
        # sims/bulk/userbase_engine.py export_rows_for("residents") used to read
        # profile.pgr_id / profile.training_start / profile.training_end / profile.training_level
        # off ResidentProfile, but that model (sims/users/models.py) has no such fields (it only
        # has registration_no, hospital, department_ref, etc). Any resident with a resident_profile
        # crashed the residents export with AttributeError. Fixed to read pgr_id from
        # ResidentProfile.registration_no and training_start/training_end/training_level from the
        # resident's sims.training.ResidentTrainingRecord (the same places the import path writes
        # them to).
        result = self.service.export_dataset(resource="residents", export_format="csv")
        self.assertIn(b"res_exp@test.com", result.content)
        self.assertIn(str(self.rtr.start_date), result.content.decode("utf-8"))

    def test_export_supervisors_xlsx(self):
        result = self.service.export_dataset(resource="supervisors", export_format="xlsx")
        self.assertTrue(result.filename.endswith(".xlsx"))
        self.assertGreater(len(result.content), 0)

    def test_export_departments_csv(self):
        result = self.service.export_dataset(resource="departments", export_format="csv")
        self.assertIn(b"MED-EXP", result.content)

    def test_export_hospitals_csv(self):
        result = self.service.export_dataset(resource="hospitals", export_format="csv")
        self.assertIn(b"AH", result.content)

    def test_export_matrix_csv(self):
        result = self.service.export_dataset(resource="matrix", export_format="csv")
        self.assertIn(b"AH", result.content)
        self.assertIn(b"MED-EXP", result.content)

    def test_export_supervision_links_csv(self):
        from sims.supervision.services import create_supervisor_assignment

        create_supervisor_assignment(
            resident=self.resident.resident_profile,
            supervisor=self.supervisor.supervisor_profile,
            assignment_type=ResidentSupervisorAssignment.ASSIGNMENT_PRIMARY,
            start_date=date.today(),
            notes="test",
            actor=self.admin,
        )
        result = self.service.export_dataset(resource="supervision_links", export_format="csv")
        self.assertIn(b"sup_exp@test.com", result.content)

    def test_export_training_programs_csv(self):
        result = self.service.export_dataset(resource="training-programs", export_format="csv")
        self.assertIn(b"MED-EXPPRG", result.content)

    def test_export_academic_sessions_csv(self):
        result = self.service.export_dataset(resource="academic-sessions", export_format="csv")
        self.assertIn(b"2026-EXP", result.content)

    def test_export_rotation_templates_csv(self):
        result = self.service.export_dataset(resource="rotation_templates", export_format="csv")
        self.assertIn(b"Core Rotation", result.content)

    def test_export_resident_training_records_csv(self):
        result = self.service.export_dataset(resource="resident_training_records", export_format="csv")
        self.assertIn(b"res_exp@test.com", result.content)

    def test_export_userbase_resource_delegates_to_userbase_engine(self):
        result = self.service.export_dataset(resource="hospitals", export_format="csv")
        self.assertIn(b"hospital_code", result.content)

    def test_export_template_hospitals(self):
        result = self.service.export_template("hospitals")
        self.assertTrue(result.filename.endswith("_template.csv"))
        self.assertIn(b"hospital_code", result.content)

    def test_export_template_training_programs(self):
        result = self.service.export_template("training_programs")
        self.assertIn(b"program_code", result.content)


class BulkServiceHelperFunctionTests(TestCase):
    def setUp(self):
        User.objects.create_user(username="jane.doe", password="pw", role="RESIDENT")

    def test_parse_name_variants(self):
        self.assertEqual(_parse_name(""), ("", ""))
        self.assertEqual(_parse_name("Dr. Jane Doe"), ("Jane", "Doe"))
        self.assertEqual(_parse_name("Ali"), ("Ali", ""))

    def test_generate_username_collision_appends_counter(self):
        username = _generate_username("Jane", "Doe")
        self.assertEqual(username, "jane.doe1")

    def test_infer_training_year_ranges(self):
        today = date.today()
        self.assertEqual(_infer_training_year(today), "1")
        self.assertEqual(_infer_training_year(today - timedelta(days=400)), "2")
        self.assertEqual(_infer_training_year(today - timedelta(days=800)), "3")
        self.assertEqual(_infer_training_year(today - timedelta(days=1200)), "4")
        self.assertEqual(_infer_training_year(today + timedelta(days=10)), "1")

    def test_parse_date_formats_and_failure(self):
        self.assertEqual(_parse_date("2026-01-15"), date(2026, 1, 15))
        self.assertEqual(_parse_date("15/01/2026"), date(2026, 1, 15))
        with self.assertRaises(ValueError):
            _parse_date("")
        with self.assertRaises(ValueError):
            _parse_date("not-a-date-at-all")

    def test_generate_trainee_template_produces_workbook(self):
        output = generate_trainee_template()
        self.assertGreater(len(output.getvalue()), 0)

    def test_convert_excel_to_trainee_format_maps_columns(self):
        from openpyxl import Workbook

        workbook = Workbook()
        sheet = workbook.active
        sheet.append(["Resident Name", "Date of Joining", "Qualification", "Mentor"])
        sheet.append(["John Doe", "2026-01-01", "FCPS", "Dr. Smith"])
        stream = io.BytesIO()
        workbook.save(stream)
        stream.seek(0)
        stream.name = "source.xlsx"

        output = convert_excel_to_trainee_format(stream)
        self.assertGreater(len(output.getvalue()), 0)

    def test_convert_excel_to_trainee_format_rejects_non_excel(self):
        file = io.BytesIO(b"not excel")
        file.name = "source.csv"
        with self.assertRaises(ValidationError):
            convert_excel_to_trainee_format(file)
