from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from sims.bulk.userbase_engine import (
    import_entity, parse_tabular_rows, _generate_username, _split_name, _normalize_specialty
)
from sims.academics.models import Department
from sims.rotations.models import Hospital, HospitalDepartment
from sims.supervision.models import ResidentSupervisorAssignment
from sims.users.models import ResidentProfile, SupervisorProfile
import io
import pandas as pd
from datetime import date

User = get_user_model()

class BulkUserbaseEngineExtendedTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username="engine_admin", role="ADMIN")
        self.hospital = Hospital.objects.create(name="H1", code="H1")
        self.dept = Department.objects.create(name="D1", code="D1")
        self.hdept = HospitalDepartment.objects.create(hospital=self.hospital, department=self.dept)
        self.resident = User.objects.create_user(username="res1", email="res1@test.com", role="RESIDENT")
        self.supervisor = User.objects.create_user(username="sup1", email="sup1@test.com", role="SUPERVISOR")
        ResidentProfile.objects.create(user=self.resident, hospital=self.hospital, department_ref=self.dept)
        SupervisorProfile.objects.create(user=self.supervisor, hospital=self.hospital, department_ref=self.dept)

    def test_split_name(self):
        self.assertEqual(_split_name("Dr. Jane Doe"), ("Jane", "Doe"))
        self.assertEqual(_split_name("Prof. John Smith"), ("John", "Smith"))
        self.assertEqual(_split_name("Alice"), ("Alice", ""))
        with self.assertRaises(ValidationError):
            _split_name("   ")

    def test_generate_username_collision(self):
        User.objects.create_user(username="jane.doe")
        new_username = _generate_username("Jane", "Doe")
        self.assertEqual(new_username, "jane.doe2")

    def test_import_faculty_supervisor_conflict_resolution(self):
        # Existing user with different data
        user = User.objects.create_user(
            username="jane.sup", email="jane@test.com", role="SUPERVISOR", specialty="surgery"
        )
        SupervisorProfile.objects.create(user=user, designation_ref="Junior")
        
        csv_content = "email,full_name,role,specialty,department_code,hospital_code,designation,active,start_date\n" \
                      "jane@test.com,Jane Supervisor,supervisor,medicine,D1,H1,Senior,true,2026-01-01\n"
        file = io.BytesIO(csv_content.encode('utf-8'))
        file.name = "sups.csv"
        
        result = import_entity(self.admin, "faculty-supervisors", file, dry_run=False, allow_partial=False)
        self.assertEqual(len(result["successes"]), 1)
        
        user.refresh_from_db()
        self.assertEqual(user.role, "SUPERVISOR")
        self.assertEqual(user.specialty, "medicine")
        self.assertEqual(user.supervisor_profile.designation_ref, "Senior")

    def test_import_residents_validation_errors(self):
        # Missing required training_start
        csv_content = "email,full_name,role,specialty,year,training_start,department_code,hospital_code\n" \
                      "res@test.com,Res,resident,medicine,1,,D1,H1\n"
        file = io.BytesIO(csv_content.encode('utf-8'))
        file.name = "res.csv"
        
        result = import_entity(self.admin, "residents", file, dry_run=False, allow_partial=True)
        self.assertEqual(len(result["failures"]), 1)
        self.assertIn("training_start is required", result["failures"][0]["error"])

    def test_import_matrix_missing_prerequisites(self):
        csv_content = "hospital_code,department_code,active\nMISSING_H,D1,true\n"
        file = io.BytesIO(csv_content.encode('utf-8'))
        file.name = "matrix.csv"
        
        result = import_entity(self.admin, "matrix", file, dry_run=False, allow_partial=True)
        self.assertEqual(len(result["failures"]), 1)
        self.assertIn("hospital 'MISSING_H'", result["failures"][0]["error"])

    def test_import_supervision_links(self):
        csv_content = "supervisor_email,resident_email,active\nsup1@test.com,res1@test.com,true\n"
        file = io.BytesIO(csv_content.encode('utf-8'))
        file.name = "links.csv"
        
        result = import_entity(self.admin, "supervision-links", file, dry_run=False, allow_partial=False)
        self.assertEqual(len(result["successes"]), 1)
        self.assertTrue(
            ResidentSupervisorAssignment.objects.filter(
                supervisor__user=self.supervisor,
                resident__user=self.resident,
                is_active=True,
            ).exists()
        )

    def test_excel_parsing(self):
        df = pd.DataFrame([
            {"hospital_code": "H2", "hospital_name": "Hospital Two", "active": "true"}
        ])
        excel_file = io.BytesIO()
        df.to_excel(excel_file, index=False)
        excel_file.name = "hospitals.xlsx"
        excel_file.seek(0)
        
        rows = parse_tabular_rows(excel_file)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["hospital_code"], "H2")

    def test_normalize_specialty(self):
        self.assertEqual(_normalize_specialty("Internal Medicine"), "medicine")
        self.assertEqual(_normalize_specialty("surgery"), "surgery")
        with self.assertRaises(ValidationError):
            _normalize_specialty("Alchemy")

    def test_import_unsupported_entity(self):
        with self.assertRaises(ValidationError):
            import_entity(self.admin, "ghosts", io.BytesIO(), dry_run=True, allow_partial=True)
