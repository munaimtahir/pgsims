from __future__ import annotations

from datetime import date, timedelta

from django.core import mail
from django.test import override_settings
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase

from sims.logbook.models import LogbookEntry
from sims.notifications.models import Notification, NotificationPreference
from sims.notifications.services import NotificationService
from sims.rotations.models import Department, Hospital, Rotation
from sims.users.models import User


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class NotificationTests(APITestCase):
    def setUp(self) -> None:
        self.supervisor = User.objects.create_user(
            username="sup",
            password="testpass",
            role="supervisor",
            email="sup@example.com",
            specialty="surgery",
        )
        self.pg = User.objects.create_user(
            username="pg",
            password="testpass",
            role="pg",
            email="pg@example.com",
            specialty="surgery",
            year="1",
            supervisor=self.supervisor,
        )
        self.client.force_authenticate(self.pg)

    def _create_logbook_entry(self, status: str) -> LogbookEntry:
        return LogbookEntry.objects.create(
            pg=self.pg,
            supervisor=self.supervisor,
            status=status,
            case_title="Sample",
            date=date(2024, 1, 1),
            location_of_activity="Ward",
            patient_history_summary="History",
            management_action="Action",
            topic_subtopic="Topic",
        )

    def test_status_change_triggers_notification(self) -> None:
        entry = self._create_logbook_entry("draft")
        entry.status = "pending"
        entry.submitted_to_supervisor_at = timezone.now()
        entry.save()

        self.assertTrue(
            Notification.objects.filter(
                recipient=self.supervisor, verb="logbook-submitted"
            ).exists()
        )
        self.assertEqual(len(mail.outbox), 1)

    def test_mark_read_api(self) -> None:
        entry = self._create_logbook_entry("draft")
        entry.status = "approved"
        entry.supervisor_action_at = timezone.now()
        entry.save()

        notification = Notification.objects.get(recipient=self.pg)
        url = reverse("notifications_api:mark_read")
        response = self.client.post(url, {"notification_ids": [notification.pk]}, format="json")
        self.assertEqual(response.status_code, 200)
        notification.refresh_from_db()
        self.assertIsNotNone(notification.read_at)

    def test_preferences_api(self) -> None:
        url = reverse("notifications_api:preferences")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response = self.client.patch(url, {"email_enabled": False}, format="json")
        self.assertEqual(response.status_code, 200)
        prefs = NotificationPreference.for_user(self.pg)
        self.assertFalse(prefs.email_enabled)

    def test_rotation_deadline_trigger(self) -> None:
        hospital = Hospital.objects.create(name="General Hospital")
        department = Department.objects.create(name="Surgery", hospital=hospital)
        rotation = Rotation.objects.create(
            pg=self.pg,
            department=department,
            hospital=hospital,
            supervisor=self.supervisor,
            start_date=date.today() - timedelta(days=20),
            end_date=date.today() + timedelta(days=1),
            status="ongoing",
        )
        service = NotificationService(actor=self.supervisor)
        count = service.upcoming_rotation_deadlines(days=3)
        self.assertEqual(count, 1)
        self.assertTrue(
            Notification.objects.filter(recipient=self.pg, verb="rotation-ending").exists()
        )
