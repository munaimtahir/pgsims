from datetime import date, timedelta
from types import SimpleNamespace
from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.test import RequestFactory, SimpleTestCase, TestCase

from sims.admin import SIMSAdminSite
from sims.domain.validators import (
    sanitize_free_text,
    validate_chronology,
    validate_not_future,
    validate_same_supervisor,
)
from sims.rotations.views import department_by_hospital_api
from sims.training.dashboard_serializers import (
    DashboardReadinessSerializer,
    LogbookSummarySerializer,
    ResidentOperationalDashboardSerializer,
)
from sims.users.management.commands.import_pilot_bundle import Command as PilotImportCommand, ImportArtifacts


class DomainValidatorCoverageTests(SimpleTestCase):
    def test_date_and_chronology_validators(self):
        validate_not_future(None, "date")
        validate_not_future(date.today(), "date")
        validate_chronology(date.today(), date.today(), "start", "end")
        with self.assertRaises(ValidationError):
            validate_not_future(date.today() + timedelta(days=1), "date")
        with self.assertRaises(ValidationError):
            validate_chronology(date.today(), date.today() - timedelta(days=1), "start", "end")

    def test_supervisor_and_text_validation(self):
        validate_same_supervisor(None, None)
        validate_same_supervisor(SimpleNamespace(supervisor_id=4), SimpleNamespace(pk=4))
        with self.assertRaises(ValidationError):
            validate_same_supervisor(SimpleNamespace(supervisor_id=4), SimpleNamespace(pk=5))
        self.assertEqual(sanitize_free_text("  hello  "), "hello")
        self.assertEqual(sanitize_free_text(""), "")
        for value in ("<SCRIPT>alert(1)", "javascript:alert(1)"):
            with self.assertRaises(ValidationError):
                sanitize_free_text(value)


class DashboardSerializerCoverageTests(SimpleTestCase):
    def test_nested_dashboard_serializer(self):
        payload = {
            "training_record_id": 1,
            "logbook": {"total": 2, "draft": 0, "submitted": 1, "returned": 0,
                        "approved": 1, "threshold": {"met": True}},
            "submissions": [], "certificates": [],
            "readiness": {"logbook_threshold_met": True, "synopsis_certificate_issued": False,
                          "thesis_certificate_issued": False, "required_rotations_verified": True,
                          "required_rotation_count": 2, "verified_rotation_count": 2},
            "pending_actions": [],
        }
        serializer = ResidentOperationalDashboardSerializer(data=payload)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertTrue(LogbookSummarySerializer(data=payload["logbook"]).is_valid())
        self.assertTrue(DashboardReadinessSerializer(data=payload["readiness"]).is_valid())


class RecomputeEligibilityCommandCoverageTests(TestCase):
    @patch("sims.training.eligibility.recompute_for_record")
    @patch("sims.training.models.ResidentTrainingRecord.objects")
    def test_all_records_success_and_error(self, objects, recompute):
        good = SimpleNamespace(pk=1, active=True, program=None)
        bad = SimpleNamespace(pk=2, active=True, program=None)
        good.__str__ = lambda self: "good"
        bad.__str__ = lambda self: "bad"
        objects.filter.return_value.select_related.return_value.count.return_value = 2
        objects.filter.return_value.select_related.return_value.iterator.return_value = [good, bad]
        recompute.side_effect = [[1, 2], RuntimeError("broken")]
        call_command("recompute_eligibility")
        self.assertEqual(recompute.call_count, 2)

    @patch("sims.training.eligibility.recompute_for_record", return_value=[])
    @patch("sims.training.models.ResidentTrainingRecord.objects")
    def test_single_record_filter(self, objects, recompute):
        qs = objects.filter.return_value
        qs.count.return_value = 0
        qs.iterator.return_value = []
        call_command("recompute_eligibility", rtr_id=9)
        objects.filter.assert_called_once_with(pk=9, active=True)


class RotationViewCoverageTests(TestCase):
    def test_missing_hospital_returns_empty(self):
        request = RequestFactory().get("/api/departments/999/")
        request.user = SimpleNamespace(is_authenticated=True)
        response = department_by_hospital_api(request, 999)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'{"departments": []}')


