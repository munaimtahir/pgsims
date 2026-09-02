"""Additional coverage for sims.bulk.userbase_engine: _import_rotation_assignments (previously
0% covered), export_rows_for's supervision-links/rotation-assignments branches, and the small
validation helper functions that raise on bad input.
"""

import io
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from sims.academics.models import Department
from sims.bulk.userbase_engine import (
    _department_or_none,
    _error_text,
    _normalize_resident_role,
    _normalize_staff_role,
    _normalize_year,
    _parse_bool,
    _resolve_department,
    _resolve_hospital_department,
    export_rows_for,
    import_entity,
    template_rows_for,
)
from sims.rotations.models import Hospital, HospitalDepartment
from sims.supervision.models import ResidentSupervisorAssignment
from sims.supervision.services import create_supervisor_assignment
from sims.training.models import ResidentTrainingRecord, RotationAssignment, TrainingProgram
from sims.users.models import ResidentProfile, SupervisorProfile

User = get_user_model()


def _csv(content: str, name: str = "upload.csv") -> io.BytesIO:
    file = io.BytesIO(content.encode("utf-8"))
    file.name = name
    return file


class RotationAssignmentsImportTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username="admin_ra", role="ADMIN")
        self.hospital = Hospital.objects.create(name="Allied Hospital", code="AH-RA")
        self.dept = Department.objects.create(name="Medicine", code="MED-RA")
        self.hdept = HospitalDepartment.objects.create(hospital=self.hospital, department=self.dept, is_active=True)
        self.resident = User.objects.create_user(username="res_ra", email="res_ra@test.com", role="RESIDENT")
        self.program = TrainingProgram.objects.create(name="Medicine", code="MED-RA-PRG", duration_months=48)
        self.rtr = ResidentTrainingRecord.objects.create(
            resident_user=self.resident, program=self.program, start_date=date.today(), active=True
        )

    def test_apply_creates_rotation_assignment(self):
        file = _csv(
            "resident_email,hospital_code,department_code,start_date,end_date,status\n"
            "res_ra@test.com,AH-RA,MED-RA,2026-01-01,2026-02-01,DRAFT\n"
        )
        result = import_entity(self.admin, "rotation-assignments", file, dry_run=False, allow_partial=False)
        self.assertEqual(len(result["successes"]), 1)
        self.assertEqual(RotationAssignment.objects.filter(resident_training=self.rtr).count(), 1)

    def test_dry_run_does_not_create_row(self):
        file = _csv(
            "resident_email,hospital_code,department_code,start_date,end_date,status\n"
            "res_ra@test.com,AH-RA,MED-RA,2026-01-01,2026-02-01,DRAFT\n"
        )
        result = import_entity(self.admin, "rotation-assignments", file, dry_run=True, allow_partial=False)
        self.assertEqual(len(result["successes"]), 1)
        self.assertEqual(RotationAssignment.objects.count(), 0)

    def test_missing_training_record_fails(self):
        User.objects.create_user(username="res_ra2", email="res_ra2@test.com", role="RESIDENT")
        file = _csv(
            "resident_email,hospital_code,department_code,start_date,end_date,status\n"
            "res_ra2@test.com,AH-RA,MED-RA,2026-01-01,2026-02-01,DRAFT\n"
        )
        result = import_entity(self.admin, "rotation-assignments", file, dry_run=True, allow_partial=True)
        self.assertEqual(len(result["failures"]), 1)
        self.assertIn("training record", result["failures"][0]["error"])

    def test_missing_matrix_link_fails(self):
        file = _csv(
            "resident_email,hospital_code,department_code,start_date,end_date,status\n"
            "res_ra@test.com,NOPE,MED-RA,2026-01-01,2026-02-01,DRAFT\n"
        )
        result = import_entity(self.admin, "rotation-assignments", file, dry_run=True, allow_partial=True)
        self.assertEqual(len(result["failures"]), 1)
        self.assertIn("matrix link", result["failures"][0]["error"])

    def test_end_date_before_start_date_fails(self):
        file = _csv(
            "resident_email,hospital_code,department_code,start_date,end_date,status\n"
            "res_ra@test.com,AH-RA,MED-RA,2026-02-01,2026-01-01,DRAFT\n"
        )
        result = import_entity(self.admin, "rotation-assignments", file, dry_run=True, allow_partial=True)
        self.assertEqual(len(result["failures"]), 1)
        self.assertIn("End date must be after start date", result["failures"][0]["error"])

    def test_overlapping_active_assignment_fails(self):
        RotationAssignment.objects.create(
            resident_training=self.rtr,
            hospital_department=self.hdept,
            start_date=date(2026, 1, 1),
            end_date=date(2026, 3, 1),
            status=RotationAssignment.STATUS_ACTIVE,
            requested_by=self.admin,
        )
        file = _csv(
            "resident_email,hospital_code,department_code,start_date,end_date,status\n"
            "res_ra@test.com,AH-RA,MED-RA,2026-02-01,2026-04-01,ACTIVE\n"
        )
        result = import_entity(self.admin, "rotation-assignments", file, dry_run=True, allow_partial=True)
        self.assertEqual(len(result["failures"]), 1)
        self.assertIn("Overlapping", result["failures"][0]["error"])

    def test_missing_required_field_fails(self):
        file = _csv(
            "resident_email,hospital_code,department_code,start_date,end_date,status\n"
            ",AH-RA,MED-RA,2026-01-01,2026-02-01,DRAFT\n"
        )
        result = import_entity(self.admin, "rotation-assignments", file, dry_run=True, allow_partial=True)
        self.assertEqual(len(result["failures"]), 1)

    def test_invalid_status_defaults_to_draft(self):
        file = _csv(
            "resident_email,hospital_code,department_code,start_date,end_date,status\n"
            "res_ra@test.com,AH-RA,MED-RA,2026-01-01,2026-02-01,NOT_A_STATUS\n"
        )
        result = import_entity(self.admin, "rotation-assignments", file, dry_run=False, allow_partial=False)
        self.assertEqual(len(result["successes"]), 1)
        assignment = RotationAssignment.objects.get(resident_training=self.rtr)
        self.assertEqual(assignment.status, RotationAssignment.STATUS_DRAFT)

    def test_no_allow_partial_stops_on_first_failure(self):
        file = _csv(
            "resident_email,hospital_code,department_code,start_date,end_date,status\n"
            ",AH-RA,MED-RA,2026-01-01,2026-02-01,DRAFT\n"
            "res_ra@test.com,AH-RA,MED-RA,2026-03-01,2026-04-01,DRAFT\n"
        )
        result = import_entity(self.admin, "rotation-assignments", file, dry_run=True, allow_partial=False)
        self.assertEqual(len(result["failures"]), 1)
        self.assertEqual(len(result["successes"]), 0)


