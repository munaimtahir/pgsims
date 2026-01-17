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


class PGLogbookEntryAPITests(TestCase):
    """Tests for PG logbook CRUD API endpoints."""

    def setUp(self):
        self.supervisor = User.objects.create_user(
            username="supervisor_pg",
            password="testpass",
            role="supervisor",
            email="supervisor_pg@example.com",
            specialty="surgery",
        )
        self.pg = User.objects.create_user(
            username="pg_user",
            password="testpass",
            role="pg",
            email="pg_user@example.com",
            specialty="surgery",
            year="1",
            supervisor=self.supervisor,
        )
        self.other_pg = User.objects.create_user(
            username="pg_user_2",
            password="testpass",
            role="pg",
            email="pg_user_2@example.com",
            specialty="medicine",
            year="2",
            supervisor=self.supervisor,
        )
        self.client = APIClient()

        self.entry_payload = {
            "case_title": "Initial Case",
            "date": date.today(),
            "location_of_activity": "Ward",
            "patient_history_summary": "History summary",
            "management_action": "Management action",
            "topic_subtopic": "Topic",
        }

    def test_pg_create_list_update_entry(self):
        """PG can create, list, and update their own draft entry."""
        self.client.force_authenticate(self.pg)
        create_url = reverse("logbook_api:my_entries")
        response = self.client.post(create_url, self.entry_payload, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["status"], "draft")

        list_response = self.client.get(create_url)
        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(list_response.data["count"], 1)

        entry_id = list_response.data["results"][0]["id"]
        update_url = reverse("logbook_api:my_entry_detail", kwargs={"pk": entry_id})
        update_response = self.client.patch(
            update_url, {"case_title": "Updated Case"}, format="json"
        )
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.data["case_title"], "Updated Case")

    def test_pg_cannot_access_others_entries(self):
        """PG cannot access another PG's entries."""
        entry = LogbookEntry.objects.create(
            pg=self.pg,
            case_title="Private Case",
            date=date.today(),
            location_of_activity="Clinic",
            patient_history_summary="History",
            management_action="Action",
            topic_subtopic="Topic",
            status="draft",
        )

        self.client.force_authenticate(self.other_pg)
        list_response = self.client.get(reverse("logbook_api:my_entries"))
        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(list_response.data["count"], 0)

        update_url = reverse("logbook_api:my_entry_detail", kwargs={"pk": entry.id})
        update_response = self.client.patch(update_url, {"case_title": "Hack"}, format="json")
        self.assertEqual(update_response.status_code, 404)

    def test_pg_cannot_edit_after_submit(self):
        """PG cannot edit entries after submission."""
        entry = LogbookEntry.objects.create(
            pg=self.pg,
            case_title="Pending Case",
            date=date.today(),
            location_of_activity="Clinic",
            patient_history_summary="History",
            management_action="Action",
            topic_subtopic="Topic",
            status="pending",
            supervisor=self.supervisor,
            submitted_to_supervisor_at=timezone.now(),
        )

        self.client.force_authenticate(self.pg)
        update_url = reverse("logbook_api:my_entry_detail", kwargs={"pk": entry.id})
        response = self.client.patch(update_url, {"case_title": "Updated"}, format="json")
        self.assertEqual(response.status_code, 400)

    def test_pg_submit_entry_shows_in_pending_queue(self):
        """Submitting a draft entry moves it to pending and appears in supervisor queue."""
        entry = LogbookEntry.objects.create(
            pg=self.pg,
            case_title="Draft Case",
            date=date.today(),
            location_of_activity="Ward",
            patient_history_summary="History",
            management_action="Action",
            topic_subtopic="Topic",
            status="draft",
        )

        self.client.force_authenticate(self.pg)
        submit_url = reverse("logbook_api:my_entry_submit", kwargs={"pk": entry.id})
        response = self.client.post(submit_url, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "pending")

        entry.refresh_from_db()
        self.assertEqual(entry.status, "pending")
        self.assertIsNotNone(entry.submitted_to_supervisor_at)

        self.client.force_authenticate(self.supervisor)
        pending_response = self.client.get(reverse("logbook_api:pending"))
        self.assertEqual(pending_response.status_code, 200)
        pending_ids = [item["id"] for item in pending_response.data["results"]]
        self.assertIn(entry.id, pending_ids)
