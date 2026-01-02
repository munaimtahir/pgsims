"""Comprehensive tests for search functionality."""

from __future__ import annotations

from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase

from sims.cases.models import CaseCategory, ClinicalCase
from sims.certificates.models import Certificate, CertificateType
from sims.logbook.models import Diagnosis, LogbookEntry
from sims.rotations.models import Department, Hospital, Rotation

from .models import SavedSearchSuggestion, SearchQueryLog
from .services import SearchService

User = get_user_model()


class SearchServiceTests(TestCase):
    """Test search service with RBAC."""

    def setUp(self):
        """Set up test data."""
        # Create users with different roles
        self.admin = User.objects.create_user(
            username="admin",
            password="testpass",
            role="admin",
            email="admin@test.com",
        )
        self.supervisor = User.objects.create_user(
            username="supervisor",
            password="testpass",
            role="supervisor",
            email="supervisor@test.com",
            specialty="surgery",
        )
        self.pg1 = User.objects.create_user(
            username="pg1",
            password="testpass",
            role="pg",
            email="pg1@test.com",
            specialty="surgery",
            year="1",
            supervisor=self.supervisor,
        )
        self.pg2 = User.objects.create_user(
            username="pg2",
            password="testpass",
            role="pg",
            email="pg2@test.com",
            specialty="medicine",
            year="1",
            supervisor=self.supervisor,
        )

        # Create hospital and department
        self.hospital = Hospital.objects.create(
            name="Test Hospital",
            code="TH001",
            address="123 Test St",
            phone="+1234567890",
        )
        self.department = Department.objects.create(
            name="Surgery",
            hospital=self.hospital,
        )

        # Create rotation for pg1
        self.rotation = Rotation.objects.create(
            pg=self.pg1,
            department=self.department,
            hospital=self.hospital,
            supervisor=self.supervisor,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=180),
            status="ongoing",
        )

        # Create logbook entry for pg1
        self.logbook_entry = LogbookEntry.objects.create(
            pg=self.pg1,
            rotation=self.rotation,
            supervisor=self.supervisor,
            date=date.today(),
            case_title="Test Surgery Case",
            patient_history_summary="Patient history",
            management_action="Management action",
            topic_subtopic="Surgery subtopic",
            location_of_activity="Ward",
            status="approved",
        )

        # Create case category and clinical case
        self.case_category = CaseCategory.objects.create(name="Emergency")
        self.diagnosis = Diagnosis.objects.create(name="Chest Pain", icd_code="R07.9")
        self.clinical_case = ClinicalCase.objects.create(
            pg=self.pg1,
            category=self.case_category,
            case_title="Emergency Case",
            chief_complaint="Chest pain",
            clinical_reasoning="Reasoning text",
            date_encountered=date.today(),
            patient_age=45,
            patient_gender="M",
            history_of_present_illness="Patient presented with chest pain",
            physical_examination="Normal exam",
            primary_diagnosis=self.diagnosis,
            management_plan="Observation",
            learning_points="Important case",
        )

        # Create certificate type and certificate
        self.cert_type = CertificateType.objects.create(
            name="BLS",
            description="Basic Life Support",
        )
        self.certificate = Certificate.objects.create(
            pg=self.pg1,
            certificate_type=self.cert_type,
            title="BLS Certificate",
            issuing_organization="Medical Board",
            issue_date=date.today(),
            status="approved",
        )

    def test_search_users_admin_sees_all(self):
        """Admin can see all users."""
        service = SearchService(self.admin)
        results = service._search_users("pg", {})
        self.assertGreaterEqual(len(results), 2)  # At least pg1 and pg2

    def test_search_users_supervisor_sees_supervised(self):
        """Supervisor sees only their PGs."""
        service = SearchService(self.supervisor)
        results = service._search_users("pg", {})
        self.assertGreaterEqual(len(results), 2)
        user_ids = [r.object_id for r in results]
        self.assertIn(self.pg1.pk, user_ids)
        self.assertIn(self.pg2.pk, user_ids)

    def test_search_users_pg_sees_only_self(self):
        """PG sees only themselves."""
        service = SearchService(self.pg1)
        results = service._search_users("pg", {})
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].object_id, self.pg1.pk)

    def test_search_rotations_admin_sees_all(self):
        """Admin can see all rotations."""
        service = SearchService(self.admin)
        results = service._search_rotations("Test", {})
        self.assertGreaterEqual(len(results), 1)

    def test_search_rotations_supervisor_sees_supervised(self):
        """Supervisor sees rotations they supervise."""
        service = SearchService(self.supervisor)
        results = service._search_rotations("Test", {})
        self.assertGreaterEqual(len(results), 1)

    def test_search_rotations_pg_sees_only_own(self):
        """PG sees only their own rotations."""
        service = SearchService(self.pg1)
        results = service._search_rotations("Test", {})
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].object_id, self.rotation.pk)

    def test_search_logbook_with_filters(self):
        """Search logbook with status filter."""
        service = SearchService(self.admin)
        results = service._search_logbook("Surgery", {"status": "approved"})
        self.assertGreaterEqual(len(results), 1)

    def test_search_certificates_supervisor_permission(self):
        """Supervisor can see supervised PG certificates."""
        service = SearchService(self.supervisor)
        results = service._search_certificates("BLS", {})
        self.assertGreaterEqual(len(results), 1)

    def test_search_cases_pg_permission(self):
        """PG can see only their own cases."""
        service = SearchService(self.pg1)
        results = service._search_cases("Emergency", {})
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].object_id, self.clinical_case.pk)

        # pg2 shouldn't see pg1's cases
        service2 = SearchService(self.pg2)
        results2 = service2._search_cases("Emergency", {})
        self.assertEqual(len(results2), 0)

    def test_search_empty_query(self):
        """Empty query returns empty results."""
        service = SearchService(self.admin)
        results = service.search("", {})
        self.assertEqual(len(results), 0)

    def test_search_combined_results(self):
        """Search combines results from all modules."""
        service = SearchService(self.admin)
        results = service.search("Test", {})
        self.assertGreater(len(results), 0)
        # Results should be sorted by score
        if len(results) > 1:
            self.assertGreaterEqual(results[0].score, results[-1].score)

    def test_log_query(self):
        """Search logs are created."""
        service = SearchService(self.admin)
        initial_count = SearchQueryLog.objects.count()
        service.log_query("test query", {}, 5, 100)
        self.assertEqual(SearchQueryLog.objects.count(), initial_count + 1)
        log = SearchQueryLog.objects.latest("created_at")
        self.assertEqual(log.query, "test query")
        self.assertEqual(log.result_count, 5)
        self.assertEqual(log.duration_ms, 100)

    def test_get_recent_history(self):
        """Recent search history is retrieved."""
        service = SearchService(self.admin)
        service.log_query("query1", {}, 1, 10)
        service.log_query("query2", {}, 2, 20)
        history = service.get_recent_history()
        self.assertIn("query1", history)
        self.assertIn("query2", history)

    def test_get_suggestions(self):
        """Suggestions are retrieved."""
        SavedSearchSuggestion.objects.create(label="surgery procedures")
        SavedSearchSuggestion.objects.create(label="medicine cases")
        service = SearchService(self.admin)
        suggestions = service.get_suggestions("sur")
        self.assertIn("surgery procedures", suggestions)
        self.assertNotIn("medicine cases", suggestions)

    def test_get_suggestions_empty_prefix(self):
        """Suggestions work with empty prefix."""
        SavedSearchSuggestion.objects.create(label="test suggestion")
        service = SearchService(self.admin)
        suggestions = service.get_suggestions("")
        self.assertIn("test suggestion", suggestions)