class ExportRowsForCoverageTests(TestCase):
    def setUp(self):
        self.hospital = Hospital.objects.create(name="Allied Hospital", code="AH-EX")
        self.dept = Department.objects.create(name="Medicine", code="MED-EX")
        self.hdept = HospitalDepartment.objects.create(hospital=self.hospital, department=self.dept, is_active=True)
        self.supervisor = User.objects.create_user(username="sup_ex", email="sup_ex@test.com", role="SUPERVISOR")
        self.resident = User.objects.create_user(username="res_ex", email="res_ex@test.com", role="RESIDENT")
        SupervisorProfile.objects.create(user=self.supervisor, hospital=self.hospital, department_ref=self.dept)
        ResidentProfile.objects.create(user=self.resident, hospital=self.hospital, department_ref=self.dept)
        self.program = TrainingProgram.objects.create(name="Medicine", code="MED-EX-PRG", duration_months=48)
        self.rtr = ResidentTrainingRecord.objects.create(
            resident_user=self.resident, program=self.program, start_date=date.today(), active=True
        )

    def test_export_supervision_links(self):
        create_supervisor_assignment(
            resident=self.resident.resident_profile,
            supervisor=self.supervisor.supervisor_profile,
            assignment_type=ResidentSupervisorAssignment.ASSIGNMENT_PRIMARY,
            start_date=date.today(),
            notes="test",
            actor=self.supervisor,
        )
        rows = export_rows_for("supervision-links")
        matching = [r for r in rows if r["supervisor_email"] == "sup_ex@test.com"]
        self.assertEqual(len(matching), 1)

    def test_export_rotation_assignments(self):
        RotationAssignment.objects.create(
            resident_training=self.rtr,
            hospital_department=self.hdept,
            start_date=date(2026, 1, 1),
            end_date=date(2026, 2, 1),
            status=RotationAssignment.STATUS_DRAFT,
            requested_by=self.supervisor,
        )
        rows = export_rows_for("rotation-assignments")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["resident_email"], "res_ex@test.com")

    def test_unsupported_export_resource_raises(self):
        with self.assertRaises(ValidationError):
            export_rows_for("not-a-resource")

    def test_unsupported_template_resource_raises(self):
        with self.assertRaises(ValidationError):
            template_rows_for("not-a-resource")


class HelperFunctionCoverageTests(TestCase):
    def setUp(self):
        self.dept = Department.objects.create(name="Medicine", code="MED-HF")
        self.hospital = Hospital.objects.create(name="Allied Hospital", code="AH-HF")

    def test_department_or_none_blank(self):
        self.assertIsNone(_department_or_none(""))
        self.assertIsNone(_department_or_none(None))

    def test_resolve_department_not_found_raises(self):
        with self.assertRaises(ValidationError):
            _resolve_department("NOPE")

    def test_resolve_hospital_department_requires_department(self):
        with self.assertRaises(ValidationError):
            _resolve_hospital_department(hospital_code="AH-HF", department=None)

    def test_resolve_hospital_department_unknown_hospital(self):
        with self.assertRaises(ValidationError):
            _resolve_hospital_department(hospital_code="NOPE", department=self.dept)

    def test_resolve_hospital_department_not_in_matrix(self):
        with self.assertRaises(ValidationError):
            _resolve_hospital_department(hospital_code="AH-HF", department=self.dept)

    def test_resolve_hospital_department_blank_code_returns_none(self):
        self.assertIsNone(_resolve_hospital_department(hospital_code="", department=self.dept))

    def test_normalize_staff_role_invalid(self):
        with self.assertRaises(ValidationError):
            _normalize_staff_role("nurse")
        self.assertEqual(_normalize_staff_role("faculty"), "SUPERVISOR")

    def test_normalize_resident_role_invalid(self):
        with self.assertRaises(ValidationError):
            _normalize_resident_role("nobody")
        self.assertEqual(_normalize_resident_role("pg"), "RESIDENT")

    def test_normalize_year_invalid(self):
        with self.assertRaises(ValidationError):
            _normalize_year("99")

    def test_parse_bool_invalid_raises(self):
        with self.assertRaises(ValidationError):
            _parse_bool("maybe", default=True)
        self.assertTrue(_parse_bool("", default=True))
        self.assertTrue(_parse_bool("yes", default=False))
        self.assertFalse(_parse_bool("no", default=True))

    def test_error_text_with_message_dict(self):
        exc = ValidationError({"field": ["bad value"]})
        text = _error_text(exc)
        self.assertIn("field", text)
        self.assertIn("bad value", text)

    def test_error_text_with_plain_message(self):
        exc = ValidationError("plain error")
        text = _error_text(exc)
        self.assertEqual(text, "plain error")
