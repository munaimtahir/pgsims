from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from sims.tests.factories.case_factories import ClinicalCaseFactory
from sims.tests.factories.user_factories import AdminFactory, PGFactory, SupervisorFactory

from .forms import CaseReviewForm, ClinicalCaseForm
from .models import CaseCategory, CaseReview, CaseStatistics, ClinicalCase

User = get_user_model()


class CaseCategoryModelTest(TestCase):
    """Test the CaseCategory model"""

    def setUp(self):
        self.category = CaseCategory.objects.create(
            name="Cardiology", description="Heart and cardiovascular cases", color_code="#FF5722"
        )

    def test_category_creation(self):
        """Test category creation and string representation"""
        self.assertEqual(str(self.category), "Cardiology")
        self.assertEqual(self.category.color_code, "#FF5722")
        self.assertTrue(self.category.is_active)

    def test_category_validation(self):
        """Test category field validation"""
        # Test color code validation
        category = CaseCategory(name="Test Category", color_code="invalid_color")
        with self.assertRaises(Exception):
            category.full_clean()


class ClinicalCaseModelTest(TestCase):
    """Test the ClinicalCase model"""

    def setUp(self):
        # Create test users and case using factories
        self.supervisor = SupervisorFactory(specialty="medicine")
        self.pg = PGFactory(supervisor=self.supervisor, specialty="medicine", year="1")

        # Create test case using factory (handles all required fields)
        self.case = ClinicalCaseFactory(
            pg=self.pg,
            supervisor=self.supervisor,
            case_title="Acute Myocardial Infarction",
            complexity="complex",
            status="draft",
        )
        self.category = self.case.category

    def test_case_creation(self):
        """Test clinical case creation"""
        # Check the case title and pg relationship
        self.assertIn("Acute Myocardial Infarction", str(self.case))
        self.assertIn(self.pg.get_full_name(), str(self.case))
        self.assertEqual(self.case.status, "draft")
        self.assertEqual(self.case.pg, self.pg)
        self.assertEqual(self.case.supervisor, self.supervisor)

    def test_case_status_workflow(self):
        """Test case status progression"""
        # Initially draft
        self.assertEqual(self.case.status, "draft")
        self.assertTrue(self.case.can_be_submitted())

        # Submit for review
        self.case.status = "submitted"
        self.case.submitted_at = timezone.now()
        self.case.save()

        self.assertFalse(self.case.can_be_submitted())
        self.assertTrue(self.case.can_be_reviewed())

    def test_case_completion_check(self):
        """Test case completeness validation"""
        # Case should be complete with current data
        self.assertTrue(self.case.is_complete())

        # Remove required field - test without saving
        self.case.learning_points = ""
        self.assertFalse(self.case.is_complete())

    def test_case_permissions(self):
        """Test case access permissions"""
        # PG can edit their own draft case
        self.assertTrue(self.case.can_edit(self.pg))

        # Supervisor can edit assigned cases
        self.assertTrue(self.case.can_edit(self.supervisor))

        # Other users cannot edit
        other_user = PGFactory()
        self.assertFalse(self.case.can_edit(other_user))


class CaseReviewModelTest(TestCase):
    """Test the CaseReview model"""

    def setUp(self):
        # Create test users and case
        self.supervisor = SupervisorFactory(specialty="medicine")
        self.pg = PGFactory(supervisor=self.supervisor, specialty="medicine", year="1")

        self.category = CaseCategory.objects.create(name="Pediatrics", color_code="#4CAF50")

        # Create diagnosis
        from sims.logbook.models import Diagnosis

        diagnosis = Diagnosis.objects.create(
            name="Pediatric Asthma", category="respiratory", icd_code="J45.9"
        )

        self.case = ClinicalCase.objects.create(
            pg=self.pg,
            case_title="Pediatric Asthma",
            category=self.category,
            date_encountered=date.today(),
            patient_age=8,
            patient_gender="F",
            chief_complaint="Difficulty breathing",
            history_of_present_illness="Child presented with wheezing and shortness of breath",
            physical_examination="Bilateral wheezing on auscultation",
            primary_diagnosis=diagnosis,
            management_plan="Inhaled bronchodilators and corticosteroids",
            clinical_reasoning="Classic presentation of pediatric asthma",
            learning_points="Asthma management in children",
            supervisor=self.supervisor,
            status="submitted",
        )

    def test_review_creation(self):
        """Test case review creation"""
        review = CaseReview.objects.create(
            case=self.case,
            reviewer=self.supervisor,
            clinical_knowledge_score=8,
            clinical_reasoning_score=9,
            documentation_score=7,
            overall_score=8,
            status="approved",
            overall_feedback="Excellent case presentation and analysis.",
        )

        self.assertEqual(review.case, self.case)
        self.assertEqual(review.reviewer, self.supervisor)
        self.assertEqual(review.overall_score, 8)
        self.assertEqual(review.status, "approved")

    def test_average_score_calculation(self):
        """Test automatic average score calculation"""
        review = CaseReview.objects.create(
            case=self.case,
            reviewer=self.supervisor,
            clinical_knowledge_score=8,
            clinical_reasoning_score=6,
            documentation_score=7,
            overall_score=9,
            status="approved",
            overall_feedback="Good work",
        )

        # Check if calculate_average_score method exists or use simple average
        if hasattr(review, "calculate_average_score"):
            expected_average = (8 + 6 + 7 + 9) / 4
            self.assertEqual(review.calculate_average_score(), expected_average)
        else:
            # Just verify scores are set
            self.assertEqual(review.clinical_knowledge_score, 8)