class SearchAPITests(APITestCase):
    """Test search API endpoints."""

    def setUp(self):
        """Set up test data."""
        self.admin = User.objects.create_user(
            username="admin",
            password="testpass",
            role="admin",
            email="admin@test.com",
        )
        self.supervisor = User.objects.create_user(
            username="supervisor",
            password="testpass",
            role="supervisor",
            email="supervisor@test.com",
            specialty="surgery",
        )
        self.pg = User.objects.create_user(
            username="pg",
            password="testpass",
            role="pg",
            email="pg@test.com",
            specialty="surgery",
            year="1",
            supervisor=self.supervisor,
        )

    def test_global_search_requires_auth(self):
        """Search endpoint requires authentication."""
        url = reverse("search:global_search")
        response = self.client.get(url, {"q": "test"})
        self.assertEqual(response.status_code, 401)

    def test_global_search_with_query(self):
        """Search endpoint returns results."""
        self.client.force_authenticate(self.admin)
        url = reverse("search:global_search")
        response = self.client.get(url, {"q": "admin"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("results", response.data)
        self.assertIn("count", response.data)
        self.assertIn("duration_ms", response.data)
        self.assertIn("history", response.data)
        self.assertIn("suggestions", response.data)

    def test_global_search_empty_query(self):
        """Search with empty query returns empty results."""
        self.client.force_authenticate(self.admin)
        url = reverse("search:global_search")
        response = self.client.get(url, {"q": ""})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 0)

    def test_global_search_with_filters(self):
        """Search with filters works."""
        self.client.force_authenticate(self.admin)
        url = reverse("search:global_search")
        response = self.client.get(url, {"q": "test", "filter_role": "admin"})
        self.assertEqual(response.status_code, 200)

    def test_search_history_endpoint(self):
        """Search history endpoint works."""
        self.client.force_authenticate(self.admin)
        # Create a search log
        SearchQueryLog.objects.create(
            user=self.admin,
            query="test query",
            result_count=5,
            duration_ms=100,
        )
        url = reverse("search:history")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)

    def test_search_suggestions_endpoint(self):
        """Search suggestions endpoint works."""
        SavedSearchSuggestion.objects.create(label="test suggestion")
        self.client.force_authenticate(self.admin)
        url = reverse("search:suggestions")
        response = self.client.get(url, {"q": "test"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("suggestions", response.data)
        self.assertIn("test suggestion", response.data["suggestions"])

    def test_search_logs_query(self):
        """Search creates query log."""
        self.client.force_authenticate(self.admin)
        initial_count = SearchQueryLog.objects.count()
        url = reverse("search:global_search")
        response = self.client.get(url, {"q": "test"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(SearchQueryLog.objects.count(), initial_count + 1)

    def test_search_permission_enforcement(self):
        """Search enforces RBAC permissions."""
        # Create another user's data that pg shouldn't see
        admin_user = User.objects.create_user(
            username="other_admin",
            password="testpass",
            role="admin",
            email="other@test.com",
        )

        self.client.force_authenticate(self.pg)
        url = reverse("search:global_search")
        response = self.client.get(url, {"q": "other_admin"})
        self.assertEqual(response.status_code, 200)
        # PG shouldn't see other admin
        self.assertEqual(response.data["count"], 0)
