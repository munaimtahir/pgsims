"""Tests for logbook supervisor verification API endpoints."""

from datetime import date, timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

from sims.logbook.models import LogbookEntry
from sims.rotations.models import Department, Hospital, Rotation
from sims.users.models import User


class LogbookVerificationAPITests(TestCase):
    """Tests for supervisor verification workflow API."""

    def setUp(self):
        """Set up test data."""
        # Create users
        self.admin = User.objects.create_user(
            username="admin",
            password="testpass",
            role="admin",
            email="admin@example.com",
        )
        self.supervisor = User.objects.create_user(
            username="supervisor",
            password="testpass",
            role="supervisor",
            email="supervisor@example.com",
            specialty="surgery",
        )
        self.pg = User.objects.create_user(
            username="pg1",
            password="testpass",
            role="pg",
            email="pg1@example.com",
            specialty="surgery",
            year="1",
            supervisor=self.supervisor,
        )
        self.other_pg = User.objects.create_user(
            username="pg2",
            password="testpass",
            role="pg",
            email="pg2@example.com",
            specialty="medicine",
            year="1",
            supervisor=self.supervisor,  # Added supervisor
        )

        # Create hospital and department
        self.hospital = Hospital.objects.create(name="Test Hospital")
        self.department = Department.objects.create(name="Surgery", hospital=self.hospital)

        # Create rotation
        self.rotation = Rotation.objects.create(
            pg=self.pg,
            department=self.department,
            hospital=self.hospital,
            supervisor=self.supervisor,
            start_date=date.today() - timedelta(days=30),
            end_date=date.today() + timedelta(days=30),
            status="ongoing",
        )

        # Create logbook entries
        self.pending_entry = LogbookEntry.objects.create(
            pg=self.pg,
            case_title="Test Case 1",
            date=date.today(),
            location_of_activity="Ward",
            patient_history_summary="History",
            management_action="Action",
            topic_subtopic="Topic",
            status="pending",
            supervisor=self.supervisor,
            rotation=self.rotation,
            submitted_to_supervisor_at=timezone.now(),
        )

        self.approved_entry = LogbookEntry.objects.create(
            pg=self.pg,
            case_title="Test Case 2",
            date=date.today(),
            location_of_activity="Ward",
            patient_history_summary="History",
            management_action="Action",
            topic_subtopic="Topic",
            status="approved",
            supervisor=self.supervisor,
            rotation=self.rotation,
            submitted_to_supervisor_at=timezone.now(),
            verified_by=self.supervisor,
            verified_at=timezone.now(),
        )

        self.client = APIClient()

    def test_pending_entries_supervisor(self):
        """Supervisor can see pending entries from assigned PGs."""
        self.client.force_authenticate(self.supervisor)
        url = reverse("logbook_api:pending")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["id"], self.pending_entry.id)

    def test_pending_entries_admin(self):
        """Admin can see all pending entries."""
        self.client.force_authenticate(self.admin)
        url = reverse("logbook_api:pending")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)

    def test_pending_entries_pg_denied(self):
        """PG users cannot access pending entries list."""
        self.client.force_authenticate(self.pg)
        url = reverse("logbook_api:pending")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 403)

    def test_verify_entry_supervisor(self):
        """Supervisor can verify entry from assigned PG."""
        self.client.force_authenticate(self.supervisor)
        url = reverse("logbook_api:verify", kwargs={"pk": self.pending_entry.id})
        response = self.client.patch(url, {"feedback": "Good work!"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "approved")
        self.assertIn("verified_at", response.data)

        # Verify database was updated
        self.pending_entry.refresh_from_db()
        self.assertEqual(self.pending_entry.status, "approved")
        self.assertEqual(self.pending_entry.verified_by, self.supervisor)
        self.assertIsNotNone(self.pending_entry.verified_at)

    def test_verify_entry_admin(self):
        """Admin can verify any entry."""
        self.client.force_authenticate(self.admin)
        url = reverse("logbook_api:verify", kwargs={"pk": self.pending_entry.id})
        response = self.client.patch(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "approved")

    def test_verify_entry_pg_denied(self):
        """PG users cannot verify entries."""
        self.client.force_authenticate(self.pg)
        url = reverse("logbook_api:verify", kwargs={"pk": self.pending_entry.id})
        response = self.client.patch(url)

        self.assertEqual(response.status_code, 403)

    def test_verify_entry_wrong_supervisor(self):
        """Supervisor cannot verify entries from non-assigned PGs."""
        other_supervisor = User.objects.create_user(
            username="supervisor2",
            password="testpass",
            role="supervisor",
            email="supervisor2@example.com",
            specialty="medicine",
        )
        self.client.force_authenticate(other_supervisor)
        url = reverse("logbook_api:verify", kwargs={"pk": self.pending_entry.id})
        response = self.client.patch(url)

        self.assertEqual(response.status_code, 403)

    def test_verify_already_verified(self):
        """Cannot verify an already verified entry."""
        self.client.force_authenticate(self.supervisor)
        url = reverse("logbook_api:verify", kwargs={"pk": self.approved_entry.id})
        response = self.client.patch(url)

        self.assertEqual(response.status_code, 400)
        self.assertIn("already verified", response.data["error"])

    def test_verify_nonexistent_entry(self):
        """Returns 404 for nonexistent entry."""
        self.client.force_authenticate(self.supervisor)
        url = reverse("logbook_api:verify", kwargs={"pk": 99999})
        response = self.client.patch(url)

        self.assertEqual(response.status_code, 404)
