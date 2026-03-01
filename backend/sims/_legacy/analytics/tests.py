from __future__ import annotations

from datetime import timedelta

from django.core.management import call_command
from django.core.cache import cache
from django.test import override_settings
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase

from sims.academics.models import Department
from sims.analytics.models import AnalyticsDailyRollup, AnalyticsEvent, AnalyticsValidationRejection
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

        with override_settings(ANALYTICS_SUPERVISOR_ACCESS_ENABLED=True):
            allowed = self.client.get(reverse("analytics_api:v1-tab", kwargs={"tab": "overview"}))
            self.assertEqual(allowed.status_code, 200)

    @override_settings(ANALYTICS_UI_INGEST_ENABLED=True)
    def test_ui_ingest_normalizes_type(self):
        self.client.force_authenticate(self.admin)
        response = self.client.post(
            reverse("analytics_api:events-ingest"),
            {
                "event_type": "page.view",
                "metadata": {
                    "feature": "filters_opened",
                    "tab": "overview",
                },
            },
            format="json",
        )
        self.assertEqual(response.status_code, 202)
        event = AnalyticsEvent.objects.latest("occurred_at")
        self.assertEqual(event.event_type, "ui.page.view")
        self.assertIn("feature", event.metadata)

    @override_settings(ANALYTICS_UI_INGEST_ENABLED=True)
    def test_ui_ingest_rejects_pii_key(self):
        self.client.force_authenticate(self.admin)
        response = self.client.post(
            reverse("analytics_api:events-ingest"),
            {
                "event_type": "page.view",
                "metadata": {
                    "tab": "live",
                    "patient_name": "John Doe",
                },
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("PII-like metadata key", response.data["detail"])
        self.assertTrue(AnalyticsValidationRejection.objects.filter(source="ui_ingest").exists())

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

    def test_track_event_requires_hospital_dimension(self):
        Hospital.objects.all().delete()
        no_hospital_user = User.objects.create_user(
            username="nohosp",
            password="testpass",
            role="admin",
            email="nohosp@example.com",
            first_name="No",
            last_name="Hospital",
        )
        with self.assertRaisesMessage(ValueError, "hospital_id is required"):
            track_event(
                event_type="auth.login.succeeded",
                actor=no_hospital_user,
                request_id="req-no-h",
                event_key="no-h",
                metadata={"source": "tests"},
            )

    def test_track_event_rejects_pii_metadata_key(self):
        with self.assertRaisesMessage(ValueError, "PII-like metadata key"):
            track_event(
                event_type="auth.login.succeeded",
                actor=self.admin,
                request_id="req-pii",
                event_key="pii",
                metadata={"email": "hidden@example.com"},
            )

    def test_live_cursor_fetches_only_new_events(self):
        self.client.force_authenticate(self.admin)
        first = track_event(
            event_type="auth.login.succeeded",
            actor=self.admin,
            request_id="cursor-1",
            event_key="cursor-1",
            metadata={"source": "tests"},
            occurred_at=timezone.now() - timedelta(minutes=2),
        )
        second = track_event(
            event_type="auth.login.succeeded",
            actor=self.admin,
            request_id="cursor-2",
            event_key="cursor-2",
            metadata={"source": "tests"},
            occurred_at=timezone.now() - timedelta(minutes=1),
        )
        initial = self.client.get(reverse("analytics_api:events-live"))
        self.assertEqual(initial.status_code, 200)
        self.assertEqual(len(initial.data["events"]), 2)
        cursor = initial.data["cursor"]

        newest = track_event(
            event_type="auth.login.succeeded",
            actor=self.admin,
            request_id="cursor-3",
            event_key="cursor-3",
            metadata={"source": "tests"},
            occurred_at=timezone.now(),
        )
        incremental = self.client.get(reverse("analytics_api:events-live"), {"cursor": cursor})
        self.assertEqual(incremental.status_code, 200)
        self.assertEqual(len(incremental.data["events"]), 1)
        self.assertEqual(incremental.data["events"][0]["id"], str(newest.id))
        self.assertNotEqual(str(first.id), str(second.id))

    def test_rollup_command_is_idempotent(self):
        when = timezone.now() - timedelta(days=1)
        track_event(
            event_type="data.export.completed",
            actor=self.admin,
            request_id="rollup-1",
            event_key="rollup-1",
            metadata={"source": "tests"},
            occurred_at=when,
        )
        track_event(
            event_type="data.export.completed",
            actor=self.admin,
            request_id="rollup-2",
            event_key="rollup-2",
            metadata={"source": "tests"},
            occurred_at=when,
        )
        call_command(
            "rebuild_analytics_rollups",
            start_date=when.date().isoformat(),
            end_date=when.date().isoformat(),
        )
        call_command(
            "rebuild_analytics_rollups",
            start_date=when.date().isoformat(),
            end_date=when.date().isoformat(),
        )
        rollup = AnalyticsDailyRollup.objects.get(
            day=when.date(),
            event_type="data.export.completed",
        )
        self.assertEqual(rollup.count, 2)

    def test_quality_endpoint_shape(self):
        self.client.force_authenticate(self.admin)
        AnalyticsValidationRejection.objects.create(
            source="safe_track_event",
            event_type="ui.page.view",
            reason="Unexpected metadata keys",
            actor_role="admin",
        )
        response = self.client.get(reverse("analytics_api:v1-quality"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("anomaly", response.data)
        self.assertIn("top_rejections", response.data)
        self.assertIn("missing_dimensions", response.data)
        self.assertIn("schema_drift", response.data)

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
