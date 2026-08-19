"""Additional coverage for sims.bulk.views: the review/assignment/logbook-import endpoints,
per-entity import endpoints, export/template permission checks, the unified import/<entity>/
endpoint, the flexible column-mapping import flow, and MappingPresetViewSet -- none of which had
any prior test coverage beyond the three happy-path cases in test_bulk_views.py.
"""

import io
import json
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.utils import timezone

from sims.academics.models import Department
from sims.bulk.models import MappingPreset
from sims.rotations.models import Hospital, HospitalDepartment
from sims.training.models import LogbookEntry, ResidentTrainingRecord, TrainingProgram

User = get_user_model()


def _csv_file(content: str, name: str = "upload.csv") -> io.BytesIO:
    file = io.BytesIO(content.encode("utf-8"))
    file.name = name
    return file


class BulkReviewAssignmentViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(username="admin_rv", password="pw", role="ADMIN")
        self.supervisor = User.objects.create_user(
            username="sup_rv", password="pw", role="SUPERVISOR", email="sup_rv@test.com"
        )
        self.pg = User.objects.create_user(
            username="pg_rv", password="pw", role="RESIDENT", email="pg_rv@test.com"
        )
        self.client.login(username="admin_rv", password="pw")
        self.program = TrainingProgram.objects.create(name="Medicine", code="MED-RV", duration_months=48)
        self.rtr = ResidentTrainingRecord.objects.create(
            resident_user=self.pg, program=self.program, start_date=date.today()
        )
        self.entry = LogbookEntry.objects.create(
            resident_training_record=self.rtr,
            patient_id_number="P-RV-1",
            patient_seen_at=timezone.now(),
            status="DRAFT",
        )

    def test_review_view_success(self):
        # BulkService.review_entries() previously crashed with ValueError on every call (see
        # test_bulk_services_coverage.py for full detail: it saved a nonexistent `verified_at`
        # field on sims.training.LogbookEntry). Now fixed to only update `status`.
        response = self.client.post(
            "/api/bulk/review/",
            data=json.dumps({"entry_ids": [self.entry.id], "status": "approved"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["success_count"], 1)

    def test_review_view_invalid_status_rejected_by_serializer(self):
        response = self.client.post(
            "/api/bulk/review/",
            data=json.dumps({"entry_ids": [self.entry.id], "status": "not-a-status"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_assignment_view_success(self):
        response = self.client.post(
            "/api/bulk/assignment/",
            data=json.dumps({"entry_ids": [self.entry.id], "supervisor_id": self.supervisor.id}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["success_count"], 1)

    def test_assignment_view_unknown_supervisor_404(self):
        response = self.client.post(
            "/api/bulk/assignment/",
            data=json.dumps({"entry_ids": [self.entry.id], "supervisor_id": 999999}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 404)


class BulkImportViewTests(TestCase):
    """Logbook import, trainee import, supervisor import, resident import endpoints."""

    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(username="admin_iv", password="pw", role="ADMIN")
        self.client.login(username="admin_iv", password="pw")
        self.pg = User.objects.create_user(
            username="pg_iv", password="pw", role="RESIDENT", email="pg_iv@test.com"
        )
        self.program = TrainingProgram.objects.create(name="Medicine", code="MED-IV", duration_months=48)
        ResidentTrainingRecord.objects.create(resident_user=self.pg, program=self.program, start_date=date.today())

    def test_logbook_import_success(self):
        file = _csv_file(
            f"pg_username,case_title,date,status\n{self.pg.username},Case 1,2026-01-01,submitted\n",
            "logbook.csv",
        )
        response = self.client.post("/api/bulk/import/", {"file": file, "dry_run": "false"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "completed")

    def test_logbook_import_bad_file_returns_400(self):
        file = _csv_file("wrong_col\nvalue\n", "logbook.csv")
        response = self.client.post("/api/bulk/import/", {"file": file, "dry_run": "true"})
        self.assertEqual(response.status_code, 400)

    def test_trainee_import_success(self):
        file = _csv_file(
            "Name of Trainee,Date of Joining,Supervisor Name\nJane Trainee,2026-01-01,Dr. Mentor\n",
            "trainees.csv",
        )
        response = self.client.post("/api/bulk/import-trainees/", {"file": file, "dry_run": "false"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "completed")

    def test_supervisor_import_success(self):
        file = _csv_file(
            "Name,Email,Specialty\nDr. New Sup,newsup_iv@test.com,urology\n",
            "sups.csv",
        )
        response = self.client.post("/api/bulk/import-supervisors/", {"file": file, "dry_run": "false"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["success_count"], 1)

    def test_resident_import_success(self):
        supervisor = User.objects.create_user(
            username="sup_res_iv", password="pw", role="SUPERVISOR", email="sup_res_iv@test.com"
        )
        file = _csv_file(
            f"name,year,specialty,supervisor_username,email\nNew Resident IV,1,urology,{supervisor.username},newres_iv@test.com\n",
            "res.csv",
        )
        response = self.client.post("/api/bulk/import-residents/", {"file": file, "dry_run": "false"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["success_count"], 1)

    def test_department_import_requires_admin_role(self):
        supervisor = User.objects.create_user(
            username="sup_dept_iv", password="pw", role="SUPERVISOR", email="sup_dept_iv@test.com"
        )
        client = Client()
        client.login(username="sup_dept_iv", password="pw")
        file = _csv_file("code,name,active\nSURG,Surgery,true\n", "dept.csv")
        response = client.post("/api/bulk/import-departments/", {"file": file, "dry_run": "true"})
        self.assertEqual(response.status_code, 403)

    def test_department_import_success_for_admin(self):
        Hospital.objects.create(name="Allied Hospital", code="AH-IV", is_active=True)
        file = _csv_file("code,name,active\nSURG-IV,Surgery,true\n", "dept.csv")
        response = self.client.post("/api/bulk/import-departments/", {"file": file, "dry_run": "false"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Department.objects.filter(code="SURG-IV").exists())


class BulkExportTemplateViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(username="admin_et", password="pw", role="ADMIN")
        self.supervisor = User.objects.create_user(
            username="sup_et", password="pw", role="SUPERVISOR", email="sup_et@test.com"
        )

    def test_export_forbidden_for_non_admin(self):
        client = Client()
        client.login(username="sup_et", password="pw")
        response = client.get("/api/bulk/exports/residents/?file_format=csv")
        self.assertEqual(response.status_code, 403)

    def test_export_invalid_resource_returns_400(self):
        self.client.login(username="admin_et", password="pw")
        response = self.client.get("/api/bulk/exports/not-a-resource/?file_format=csv")
        self.assertEqual(response.status_code, 400)

    def test_export_defaults_to_xlsx(self):
        self.client.login(username="admin_et", password="pw")
        response = self.client.get("/api/bulk/exports/residents/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response["Content-Type"],
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    def test_template_forbidden_for_non_admin(self):
        client = Client()
        client.login(username="sup_et", password="pw")
        response = client.get("/api/bulk/templates/hospitals/")
        self.assertEqual(response.status_code, 403)

    def test_template_invalid_resource_returns_400(self):
        self.client.login(username="admin_et", password="pw")
        response = self.client.get("/api/bulk/templates/not-a-resource/")
        self.assertEqual(response.status_code, 400)


class BulkImportEntityViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(username="admin_ie", password="pw", role="ADMIN")
        self.supervisor = User.objects.create_user(
            username="sup_ie", password="pw", role="SUPERVISOR", email="sup_ie@test.com"
        )
        self.client.login(username="admin_ie", password="pw")

    def test_forbidden_for_non_admin(self):
        client = Client()
        client.login(username="sup_ie", password="pw")
        file = _csv_file("hospital_code,hospital_name,active\nH1,Hospital 1,true\n")
        response = client.post("/api/bulk/import/hospitals/dry-run/", {"file": file})
        self.assertEqual(response.status_code, 403)

    def test_invalid_action_rejected(self):
        file = _csv_file("hospital_code,hospital_name,active\nH1,Hospital 1,true\n")
        response = self.client.post("/api/bulk/import/hospitals/not-a-real-action/", {"file": file})
        self.assertEqual(response.status_code, 400)

    def test_unknown_entity_rejected(self):
        file = _csv_file("a,b\n1,2\n")
        response = self.client.post("/api/bulk/import/not-a-real-entity/dry-run/", {"file": file})
        self.assertEqual(response.status_code, 400)

    def test_missing_file_rejected(self):
        response = self.client.post("/api/bulk/import/hospitals/dry-run/", {})
        self.assertEqual(response.status_code, 400)

    def test_apply_creates_hospital(self):
        file = _csv_file("hospital_code,hospital_name,active\nH-APPLY,Hospital Apply,true\n")
        response = self.client.post("/api/bulk/import/hospitals/apply/", {"file": file})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data["dry_run"])
        self.assertTrue(Hospital.objects.filter(code="H-APPLY").exists())


class FlexibleImportViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(username="admin_fx", password="pw", role="ADMIN")
        self.supervisor = User.objects.create_user(
            username="sup_fx", password="pw", role="SUPERVISOR", email="sup_fx@test.com"
        )
        self.client.login(username="admin_fx", password="pw")

    def test_schemas_view_returns_entities(self):
        response = self.client.get("/api/bulk/flexible/schemas/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("hospitals", response.data)

    def test_detect_headers_forbidden_for_non_admin(self):
        client = Client()
        client.login(username="sup_fx", password="pw")
        file = _csv_file("Code,Name\nAH,Allied\n")
        response = client.post("/api/bulk/flexible/detect-headers/", {"file": file})
        self.assertEqual(response.status_code, 403)

    def test_detect_headers_csv(self):
        file = _csv_file("Hospital Code,Hospital Name\nAH-FX,Allied Hospital\n")
        response = self.client.post("/api/bulk/flexible/detect-headers/", {"file": file})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Hospital Code", response.data["headers"])
        self.assertEqual(response.data["total_rows"], 1)

    def test_detect_headers_missing_file(self):
        response = self.client.post("/api/bulk/flexible/detect-headers/", {})
        self.assertEqual(response.status_code, 400)

    def test_detect_headers_unsupported_format(self):
        file = io.BytesIO(b"not tabular")
        file.name = "data.txt"
        response = self.client.post("/api/bulk/flexible/detect-headers/", {"file": file})
        self.assertEqual(response.status_code, 400)

    def test_validate_mapping_missing_required(self):
        response = self.client.post(
            "/api/bulk/flexible/validate-mapping/",
            data=json.dumps({"entity": "hospitals", "mapping": {"hospital_code": "Code"}}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data["ready"])
        self.assertIn("hospital_name", response.data["missing_required"])

    def test_validate_mapping_duplicate_columns(self):
        response = self.client.post(
            "/api/bulk/flexible/validate-mapping/",
            data=json.dumps(
                {
                    "entity": "hospitals",
                    "mapping": {"hospital_code": "Col", "hospital_name": "Col"},
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data["ready"])
        self.assertIn("Col", response.data["duplicate_mappings"])

    def test_validate_mapping_ready(self):
        response = self.client.post(
            "/api/bulk/flexible/validate-mapping/",
            data=json.dumps(
                {
                    "entity": "hospitals",
                    "mapping": {"hospital_code": "Code", "hospital_name": "Name"},
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["ready"])

    def test_validate_mapping_invalid_entity(self):
        response = self.client.post(
            "/api/bulk/flexible/validate-mapping/",
            data=json.dumps({"entity": "not-real", "mapping": {}}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_dry_run_flow(self):
        file = _csv_file("Code,Name\nAH-DR,Allied Hospital\n")
        mapping = json.dumps({"hospital_code": "Code", "hospital_name": "Name"})
        response = self.client.post(
            "/api/bulk/flexible/dry-run/",
            {"entity": "hospitals", "mapping": mapping, "file": file},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["dry_run"])
        self.assertEqual(response.data["success_count"], 1)
        self.assertFalse(Hospital.objects.filter(code="AH-DR").exists())

    def test_dry_run_invalid_mapping_json(self):
        file = _csv_file("Code,Name\nAH,Allied\n")
        response = self.client.post(
            "/api/bulk/flexible/dry-run/",
            {"entity": "hospitals", "mapping": "not-json", "file": file},
        )
        self.assertEqual(response.status_code, 400)

    def test_apply_strict_success(self):
        file = _csv_file("Code,Name\nAH-STRICT,Allied Hospital\n")
        mapping = json.dumps({"hospital_code": "Code", "hospital_name": "Name"})
        response = self.client.post(
            "/api/bulk/flexible/apply/",
            {"entity": "hospitals", "mapping": mapping, "file": file, "import_mode": "strict"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Hospital.objects.filter(code="AH-STRICT").exists())

    def test_apply_strict_rejects_on_row_errors(self):
        file = _csv_file("Code,Name\n,Missing Code\n")
        mapping = json.dumps({"hospital_code": "Code", "hospital_name": "Name"})
        response = self.client.post(
            "/api/bulk/flexible/apply/",
            {"entity": "hospitals", "mapping": mapping, "file": file, "import_mode": "strict"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["failure_count"], 1)

    def test_apply_non_strict_allows_partial(self):
        file = _csv_file("Code,Name\nAH-OK,Allied Hospital\n,Missing Code\n")
        mapping = json.dumps({"hospital_code": "Code", "hospital_name": "Name"})
        response = self.client.post(
            "/api/bulk/flexible/apply/",
            {"entity": "hospitals", "mapping": mapping, "file": file, "import_mode": "lenient"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Hospital.objects.filter(code="AH-OK").exists())

    def test_apply_missing_file(self):
        response = self.client.post(
            "/api/bulk/flexible/apply/",
            {"entity": "hospitals", "mapping": json.dumps({})},
        )
        self.assertEqual(response.status_code, 400)


class MappingPresetViewSetTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(username="admin_mp", password="pw", role="ADMIN")
        self.client.login(username="admin_mp", password="pw")

    def test_create_and_list_presets(self):
        response = self.client.post(
            "/api/bulk/flexible/presets/",
            data=json.dumps(
                {
                    "name": "My Preset",
                    "entity": "hospitals",
                    "mapping": {"hospital_code": "Code"},
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        preset_id = response.data["id"]
        self.assertTrue(MappingPreset.objects.filter(id=preset_id, created_by=self.admin).exists())

        response = self.client.get("/api/bulk/flexible/presets/?entity=hospitals")
        self.assertEqual(response.status_code, 200)
        names = [row["name"] for row in response.data["results"]]
        self.assertIn("My Preset", names)
        self.assertTrue(all(row["name"] != "Other Preset" for row in response.data["results"]))

    def test_list_filters_by_other_users_presets(self):
        other = User.objects.create_superuser(username="admin_mp2", password="pw", role="ADMIN")
        MappingPreset.objects.create(
            name="Other Preset", entity="hospitals", mapping={}, created_by=other
        )
        response = self.client.get("/api/bulk/flexible/presets/")
        self.assertEqual(response.status_code, 200)
        names = [row["name"] for row in response.data["results"]]
        self.assertNotIn("Other Preset", names)
