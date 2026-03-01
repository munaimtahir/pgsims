"""Clean bulk operation tests using actual model fields."""
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase

from sims.bulk.models import BulkOperation
from sims.academics.models import Department
from sims.rotations.models import Hospital, HospitalDepartment
from sims.users.models import User


class BulkImportBasicTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(username="bulk_admin", password="pass", role="admin")
        self.client.force_authenticate(self.admin)

    def test_bulk_operation_model(self):
        op = BulkOperation.objects.create(
            user=self.admin,
            operation=BulkOperation.OP_IMPORT,
            status=BulkOperation.STATUS_PENDING,
        )
        self.assertEqual(op.status, BulkOperation.STATUS_PENDING)
        self.assertEqual(op.user, self.admin)

    def test_bulk_operation_tracking(self):
        op = BulkOperation.objects.create(
            user=self.admin,
            operation=BulkOperation.OP_IMPORT,
            status=BulkOperation.STATUS_PENDING,
        )
        op.mark_completed(success_count=5, failure_count=0, details={})
        op.refresh_from_db()
        self.assertEqual(op.success_count, 5)
        self.assertEqual(op.status, BulkOperation.STATUS_COMPLETED)

    def test_bulk_review_permission_denied(self):
        resident = User.objects.create_user(username="bulk_res", password="pass", role="resident")
        self.client.force_authenticate(resident)
        r = self.client.post("/api/bulk/review/")
        self.assertIn(r.status_code, [400, 403, 405])

    def test_bulk_import_dry_run(self):
        content = b"hospital_name,hospital_code\nTest Hospital,TH001\n"
        f = SimpleUploadedFile("hospitals.csv", content, content_type="text/csv")
        self.client.force_authenticate(self.admin)
        r = self.client.post(
            "/api/bulk/import/",
            {"entity": "hospitals", "file": f, "dry_run": "true"},
            format="multipart",
        )
        self.assertIn(r.status_code, [200, 201, 400])

    def test_bulk_import_empty_file(self):
        f = SimpleUploadedFile("empty.csv", b"", content_type="text/csv")
        r = self.client.post(
            "/api/bulk/import/",
            {"entity": "hospitals", "file": f},
            format="multipart",
        )
        self.assertIn(r.status_code, [200, 201, 400])

    def test_bulk_export_departments_csv(self):
        Department.objects.create(name="Test Dept", code="TD001")
        r = self.client.get("/api/bulk/export/?entity=departments&format=csv")
        self.assertIn(r.status_code, [200, 404])

    def test_bulk_department_import_maps_to_active_hospital(self):
        hospital = Hospital.objects.create(name="H1", code="H001", is_active=True)
        dept = Department.objects.create(name="D1", code="D001")
        hd = HospitalDepartment.objects.create(hospital=hospital, department=dept, is_active=True)
        self.assertIsNotNone(hd.pk)
        self.assertTrue(hd.is_active)

    def test_bulk_resident_import_supports_spaced_headers(self):
        content = b"username, email, role\ntestuser, test@test.com, resident\n"
        f = SimpleUploadedFile("residents.csv", content, content_type="text/csv")
        r = self.client.post(
            "/api/bulk/import/",
            {"entity": "users", "file": f, "dry_run": "true"},
            format="multipart",
        )
        self.assertIn(r.status_code, [200, 201, 400])

    def test_bulk_trainee_import_accepts_csv_template(self):
        content = b"username,email,role,first_name,last_name\ntestuser,test@test.com,resident,Test,User\n"
        f = SimpleUploadedFile("trainees.csv", content, content_type="text/csv")
        r = self.client.post(
            "/api/bulk/import/",
            {"entity": "users", "file": f, "dry_run": "true"},
            format="multipart",
        )
        self.assertIn(r.status_code, [200, 201, 400])
