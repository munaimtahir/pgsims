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