class AdminIndexCoverageTests(TestCase):
    def test_index_handles_stats_query_failure(self):
        request = RequestFactory().get("/admin/")
        request.user = SimpleNamespace(is_staff=True, is_active=True)
        with patch("sims.admin.User.objects.filter", side_effect=RuntimeError("db")):
            # Exercise the custom implementation without rendering the admin template.
            with patch("django.contrib.admin.AdminSite.index", return_value=SimpleNamespace()) as parent:
                result = SIMSAdminSite().index(request)
        self.assertIsNotNone(result)
        parent.assert_called_once()


class PilotBundleHelperCoverageTests(SimpleTestCase):
    def setUp(self):
        self.command = PilotImportCommand()
        self.artifacts = ImportArtifacts()

    def test_normalizers_and_dedupe(self):
        self.assertEqual(self.command._normalize_header(" Phone Number "), "phone_number")
        self.assertEqual(self.command._pick({"full_name": " Ada "}, ["name", "full_name"]), "Ada")
        self.assertEqual(self.command._resolve_department_code("medicine", {"medicine": "MED"}), "MED")
        self.assertEqual(self.command._resolve_department_code("", {}), "")
        self.assertEqual(self.command._resolve_hospital_code("h1", "H0"), "H1")
        self.assertEqual(self.command._resolve_hospital_code("", "H0"), "H0")
        self.assertEqual(self.command._generate_unique_username("Ada Lovelace", {"ada.lovelace"}), "ada.lovelace.2")
        self.assertEqual(self.command._placeholder_email("ada", "RESIDENT"), "ada.RESIDENT@pilot-placeholder.local")
        self.assertEqual(self.command._normalize_date("01/02/2025", self.artifacts, context="x"), "2025-02-01")
        self.assertEqual(self.command._normalize_optional_date("", self.artifacts, context="x"), "")
        self.assertEqual(self.command._normalize_optional_date("bad", self.artifacts, context="x"), "")
        self.assertEqual(self.command._normalize_date("bad", self.artifacts, context="x"), date.today().isoformat())
        self.assertEqual(self.command._normalize_year("year 3", "2025-01-01"), "3")
        self.assertEqual(self.command._normalize_year("", "bad"), "1")
        self.assertEqual(self.command._normalize_program_code("ms/fcps"), "MS-FCPS")
        self.assertEqual(self.command._dedupe([{"a": 1}, {"a": 1}, {"a": 2}]), [{"a": 1}, {"a": 2}])

    @patch("sims.users.management.commands.import_pilot_bundle.Hospital")
    @patch("sims.users.management.commands.import_pilot_bundle.Department")
    @patch("sims.users.management.commands.import_pilot_bundle.User")
    def test_mapping_rows(self, user_model, department_model, hospital_model):
        user_model.objects.values_list.return_value = []
        department_model.objects.filter.return_value = [SimpleNamespace(code="MED", name="Medicine")]
        hospital_model.objects.filter.return_value.order_by.return_value.first.return_value = SimpleNamespace(code="H1")
        supervisors = self.command._map_supervisors([{"name": "Dr Ada", "department": "Medicine", "start_date": "2025-01-01"}], self.artifacts)
        residents = self.command._map_residents([{"name": "Bob", "department": "MED", "year": "Y2", "training_start": "2025-01-01", "supervisor_name": "Dr Ada", "program": "MS FCPS"}], self.artifacts)
        programs = self.command._map_programs([{"code": "ms/fcps", "name": "MS FCPS", "duration": "60"}, {"code": "", "name": "", "duration": ""}], self.artifacts)
        records = self.command._map_training_records([{"email": "bob@example.com", "program": "ms/fcps", "start_date": "2025-01-01"}], self.artifacts)
        self.assertEqual(supervisors[0]["department_code"], "MED")
        self.assertEqual(residents[0]["year"], "2")
        self.assertEqual(programs[0]["program_code"], "MS-FCPS")
        self.assertEqual(records[0]["program_code"], "MS-FCPS")

    def test_csv_bytes(self):
        self.assertIn(b"name", self.command._rows_to_csv_bytes([{"name": "Ada"}]))