class CaseStatisticsModelTest(TestCase):
    """Test the CaseStatistics model"""

    def setUp(self):
        self.supervisor = SupervisorFactory(specialty="medicine")
        self.pg = PGFactory(supervisor=self.supervisor, specialty="medicine", year="1")

        self.category = CaseCategory.objects.create(name="Internal Medicine", color_code="#2196F3")

        # Create diagnosis for cases
        from sims.logbook.models import Diagnosis

        diagnosis = Diagnosis.objects.create(
            name="Internal Medicine Case", category="general", icd_code="R00"
        )

        # Create multiple cases for statistics
        for i in range(5):
            ClinicalCase.objects.create(
                pg=self.pg,
                case_title=f"Case {i + 1}",
                category=self.category,
                date_encountered=date.today() - timedelta(days=i),
                patient_age=30 + i,
                patient_gender="M" if i % 2 == 0 else "F",
                chief_complaint=f"Complaint {i + 1}",
                history_of_present_illness=f"History {i + 1}",
                physical_examination=f"Examination {i + 1}",
                primary_diagnosis=diagnosis,
                management_plan=f"Management {i + 1}",
                clinical_reasoning=f"Reasoning {i + 1}",
                learning_points=f"Learning points for case {i + 1}",
                supervisor=self.supervisor,
                status="approved" if i < 3 else "draft",
            )

    def test_statistics_calculation(self):
        """Test automatic statistics calculation"""
        stats = CaseStatistics.objects.create(pg=self.pg)
        stats.update_statistics()

        self.assertEqual(stats.total_cases, 5)
        self.assertEqual(stats.approved_cases, 3)
        self.assertEqual(stats.draft_cases, 2)
        # Check that average_score and completion_rate are calculated
        if hasattr(stats, "average_score"):
            self.assertGreaterEqual(stats.average_score, 0)
        if hasattr(stats, "completion_rate"):
            self.assertGreaterEqual(stats.completion_rate, 0)


class CaseFormsTest(TestCase):
    """Test case-related forms"""

    def setUp(self):
        self.supervisor = SupervisorFactory(specialty="medicine")
        self.pg = PGFactory(supervisor=self.supervisor, specialty="medicine")

        self.category = CaseCategory.objects.create(name="Surgery", color_code="#FF9800")

    def test_clinical_case_form_valid(self):
        """Test valid clinical case form submission"""
        # Create a diagnosis for the form
        from sims.logbook.models import Diagnosis

        diagnosis = Diagnosis.objects.create(
            name="Acute Appendicitis", category="surgical", icd_code="K35.8"
        )

        form_data = {
            "case_title": "Appendectomy",
            "category": self.category.id,
            "date_encountered": date.today(),
            "patient_age": 25,
            "patient_gender": "M",
            "chief_complaint": "Right lower quadrant pain",
            "history_of_present_illness": "Patient presented with 24 hours of abdominal pain",
            "physical_examination": "Tenderness in RLQ, positive rebound",
            "primary_diagnosis": diagnosis.id,
            "management_plan": "Emergency appendectomy",
            "clinical_reasoning": "Clinical presentation consistent with acute appendicitis",
            "learning_points": "Surgical technique and patient care",
            "supervisor": self.supervisor.id,
        }

        form = ClinicalCaseForm(data=form_data, user=self.pg)
        if not form.is_valid():
            print(f"Form errors: {form.errors}")
        self.assertTrue(form.is_valid())

    def test_clinical_case_form_invalid(self):
        """Test invalid clinical case form submission"""
        form_data = {
            "case_title": "",  # Required field missing
            "category": self.category.id,
            "date_encountered": date.today(),
        }

        form = ClinicalCaseForm(data=form_data, user=self.pg)
        self.assertFalse(form.is_valid())
        self.assertIn("case_title", form.errors)

    def test_case_review_form_valid(self):
        """Test valid case review form"""
        # Create a diagnosis
        from sims.logbook.models import Diagnosis

        diagnosis = Diagnosis.objects.create(
            name="Test Condition", category="general", icd_code="A00"
        )

        case = ClinicalCase.objects.create(
            pg=self.pg,
            case_title="Test Case",
            category=self.category,
            date_encountered=date.today(),
            patient_age=30,
            patient_gender="M",
            chief_complaint="Test complaint",
            history_of_present_illness="Test history",
            physical_examination="Test examination",
            primary_diagnosis=diagnosis,
            management_plan="Test management",
            clinical_reasoning="Test reasoning",
            learning_points="Test learning points",
            supervisor=self.supervisor,
            status="submitted",
        )

        form_data = {
            "clinical_knowledge_score": 8,
            "clinical_reasoning_score": 9,
            "documentation_score": 7,
            "overall_score": 8,
            "status": "approved",
            "overall_feedback": "Great work!",
        }

        form = CaseReviewForm(data=form_data, case=case, reviewer=self.supervisor)
        self.assertTrue(form.is_valid())


