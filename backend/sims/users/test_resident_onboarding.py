from io import BytesIO

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from openpyxl import Workbook
from rest_framework.test import APIClient

from sims.academics.models import Department
from sims.rotations.models import Hospital, HospitalDepartment
from sims.training.models import TrainingProgram
from sims.users.models import DepartmentMembership, OnboardingImportBatch, ResidentProfile

UserModel = get_user_model()


def _xlsx_file(headers, rows, filename="resident_onboarding.xlsx"):
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(headers)
    for row in rows:
        sheet.append(row)
    buffer = BytesIO()
    workbook.save(buffer)
    return SimpleUploadedFile(
        filename,
        buffer.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


class ResidentOnboardingFlowTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = UserModel.objects.create_user(
            username="admin-onboarding",
            password="pass12345",
            role="admin",
            email="admin@example.com",
        )
        self.department = Department.objects.create(name="Urology", code="URO")
        self.hospital = Hospital.objects.create(name="FMU Hospital", code="FMU")
        HospitalDepartment.objects.create(hospital=self.hospital, department=self.department, is_active=True)
        self.program = TrainingProgram.objects.create(
            name="FCPS",
            code="FCPS-URO",
            duration_months=60,
            degree_type=TrainingProgram.DEGREE_FCPS,
            department=self.department,
            active=True,
        )
        self.supervisor = UserModel.objects.create_user(
            username="supervisor-onboarding",
            password="pass12345",
            role="supervisor",
            first_name="Dr",
            last_name="Supervisor",
            email="supervisor@example.com",
        )
        self.existing = UserModel.objects.create_user(
            username="resident-existing",
            password="pass12345",
            role="resident",
            first_name="Ali",
            last_name="Khan",
            email="ali@example.com",
            cnic="12345-1234567-1",
            phone_number="03001234567",
            home_department=self.department,
        )
        DepartmentMembership.objects.create(
            user=self.existing,
            department=self.department,
            member_type=DepartmentMembership.MEMBER_RESIDENT,
            is_primary=True,
            start_date="2026-01-01",
            created_by=self.admin,
            updated_by=self.admin,
        )
        ResidentProfile.objects.create(
            user=self.existing,
            training_start="2026-01-01",
            training_end=None,
            training_level="y1",
            pgr_id="",
            program_name="FCPS",
            training_year="1",
            joining_date="2026-01-01",
            profile_completed=True,
            login_generated=True,
            login_issued=True,
        )
        UserModel.objects.create_user(
            username="pgr001",
            password="pass12345",
            role="resident",
            email="seed@example.com",
        )

        self.client.force_authenticate(self.admin)

    def _mapping(self):
        return {
            "resident_name": "Name",
            "father_name": "Father",
            "department": "Dept",
            "program_name": "Program",
            "training_year": "Year",
            "supervisor_name": "Supervisor",
            "mobile_number": "Mobile",
            "email": "Email",
            "cnic": "CNIC",
            "registration_number": "PMDC",
            "joining_date": "Joining Date",
        }

    def _upload(self):
        headers = [
            "Name",
            "Father",
            "Dept",
            "Program",
            "Year",
            "Supervisor",
            "Mobile",
            "Email",
            "CNIC",
            "PMDC",
            "Joining Date",
            "Ignored Extra",
        ]
        rows = [
            [
                "Sara Iqbal",
                "Iqbal",
                "Urology",
                "FCPS",
                "1",
                "supervisor@example.com",
                "03011111111",
                "sara@example.com",
                "12345-7654321-2",
                "PMC-01",
                "2026-02-01",
                "skip",
            ],
            [
                "",
                "No Name",
                "Urology",
                "FCPS",
                "1",
                "supervisor@example.com",
                "03022222222",
                "invalid-email",
                "12345-7654321-3",
                "PMC-02",
                "2026-02-02",
                "skip",
            ],
            [
                "Ali Khan",
                "Same",
                "Urology",
                "FCPS",
                "1",
                "supervisor@example.com",
                "03001234567",
                "ali.dup@example.com",
                "12345-1234567-1",
                "PMC-03",
                "2026-02-03",
                "skip",
            ],
        ]
        uploaded = _xlsx_file(headers, rows)
        response = self.client.post("/api/onboarding/residents/upload-preview/", {"file": uploaded}, format="multipart")
        self.assertEqual(response.status_code, 200)
        return response.data

    def test_upload_preview_and_mapping_generate_expected_row_statuses(self):
        upload = self._upload()
        self.assertEqual(upload["headers"][0], "Name")
        self.assertEqual(upload["total_rows"], 3)
        self.assertIn("resident_name", upload["suggested_mapping"])

        response = self.client.post(
            "/api/onboarding/residents/map-columns/",
            {"batch_id": upload["batch_id"], "mapping": self._mapping()},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        statuses = [row["status"] for row in response.data["preview_rows"]]
        self.assertEqual(statuses.count("Ready"), 1)
        self.assertEqual(statuses.count("Error"), 1)
        self.assertEqual(statuses.count("Possible Duplicate"), 1)

    def test_optional_email_is_not_required_and_unknown_mapping_header_is_rejected(self):
        response = self.client.post(
            "/api/onboarding/residents/upload-preview/",
            {
                "file": _xlsx_file(
                    ["Name", "Dept"],
                    [["No Email Resident", "Urology"]],
                    filename="optional-email.xlsx",
                )
            },
            format="multipart",
        )
        self.assertEqual(response.status_code, 200)
        upload = response.data

        invalid_mapping = self.client.post(
            "/api/onboarding/residents/map-columns/",
            {
                "batch_id": upload["batch_id"],
                "mapping": {"resident_name": "Name", "department": "Missing Header"},
            },
            format="json",
        )
        self.assertEqual(invalid_mapping.status_code, 400)

        preview = self.client.post(
            "/api/onboarding/residents/map-columns/",
            {
                "batch_id": upload["batch_id"],
                "mapping": {"resident_name": "Name", "department": "Dept"},
            },
            format="json",
        )
        self.assertEqual(preview.status_code, 200)
        self.assertEqual(preview.data["preview_rows"][0]["status"], "Ready")

    def test_import_generates_profile_and_login_sequence_and_completion_flow(self):
        upload = self._upload()
        self.client.post(
            "/api/onboarding/residents/map-columns/",
            {"batch_id": upload["batch_id"], "mapping": self._mapping()},
            format="json",
        )

        import_response = self.client.post(
            "/api/onboarding/residents/import/",
            {"batch_id": upload["batch_id"]},
            format="json",
        )
        self.assertEqual(import_response.status_code, 200)
        self.assertEqual(import_response.data["imported_rows"], 1)

        resident = UserModel.objects.get(email="sara@example.com")
        profile = ResidentProfile.objects.get(user=resident)
        self.assertEqual(resident.role, "resident")
        self.assertEqual(resident.home_department, self.department)
        self.assertEqual(resident.home_hospital, self.hospital)
        self.assertEqual(resident.year, "1")
        self.assertTrue(resident.force_password_change)
        self.assertFalse(profile.profile_completed)
        self.assertFalse(profile.login_generated)

        self.client.force_authenticate(self.admin)
        login_response = self.client.post(
            "/api/onboarding/residents/generate-logins/",
            {"batch_id": upload["batch_id"]},
            format="json",
        )
        self.assertEqual(login_response.status_code, 200)
        self.assertEqual(login_response.data["generated"], 1)

        resident.refresh_from_db()
        profile.refresh_from_db()
        self.assertEqual(resident.username, "pgr002")
        self.assertTrue(resident.check_password("pgfmu123"))
        self.assertTrue(resident.force_password_change)
        self.assertTrue(profile.login_generated)

        repeated_login_response = self.client.post(
            "/api/onboarding/residents/generate-logins/",
            {"batch_id": upload["batch_id"]},
            format="json",
        )
        self.assertEqual(repeated_login_response.status_code, 200)
        self.assertEqual(repeated_login_response.data["generated"], 0)
        self.assertEqual(
            OnboardingImportBatch.objects.get(pk=upload["batch_id"]).logins_generated,
            1,
        )

        sheet_response = self.client.get("/api/onboarding/residents/login-sheet/")
        self.assertEqual(sheet_response.status_code, 200)
        self.assertEqual(sheet_response.data[0]["username"], "pgr002")
        self.assertEqual(sheet_response.data[0]["temporary_password"], "pgfmu123")

        self.client.force_authenticate(resident)
        status_response = self.client.get("/api/resident/me/profile-completion-status/")
        self.assertEqual(status_response.status_code, 200)
        self.assertTrue(status_response.data["needs_completion"])

        dashboard_response = self.client.get("/api/dashboard/resident/")
        self.assertEqual(dashboard_response.status_code, 403)

        complete_response = self.client.post(
            "/api/resident/complete-profile/",
            {
                "new_password": "NewPass123!",
                "confirm_new_password": "NewPass123!",
                "mobile_number": "03009998888",
                "email": "sara.updated@example.com",
                "cnic": "12345-7654321-2",
                "program": "FCPS",
                "training_year": "2",
                "joining_date": "2026-02-04",
            },
            format="json",
        )
        self.assertEqual(complete_response.status_code, 200)

        resident.refresh_from_db()
        profile.refresh_from_db()
        self.assertTrue(profile.profile_completed)
        self.assertFalse(resident.force_password_change)
        self.assertTrue(resident.is_complete_profile)
        self.assertTrue(profile.first_login_completed_at is not None)
        self.assertTrue(profile.profile_completed_at is not None)
        self.assertTrue(resident.check_password("NewPass123!"))

        dashboard_response = self.client.get("/api/dashboard/resident/")
        self.assertEqual(dashboard_response.status_code, 200)

    def test_profile_status_and_completion_support_existing_resident_without_profile(self):
        resident = UserModel.objects.create_user(
            username="legacy-resident",
            password="pass12345",
            role="resident",
            email="legacy@example.com",
            home_department=self.department,
            force_password_change=True,
        )
        self.client.force_authenticate(resident)

        status_response = self.client.get("/api/resident/me/profile-completion-status/")
        self.assertEqual(status_response.status_code, 200)
        self.assertTrue(status_response.data["needs_completion"])
        self.assertFalse(status_response.data["profile_completed"])

        complete_response = self.client.post(
            "/api/resident/complete-profile/",
            {
                "new_password": "LegacyPass123!",
                "confirm_new_password": "LegacyPass123!",
                "mobile_number": "03005555555",
                "email": "legacy.updated@example.com",
                "cnic": "12345-5555555-5",
                "program": "FCPS",
                "training_year": "1",
                "joining_date": "2026-02-05",
            },
            format="json",
        )
        self.assertEqual(complete_response.status_code, 200)
        self.assertTrue(ResidentProfile.objects.get(user=resident).profile_completed)

    def test_completion_does_not_create_profile_before_validation_passes(self):
        resident = UserModel.objects.create_user(
            username="atomic-resident",
            password="pass12345",
            role="resident",
            email="atomic@example.com",
            home_department=self.department,
            home_hospital=self.hospital,
            year="1",
            force_password_change=True,
        )
        self.client.force_authenticate(resident)

        self.assertFalse(ResidentProfile.objects.filter(user=resident).exists())

        response = self.client.post(
            "/api/resident/complete-profile/",
            {
                "new_password": "AtomicPass123!",
                "confirm_new_password": "Mismatch123!",
                "mobile_number": "03004444444",
                "email": "atomic.updated@example.com",
                "cnic": "12345-4444444-4",
                "program": "FCPS",
                "training_year": "1",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertFalse(ResidentProfile.objects.filter(user=resident).exists())
        resident.refresh_from_db()
        self.assertTrue(resident.force_password_change)
        self.assertEqual(resident.email, "atomic@example.com")

    def test_batches_and_incomplete_profile_views_are_visible(self):
        upload = self._upload()
        self.client.post(
            "/api/onboarding/residents/map-columns/",
            {"batch_id": upload["batch_id"], "mapping": self._mapping()},
            format="json",
        )
        self.client.post("/api/onboarding/residents/import/", {"batch_id": upload["batch_id"]}, format="json")

        batches = self.client.get("/api/onboarding/residents/batches/")
        self.assertEqual(batches.status_code, 200)
        self.assertEqual(batches.data[0]["file_name"], upload["file_name"])

        incomplete = self.client.get("/api/onboarding/residents/incomplete-profiles/")
        self.assertEqual(incomplete.status_code, 200)
        self.assertGreaterEqual(len(incomplete.data), 1)

        batch_error_report = self.client.get(f"/api/onboarding/residents/batches/{upload['batch_id']}/error-report/")
        self.assertEqual(batch_error_report.status_code, 200)

        login_export = self.client.get(f"/api/onboarding/residents/batches/{upload['batch_id']}/login-sheet/export/")
        self.assertEqual(login_export.status_code, 200)

    def test_mark_issued_and_reset_password_are_available_from_login_sheet(self):
        upload = self._upload()
        self.client.post(
            "/api/onboarding/residents/map-columns/",
            {"batch_id": upload["batch_id"], "mapping": self._mapping()},
            format="json",
        )
        self.client.post("/api/onboarding/residents/import/", {"batch_id": upload["batch_id"]}, format="json")
        self.client.post("/api/onboarding/residents/generate-logins/", {"batch_id": upload["batch_id"]}, format="json")

        resident = UserModel.objects.get(email="sara@example.com")
        self.assertTrue(resident.force_password_change)
        resident.force_password_change = True
        resident.save(update_fields=["force_password_change"])

        issue_response = self.client.post(
            "/api/onboarding/residents/mark-issued/",
            {"resident_ids": [resident.id]},
            format="json",
        )
        self.assertEqual(issue_response.status_code, 200)

        resident.refresh_from_db()
        profile = ResidentProfile.objects.get(user=resident)
        self.assertTrue(profile.login_issued)
        self.assertIsNotNone(profile.login_issued_at)

        self.client.post(
            f"/api/onboarding/residents/{resident.id}/mark-profile-complete/",
            format="json",
        )
        resident.refresh_from_db()
        profile.refresh_from_db()
        self.assertTrue(profile.profile_completed)
        self.assertTrue(resident.force_password_change)

        reset_response = self.client.post(f"/api/onboarding/residents/{resident.id}/reset-password/", format="json")
        self.assertEqual(reset_response.status_code, 200)

        resident.refresh_from_db()
        self.assertTrue(resident.check_password("pgfmu123"))
        self.assertTrue(resident.force_password_change)
