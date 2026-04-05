from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIClient

from sims.academics.models import Department
from sims.bulk.models import BulkOperation
from sims.rotations.models import Hospital, HospitalDepartment
from sims.users.models import (
    DepartmentMembership,
    HODAssignment,
    HospitalAssignment,
    ResidentProfile,
    StaffProfile,
    SupervisorResidentLink,
    User,
)


class ActiveUserbaseBulkEngineTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(
            username="bulk_admin",
            password="pass12345",
            role="admin",
            email="bulk_admin@example.com",
        )
        self.utrmc_admin = User.objects.create_user(
            username="bulk_utrmc_admin",
            password="pass12345",
            role="utrmc_admin",
            email="bulk_utrmc_admin@example.com",
        )
        self.pg = User.objects.create_user(
            username="bulk_pg",
            password="pass12345",
            role="pg",
            email="bulk_pg@example.com",
            specialty="medicine",
            year="1",
        )

    def _upload(self, name: str, content: str):
        return SimpleUploadedFile(name, content.encode("utf-8"), content_type="text/csv")

    def test_bulk_operation_model_tracking_still_works(self):
        operation = BulkOperation.objects.create(user=self.admin, operation=BulkOperation.OP_IMPORT)
        operation.mark_completed(success_count=2, failure_count=1, details={"ok": True})
        operation.refresh_from_db()
        self.assertEqual(operation.status, BulkOperation.STATUS_COMPLETED)
        self.assertEqual(operation.total_items, 3)

    def test_admin_can_download_hospital_template(self):
        self.client.force_authenticate(self.admin)
        response = self.client.get("/api/bulk/templates/hospitals/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("hospital_code,hospital_name,address,phone,email,active", response.content.decode("utf-8"))

    def test_pg_cannot_use_active_bulk_surface(self):
        self.client.force_authenticate(self.pg)
        template_response = self.client.get("/api/bulk/templates/hospitals/")
        export_response = self.client.get("/api/bulk/exports/hospitals/")
        import_response = self.client.post(
            "/api/bulk/import/hospitals/dry-run/",
            {"file": self._upload("hospitals.csv", "hospital_code,hospital_name\nAH,Allied Hospital\n")},
            format="multipart",
        )
        self.assertEqual(template_response.status_code, 403)
        self.assertEqual(export_response.status_code, 403)
        self.assertEqual(import_response.status_code, 403)

    def test_utrmc_admin_can_import_hospitals_departments_and_matrix(self):
        self.client.force_authenticate(self.utrmc_admin)

        hospitals_response = self.client.post(
            "/api/bulk/import/hospitals/apply/",
            {
                "file": self._upload(
                    "hospitals.csv",
                    "hospital_code,hospital_name,address,phone,email,active\nAH,Allied Hospital,Faisalabad,0410000000,ah@example.com,true\n",
                )
            },
            format="multipart",
        )
        departments_response = self.client.post(
            "/api/bulk/import/departments/apply/",
            {
                "file": self._upload(
                    "departments.csv",
                    "department_code,department_name,description,active\nMED,Internal Medicine,Core department,true\n",
                )
            },
            format="multipart",
        )
        matrix_response = self.client.post(
            "/api/bulk/import/matrix/apply/",
            {
                "file": self._upload(
                    "matrix.csv",
                    "hospital_code,department_code,active\nAH,MED,true\n",
                )
            },
            format="multipart",
        )

        self.assertEqual(hospitals_response.status_code, 200)
        self.assertEqual(departments_response.status_code, 200)
        self.assertEqual(matrix_response.status_code, 200)
        self.assertTrue(Hospital.objects.filter(code="AH").exists())
        self.assertTrue(Department.objects.filter(code="MED").exists())
        self.assertTrue(HospitalDepartment.objects.filter(hospital__code="AH", department__code="MED").exists())

    def test_bulk_export_hospitals_matches_active_schema(self):
        Hospital.objects.create(name="Allied Hospital", code="AH", is_active=True, address="Faisalabad")
        self.client.force_authenticate(self.admin)
        response = self.client.get("/api/bulk/exports/hospitals/?file_format=csv")
        self.assertEqual(response.status_code, 200)
        body = response.content.decode("utf-8")
        self.assertIn("hospital_code,hospital_name,address,phone,email,active", body)
        self.assertIn("AH,Allied Hospital,Faisalabad", body)

    def test_bulk_import_faculty_supervisors_creates_profiles_and_memberships(self):
        hospital = Hospital.objects.create(name="Allied Hospital", code="AH", is_active=True)
        department = Department.objects.create(name="Internal Medicine", code="MED")
        HospitalDepartment.objects.create(hospital=hospital, department=department, is_active=True)

        self.client.force_authenticate(self.admin)
        response = self.client.post(
            "/api/bulk/import/faculty-supervisors/apply/",
            {
                "file": self._upload(
                    "faculty_supervisors.csv",
                    "\n".join(
                        [
                            "email,full_name,phone_number,role,specialty,department_code,hospital_code,designation,registration_number,username,password,active,start_date",
                            "supervisor@example.com,Dr Jane Supervisor,03001234567,supervisor,medicine,MED,AH,Consultant,PMC-12345,jane.supervisor,,true,2026-01-01",
                        ]
                    ),
                )
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, 200)
        user = User.objects.get(email="supervisor@example.com")
        self.assertEqual(user.role, "supervisor")
        self.assertTrue(StaffProfile.objects.filter(user=user, designation="Consultant").exists())
        self.assertTrue(
            DepartmentMembership.objects.filter(
                user=user,
                department=department,
                member_type=DepartmentMembership.MEMBER_SUPERVISOR,
                is_primary=True,
                active=True,
            ).exists()
        )
        self.assertTrue(
            HospitalAssignment.objects.filter(
                user=user,
                hospital_department__hospital=hospital,
                assignment_type=HospitalAssignment.ASSIGNMENT_FACULTY_SITE,
                active=True,
            ).exists()
        )

    def test_bulk_import_residents_creates_profiles_memberships_and_sites(self):
        hospital = Hospital.objects.create(name="Allied Hospital", code="AH", is_active=True)
        department = Department.objects.create(name="Internal Medicine", code="MED")
        hospital_department = HospitalDepartment.objects.create(hospital=hospital, department=department, is_active=True)
        supervisor = User.objects.create_user(
            username="existing.supervisor",
            password="pass12345",
            role="supervisor",
            email="supervisor@example.com",
            specialty="medicine",
        )

        self.client.force_authenticate(self.admin)
        response = self.client.post(
            "/api/bulk/import/residents/apply/",
            {
                "file": self._upload(
                    "residents.csv",
                    "\n".join(
                        [
                            "email,full_name,phone_number,role,specialty,year,pgr_id,training_start,training_end,training_level,department_code,hospital_code,supervisor_email,username,password,active",
                            "resident@example.com,Dr Ali Resident,03009876543,resident,medicine,1,PGR001,2026-01-01,,Y1,MED,AH,supervisor@example.com,ali.resident,,true",
                        ]
                    ),
                )
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, 200)
        user = User.objects.get(email="resident@example.com")
        self.assertEqual(user.role, "resident")
        self.assertEqual(user.home_department, department)
        self.assertEqual(user.home_hospital, hospital)
        self.assertEqual(user.supervisor, supervisor)
        self.assertTrue(
            ResidentProfile.objects.filter(
                user=user,
                pgr_id="PGR001",
                training_start="2026-01-01",
                training_level="Y1",
                active=True,
            ).exists()
        )
        self.assertTrue(
            DepartmentMembership.objects.filter(
                user=user,
                department=department,
                member_type=DepartmentMembership.MEMBER_RESIDENT,
                is_primary=True,
                active=True,
            ).exists()
        )
        self.assertTrue(
            HospitalAssignment.objects.filter(
                user=user,
                hospital_department=hospital_department,
                assignment_type=HospitalAssignment.ASSIGNMENT_PRIMARY_TRAINING,
                active=True,
            ).exists()
        )

    def test_bulk_import_supervision_and_hod_assignments_close_prerequisite_chain(self):
        department = Department.objects.create(name="Internal Medicine", code="MED")
        supervisor = User.objects.create_user(
            username="faculty.supervisor",
            password="pass12345",
            role="faculty",
            email="faculty@example.com",
        )
        resident = User.objects.create_user(
            username="resident.user",
            password="pass12345",
            role="resident",
            email="resident@example.com",
            specialty="medicine",
            year="1",
        )

        self.client.force_authenticate(self.admin)
        links_response = self.client.post(
            "/api/bulk/import/supervision-links/apply/",
            {
                "file": self._upload(
                    "supervision_links.csv",
                    "supervisor_email,resident_email,department_code,start_date,end_date,active\nfaculty@example.com,resident@example.com,MED,2026-01-01,,true\n",
                )
            },
            format="multipart",
        )
        hod_response = self.client.post(
            "/api/bulk/import/hod-assignments/apply/",
            {
                "file": self._upload(
                    "hod_assignments.csv",
                    "department_code,hod_email,start_date,end_date,active\nMED,faculty@example.com,2026-01-01,,true\n",
                )
            },
            format="multipart",
        )

        self.assertEqual(links_response.status_code, 200)
        self.assertEqual(hod_response.status_code, 200)
        self.assertTrue(
            SupervisorResidentLink.objects.filter(
                supervisor_user=supervisor,
                resident_user=resident,
                department=department,
                active=True,
            ).exists()
        )
        self.assertTrue(
            HODAssignment.objects.filter(
                department=department,
                hod_user=supervisor,
                active=True,
            ).exists()
        )

    def test_dry_run_reports_missing_prerequisite_without_writing(self):
        self.client.force_authenticate(self.admin)
        response = self.client.post(
            "/api/bulk/import/matrix/dry-run/",
            {
                "file": self._upload(
                    "matrix.csv",
                    "hospital_code,department_code,active\nAH,MED,true\n",
                )
            },
            format="multipart",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["success_count"], 0)
        self.assertEqual(response.data["failure_count"], 1)
        self.assertFalse(HospitalDepartment.objects.exists())