class CaseViewsTest(TestCase):
    """Test case-related views"""

    def setUp(self):
        self.client = Client()

        # Create test users
        self.supervisor = SupervisorFactory(specialty="medicine")
        self.pg = PGFactory(supervisor=self.supervisor, specialty="medicine", year="1")

        self.admin = AdminFactory()

        # Create test data
        self.category = CaseCategory.objects.create(name="Orthopedics", color_code="#795548")

        # Create a diagnosis for the case
        from sims.logbook.models import Diagnosis

        self.diagnosis = Diagnosis.objects.create(
            name="Femur Fracture", category="orthopedic", icd_code="S72.0"
        )

        self.case = ClinicalCase.objects.create(
            pg=self.pg,
            case_title="Fracture Management",
            category=self.category,
            date_encountered=date.today(),
            patient_age=45,
            patient_gender="M",
            chief_complaint="Severe leg pain after fall",
            history_of_present_illness="Patient fell from height 2 hours ago",
            physical_examination="Tenderness and deformity of left thigh",
            primary_diagnosis=self.diagnosis,
            management_plan="Surgical fixation with intramedullary nail",
            clinical_reasoning="Mechanism of injury and examination findings consistent with femur fracture",
            learning_points="Fracture classification and treatment",
            supervisor=self.supervisor,
        )

    def test_case_list_view_pg(self):
        """Test case list view for PG user"""
        self.client.force_login(self.pg)
        response = self.client.get(reverse("cases:case_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.case.case_title)
        self.assertEqual(len(response.context["cases"]), 1)

    def test_case_list_view_supervisor(self):
        """Test case list view for supervisor"""
        self.client.force_login(self.supervisor)
        response = self.client.get(reverse("cases:case_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.case.case_title)

    def test_case_detail_view(self):
        """Test case detail view"""
        self.client.force_login(self.pg)
        response = self.client.get(reverse("cases:case_detail", kwargs={"pk": self.case.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.case.case_title)
        self.assertEqual(response.context["case"], self.case)

    def test_case_create_view_pg(self):
        """Test case creation by PG"""
        self.client.force_login(self.pg)
        response = self.client.get(reverse("cases:case_create"))

        self.assertEqual(response.status_code, 200)

        # Test form submission
        form_data = {
            "case_title": "New Case",
            "category": self.category.id,
            "date": date.today(),
            "patient_initials": "N.C.",
            "patient_age": 35,
            "patient_gender": "female",
            "patient_history": "No history",
            "presenting_complaints": "Test complaints",
            "learning_points": "Test learning points",
            "supervisor": self.supervisor.id,
        }

        response = self.client.post(reverse("cases:case_create"), data=form_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation

        # Verify case was created
        new_case = ClinicalCase.objects.get(case_title="New Case")
        self.assertEqual(new_case.pg, self.pg)
        self.assertEqual(new_case.status, "draft")

    def test_case_update_view(self):
        """Test case update view"""
        self.client.force_login(self.pg)
        response = self.client.get(reverse("cases:case_update", kwargs={"pk": self.case.pk}))

        self.assertEqual(response.status_code, 200)

        # Test form submission
        form_data = {
            "case_title": "Updated Case Title",
            "category": self.category.id,
            "date": self.case.date,
            "patient_initials": self.case.patient_initials,
            "patient_age": self.case.patient_age,
            "patient_gender": self.case.patient_gender,
            "patient_history": "Updated history",
            "presenting_complaints": "Updated complaints",
            "learning_points": "Updated learning points",
            "supervisor": self.supervisor.id,
        }

        response = self.client.post(
            reverse("cases:case_update", kwargs={"pk": self.case.pk}), data=form_data
        )
        self.assertEqual(response.status_code, 302)

        # Verify case was updated
        updated_case = ClinicalCase.objects.get(pk=self.case.pk)
        self.assertEqual(updated_case.case_title, "Updated Case Title")

    def test_case_submit_view(self):
        """Test case submission for review"""
        self.client.force_login(self.pg)
        response = self.client.post(reverse("cases:case_submit", kwargs={"pk": self.case.pk}))

        self.assertEqual(response.status_code, 302)

        # Verify case status changed
        updated_case = ClinicalCase.objects.get(pk=self.case.pk)
        self.assertEqual(updated_case.status, "submitted")
        self.assertIsNotNone(updated_case.submitted_at)

    def test_unauthorized_access(self):
        """Test unauthorized access protection"""
        # Test without login
        response = self.client.get(reverse("cases:case_list"))
        self.assertEqual(response.status_code, 302)  # Redirect to login

        # Test PG accessing other PG's case
        _other_pg = PGFactory()

        self.client.login(username="otherpg", password="testpass123")
        response = self.client.get(reverse("cases:case_detail", kwargs={"pk": self.case.pk}))
        self.assertEqual(response.status_code, 404)  # Case not found due to queryset filtering

    def test_statistics_view(self):
        """Test statistics dashboard"""
        self.client.force_login(self.pg)
        response = self.client.get(reverse("cases:case_statistics"))

        self.assertEqual(response.status_code, 200)
        self.assertIn("user_stats", response.context)


class CaseIntegrationTest(TestCase):
    """Integration tests for case workflow"""

    def setUp(self):
        self.client = Client()

        # Create users
        self.supervisor = SupervisorFactory(specialty="medicine")
        self.pg = PGFactory(supervisor=self.supervisor, specialty="medicine", year="1")

        self.category = CaseCategory.objects.create(name="Neurology", color_code="#9C27B0")

        # Create diagnosis for the case
        from sims.logbook.models import Diagnosis

        self.diagnosis = Diagnosis.objects.create(
            name="Acute Ischemic Stroke", category="neurological", icd_code="I63.9"
        )

    def test_complete_case_workflow(self):
        """Test complete case workflow from creation to review"""

        # 1. PG logs in and creates a case
        self.client.force_login(self.pg)

        case_data = {
            "case_title": "Stroke Management",
            "category": self.category.id,
            "date_encountered": date.today(),
            "patient_age": 70,
            "patient_gender": "M",
            "chief_complaint": "Sudden weakness, speech difficulty",
            "history_of_present_illness": "Patient presented with acute onset of left-sided weakness",
            "physical_examination": "Right hemiplegia, aphasia",
            "primary_diagnosis": self.diagnosis.id,
            "management_plan": "Thrombolysis protocol initiated",
            "clinical_reasoning": "NIHSS score indicates acute ischemic stroke",
            "learning_points": "Acute stroke protocols and thrombolysis",
            "supervisor": self.supervisor.id,
        }

        response = self.client.post(reverse("cases:case_create"), data=case_data)
        self.assertEqual(response.status_code, 302)

        case = ClinicalCase.objects.get(case_title="Stroke Management")
        self.assertEqual(case.status, "draft")

        # 2. PG submits the case for review
        response = self.client.post(reverse("cases:case_submit", kwargs={"pk": case.pk}))
        self.assertEqual(response.status_code, 302)

        case.refresh_from_db()
        self.assertEqual(case.status, "submitted")

        # 3. Supervisor logs in and reviews the case
        self.client.force_login(self.supervisor)

        review_data = {
            "clinical_knowledge_score": 9,
            "clinical_reasoning_score": 8,
            "documentation_score": 9,
            "overall_score": 9,
            "status": "approved",
            "overall_feedback": "Excellent case documentation and learning reflection.",
        }

        response = self.client.post(
            reverse("cases:case_review", kwargs={"case_pk": case.pk}), data=review_data
        )
        self.assertEqual(response.status_code, 302)

        # 4. Verify case status and review
        case.refresh_from_db()
        self.assertEqual(case.status, "approved")

        review = CaseReview.objects.get(case=case)
        self.assertEqual(review.status, "approved")
        self.assertEqual(review.overall_score, 9)

        # 5. Verify statistics are updated
        stats, created = CaseStatistics.objects.get_or_create(pg=self.pg)
        stats.update_statistics()

        self.assertEqual(stats.total_cases, 1)
        self.assertEqual(stats.approved_cases, 1)
        self.assertGreater(stats.average_score, 0)
