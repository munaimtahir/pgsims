from datetime import date, timedelta

from django.conf import settings
from django.core.management import call_command
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from django.test.utils import override_settings
from rest_framework.test import APIClient

from sims.academics.models import Department
from sims.rotations.models import Hospital, HospitalDepartment
from sims.training.models import ResidentTrainingRecord, TrainingProgram
from sims.users.data_quality import recompute_flags_for_user
from sims.users.models import DataCorrectionAudit, HODAssignment, ResidentProfile, SupervisorResidentLink, User


class UserbasePermissionAndConstraintTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(
            username="admin_userbase",
            password="pass12345",
            role="admin",
            email="admin_userbase@example.com",
        )
        self.utrmc_admin = User.objects.create_user(
            username="utrmc_admin_userbase",
            password="pass12345",
            role="utrmc_admin",
            email="utrmc_admin_userbase@example.com",
        )
        self.supervisor = User.objects.create_user(
            username="supervisor_userbase",
            password="pass12345",
            role="supervisor",
            specialty="medicine",
            email="supervisor_userbase@example.com",
        )
        self.faculty = User.objects.create_user(
            username="faculty_userbase",
            password="pass12345",
            role="faculty",
            specialty="medicine",
            email="faculty_userbase@example.com",
        )
        self.resident = User.objects.create_user(
            username="resident_userbase",
            password="pass12345",
            role="resident",
            specialty="medicine",
            year="1",
            email="resident_userbase@example.com",
        )
        self.department = Department.objects.create(name="Medicine Userbase", code="MED-UB")
        self.hospital = Hospital.objects.create(name="Hospital Userbase", code="HOSP-UB")
        self.hospital_department = HospitalDepartment.objects.create(
            hospital=self.hospital,
            department=self.department,
        )

    def test_resident_cannot_create_departments(self):
        self.client.force_authenticate(self.resident)
        response = self.client.post(
            "/api/departments/",
            {"name": "Blocked Department", "code": "BLK", "active": True},
            format="json",
        )
        self.assertEqual(response.status_code, 403)

    def test_supervisor_cannot_create_users(self):
        self.client.force_authenticate(self.supervisor)
        response = self.client.post(
            "/api/users/",
            {
                "username": "blocked_user_create",
                "email": "blocked_user_create@example.com",
                "password": "Pass123456!",
                "first_name": "Blocked",
                "last_name": "User",
                "role": "resident",
                "specialty": "medicine",
                "year": "1",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 403)

    def test_utrmc_admin_can_create_supervision_link(self):
        self.client.force_authenticate(self.utrmc_admin)
        response = self.client.post(
            "/api/supervision-links/",
            {
                "supervisor_user_id": self.faculty.id,
                "resident_user_id": self.resident.id,
                "department_id": self.department.id,
                "start_date": date.today().isoformat(),
                "active": True,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["supervisor_user"]["id"], self.faculty.id)
        self.assertEqual(response.data["resident_user"]["id"], self.resident.id)

    def test_hod_assignment_allows_only_one_active_per_department(self):
        HODAssignment.objects.create(
            department=self.department,
            hod_user=self.faculty,
            start_date=date.today(),
            active=True,
            created_by=self.admin,
            updated_by=self.admin,
        )
        with self.assertRaises(ValidationError):
            HODAssignment.objects.create(
                department=self.department,
                hod_user=self.supervisor,
                start_date=date.today() + timedelta(days=1),
                active=True,
                created_by=self.admin,
                updated_by=self.admin,
            )

    def test_hospital_department_pair_is_unique(self):
        with self.assertRaises(IntegrityError):
            HospitalDepartment.objects.create(hospital=self.hospital, department=self.department)

    def test_supervision_link_role_constraints(self):
        with self.assertRaises(ValidationError):
            SupervisorResidentLink.objects.create(
                supervisor_user=self.resident,
                resident_user=self.supervisor,
                department=self.department,
                start_date=date.today(),
                active=True,
                created_by=self.admin,
                updated_by=self.admin,
            )


@override_settings(ENABLE_DATA_CORRECTION_LAYER=True)
class DataQualityAdminApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(
            username="dq_admin",
            password="pass12345",
            role="utrmc_admin",
            email="dq_admin@example.com",
            is_staff=True,
        )
        self.viewer = User.objects.create_user(
            username="dq_viewer",
            password="pass12345",
            role="utrmc_user",
            email="dq_viewer@example.com",
        )
        self.supervisor = User.objects.create_user(
            username="dq_supervisor",
            password="pass12345",
            role="supervisor",
            email="dq_supervisor@example.com",
            specialty="medicine",
        )
        self.resident = User.objects.create_user(
            username="dq_resident",
            password="pass12345",
            role="resident",
            email="dq_resident@pilot-placeholder.local",
            year="5",
            specialty="medicine",
            supervisor=self.supervisor,
        )
        self.department = Department.objects.create(name="DQ Medicine", code="MED-DQ")
        ResidentProfile.objects.create(
            user=self.resident,
            pgr_id="DQ-001",
            training_start=date(2026, 1, 1),
            training_level="y5",
            active=True,
        )
        SupervisorResidentLink.objects.create(
            supervisor_user=self.supervisor,
            resident_user=self.resident,
            department=self.department,
            start_date=date(2026, 1, 1),
            active=True,
            created_by=self.admin,
            updated_by=self.admin,
        )
        program = TrainingProgram.objects.create(name="DQ Program", code="DQP", duration_months=60)
        ResidentTrainingRecord.objects.create(
            resident_user=self.resident,
            program=program,
            start_date=date(2026, 1, 1),
            current_level="y5",
            active=True,
            created_by=self.admin,
        )
        recompute_flags_for_user(self.resident)

    def test_summary_and_users_require_admin(self):
        self.client.force_authenticate(self.viewer)
        denied = self.client.get("/api/admin/data-quality/summary")
        self.assertEqual(denied.status_code, 403)

        self.client.force_authenticate(self.admin)
        recompute = self.client.post("/api/admin/data-quality/recompute", {}, format="json")
        self.assertEqual(recompute.status_code, 200)
        summary = self.client.get("/api/admin/data-quality/summary")
        self.assertEqual(summary.status_code, 200)
        self.assertIn("total_users", summary.data)
        self.assertIn("users_with_placeholder_email", summary.data)

        users = self.client.get("/api/admin/data-quality/users", {"filter": "placeholder_email"})
        self.assertEqual(users.status_code, 200)
        self.assertEqual(len(users.data), 1)
        self.assertEqual(users.data[0]["id"], self.resident.id)

    def test_recompute_and_patch_generate_audit(self):
        self.client.force_authenticate(self.admin)
        response = self.client.post("/api/admin/data-quality/recompute", {}, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(response.data["total_users"], 1)

        patch_response = self.client.patch(
            f"/api/users/{self.resident.id}/",
            {"email": "resident.corrected@example.com"},
            format="json",
        )
        self.assertEqual(patch_response.status_code, 200)
        self.assertTrue(
            DataCorrectionAudit.objects.filter(
                entity_type="user",
                entity_id=str(self.resident.id),
                field_name="email",
            ).exists()
        )

        audit_response = self.client.get("/api/admin/data-quality/audit")
        self.assertEqual(audit_response.status_code, 200)
        self.assertGreaterEqual(len(audit_response.data), 1)


@override_settings(ENABLE_DATA_CORRECTION_LAYER=True)
class ImportCorrectionsCommandTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username="dq_admin_cmd",
            password="pass12345",
            role="admin",
            email="dq_admin_cmd@example.com",
            is_staff=True,
        )
        self.supervisor = User.objects.create_user(
            username="dq_sup_cmd",
            password="pass12345",
            role="supervisor",
            specialty="medicine",
            email="dq_sup_cmd@example.com",
        )
        self.resident = User.objects.create_user(
            username="dq_res_cmd",
            password="pass12345",
            role="resident",
            specialty="medicine",
            email="dq_res_cmd@pilot-placeholder.local",
            year="1",
            supervisor=self.supervisor,
        )
        ResidentProfile.objects.create(
            user=self.resident,
            pgr_id="DQ-CMD-1",
            training_start=date(2026, 1, 1),
            training_level="y1",
            active=True,
        )

    def test_dry_run_does_not_mutate(self):
        from pathlib import Path

        sample = Path(settings.BASE_DIR) / "tmp_corrections_dry_run.csv"
        sample.write_text(
            "resident_email,field_name,new_value\n"
            "dq_res_cmd@pilot-placeholder.local,email,resident.one@example.com\n",
            encoding="utf-8",
        )
        try:
            call_command("import_corrections_csv", str(sample))
            self.resident.refresh_from_db()
            self.assertEqual(self.resident.email, "dq_res_cmd@pilot-placeholder.local")
            self.assertFalse(DataCorrectionAudit.objects.exists())
        finally:
            if sample.exists():
                sample.unlink()

    def test_apply_updates_and_audits(self):
        from pathlib import Path

        sample = Path(settings.BASE_DIR) / "tmp_corrections_apply.csv"
        sample.write_text(
            "resident_email,field_name,new_value\n"
            "dq_res_cmd@pilot-placeholder.local,email,resident.two@example.com\n"
            "dq_res_cmd@pilot-placeholder.local,year,5\n",
            encoding="utf-8",
        )
        try:
            call_command(
                "import_corrections_csv",
                str(sample),
                "--apply",
                "--confirm",
                "--actor-username",
                self.admin.username,
            )
            self.resident.refresh_from_db()
            self.assertEqual(self.resident.email, "resident.two@example.com")
            self.assertEqual(self.resident.year, "5")
            self.assertGreaterEqual(DataCorrectionAudit.objects.count(), 2)
        finally:
            if sample.exists():
                sample.unlink()
