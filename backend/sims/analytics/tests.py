from __future__ import annotations

from django.core.cache import cache
from django.test import override_settings
from django.urls import reverse
from rest_framework.test import APITestCase

from sims.academics.models import Department
from sims.analytics.models import AnalyticsEvent
from sims.analytics.services import track_event
from sims.rotations.models import Hospital
from sims.users.models import User


class AnalyticsV1ApiTests(APITestCase):
    def setUp(self) -> None:
        cache.clear()
        self.department = Department.objects.create(name="Surgery", code="SURG")
        self.hospital = Hospital.objects.create(name="Teaching Hospital", code="TH1")

        self.admin = User.objects.create_user(
            username="admin",
            password="testpass",
            role="admin",
            email="admin@example.com",
            first_name="Admin",
            last_name="User",
        )
        self.supervisor = User.objects.create_user(
            username="supervisor",
            password="testpass",
            role="supervisor",
            email="supervisor@example.com",
            specialty="surgery",
            first_name="Sup",
            last_name="Visor",
        )
        self.pg = User.objects.create_user(
            username="pg1",
            password="testpass",
            role="pg",
            email="pg1@example.com",
            specialty="surgery",
            year="1",
            supervisor=self.supervisor,
            first_name="PG",
            last_name="One",
            home_department=self.department,
            home_hospital=self.hospital,
        )

    def test_v1_overview_empty_shape(self):
        self.client.force_authenticate(self.admin)
        response = self.client.get(reverse("analytics_api:v1-tab", kwargs={"tab": "overview"}))
        self.assertEqual(response.status_code, 200)
        self.assertIn("cards", response.data)
        self.assertIn("table", response.data)
        self.assertIn("series", response.data)

    def test_v1_all_tabs_empty_shape(self):
        self.client.force_authenticate(self.admin)
        tabs = [
            "overview",
            "adoption",
            "logbook",
            "review-sla",
            "departments",
            "rotations",
            "research",
            "data-ops",
            "system",
            "security",
            "live",
        ]
        for tab in tabs:
            response = self.client.get(reverse("analytics_api:v1-tab", kwargs={"tab": tab}))
            self.assertEqual(response.status_code, 200)
            self.assertIn("cards", response.data)
            self.assertIn("table", response.data)

    def test_live_endpoint_limit(self):
        self.client.force_authenticate(self.admin)
        for index in range(5):
            track_event(
                event_type="auth.login.succeeded",
                actor=self.admin,
                event_key=f"live-{index}",
                request_id=f"live-{index}",
                metadata={"source": "tests"},
            )
        response = self.client.get(reverse("analytics_api:v1-live"), {"limit": 2})
        self.assertEqual(response.status_code, 200)
        self.assertLessEqual(len(response.data["events"]), 2)

    def test_supervisor_access_is_flag_controlled(self):
        self.client.force_authenticate(self.supervisor)
        denied = self.client.get(reverse("analytics_api:v1-tab", kwargs={"tab": "overview"}))
        self.assertEqual(denied.status_code, 403)

        with override_settings(ANALYTICS_ALLOW_SUPERVISOR_ACCESS=True):
            allowed = self.client.get(reverse("analytics_api:v1-tab", kwargs={"tab": "overview"}))
            self.assertEqual(allowed.status_code, 200)

    @override_settings(ANALYTICS_UI_INGEST_ENABLED=True)
    def test_ui_ingest_normalizes_type_and_drops_pii(self):
        self.client.force_authenticate(self.admin)
        response = self.client.post(
            reverse("analytics_api:events-ingest"),
            {
                "event_type": "page.view",
                "metadata": {
                    "feature": "filters_opened",
                    "email": "hidden@example.com",
                },
            },
            format="json",
        )
        self.assertEqual(response.status_code, 202)
        event = AnalyticsEvent.objects.latest("occurred_at")
        self.assertEqual(event.event_type, "ui.page.view")
        self.assertIn("feature", event.metadata)
        self.assertNotIn("email", event.metadata)

    def test_rbac_denied_event_recorded(self):
        self.client.force_authenticate(self.supervisor)
        response = self.client.get(reverse("logbook_api:my_entries"))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(AnalyticsEvent.objects.filter(event_type="auth.rbac.denied").exists())

    def test_logbook_workflow_records_events(self):
        self.client.force_authenticate(self.pg)
        create_response = self.client.post(
            reverse("logbook_api:my_entries"),
            {
                "case_title": "Appendicitis",
                "date": "2026-02-01",
                "location_of_activity": "Ward",
                "patient_history_summary": "History",
                "management_action": "Management",
                "topic_subtopic": "General Surgery",
            },
            format="json",
        )
        self.assertEqual(create_response.status_code, 201)
        entry_id = create_response.data["id"]

        submit_response = self.client.post(reverse("logbook_api:my_entry_submit", kwargs={"pk": entry_id}))
        self.assertEqual(submit_response.status_code, 200)

        self.client.force_authenticate(self.supervisor)
        verify_response = self.client.patch(
            reverse("logbook_api:verify", kwargs={"pk": entry_id}),
            {"action": "returned", "feedback": "Please improve details"},
            format="json",
        )
        self.assertEqual(verify_response.status_code, 200)

        entity_events = AnalyticsEvent.objects.filter(entity_type="logbook_entry", entity_id=str(entry_id))
        self.assertTrue(entity_events.filter(event_type="logbook.case.created").exists())
        self.assertTrue(entity_events.filter(event_type="logbook.case.submitted").exists())
        self.assertTrue(entity_events.filter(event_type="logbook.case.sent_back").exists())
        self.assertGreaterEqual(entity_events.filter(event_type="logbook.status.transitioned").count(), 2)

    def test_bulk_export_records_events(self):
        self.client.force_authenticate(self.admin)
        response = self.client.get(
            reverse("bulk_api:exports", kwargs={"resource": "departments"}),
            {"file_format": "csv"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(AnalyticsEvent.objects.filter(event_type="data.export.started").exists())
        self.assertTrue(AnalyticsEvent.objects.filter(event_type="data.export.completed").exists())

    def test_track_event_dedupes_by_request_id_and_event_key(self):
        track_event(
            event_type="auth.login.succeeded",
            actor=self.admin,
            request_id="req-1",
            event_key="login",
            metadata={"source": "tests"},
        )
        track_event(
            event_type="auth.login.succeeded",
            actor=self.admin,
            request_id="req-1",
            event_key="login",
            metadata={"source": "tests"},
        )
        self.assertEqual(
            AnalyticsEvent.objects.filter(
                event_type="auth.login.succeeded",
                request_id="req-1",
                event_key="login",
            ).count(),
            1,
        )

    @override_settings(ANALYTICS_ENABLED=False)
    def test_track_event_respects_global_flag(self):
        event = track_event(
            event_type="auth.login.succeeded",
            actor=self.admin,
            request_id="off-1",
            event_key="off",
            metadata={"source": "tests"},
        )
        self.assertIsNone(event)
