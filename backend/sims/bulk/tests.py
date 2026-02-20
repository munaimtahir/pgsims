from __future__ import annotations

import csv
import io
from datetime import date

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework.test import APITestCase

from sims.bulk.models import BulkOperation
from sims.bulk.services import BulkService
from sims.logbook.models import LogbookEntry
from sims.users.models import User


class BulkOperationTests(APITestCase):
    def setUp(self) -> None:
        self.admin = User.objects.create_user(username="admin", password="testpass", role="admin")
        self.supervisor = User.objects.create_user(
            username="sup",
            password="testpass",
            role="supervisor",
            specialty="surgery",
        )
        self.pg = User.objects.create_user(
            username="pg",
            password="testpass",
            role="pg",
            specialty="surgery",
            year="1",
            supervisor=self.supervisor,
        )
        self.client.force_authenticate(self.admin)
        self.entries = [
            LogbookEntry.objects.create(
                pg=self.pg,
                case_title=f"Case {i}",
                date=date(2024, 1, 1),
                location_of_activity="Ward",
                patient_history_summary="History",
                management_action="Action",
                topic_subtopic="Topic",
            )
            for i in range(3)
        ]

    def test_bulk_review_service(self) -> None:
        service = BulkService(self.admin, chunk_size=2)
        operation = service.review_entries([entry.pk for entry in self.entries], status="approved")
        self.assertEqual(operation.status, BulkOperation.STATUS_COMPLETED)
        self.assertEqual(operation.success_count, 3)
        self.assertEqual(LogbookEntry.objects.filter(status="approved").count(), 3)

    def test_bulk_assignment_api(self) -> None:
        url = reverse("bulk_api:assignment")
        payload = {
            "entry_ids": [entry.pk for entry in self.entries],
            "supervisor_id": self.supervisor.pk,
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            LogbookEntry.objects.filter(supervisor=self.supervisor).count(),
            len(self.entries),
        )

    def test_bulk_import_dry_run(self) -> None:
        csv_buffer = io.StringIO()
        writer = csv.DictWriter(
            csv_buffer, fieldnames=["pg_username", "case_title", "date", "status"]
        )
        writer.writeheader()
        writer.writerow(
            {
                "pg_username": self.pg.username,
                "case_title": "Imported Case",
                "date": date(2024, 1, 1).isoformat(),
                "status": "pending",
            }
        )
        writer.writerow(
            {
                "pg_username": "unknown",
                "case_title": "Bad Case",
                "date": date(2024, 1, 1).isoformat(),
                "status": "pending",
            }
        )
        uploaded = SimpleUploadedFile(
            "import.csv", csv_buffer.getvalue().encode("utf-8"), content_type="text/csv"
        )
        url = reverse("bulk_api:import")
        response = self.client.post(
            url, {"file": uploaded, "dry_run": True, "allow_partial": False}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["failure_count"], 1)
        self.assertEqual(LogbookEntry.objects.filter(case_title="Imported Case").count(), 0)

        uploaded = SimpleUploadedFile(
            "import.csv", csv_buffer.getvalue().encode("utf-8"), content_type="text/csv"
        )
        response = self.client.post(
            url, {"file": uploaded, "dry_run": False, "allow_partial": True}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(LogbookEntry.objects.filter(case_title="Imported Case").count(), 1)

    def test_bulk_review_permission_denied(self) -> None:
        """Test that PG cannot perform bulk review."""
        from django.core.exceptions import PermissionDenied

        self.client.force_authenticate(self.pg)
        # PG should not be able to create bulk service for review
        with self.assertRaises(PermissionDenied):
            service = BulkService(self.pg, chunk_size=2)
            operation = service.review_entries([self.entries[0].pk], status="approved")

    def test_bulk_import_empty_file(self) -> None:
        """Test bulk import with empty CSV file."""
        csv_buffer = io.StringIO()
        writer = csv.DictWriter(
            csv_buffer, fieldnames=["pg_username", "case_title", "date", "status"]
        )
        writer.writeheader()
        uploaded = SimpleUploadedFile(
            "empty.csv", csv_buffer.getvalue().encode("utf-8"), content_type="text/csv"
        )
        url = reverse("bulk_api:import")
        response = self.client.post(
            url, {"file": uploaded, "dry_run": True, "allow_partial": False}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("success_count", 0), 0)

    def test_bulk_operation_tracking(self) -> None:
        """Test that bulk operations are properly tracked."""
        initial_count = BulkOperation.objects.count()
        service = BulkService(self.admin, chunk_size=2)
        operation = service.review_entries([entry.pk for entry in self.entries], status="approved")
        self.assertEqual(BulkOperation.objects.count(), initial_count + 1)
        self.assertIsNotNone(operation.completed_at)
        self.assertEqual(operation.status, BulkOperation.STATUS_COMPLETED)
