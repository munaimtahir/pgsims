from __future__ import annotations

from datetime import date, timedelta

from django.core.cache import cache
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase

from sims.analytics.services import TrendRequest, trend_for_user
from sims.logbook.models import LogbookEntry
from sims.users.models import User


class AnalyticsAPITests(APITestCase):
    def setUp(self) -> None:
        cache.clear()
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
        self.client.force_authenticate(self.admin)
        self._create_entries()

    def _create_entries(self) -> None:
        base_date = date(2024, 1, 1)
        for day_offset in range(5):
            LogbookEntry.objects.create(
                pg=self.pg,
                case_title=f"Case {day_offset}",
                date=base_date - timedelta(days=day_offset),
                location_of_activity="Ward",
                patient_history_summary="History",
                management_action="Action",
                topic_subtopic="Topic",
                status="approved" if day_offset % 2 == 0 else "pending",
                supervisor=self.supervisor,
                submitted_to_supervisor_at=timezone.now() - timedelta(days=day_offset),
                supervisor_action_at=timezone.now() - timedelta(days=max(day_offset - 1, 0)),
            )

    def test_trend_api_returns_data(self) -> None:
        url = reverse("analytics_api:trends")
        response = self.client.get(url, {"user_id": self.pg.pk, "window": 7})
        self.assertEqual(response.status_code, 200)
        payload = response.data
        self.assertEqual(payload["metric"], "entries")
        self.assertTrue(payload["series"])
        self.assertIn("moving_average", payload["series"][0])

    def test_comparative_api_requires_permission(self) -> None:
        url = reverse("analytics_api:comparative")
        response = self.client.get(
            url,
            {
                "primary_users": str(self.pg.pk),
                "secondary_users": str(self.pg.pk),
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("primary", response.data)

        self.client.force_authenticate(self.pg)
        other_pg = User.objects.create_user(
            username="pg2",
            password="testpass",
            role="pg",
            email="pg2@example.com",
            specialty="surgery",
            year="1",
            supervisor=self.supervisor,
        )
        response = self.client.get(
            url,
            {
                "primary_users": str(other_pg.pk),
                "secondary_users": str(self.pg.pk),
            },
        )
        self.assertEqual(response.status_code, 403)

    def test_performance_metrics_api(self) -> None:
        url = reverse("analytics_api:performance")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertGreater(response.data["total_entries"], 0)

    def test_trend_service_caches_response(self) -> None:
        params = TrendRequest(window=7)
        cache_key = params.cache_key(self.pg.pk)
        self.assertIsNone(cache.get(cache_key))
        data = trend_for_user(self.admin, self.pg, params)
        cache_value = cache.get(cache_key)
        self.assertEqual(data, cache_value)

    def test_dashboard_overview_api(self) -> None:
        """Test dashboard overview endpoint."""
        url = reverse("analytics_api:dashboard-overview")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.data
        self.assertIn("total_residents", data)
        self.assertIn("active_rotations", data)
        self.assertIn("pending_certificates", data)
        self.assertIn("last_30d_logs", data)
        self.assertIn("last_30d_cases", data)
        self.assertIn("unverified_logs", data)

    def test_dashboard_trends_api(self) -> None:
        """Test dashboard trends endpoint."""
        url = reverse("analytics_api:dashboard-trends")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.data
        self.assertIn("trends", data)
        self.assertIsInstance(data["trends"], list)

    def test_dashboard_compliance_api(self) -> None:
        """Test dashboard compliance endpoint."""
        url = reverse("analytics_api:dashboard-compliance")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.data
        self.assertIn("compliance", data)
        self.assertIsInstance(data["compliance"], list)

    def test_trend_api_with_different_windows(self) -> None:
        """Test trend API with different valid window parameters."""
        url = reverse("analytics_api:trends")
        for window in [7, 30, 90]:
            response = self.client.get(url, {"user_id": self.pg.pk, "window": window})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data.get("window"), window)

    def test_trend_api_missing_user_id(self) -> None:
        """Test trend API without user_id parameter."""
        url = reverse("analytics_api:trends")
        response = self.client.get(url, {"window": 7})
        # Should handle missing user_id gracefully
        self.assertIn(response.status_code, [200, 400])

    def test_comparative_api_with_same_users(self) -> None:
        """Test comparative API comparing user with themselves."""
        url = reverse("analytics_api:comparative")
        response = self.client.get(
            url,
            {
                "primary_users": str(self.pg.pk),
                "secondary_users": str(self.pg.pk),
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_performance_metrics_with_no_data(self) -> None:
        """Test performance metrics when there are no entries."""
        LogbookEntry.objects.all().delete()
        url = reverse("analytics_api:performance")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["total_entries"], 0)

    def test_dashboard_trends_date_range(self) -> None:
        """Test dashboard trends with specific date range."""
        url = reverse("analytics_api:dashboard-trends")
        response = self.client.get(url, {"days": 7})
        self.assertEqual(response.status_code, 200)

    def test_trend_cache_invalidation(self) -> None:
        """Test that cache is properly used and can be invalidated."""
        params = TrendRequest(window=7)
        cache_key = params.cache_key(self.pg.pk)

        # First call should cache
        data1 = trend_for_user(self.admin, self.pg, params)
        cached1 = cache.get(cache_key)
        self.assertEqual(data1, cached1)

        # Add new entry
        LogbookEntry.objects.create(
            pg=self.pg,
            case_title="New Case",
            date=date(2024, 1, 10),
            location_of_activity="Ward",
            patient_history_summary="History",
            management_action="Action",
            topic_subtopic="Topic",
            status="approved",
            supervisor=self.supervisor,
            submitted_to_supervisor_at=timezone.now(),
            supervisor_action_at=timezone.now(),
        )

        # Clear cache
        cache.delete(cache_key)

        # Should get new data
        data2 = trend_for_user(self.admin, self.pg, params)
        self.assertIsNotNone(data2)
