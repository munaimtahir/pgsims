from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
import io
import json

User = get_user_model()

class BulkViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(username="admin_bulk", password="password123", role="admin")
        self.client.login(username="admin_bulk", password="password123")

    def test_bulk_import_entity_dry_run(self):
        csv_content = "hospital_code,hospital_name,active\nH-NEW,New Hospital,true\n"
        file = io.BytesIO(csv_content.encode('utf-8'))
        file.name = "hospitals.csv"
        
        response = self.client.post(
            "/api/bulk/import/hospitals/dry-run/",
            {"file": file}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "completed")
        self.assertEqual(response.data["success_count"], 1)

    def test_bulk_export_residents(self):
        # Uses file_format parameter
        response = self.client.get("/api/bulk/exports/residents/?file_format=csv")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/csv")

    def test_bulk_template_hospitals(self):
        response = self.client.get("/api/bulk/templates/hospitals/")
        self.assertEqual(response.status_code, 200)
