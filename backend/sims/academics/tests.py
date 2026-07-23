from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from sims.academics.models import (
    AcademicPeriod,
    AcademicSession,
    Department,
    ResidentTrainingRecord,
    SupervisorReviewQueueItem,
    EvaluationFormTemplate,
    LogbookCategory,
    EvaluationSubmission,
    LogbookEntry,
)
from sims.academics.services import create_training_record
from sims.rotations.models import Hospital
from sims.supervision.services import create_supervisor_assignment
from sims.training.models import TrainingProgram
from sims.users.models import ResidentProfile, SupervisorProfile, SupportStaffProfile

User = get_user_model()


class AcademicsFoundationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.department = Department.objects.create(name="Medicine", code="MED", active=True)
        self.session = AcademicSession.objects.create(name="Session 2026", code="S2026", active=True)
        self.hospital = Hospital.objects.create(name="Allied Hospital", code="AH")
        self.program = TrainingProgram.objects.create(
            name="FCPS Medicine",
            code="FCPS-MED",
            duration_months=48,
            degree_type=TrainingProgram.DEGREE_FCPS,
            department=self.department,
            active=True,
        )
        self.admin = User.objects.create_user(username="admin1", password="pass12345", role="ADMIN")
        self.resident_user = User.objects.create_user(username="pgr001", password="pass12345", role="RESIDENT")
        self.resident = ResidentProfile.objects.create(
            user=self.resident_user,
            hospital=self.hospital,
            department_ref=self.department,
            program_ref=self.program,
            academic_session_ref=self.session,
            profile_status="COMPLETE",
        )
        self.supervisor_user = User.objects.create_user(username="sup001", password="pass12345", role="SUPERVISOR")
        self.supervisor = SupervisorProfile.objects.create(
            user=self.supervisor_user,
            hospital=self.hospital,
            department_ref=self.department,
            program_ref=self.program,
            profile_status="COMPLETE",
        )
        self.staff_user = User.objects.create_user(username="staff001", password="pass12345", role="SUPPORT_STAFF")
        self.staff = SupportStaffProfile.objects.create(user=self.staff_user, hospital=self.hospital, department_ref=self.department)

    def test_create_training_record_prefills_profile_fields(self):
        record = create_training_record(
            resident=self.resident,
            start_date=date(2026, 7, 1),
            expected_end_date=date(2027, 6, 30),
            training_year=1,
            actor=self.admin,
        )
        self.assertEqual(record.program, self.program)
        self.assertEqual(record.department, self.department)
        self.assertEqual(record.training_site, self.hospital)
        self.assertEqual(record.academic_session, self.session)

    def test_only_one_active_training_record_per_resident(self):
        create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        with self.assertRaises(Exception):
            create_training_record(resident=self.resident, start_date=date(2026, 8, 1), actor=self.admin)

    def test_admin_can_create_training_record_via_api(self):
        self.client.force_authenticate(self.admin)
        response = self.client.post(
            "/api/academics/training-records/",
            {
                "resident": self.resident.id,
                "program": self.program.id,
                "academic_session": self.session.id,
                "training_site": self.hospital.id,
                "department": self.department.id,
                "start_date": "2026-07-01",
                "expected_end_date": "2027-06-30",
                "training_year": 1,
                "notes": "Pilot record",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ResidentTrainingRecord.objects.count(), 1)

    def test_resident_can_view_own_academic_summary(self):
        create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        create_supervisor_assignment(
            resident=self.resident,
            supervisor=self.supervisor,
            assignment_type="PRIMARY",
            start_date=date(2026, 7, 1),
            actor=self.admin,
        )
        self.client.force_authenticate(self.resident_user)
        response = self.client.get(f"/api/academics/residents/{self.resident.id}/summary/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["readiness"]["has_active_training_record"])
        self.assertTrue(response.data["readiness"]["has_primary_supervisor"])

    def test_supervisor_can_only_view_assigned_resident_summary(self):
        other_user = User.objects.create_user(username="pgr002", password="pass12345", role="RESIDENT")
        other_resident = ResidentProfile.objects.create(user=other_user, hospital=self.hospital, department_ref=self.department)
        self.client.force_authenticate(self.supervisor_user)
        denied = self.client.get(f"/api/academics/residents/{other_resident.id}/summary/")
        self.assertEqual(denied.status_code, status.HTTP_403_FORBIDDEN)

        create_supervisor_assignment(
            resident=self.resident,
            supervisor=self.supervisor,
            assignment_type="PRIMARY",
            start_date=date(2026, 7, 1),
            actor=self.admin,
        )
        allowed = self.client.get(f"/api/academics/residents/{self.resident.id}/summary/")
        self.assertEqual(allowed.status_code, status.HTTP_200_OK)

    def test_support_staff_cannot_mutate_training_records(self):
        self.client.force_authenticate(self.staff_user)
        response = self.client.post(
            "/api/academics/training-records/",
            {"resident": self.resident.id, "start_date": "2026-07-01"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_data_quality_endpoint_reports_missing_training_record(self):
        self.client.force_authenticate(self.admin)
        response = self.client.get("/api/academics/data-quality/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["summary"]["residents_without_training_record"], 1)

    def test_review_queue_item_flow(self):
        record = create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        create_supervisor_assignment(
            resident=self.resident,
            supervisor=self.supervisor,
            assignment_type="PRIMARY",
            start_date=date(2026, 7, 1),
            actor=self.admin,
        )
        self.client.force_authenticate(self.admin)
        response = self.client.post(
            "/api/academics/review-queue/",
            {
                "resident": self.resident.id,
                "supervisor": self.supervisor.id,
                "training_record": record.id,
                "queue_type": "TRAINING_RECORD_REVIEW",
                "due_date": "2026-07-10",
                "notes": "Check setup",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        item_id = response.data["id"]

        self.client.force_authenticate(self.supervisor_user)
        done = self.client.patch(
            f"/api/academics/review-queue/{item_id}/",
            {"status": "DONE"},
            format="json",
        )
        self.assertEqual(done.status_code, status.HTTP_200_OK)
        self.assertEqual(SupervisorReviewQueueItem.objects.get(id=item_id).status, "DONE")

    def test_seed_command_is_idempotent_minimum(self):
        self.client.force_authenticate(self.admin)
        first = self.client.post("/api/academics/seed/")
        second = self.client.post("/api/academics/seed/")
        self.assertEqual(first.status_code, status.HTTP_200_OK)
        self.assertEqual(second.status_code, status.HTTP_200_OK)
        self.assertEqual(AcademicPeriod.objects.count(), 2)

    def test_evaluation_submission_and_review_workflow(self):
        # Create Evaluation Template
        template = EvaluationFormTemplate.objects.create(
            code="EVAL-TEST",
            name="Test Template",
            form_type="ROTATION_EVALUATION",
            is_active=True,
        )
        record = create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        create_supervisor_assignment(
            resident=self.resident,
            supervisor=self.supervisor,
            assignment_type="PRIMARY",
            start_date=date(2026, 7, 1),
            actor=self.admin,
        )

        # 1. Resident creates evaluation draft
        self.client.force_authenticate(self.resident_user)
        response = self.client.post(
            "/api/academics/evaluation-submissions/",
            {
                "template": template.id,
                "resident_comments": "Did well",
                "responses": [
                    {"field_key": "clinical_skills", "value_number": 4.00}
                ]
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        submission_id = response.data["id"]
        self.assertEqual(response.data["status"], "DRAFT")

        # 2. Resident updates draft
        response = self.client.patch(
            f"/api/academics/evaluation-submissions/{submission_id}/",
            {"resident_comments": "Updated comments"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["resident_comments"], "Updated comments")

        # 3. Resident submits evaluation
        response = self.client.post(
            f"/api/academics/evaluation-submissions/{submission_id}/submit/",
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "SUBMITTED")

        # Verify a Review Queue item is created
        self.assertTrue(
            SupervisorReviewQueueItem.objects.filter(
                resident=self.resident,
                supervisor=self.supervisor,
                queue_type="EVALUATION_REVIEW",
                status="PENDING",
            ).exists()
        )

        # 4. Supervisor starts review
        self.client.force_authenticate(self.supervisor_user)
        response = self.client.post(
            f"/api/academics/evaluation-submissions/{submission_id}/start_review/",
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "UNDER_REVIEW")

        # 5. Supervisor approves evaluation
        response = self.client.post(
            f"/api/academics/evaluation-submissions/{submission_id}/approve/",
            {
                "supervisor_comments": "Approved!",
                "score": 4.5,
                "max_score": 5.0,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "APPROVED")
        self.assertEqual(response.data["score"], "4.50")

        # Verify Queue Item is DONE
        queue_item = SupervisorReviewQueueItem.objects.get(
            resident=self.resident,
            supervisor=self.supervisor,
            queue_type="EVALUATION_REVIEW"
        )
        self.assertEqual(queue_item.status, "DONE")

    def test_logbook_entry_and_verification_workflow(self):
        category = LogbookCategory.objects.create(
            code="LOG-TEST",
            name="Test Category",
            category_type="PROCEDURE",
            minimum_required=3,
            is_active=True,
        )
        record = create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        create_supervisor_assignment(
            resident=self.resident,
            supervisor=self.supervisor,
            assignment_type="PRIMARY",
            start_date=date(2026, 7, 1),
            actor=self.admin,
        )

        # 1. Resident creates logbook entry draft with procedure record
        self.client.force_authenticate(self.resident_user)
        response = self.client.post(
            "/api/academics/logbook-entries/",
            {
                "category": category.id,
                "entry_date": "2026-07-15",
                "title": "Central Line",
                "procedure_record": {
                    "procedure_name": "Ultrasound Guided IJ Central Line",
                    "role_performed": "PERFORMED_UNDER_SUPERVISION",
                    "complexity": "HIGH",
                    "outcome": "SUCCESS",
                }
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        entry_id = response.data["id"]
        self.assertEqual(response.data["status"], "DRAFT")
        self.assertEqual(response.data["procedure_record"]["complexity"], "HIGH")

        # 2. Resident submits logbook entry
        response = self.client.post(
            f"/api/academics/logbook-entries/{entry_id}/submit/",
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "SUBMITTED")

        # Verify a Logbook Review Queue item is created
        self.assertTrue(
            SupervisorReviewQueueItem.objects.filter(
                resident=self.resident,
                supervisor=self.supervisor,
                queue_type="LOGBOOK_REVIEW",
                status="PENDING",
            ).exists()
        )

        # 3. Supervisor returns for revision
        self.client.force_authenticate(self.supervisor_user)
        response = self.client.post(
            f"/api/academics/logbook-entries/{entry_id}/return_revision/",
            {"supervisor_comments": "Please add detail"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "RETURNED")

        # 4. Resident resubmits
        self.client.force_authenticate(self.resident_user)
        response = self.client.post(
            f"/api/academics/logbook-entries/{entry_id}/submit/",
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "SUBMITTED")

        # 5. Supervisor verifies entry
        self.client.force_authenticate(self.supervisor_user)
        response = self.client.post(
            f"/api/academics/logbook-entries/{entry_id}/verify/",
            {"supervisor_comments": "Looks good now"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "VERIFIED")

    def test_progress_summaries_and_data_quality_checks(self):
        record = create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        create_supervisor_assignment(
            resident=self.resident,
            supervisor=self.supervisor,
            assignment_type="PRIMARY",
            start_date=date(2026, 7, 1),
            actor=self.admin,
        )

        # Check my-progress api
        self.client.force_authenticate(self.resident_user)
        response = self.client.get("/api/academics/my-progress/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["training_record_status"], "ACTIVE")

        # Check supervisor workload api
        self.client.force_authenticate(self.supervisor_user)
        response = self.client.get("/api/academics/supervisor-workload/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["assigned_residents_count"], 1)

        # Check admin overview and DQ api
        self.client.force_authenticate(self.admin)
        response = self.client.get("/api/academics/admin-workflow-overview/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_active_residents"], 1)

        response = self.client.get("/api/academics/workflow-data-quality/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("residents_with_active_record_no_evaluations", response.data["summary"])

    def test_seed_workflows_command(self):
        self.client.force_authenticate(self.admin)
        response = self.client.post("/api/academics/seed-workflows/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(response.data["evaluation_submissions"], 0)

    def test_brick11_monitoring_and_reports(self):
        # Setup training record & supervisor assignment
        record = create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        create_supervisor_assignment(
            resident=self.resident,
            supervisor=self.supervisor,
            assignment_type="PRIMARY",
            start_date=date(2026, 7, 1),
            actor=self.admin,
        )

        # 1. Test Admin Dashboard Monitoring View
        self.client.force_authenticate(self.admin)
        response = self.client.get("/api/academics/monitoring/admin-dashboard/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_residents"], 1)

        # Resident should be blocked from admin monitoring
        self.client.force_authenticate(self.resident_user)
        response = self.client.get("/api/academics/monitoring/admin-dashboard/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # 2. Test Supervisor Dashboard Monitoring View
        self.client.force_authenticate(self.supervisor_user)
        response = self.client.get("/api/academics/monitoring/supervisor-dashboard/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["assigned_residents_count"], 1)

        # Resident should be blocked from supervisor dashboard
        self.client.force_authenticate(self.resident_user)
        response = self.client.get("/api/academics/monitoring/supervisor-dashboard/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # 3. Test My Progress Monitoring View
        self.client.force_authenticate(self.resident_user)
        response = self.client.get("/api/academics/monitoring/my-progress/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["training_record_status"], "ACTIVE")

        # 4. Department/Program/Session summaries (Admin only)
        self.client.force_authenticate(self.admin)
        response = self.client.get("/api/academics/monitoring/departments/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response = self.client.get("/api/academics/monitoring/programs/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get("/api/academics/monitoring/sessions/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.force_authenticate(self.resident_user)
        response = self.client.get("/api/academics/monitoring/departments/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # 5. Resident Progress Report View
        self.client.force_authenticate(self.admin)
        response = self.client.get(f"/api/academics/reports/resident-progress/{self.resident.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["resident"]["username"], self.resident_user.username)

        # Resident should only access self progress report
        self.client.force_authenticate(self.resident_user)
        response = self.client.get(f"/api/academics/reports/resident-progress/{self.resident.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 6. Supervisor Workload Report View
        self.client.force_authenticate(self.admin)
        response = self.client.get(f"/api/academics/reports/supervisor-workload/{self.supervisor.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["supervisor"]["username"], self.supervisor_user.username)

        # 7. Evaluation & Logbook reports
        self.client.force_authenticate(self.admin)
        response = self.client.get("/api/academics/reports/evaluations/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get("/api/academics/reports/logbook/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 8. Data Quality Report View
        response = self.client.get("/api/academics/reports/data-quality/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 9. CSV Exports
        response = self.client.get("/api/academics/reports/evaluations/export.csv")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response["Content-Type"], "text/csv")

        response = self.client.get("/api/academics/reports/logbook/export.csv")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response["Content-Type"], "text/csv")

        response = self.client.get("/api/academics/reports/data-quality/export.csv")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response["Content-Type"], "text/csv")

        response = self.client.get(f"/api/academics/reports/resident-progress/export.csv?resident_id={self.resident.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response["Content-Type"], "text/csv")

        response = self.client.get(f"/api/academics/reports/supervisor-workload/export.csv?supervisor_id={self.supervisor.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response["Content-Type"], "text/csv")

    def test_brick12_health_check_and_security_audit(self):
        # 1. API Health Check View
        self.client.force_authenticate(None)
        response = self.client.get("/api/health/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["status"], "ok")
        self.assertEqual(response.json()["database"], "ok")
        self.assertEqual(response.json()["app"], "pgms")
        self.assertEqual(response.json()["version"], "v0.12")

        # 2. Anonymous user is blocked on protected monitoring endpoints
        response = self.client.get("/api/academics/monitoring/admin-dashboard/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # 3. Resident self-scoping and restrictions
        self.client.force_authenticate(self.resident_user)
        # Resident cannot access admin dashboard
        response = self.client.get("/api/academics/monitoring/admin-dashboard/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Resident cannot list other residents progress
        response = self.client.get("/api/academics/reports/resident-progress/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Resident cannot access other resident progress detail
        other_user = User.objects.create_user(username="pgr999", password="pass12345", role="RESIDENT")
        from sims.users.models import ResidentProfile
        other_resident = ResidentProfile.objects.create(user=other_user)
        response = self.client.get(f"/api/academics/reports/resident-progress/{other_resident.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



