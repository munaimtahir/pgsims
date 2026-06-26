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
from sims.users.models import (
    DataCorrectionAudit,
    DepartmentMembership,
    HODAssignment,
    ResidentProfile,
    SupervisorResidentLink,
    User,
)


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

    def test_utrmc_admin_org_graph_routes_cover_roster_and_matrix_actions(self):
        DepartmentMembership.objects.create(
            user=self.faculty,
            department=self.department,
            member_type="faculty",
            is_primary=True,
            start_date=date.today(),
            active=True,
            created_by=self.utrmc_admin,
            updated_by=self.utrmc_admin,
        )
        DepartmentMembership.objects.create(
            user=self.resident,
            department=self.department,
            member_type="resident",
            is_primary=True,
            start_date=date.today(),
            active=True,
            created_by=self.utrmc_admin,
            updated_by=self.utrmc_admin,
        )

        self.client.force_authenticate(self.utrmc_admin)
        roster = self.client.get(f"/api/departments/{self.department.id}/roster/")
        self.assertEqual(roster.status_code, 200)
        self.assertEqual(roster.data["department"]["id"], self.department.id)
        self.assertEqual(roster.data["faculty"][0]["id"], self.faculty.id)
        self.assertEqual(roster.data["residents"][0]["id"], self.resident.id)

        hospital_departments = self.client.get(f"/api/hospitals/{self.hospital.id}/departments/")
        self.assertEqual(hospital_departments.status_code, 200)
        self.assertEqual(hospital_departments.data[0]["department"]["id"], self.department.id)

        hod = self.client.post(
            "/api/hod-assignments/",
            {
                "department_id": self.department.id,
                "hod_user_id": self.supervisor.id,
                "start_date": date.today().isoformat(),
                "active": True,
            },
            format="json",
        )
        self.assertEqual(hod.status_code, 201)
        self.assertEqual(hod.data["department"]["id"], self.department.id)
        self.assertEqual(hod.data["hod_user"]["id"], self.supervisor.id)

        inactive_matrix = HospitalDepartment.objects.create(
            hospital=Hospital.objects.create(name="Secondary Userbase", code="HOSP-UB2"),
            department=self.department,
            is_active=False,
        )
        matrix_update = self.client.patch(
            f"/api/hospital-departments/{inactive_matrix.id}/",
            {"active": True},
            format="json",
        )
        self.assertEqual(matrix_update.status_code, 200)
        self.assertTrue(matrix_update.data["active"])

    def test_utrmc_user_is_read_only_on_org_graph_mutations(self):
        utrmc_user = User.objects.create_user(
            username="utrmc_user_readonly",
            password="pass12345",
            role="utrmc_user",
            email="utrmc_user_readonly@example.com",
        )

        self.client.force_authenticate(utrmc_user)
        roster = self.client.get(f"/api/departments/{self.department.id}/roster/")
        self.assertEqual(roster.status_code, 200)

        blocked_hod = self.client.post(
            "/api/hod-assignments/",
            {
                "department_id": self.department.id,
                "hod_user_id": self.supervisor.id,
                "start_date": date.today().isoformat(),
                "active": True,
            },
            format="json",
        )
        self.assertEqual(blocked_hod.status_code, 403)

        blocked_link = self.client.post(
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
        self.assertEqual(blocked_link.status_code, 403)

        blocked_matrix = self.client.patch(
            f"/api/hospital-departments/{self.hospital_department.id}/",
            {"active": False},
            format="json",
        )
        self.assertEqual(blocked_matrix.status_code, 403)

        blocked_user = self.client.post(
            "/api/users/",
            {
                "username": "readonly_created_user",
                "email": "readonly_created_user@example.com",
                "password": "Pass123456!",
                "first_name": "Read",
                "last_name": "Only",
                "role": "resident",
            },
            format="json",
        )
        self.assertEqual(blocked_user.status_code, 403)


class UserbaseReadScopeTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(
            username="scope_admin",
            password="pass12345",
            role="admin",
            email="scope_admin@example.com",
        )
        self.supervisor = User.objects.create_user(
            username="scope_supervisor",
            password="pass12345",
            role="supervisor",
            specialty="medicine",
            email="scope_supervisor@example.com",
        )
        self.other_user = User.objects.create_user(
            username="scope_other",
            password="pass12345",
            role="resident",
            specialty="medicine",
            year="1",
            email="scope_other@example.com",
        )

    def _rows(self, response):
        return response.data if isinstance(response.data, list) else response.data.get("results", [])

    def test_supervisor_get_users_list_returns_only_self(self):
        self.client.force_authenticate(self.supervisor)
        response = self.client.get("/api/users/")
        self.assertEqual(response.status_code, 200)

        rows = self._rows(response)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["id"], self.supervisor.id)
        self.assertEqual(rows[0]["username"], self.supervisor.username)

    def test_supervisor_can_retrieve_self_but_not_other_users(self):
        self.client.force_authenticate(self.supervisor)

        own_response = self.client.get(f"/api/users/{self.supervisor.id}/")
        self.assertEqual(own_response.status_code, 200)
        self.assertEqual(own_response.data["id"], self.supervisor.id)

        blocked_response = self.client.get(f"/api/users/{self.other_user.id}/")
        self.assertEqual(blocked_response.status_code, 404)


class UserbaseFilterTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(
            username="filter_admin",
            password="pass12345",
            role="admin",
            email="filter_admin@example.com",
        )
        self.urology = Department.objects.create(name="Urology Userbase", code="URO-UB")
        self.medicine = Department.objects.create(name="Medicine Userbase 2", code="MED-UB2")
        self.complete_resident = User.objects.create_user(
            username="complete_resident",
            password="pass12345",
            role="resident",
            specialty="urology",
            year="1",
            email="complete_resident@example.com",
            is_complete_profile=True,
        )
        self.incomplete_resident = User.objects.create_user(
            username="incomplete_resident",
            password="pass12345",
            role="resident",
            specialty="urology",
            year="1",
            email="incomplete_resident@example.com",
            is_complete_profile=False,
        )
        DepartmentMembership.objects.create(
            user=self.complete_resident,
            department=self.urology,
            member_type=DepartmentMembership.MEMBER_RESIDENT,
            is_primary=True,
            active=True,
            start_date=date.today(),
            created_by=self.admin,
            updated_by=self.admin,
        )
        DepartmentMembership.objects.create(
            user=self.incomplete_resident,
            department=self.medicine,
            member_type=DepartmentMembership.MEMBER_RESIDENT,
            is_primary=True,
            active=True,
            start_date=date.today(),
            created_by=self.admin,
            updated_by=self.admin,
        )

    def _rows(self, response):
        return response.data if isinstance(response.data, list) else response.data.get("results", [])

    def test_admin_can_filter_users_by_department_active_and_completion(self):
        self.client.force_authenticate(self.admin)
        response = self.client.get(
            "/api/users/",
            {
                "role": "resident",
                "department": self.urology.id,
                "active": "true",
                "is_complete_profile": "true",
            },
        )
        self.assertEqual(response.status_code, 200)

        rows = self._rows(response)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["id"], self.complete_resident.id)
        self.assertTrue(rows[0]["is_complete_profile"])
        self.assertEqual(rows[0]["departments"][0]["code"], self.urology.code)


class UserbaseAccountActionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(
            username="action_admin",
            password="pass12345",
            role="admin",
            email="action_admin@example.com",
        )
        self.supervisor = User.objects.create_user(
            username="action_supervisor",
            password="pass12345",
            role="supervisor",
            specialty="medicine",
            email="action_supervisor@example.com",
        )
        self.department = Department.objects.create(name="Action Medicine", code="ACT-MED")
        self.program = TrainingProgram.objects.create(
            name="Action Program",
            code="ACT-PROG",
            duration_months=60,
            degree_type=TrainingProgram.DEGREE_FCPS,
            department=self.department,
            active=True,
        )
        self.resident = User.objects.create_user(
            username="action_resident",
            password="pass12345",
            role="resident",
            specialty="urology",
            year="1",
            email="action_resident@example.com",
            supervisor=self.supervisor,
            home_department=self.department,
        )
        DepartmentMembership.objects.create(
            user=self.resident,
            department=self.department,
            member_type=DepartmentMembership.MEMBER_RESIDENT,
            is_primary=True,
            active=True,
            start_date=date.today(),
            created_by=self.admin,
            updated_by=self.admin,
        )
        ResidentProfile.objects.create(
            user=self.resident,
            pgr_id="ACT-001",
            program_name=self.program.name,
            training_year="1",
            training_start=date.today(),
            active=True,
        )
        ResidentTrainingRecord.objects.create(
            resident_user=self.resident,
            program=self.program,
            start_date=date.today(),
            current_level="y1",
            active=True,
            created_by=self.admin,
        )

    def test_admin_can_filter_users_by_supervisor_and_program(self):
        self.client.force_authenticate(self.admin)
        response = self.client.get(
            "/api/users/",
            {
                "supervisor": self.supervisor.id,
                "program": self.program.id,
                "role": "resident",
            },
        )
        self.assertEqual(response.status_code, 200)
        rows = response.data if isinstance(response.data, list) else response.data.get("results", [])
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["id"], self.resident.id)

    def test_admin_reset_deactivate_and_archive_user(self):
        self.client.force_authenticate(self.admin)
        reset_response = self.client.post(
            f"/api/users/{self.resident.id}/reset-password/",
            {"password": "pgfmu123"},
            format="json",
        )
        self.assertEqual(reset_response.status_code, 200)

        self.resident.refresh_from_db()
        self.assertTrue(self.resident.check_password("pgfmu123"))
        self.assertTrue(self.resident.force_password_change)

        deactivate_response = self.client.post(f"/api/users/{self.resident.id}/deactivate/", format="json")
        self.assertEqual(deactivate_response.status_code, 200)
        self.resident.refresh_from_db()
        self.assertFalse(self.resident.is_active)

        archive_response = self.client.delete(f"/api/users/{self.resident.id}/")
        self.assertEqual(archive_response.status_code, 200)
        self.resident.refresh_from_db()
        self.assertTrue(self.resident.is_archived)



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

    def test_resident_without_training_record_or_supervisor_link_is_incomplete(self):
        # Create a new resident user with profile, but no training record or links
        resident = User.objects.create_user(
            username="dq_resident_bare",
            password="pass12345",
            role="resident",
            email="dq_resident_bare@example.com",
            year="1",
            specialty="medicine",
        )
        ResidentProfile.objects.create(
            user=resident,
            pgr_id="DQ-BARE-001",
            training_start=date(2026, 5, 1),
            training_level="y1",
            active=True,
        )
        
        # Recompute flags
        recompute_flags_for_user(resident)
        
        # Verify it has issues and is marked incomplete
        self.assertFalse(resident.is_complete_profile)
        self.assertIn("missing_training_dates", resident.data_issues)
        self.assertIn("missing_supervision_dates", resident.data_issues)

    def test_training_record_issues_propagate_to_user_issues(self):
        # Create a resident with a training record that has specific issues like missing current_level
        resident = User.objects.create_user(
            username="dq_resident_issue",
            password="pass12345",
            role="resident",
            email="dq_resident_issue@example.com",
            year="1",
            specialty="medicine",
        )
        ResidentProfile.objects.create(
            user=resident,
            pgr_id="DQ-ISSUE-001",
            training_start=date(2026, 5, 1),
            training_level="y1",
            active=True,
        )
        program = TrainingProgram.objects.create(name="DQ Issue Program", code="DQP-ISSUE", duration_months=60)
        # Training record missing current_level
        ResidentTrainingRecord.objects.create(
            resident_user=resident,
            program=program,
            start_date=date(2026, 5, 1),
            current_level="",
            active=True,
        )
        # Add a valid supervision link so that missing supervision link is not the only issue
        SupervisorResidentLink.objects.create(
            supervisor_user=self.supervisor,
            resident_user=resident,
            department=self.department,
            start_date=date(2026, 5, 1),
            active=True,
        )

        # Recompute flags
        recompute_flags_for_user(resident)

        # Verify missing_current_level propagates to the user's data_issues
        self.assertFalse(resident.is_complete_profile)
        self.assertIn("missing_current_level", resident.data_issues)


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
