from datetime import date

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from sims.cases.models import CaseCategory, ClinicalCase
from sims.logbook.models import Diagnosis
from sims.users.models import User


class CasesAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.supervisor = User.objects.create_user(
            username="cases_supervisor",
            password="pass12345",
            role="supervisor",
            specialty="medicine",
            email="cases_supervisor@example.com",
        )
        self.pg = User.objects.create_user(
            username="cases_pg",
            password="pass12345",
            role="pg",
            specialty="medicine",
            year="1",
            supervisor=self.supervisor,
            email="cases_pg@example.com",
        )
        self.pg2 = User.objects.create_user(
            username="cases_pg_2",
            password="pass12345",
            role="pg",
            specialty="medicine",
            year="1",
            supervisor=self.supervisor,
            email="cases_pg2@example.com",
        )
        self.admin = User.objects.create_user(
            username="cases_admin", password="pass12345", role="admin", email="cases_admin@example.com"
        )
        self.utrmc_user = User.objects.create_user(
            username="cases_utrmc_user",
            password="pass12345",
            role="utrmc_user",
            email="cases_utrmc_user@example.com",
        )
        self.category = CaseCategory.objects.create(name="Medicine", color_code="#123456")
        self.diagnosis = Diagnosis.objects.create(name="Acute Bronchitis", category="respiratory")
        self.base_payload = {
            "case_title": "Test Case",
            "category": self.category.id,
            "date_encountered": str(date.today()),
            "patient_age": 45,
            "patient_gender": "M",
            "chief_complaint": "Shortness of breath",
            "history_of_present_illness": "2 days history",
            "physical_examination": "Reduced air entry",
            "management_plan": "Nebulization and antibiotics",
            "clinical_reasoning": "Likely infective airway disease",
            "learning_points": "Early escalation",
            "primary_diagnosis": self.diagnosis.id,
        }

    def test_pg_can_create_list_submit_and_edit_own_case(self):
        self.client.force_authenticate(self.pg)
        create_response = self.client.post(
            reverse("cases_api:my_cases"), self.base_payload, format="json"
        )
        self.assertEqual(create_response.status_code, 201)
        case_id = create_response.data["id"]

        list_response = self.client.get(reverse("cases_api:my_cases"))
        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(len(list_response.data), 1)

        patch_response = self.client.patch(
            reverse("cases_api:my_case_detail", kwargs={"pk": case_id}),
            {"learning_points": "Updated learning point"},
            format="json",
        )
        self.assertEqual(patch_response.status_code, 200)

        submit_response = self.client.post(reverse("cases_api:my_case_submit", kwargs={"pk": case_id}))
        self.assertEqual(submit_response.status_code, 200)
        self.assertEqual(submit_response.data["status"], "submitted")

    def test_pg_cannot_view_other_pg_case(self):
        case = ClinicalCase.objects.create(
            pg=self.pg,
            supervisor=self.supervisor,
            case_title="Private Case",
            category=self.category,
            date_encountered=date.today(),
            patient_age=50,
            patient_gender="F",
            chief_complaint="Pain",
            history_of_present_illness="History",
            physical_examination="Exam",
            management_plan="Plan",
            clinical_reasoning="Reasoning",
            learning_points="Learning",
            primary_diagnosis=self.diagnosis,
            status="draft",
        )
        self.client.force_authenticate(self.pg2)
        response = self.client.get(reverse("cases_api:my_case_detail", kwargs={"pk": case.id}))
        self.assertEqual(response.status_code, 404)

    def test_supervisor_pending_and_review_workflow(self):
        case = ClinicalCase.objects.create(
            pg=self.pg,
            supervisor=self.supervisor,
            case_title="Pending Case",
            category=self.category,
            date_encountered=date.today(),
            patient_age=50,
            patient_gender="F",
            chief_complaint="Pain",
            history_of_present_illness="History",
            physical_examination="Exam",
            management_plan="Plan",
            clinical_reasoning="Reasoning",
            learning_points="Learning",
            primary_diagnosis=self.diagnosis,
            status="submitted",
        )
        self.client.force_authenticate(self.supervisor)
        pending = self.client.get(reverse("cases_api:pending_cases"))
        self.assertEqual(pending.status_code, 200)
        self.assertEqual(len(pending.data), 1)

        review = self.client.post(
            reverse("cases_api:review_case", kwargs={"pk": case.id}),
            {"status": "needs_revision", "overall_feedback": "Please improve details"},
            format="json",
        )
        self.assertEqual(review.status_code, 200)
        case.refresh_from_db()
        self.assertEqual(case.status, "needs_revision")

    def test_utrmc_user_read_only_pending_allowed_review_denied(self):
        case = ClinicalCase.objects.create(
            pg=self.pg,
            supervisor=self.supervisor,
            case_title="Pending Case 2",
            category=self.category,
            date_encountered=date.today(),
            patient_age=50,
            patient_gender="F",
            chief_complaint="Pain",
            history_of_present_illness="History",
            physical_examination="Exam",
            management_plan="Plan",
            clinical_reasoning="Reasoning",
            learning_points="Learning",
            primary_diagnosis=self.diagnosis,
            status="submitted",
        )
        self.client.force_authenticate(self.utrmc_user)
        pending = self.client.get(reverse("cases_api:pending_cases"))
        self.assertEqual(pending.status_code, 200)
        review = self.client.post(
            reverse("cases_api:review_case", kwargs={"pk": case.id}),
            {"status": "approved", "overall_feedback": "OK"},
            format="json",
        )
        self.assertEqual(review.status_code, 403)

    def test_statistics_endpoint(self):
        ClinicalCase.objects.create(
            pg=self.pg,
            supervisor=self.supervisor,
            case_title="Approved",
            category=self.category,
            date_encountered=date.today(),
            patient_age=50,
            patient_gender="F",
            chief_complaint="Pain",
            history_of_present_illness="History",
            physical_examination="Exam",
            management_plan="Plan",
            clinical_reasoning="Reasoning",
            learning_points="Learning",
            primary_diagnosis=self.diagnosis,
            status="approved",
        )
        self.client.force_authenticate(self.admin)
        response = self.client.get(reverse("cases_api:statistics"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("total_cases", response.data)
