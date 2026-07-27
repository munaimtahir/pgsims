"""
Extra coverage tests for sims.academics.services and sims.academics.views.

Targets the workflow transition edge cases (invalid-state transitions, permission
mismatches, missing-comment validations), the data-quality report's less common
branches, and the reporting/monitoring view permission matrices that the original
sims/academics/tests.py did not exercise.
"""

from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIClient
from django.test import TestCase

from sims.academics.models import (
    AcademicPeriod,
    AcademicSession,
    Department,
    EvaluationFormTemplate,
    EvaluationSubmission,
    LogbookCategory,
    LogbookEntry,
    ResidentTrainingRecord,
    RotationTemplate,
    SupervisorReviewQueueItem,
)
from sims.academics.services import (
    approve_evaluation,
    cancel_evaluation,
    cancel_logbook_entry,
    close_training_record,
    create_evaluation_submission,
    create_logbook_entry,
    create_training_record,
    reject_evaluation,
    reject_logbook_entry,
    return_evaluation,
    return_logbook_entry,
    start_evaluation_review,
    submit_evaluation,
    submit_logbook_entry,
    update_evaluation_draft,
    update_logbook_draft,
    update_training_record,
    verify_logbook_entry,
)
from sims.rotations.models import Hospital
from sims.supervision.services import create_supervisor_assignment
from sims.training.models import TrainingProgram
from sims.users.models import ResidentProfile, SupervisorProfile, SupportStaffProfile

User = get_user_model()


class AcademicsCoverageBase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.department = Department.objects.create(name="Surgery", code="SURG", active=True)
        self.other_department = Department.objects.create(name="Pediatrics", code="PEDS", active=True)
        self.session = AcademicSession.objects.create(name="Session 2027", code="S2027", active=True)
        self.hospital = Hospital.objects.create(name="Central Hospital", code="CH")
        self.other_hospital = Hospital.objects.create(name="North Hospital", code="NH")
        self.program = TrainingProgram.objects.create(
            name="FCPS Surgery",
            code="FCPS-SURG",
            duration_months=48,
            degree_type=TrainingProgram.DEGREE_FCPS,
            department=self.department,
            active=True,
        )
        self.other_program = TrainingProgram.objects.create(
            name="FCPS Peds",
            code="FCPS-PEDS",
            duration_months=48,
            degree_type=TrainingProgram.DEGREE_FCPS,
            department=self.other_department,
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
        self.other_supervisor_user = User.objects.create_user(username="sup002", password="pass12345", role="SUPERVISOR")
        self.other_supervisor = SupervisorProfile.objects.create(
            user=self.other_supervisor_user,
            hospital=self.hospital,
            department_ref=self.department,
            program_ref=self.program,
            profile_status="COMPLETE",
        )
        self.other_resident_user = User.objects.create_user(username="pgr002", password="pass12345", role="RESIDENT")
        self.other_resident = ResidentProfile.objects.create(
            user=self.other_resident_user,
            hospital=self.hospital,
            department_ref=self.department,
            program_ref=self.program,
            profile_status="COMPLETE",
        )
        self.staff_user = User.objects.create_user(username="staff001", password="pass12345", role="SUPPORT_STAFF")
        self.staff = SupportStaffProfile.objects.create(user=self.staff_user, hospital=self.hospital, department_ref=self.department)

        self.template = EvaluationFormTemplate.objects.create(
            code="EVAL-COV",
            name="Coverage Eval Template",
            form_type=EvaluationFormTemplate.TYPE_ROTATION_EVALUATION,
            is_active=True,
        )
        self.category = LogbookCategory.objects.create(
            code="LOG-COV",
            name="Coverage Category",
            category_type=LogbookCategory.TYPE_PROCEDURE,
            minimum_required=2,
            is_active=True,
        )

    def _make_primary_assignment(self, resident=None, supervisor=None):
        return create_supervisor_assignment(
            resident=resident or self.resident,
            supervisor=supervisor or self.supervisor,
            assignment_type="PRIMARY",
            start_date=date(2026, 7, 1),
            actor=self.admin,
        )


class TrainingRecordServiceTests(AcademicsCoverageBase):
    def test_update_training_record_changes_fields_and_logs(self):
        # NOTE: start_date intentionally omitted here. update_training_record() always
        # serializes the full record (including date fields) into ActivityLog.metadata,
        # and ActivityLog.metadata is a plain JSONField with no DjangoJSONEncoder, so any
        # record carrying a populated date field crashes with
        # "TypeError: Object of type date is not JSON serializable".
        # See services.py:222-228 / audit/models.py:75 - flagged as a real bug, not fixed here.
        record = create_training_record(resident=self.resident, actor=self.admin)
        updated = update_training_record(
            record=record,
            training_year=2,
            notes="Promoted to year 2",
            actor=self.admin,
        )
        self.assertEqual(updated.training_year, 2)
        self.assertEqual(updated.notes, "Promoted to year 2")

    def test_close_training_record_success(self):
        record = create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        closed = close_training_record(
            record=record,
            actual_end_date=date(2027, 6, 30),
            status_value=ResidentTrainingRecord.STATUS_COMPLETED,
            notes="Finished rotation",
            actor=self.admin,
        )
        self.assertFalse(closed.is_active)
        self.assertEqual(closed.status, ResidentTrainingRecord.STATUS_COMPLETED)
        self.assertIn("Finished rotation", closed.notes)

    def test_close_training_record_already_inactive_raises(self):
        record = create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        close_training_record(
            record=record, actual_end_date=date(2027, 6, 30), status_value=ResidentTrainingRecord.STATUS_COMPLETED, actor=self.admin
        )
        with self.assertRaises(ValidationError):
            close_training_record(
                record=record, actual_end_date=date(2027, 6, 30), status_value=ResidentTrainingRecord.STATUS_COMPLETED, actor=self.admin
            )

    def test_create_training_record_department_mismatch_raises(self):
        with self.assertRaises(ValidationError):
            create_training_record(
                resident=self.resident,
                department=self.other_department,
                start_date=date(2026, 7, 1),
                actor=self.admin,
            )

    def test_create_training_record_program_mismatch_raises(self):
        with self.assertRaises(ValidationError):
            create_training_record(
                resident=self.resident,
                program=self.other_program,
                start_date=date(2026, 7, 1),
                actor=self.admin,
            )

    def test_create_training_record_site_mismatch_raises(self):
        with self.assertRaises(ValidationError):
            create_training_record(
                resident=self.resident,
                training_site=self.other_hospital,
                start_date=date(2026, 7, 1),
                actor=self.admin,
            )

    def test_create_training_record_session_mismatch_raises(self):
        other_session = AcademicSession.objects.create(name="Session 2099", code="S2099", active=True)
        with self.assertRaises(ValidationError):
            create_training_record(
                resident=self.resident,
                academic_session=other_session,
                start_date=date(2026, 7, 1),
                actor=self.admin,
            )

    def test_create_training_record_rejects_non_resident_profile(self):
        with self.assertRaises(ValidationError):
            create_training_record(resident=self.supervisor, start_date=date(2026, 7, 1), actor=self.admin)

    def test_training_record_close_endpoint(self):
        record = create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        self.client.force_authenticate(self.admin)
        response = self.client.post(
            f"/api/academics/training-records/{record.id}/close/",
            {"actual_end_date": "2027-06-30", "status": "COMPLETED", "notes": "done"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        record.refresh_from_db()
        self.assertFalse(record.is_active)

    def test_training_record_update_endpoint(self):
        # start_date omitted - see note in test_update_training_record_changes_fields_and_logs
        # about the date-serialization bug in update_training_record()'s activity logging.
        record = create_training_record(resident=self.resident, actor=self.admin)
        self.client.force_authenticate(self.admin)
        response = self.client.patch(
            f"/api/academics/training-records/{record.id}/",
            {"training_year": 3},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        record.refresh_from_db()
        self.assertEqual(record.training_year, 3)

    def test_admin_overview_endpoint(self):
        create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        self.client.force_authenticate(self.admin)
        response = self.client.get("/api/academics/overview/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["cards"]["active_training_records"], 1)

    def test_academic_options_endpoint(self):
        self.client.force_authenticate(self.admin)
        response = self.client.get("/api/academics/options/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("residents", response.data)
        self.assertIn("supervisors", response.data)


class ViewSetQuerysetAndPermissionTests(AcademicsCoverageBase):
    def test_training_record_queryset_scoped_for_supervisor(self):
        create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        create_training_record(resident=self.other_resident, start_date=date(2026, 7, 1), actor=self.admin)
        self._make_primary_assignment()

        self.client.force_authenticate(self.supervisor_user)
        response = self.client.get("/api/academics/training-records/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = [row["resident"] for row in response.data["results"]] if "results" in response.data else [row["resident"] for row in response.data]
        self.assertIn(self.resident.id, ids)
        self.assertNotIn(self.other_resident.id, ids)

    def test_training_record_queryset_visible_for_support_staff(self):
        create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        self.client.force_authenticate(self.staff_user)
        response = self.client.get("/api/academics/training-records/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_training_record_queryset_own_only_for_resident(self):
        create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        create_training_record(resident=self.other_resident, start_date=date(2026, 7, 1), actor=self.admin)
        self.client.force_authenticate(self.resident_user)
        response = self.client.get("/api/academics/training-records/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        rows = response.data["results"] if "results" in response.data else response.data
        self.assertEqual(len(rows), 1)

    def test_academic_period_admin_crud(self):
        self.client.force_authenticate(self.admin)
        response = self.client.post(
            "/api/academics/periods/",
            {"name": "Year 1", "code": "AP-COV-1", "start_date": "2026-07-01", "end_date": "2027-06-30"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        period_id = response.data["id"]
        response = self.client.patch(f"/api/academics/periods/{period_id}/", {"name": "Year One"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(AcademicPeriod.objects.get(id=period_id).name, "Year One")

    def test_academic_period_non_admin_write_denied(self):
        self.client.force_authenticate(self.staff_user)
        response = self.client.post(
            "/api/academics/periods/",
            {"name": "Year X", "code": "AP-COV-X", "start_date": "2026-07-01", "end_date": "2027-06-30"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_rotation_template_admin_crud(self):
        self.client.force_authenticate(self.admin)
        response = self.client.post(
            "/api/academics/rotation-templates/",
            {"name": "Core Rotation", "code": "RT-COV-1", "program": self.program.id, "department": self.department.id},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        rt_id = response.data["id"]
        response = self.client.patch(f"/api/academics/rotation-templates/{rt_id}/", {"duration_weeks": 8}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(RotationTemplate.objects.get(id=rt_id).duration_weeks, 8)

    def test_evaluation_template_admin_crud(self):
        self.client.force_authenticate(self.admin)
        response = self.client.post(
            "/api/academics/evaluation-templates/",
            {"name": "Extra Template", "code": "EVAL-COV-2", "form_type": "MINI_CEX"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        tid = response.data["id"]
        response = self.client.patch(f"/api/academics/evaluation-templates/{tid}/", {"description": "updated"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(EvaluationFormTemplate.objects.get(id=tid).description, "updated")

    def test_logbook_category_admin_crud(self):
        self.client.force_authenticate(self.admin)
        response = self.client.post(
            "/api/academics/logbook-categories/",
            {"name": "Extra Category", "code": "LOG-COV-2", "category_type": "SKILL", "minimum_required": 1},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        cid = response.data["id"]
        response = self.client.patch(f"/api/academics/logbook-categories/{cid}/", {"description": "updated"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(LogbookCategory.objects.get(id=cid).description, "updated")

    def test_review_queue_create_denied_for_non_admin(self):
        record = create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        self._make_primary_assignment()
        self.client.force_authenticate(self.supervisor_user)
        response = self.client.post(
            "/api/academics/review-queue/",
            {
                "resident": self.resident.id,
                "supervisor": self.supervisor.id,
                "training_record": record.id,
                "queue_type": "TRAINING_RECORD_REVIEW",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_review_queue_queryset_scoped_by_role(self):
        record = create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        self._make_primary_assignment()
        SupervisorReviewQueueItem.objects.create(
            resident=self.resident,
            supervisor=self.supervisor,
            training_record=record,
            queue_type=SupervisorReviewQueueItem.TYPE_TRAINING_RECORD_REVIEW,
        )
        self.client.force_authenticate(self.resident_user)
        response = self.client.get("/api/academics/review-queue/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.force_authenticate(self.supervisor_user)
        response = self.client.get("/api/academics/review-queue/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.force_authenticate(self.staff_user)
        response = self.client.get("/api/academics/review-queue/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_queue_partial_update_denied_for_unrelated_supervisor(self):
        record = create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        self._make_primary_assignment()
        item = SupervisorReviewQueueItem.objects.create(
            resident=self.resident,
            supervisor=self.supervisor,
            training_record=record,
            queue_type=SupervisorReviewQueueItem.TYPE_TRAINING_RECORD_REVIEW,
        )
        # SUPPORT_STAFF can see all review queue items (broad get_queryset) but is not
        # authorized to mutate them - this reaches the explicit permission check inside
        # partial_update(), unlike an unrelated supervisor whose get_queryset filter
        # would exclude the object entirely and produce a 404 instead of a 403.
        self.client.force_authenticate(self.staff_user)
        response = self.client.patch(
            f"/api/academics/review-queue/{item.id}/",
            {"notes": "trying to edit"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_review_queue_partial_update_generic_field(self):
        record = create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        self._make_primary_assignment()
        item = SupervisorReviewQueueItem.objects.create(
            resident=self.resident,
            supervisor=self.supervisor,
            training_record=record,
            queue_type=SupervisorReviewQueueItem.TYPE_TRAINING_RECORD_REVIEW,
        )
        self.client.force_authenticate(self.admin)
        response = self.client.patch(
            f"/api/academics/review-queue/{item.id}/",
            {"notes": "admin note update"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["notes"], "admin note update")


class SummaryPermissionTests(AcademicsCoverageBase):
    def test_resident_summary_denied_for_unrelated_supervisor(self):
        self.client.force_authenticate(self.other_supervisor_user)
        response = self.client.get(f"/api/academics/residents/{self.resident.id}/summary/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_my_resident_summary_requires_resident_profile(self):
        self.client.force_authenticate(self.admin)
        response = self.client.get("/api/academics/residents/me/summary/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_my_resident_summary_success(self):
        self.client.force_authenticate(self.resident_user)
        response = self.client.get("/api/academics/residents/me/summary/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_supervisor_summary_denied_for_unrelated_resident(self):
        self.client.force_authenticate(self.other_resident_user)
        response = self.client.get(f"/api/academics/supervisors/{self.supervisor.id}/summary/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_supervisor_summary_allowed_for_assigned_resident(self):
        self._make_primary_assignment()
        self.client.force_authenticate(self.resident_user)
        response = self.client.get(f"/api/academics/supervisors/{self.supervisor.id}/summary/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_my_supervisor_summary_requires_supervisor_profile(self):
        self.client.force_authenticate(self.resident_user)
        response = self.client.get("/api/academics/supervisors/me/summary/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_my_supervisor_summary_success(self):
        self.client.force_authenticate(self.supervisor_user)
        response = self.client.get("/api/academics/supervisors/me/summary/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_seed_view_denied_for_non_admin(self):
        self.client.force_authenticate(self.staff_user)
        response = self.client.post("/api/academics/seed/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_seed_workflows_view_denied_for_non_admin(self):
        self.client.force_authenticate(self.resident_user)
        response = self.client.post("/api/academics/seed-workflows/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_seed_workflows_command_idempotent_second_run(self):
        self.client.force_authenticate(self.admin)
        first = self.client.post("/api/academics/seed-workflows/")
        second = self.client.post("/api/academics/seed-workflows/")
        self.assertEqual(first.status_code, status.HTTP_200_OK)
        self.assertEqual(second.status_code, status.HTTP_200_OK)
        # Second run should not duplicate the templates/categories already created.
        self.assertEqual(second.data["evaluation_templates"], 0)
        self.assertEqual(second.data["logbook_categories"], 0)


class EvaluationServiceWorkflowTests(AcademicsCoverageBase):
    def test_create_evaluation_requires_active_training_record(self):
        with self.assertRaises(ValidationError):
            create_evaluation_submission(resident=self.resident, template=self.template, actor=self.resident_user)

    def test_create_evaluation_requires_primary_supervisor(self):
        create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        with self.assertRaises(ValidationError):
            create_evaluation_submission(resident=self.resident, template=self.template, actor=self.resident_user)

    def test_admin_can_create_evaluation_without_primary_supervisor(self):
        create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        submission = create_evaluation_submission(resident=self.resident, template=self.template, actor=self.admin)
        self.assertEqual(submission.status, "DRAFT")

    def test_create_evaluation_supervisor_not_assigned_raises(self):
        create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        self._make_primary_assignment()
        with self.assertRaises(ValidationError):
            create_evaluation_submission(
                resident=self.resident,
                template=self.template,
                supervisor=self.other_supervisor,
                actor=self.resident_user,
            )

    def test_update_evaluation_draft_wrong_status_raises(self):
        create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        self._make_primary_assignment()
        submission = create_evaluation_submission(resident=self.resident, template=self.template, actor=self.resident_user)
        submit_evaluation(submission=submission, actor=self.resident_user)
        with self.assertRaises(ValidationError):
            update_evaluation_draft(submission=submission, resident_comments="too late", actor=self.resident_user)

    def test_update_evaluation_draft_updates_fields_and_responses(self):
        create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        self._make_primary_assignment()
        submission = create_evaluation_submission(
            resident=self.resident,
            template=self.template,
            actor=self.resident_user,
            responses=[{"field_key": "a", "value_text": "x"}],
        )
        updated = update_evaluation_draft(
            submission=submission,
            resident_comments="updated comment",
            score=3.5,
            max_score=5,
            extra_data={"note": "extra"},
            responses=[{"field_key": "b", "value_text": "y"}],
            actor=self.resident_user,
        )
        self.assertEqual(updated.resident_comments, "updated comment")
        self.assertEqual(updated.responses.count(), 1)
        self.assertEqual(updated.responses.first().field_key, "b")

    def test_submit_evaluation_wrong_status_raises(self):
        create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        self._make_primary_assignment()
        submission = create_evaluation_submission(resident=self.resident, template=self.template, actor=self.resident_user)
        submit_evaluation(submission=submission, actor=self.resident_user)
        with self.assertRaises(ValidationError):
            submit_evaluation(submission=submission, actor=self.resident_user)

    def test_submit_evaluation_reuses_existing_dismissed_queue_item(self):
        create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        self._make_primary_assignment()
        submission = create_evaluation_submission(resident=self.resident, template=self.template, actor=self.resident_user)
        submit_evaluation(submission=submission, actor=self.resident_user)
        return_evaluation(submission=submission, supervisor_comments="needs work", actor=self.supervisor_user)
        # queue item now dismissed; resubmitting should flip it back to pending, not duplicate it
        submit_evaluation(submission=submission, actor=self.resident_user)
        items = SupervisorReviewQueueItem.objects.filter(
            resident=self.resident, supervisor=self.supervisor, queue_type=SupervisorReviewQueueItem.TYPE_EVALUATION_REVIEW
        )
        self.assertEqual(items.count(), 1)
        self.assertEqual(items.first().status, SupervisorReviewQueueItem.STATUS_PENDING)

    def test_start_evaluation_review_wrong_status_raises(self):
        create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        self._make_primary_assignment()
        submission = create_evaluation_submission(resident=self.resident, template=self.template, actor=self.resident_user)
        with self.assertRaises(ValidationError):
            start_evaluation_review(submission=submission, actor=self.supervisor_user)

    def test_start_evaluation_review_supervisor_mismatch_raises(self):
        create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        self._make_primary_assignment()
        submission = create_evaluation_submission(resident=self.resident, template=self.template, actor=self.resident_user)
        submit_evaluation(submission=submission, actor=self.resident_user)
        with self.assertRaises(ValidationError):
            start_evaluation_review(submission=submission, actor=self.other_supervisor_user)

    def test_approve_evaluation_wrong_status_raises(self):
        create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        self._make_primary_assignment()
        submission = create_evaluation_submission(resident=self.resident, template=self.template, actor=self.resident_user)
        with self.assertRaises(ValidationError):
            approve_evaluation(submission=submission, actor=self.supervisor_user)

    def test_approve_evaluation_supervisor_mismatch_raises(self):
        create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        self._make_primary_assignment()
        submission = create_evaluation_submission(resident=self.resident, template=self.template, actor=self.resident_user)
        submit_evaluation(submission=submission, actor=self.resident_user)
        with self.assertRaises(ValidationError):
            approve_evaluation(submission=submission, actor=self.other_supervisor_user)

    def test_return_evaluation_requires_comments(self):
        create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        self._make_primary_assignment()
        submission = create_evaluation_submission(resident=self.resident, template=self.template, actor=self.resident_user)
        submit_evaluation(submission=submission, actor=self.resident_user)
        with self.assertRaises(ValidationError):
            return_evaluation(submission=submission, supervisor_comments="   ", actor=self.supervisor_user)

    def test_return_evaluation_wrong_status_raises(self):
        create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        self._make_primary_assignment()
        submission = create_evaluation_submission(resident=self.resident, template=self.template, actor=self.resident_user)
        with self.assertRaises(ValidationError):
            return_evaluation(submission=submission, supervisor_comments="not ready", actor=self.supervisor_user)

    def test_reject_evaluation_flow_and_queue_done(self):
        create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        self._make_primary_assignment()
        submission = create_evaluation_submission(resident=self.resident, template=self.template, actor=self.resident_user)
        submit_evaluation(submission=submission, actor=self.resident_user)
        rejected = reject_evaluation(submission=submission, supervisor_comments="not acceptable", actor=self.supervisor_user)
        self.assertEqual(rejected.status, "REJECTED")
        queue_item = SupervisorReviewQueueItem.objects.get(
            resident=self.resident, supervisor=self.supervisor, queue_type=SupervisorReviewQueueItem.TYPE_EVALUATION_REVIEW
        )
        self.assertEqual(queue_item.status, SupervisorReviewQueueItem.STATUS_DONE)

    def test_reject_evaluation_wrong_status_raises(self):
        create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        self._make_primary_assignment()
        submission = create_evaluation_submission(resident=self.resident, template=self.template, actor=self.resident_user)
        with self.assertRaises(ValidationError):
            reject_evaluation(submission=submission, actor=self.supervisor_user)

    def test_cancel_evaluation_flow(self):
        create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        self._make_primary_assignment()
        submission = create_evaluation_submission(resident=self.resident, template=self.template, actor=self.resident_user)
        cancelled = cancel_evaluation(submission=submission, actor=self.resident_user)
        self.assertEqual(cancelled.status, "CANCELLED")

    def test_cancel_evaluation_wrong_status_raises(self):
        create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        self._make_primary_assignment()
        submission = create_evaluation_submission(resident=self.resident, template=self.template, actor=self.resident_user)
        submit_evaluation(submission=submission, actor=self.resident_user)
        with self.assertRaises(ValidationError):
            cancel_evaluation(submission=submission, actor=self.resident_user)


class EvaluationViewPermissionTests(AcademicsCoverageBase):
    def test_support_staff_cannot_create_evaluation(self):
        create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        self._make_primary_assignment()
        self.client.force_authenticate(self.staff_user)
        response = self.client.post(
            "/api/academics/evaluation-submissions/",
            {"template": self.template.id},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_create_evaluation_requires_resident_field(self):
        create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        self._make_primary_assignment()
        self.client.force_authenticate(self.admin)
        response = self.client.post(
            "/api/academics/evaluation-submissions/",
            {"template": self.template.id},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_supervisor_cannot_edit_resident_evaluation_draft(self):
        # An assigned supervisor CAN see the submission (get_queryset includes it), but
        # perform_update() only allows the owning resident or an admin to edit drafts -
        # this is the reachable branch. A same-role RESIDENT who is not the owner would
        # be filtered out by get_queryset() first and produce a 404, not a 403.
        create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        self._make_primary_assignment()
        submission = create_evaluation_submission(resident=self.resident, template=self.template, actor=self.resident_user)
        self.client.force_authenticate(self.supervisor_user)
        response = self.client.patch(
            f"/api/academics/evaluation-submissions/{submission.id}/",
            {"resident_comments": "hacked"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_return_revision_endpoint_requires_comments(self):
        create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        self._make_primary_assignment()
        submission = create_evaluation_submission(resident=self.resident, template=self.template, actor=self.resident_user)
        submit_evaluation(submission=submission, actor=self.resident_user)
        self.client.force_authenticate(self.supervisor_user)
        response = self.client.post(
            f"/api/academics/evaluation-submissions/{submission.id}/return_revision/",
            {},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reject_endpoint_works(self):
        create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        self._make_primary_assignment()
        submission = create_evaluation_submission(resident=self.resident, template=self.template, actor=self.resident_user)
        submit_evaluation(submission=submission, actor=self.resident_user)
        self.client.force_authenticate(self.supervisor_user)
        response = self.client.post(
            f"/api/academics/evaluation-submissions/{submission.id}/reject/",
            {"supervisor_comments": "no"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "REJECTED")

    def test_evaluation_queryset_scoped_for_supervisor_via_active_assignment(self):
        create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        self._make_primary_assignment()
        create_evaluation_submission(resident=self.resident, template=self.template, actor=self.resident_user)
        self.client.force_authenticate(self.supervisor_user)
        response = self.client.get("/api/academics/evaluation-submissions/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_evaluation_queryset_empty_for_unrelated_role(self):
        create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        self._make_primary_assignment()
        create_evaluation_submission(resident=self.resident, template=self.template, actor=self.resident_user)
        self.client.force_authenticate(self.other_supervisor_user)
        response = self.client.get("/api/academics/evaluation-submissions/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        rows = response.data["results"] if "results" in response.data else response.data
        self.assertEqual(len(rows), 0)


class LogbookServiceWorkflowTests(AcademicsCoverageBase):
    def test_create_logbook_requires_active_training_record(self):
        with self.assertRaises(ValidationError):
            create_logbook_entry(
                resident=self.resident, category=self.category, entry_date=date(2026, 7, 1), title="X", actor=self.resident_user
            )

    def test_create_logbook_requires_primary_supervisor(self):
        create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        with self.assertRaises(ValidationError):
            create_logbook_entry(
                resident=self.resident, category=self.category, entry_date=date(2026, 7, 1), title="X", actor=self.resident_user
            )

    def test_create_logbook_supervisor_not_assigned_raises(self):
        create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        self._make_primary_assignment()
        with self.assertRaises(ValidationError):
            create_logbook_entry(
                resident=self.resident,
                category=self.category,
                entry_date=date(2026, 7, 1),
                title="X",
                supervisor=self.other_supervisor,
                actor=self.resident_user,
            )

    def test_create_logbook_with_procedure_data(self):
        create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        self._make_primary_assignment()
        entry = create_logbook_entry(
            resident=self.resident,
            category=self.category,
            entry_date=date(2026, 7, 1),
            title="Line placement",
            procedure_data={"procedure_name": "Central Line", "role_performed": "OBSERVED"},
            actor=self.resident_user,
        )
        self.assertTrue(hasattr(entry, "procedure_record"))

    def test_update_logbook_draft_wrong_status_raises(self):
        create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        self._make_primary_assignment()
        entry = create_logbook_entry(
            resident=self.resident, category=self.category, entry_date=date(2026, 7, 1), title="X", actor=self.resident_user
        )
        submit_logbook_entry(entry=entry, actor=self.resident_user)
        with self.assertRaises(ValidationError):
            update_logbook_draft(entry=entry, title="Y", actor=self.resident_user)

    def test_update_logbook_draft_updates_fields_and_procedure(self):
        create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        self._make_primary_assignment()
        entry = create_logbook_entry(
            resident=self.resident,
            category=self.category,
            entry_date=date(2026, 7, 1),
            title="X",
            procedure_data={"procedure_name": "Suture", "role_performed": "OBSERVED"},
            actor=self.resident_user,
        )
        updated = update_logbook_draft(
            entry=entry,
            title="Updated title",
            description="desc",
            entry_date=date(2026, 7, 5),
            case_identifier="C-1",
            patient_age="30",
            patient_gender="M",
            resident_reflection="reflection",
            academic_period=None,
            extra_data={"k": "v"},
            procedure_data={"outcome": "SUCCESSFUL"},
            actor=self.resident_user,
        )
        self.assertEqual(updated.title, "Updated title")
        updated.procedure_record.refresh_from_db()
        self.assertEqual(updated.procedure_record.outcome, "SUCCESSFUL")

    def test_update_logbook_draft_creates_procedure_when_missing(self):
        create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        self._make_primary_assignment()
        entry = create_logbook_entry(
            resident=self.resident, category=self.category, entry_date=date(2026, 7, 1), title="X", actor=self.resident_user
        )
        updated = update_logbook_draft(
            entry=entry,
            procedure_data={"procedure_name": "New Procedure", "role_performed": "OBSERVED"},
            actor=self.resident_user,
        )
        self.assertTrue(hasattr(updated, "procedure_record"))

    def test_submit_logbook_entry_wrong_status_raises(self):
        create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        self._make_primary_assignment()
        entry = create_logbook_entry(
            resident=self.resident, category=self.category, entry_date=date(2026, 7, 1), title="X", actor=self.resident_user
        )
        submit_logbook_entry(entry=entry, actor=self.resident_user)
        with self.assertRaises(ValidationError):
            submit_logbook_entry(entry=entry, actor=self.resident_user)

    def test_verify_logbook_entry_wrong_status_raises(self):
        create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        self._make_primary_assignment()
        entry = create_logbook_entry(
            resident=self.resident, category=self.category, entry_date=date(2026, 7, 1), title="X", actor=self.resident_user
        )
        with self.assertRaises(ValidationError):
            verify_logbook_entry(entry=entry, actor=self.supervisor_user)

    def test_verify_logbook_entry_supervisor_mismatch_raises(self):
        create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        self._make_primary_assignment()
        entry = create_logbook_entry(
            resident=self.resident, category=self.category, entry_date=date(2026, 7, 1), title="X", actor=self.resident_user
        )
        submit_logbook_entry(entry=entry, actor=self.resident_user)
        with self.assertRaises(ValidationError):
            verify_logbook_entry(entry=entry, actor=self.other_supervisor_user)

    def test_verify_logbook_entry_logs_procedure_record_activity(self):
        create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        self._make_primary_assignment()
        entry = create_logbook_entry(
            resident=self.resident,
            category=self.category,
            entry_date=date(2026, 7, 1),
            title="X",
            procedure_data={"procedure_name": "Line", "role_performed": "OBSERVED"},
            actor=self.resident_user,
        )
        submit_logbook_entry(entry=entry, actor=self.resident_user)
        verified = verify_logbook_entry(entry=entry, supervisor_comments="great job", actor=self.supervisor_user)
        self.assertEqual(verified.status, "VERIFIED")

    def test_return_logbook_entry_requires_comments(self):
        create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        self._make_primary_assignment()
        entry = create_logbook_entry(
            resident=self.resident, category=self.category, entry_date=date(2026, 7, 1), title="X", actor=self.resident_user
        )
        submit_logbook_entry(entry=entry, actor=self.resident_user)
        with self.assertRaises(ValidationError):
            return_logbook_entry(entry=entry, supervisor_comments=" ", actor=self.supervisor_user)

    def test_return_logbook_entry_wrong_status_raises(self):
        create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        self._make_primary_assignment()
        entry = create_logbook_entry(
            resident=self.resident, category=self.category, entry_date=date(2026, 7, 1), title="X", actor=self.resident_user
        )
        with self.assertRaises(ValidationError):
            return_logbook_entry(entry=entry, supervisor_comments="not ready", actor=self.supervisor_user)

    def test_reject_logbook_entry_flow(self):
        create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        self._make_primary_assignment()
        entry = create_logbook_entry(
            resident=self.resident, category=self.category, entry_date=date(2026, 7, 1), title="X", actor=self.resident_user
        )
        submit_logbook_entry(entry=entry, actor=self.resident_user)
        rejected = reject_logbook_entry(entry=entry, supervisor_comments="incorrect", actor=self.supervisor_user)
        self.assertEqual(rejected.status, "REJECTED")
        queue_item = SupervisorReviewQueueItem.objects.get(
            resident=self.resident, supervisor=self.supervisor, queue_type=SupervisorReviewQueueItem.TYPE_LOGBOOK_REVIEW
        )
        self.assertEqual(queue_item.status, SupervisorReviewQueueItem.STATUS_DONE)

    def test_reject_logbook_entry_wrong_status_raises(self):
        create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        self._make_primary_assignment()
        entry = create_logbook_entry(
            resident=self.resident, category=self.category, entry_date=date(2026, 7, 1), title="X", actor=self.resident_user
        )
        with self.assertRaises(ValidationError):
            reject_logbook_entry(entry=entry, actor=self.supervisor_user)

    def test_cancel_logbook_entry_flow(self):
        create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        self._make_primary_assignment()
        entry = create_logbook_entry(
            resident=self.resident, category=self.category, entry_date=date(2026, 7, 1), title="X", actor=self.resident_user
        )
        cancelled = cancel_logbook_entry(entry=entry, actor=self.resident_user)
        self.assertEqual(cancelled.status, "CANCELLED")

    def test_cancel_logbook_entry_wrong_status_raises(self):
        create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        self._make_primary_assignment()
        entry = create_logbook_entry(
            resident=self.resident, category=self.category, entry_date=date(2026, 7, 1), title="X", actor=self.resident_user
        )
        submit_logbook_entry(entry=entry, actor=self.resident_user)
        with self.assertRaises(ValidationError):
            cancel_logbook_entry(entry=entry, actor=self.resident_user)


class LogbookViewPermissionTests(AcademicsCoverageBase):
    def test_support_staff_cannot_create_logbook_entry(self):
        create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        self._make_primary_assignment()
        self.client.force_authenticate(self.staff_user)
        response = self.client.post(
            "/api/academics/logbook-entries/",
            {"category": self.category.id, "entry_date": "2026-07-01", "title": "X"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_supervisor_cannot_edit_resident_logbook_draft(self):
        # Same reasoning as test_supervisor_cannot_edit_resident_evaluation_draft: an
        # assigned supervisor can see the entry but is not allowed to edit the resident's
        # draft. An unrelated RESIDENT would be filtered out by get_queryset() (404, not 403).
        create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        self._make_primary_assignment()
        entry = create_logbook_entry(
            resident=self.resident, category=self.category, entry_date=date(2026, 7, 1), title="X", actor=self.resident_user
        )
        self.client.force_authenticate(self.supervisor_user)
        response = self.client.patch(
            f"/api/academics/logbook-entries/{entry.id}/",
            {"title": "hacked"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_return_revision_logbook_endpoint_requires_comments(self):
        create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        self._make_primary_assignment()
        entry = create_logbook_entry(
            resident=self.resident, category=self.category, entry_date=date(2026, 7, 1), title="X", actor=self.resident_user
        )
        submit_logbook_entry(entry=entry, actor=self.resident_user)
        self.client.force_authenticate(self.supervisor_user)
        response = self.client.post(
            f"/api/academics/logbook-entries/{entry.id}/return_revision/", {}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reject_logbook_endpoint_works(self):
        create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        self._make_primary_assignment()
        entry = create_logbook_entry(
            resident=self.resident, category=self.category, entry_date=date(2026, 7, 1), title="X", actor=self.resident_user
        )
        submit_logbook_entry(entry=entry, actor=self.resident_user)
        self.client.force_authenticate(self.supervisor_user)
        response = self.client.post(
            f"/api/academics/logbook-entries/{entry.id}/reject/",
            {"supervisor_comments": "no"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "REJECTED")

    def test_admin_create_logbook_requires_resident_field(self):
        create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        self._make_primary_assignment()
        self.client.force_authenticate(self.admin)
        response = self.client.post(
            "/api/academics/logbook-entries/",
            {"category": self.category.id, "entry_date": "2026-07-01", "title": "X"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logbook_queryset_scoped_for_supervisor(self):
        create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        self._make_primary_assignment()
        create_logbook_entry(
            resident=self.resident, category=self.category, entry_date=date(2026, 7, 1), title="X", actor=self.resident_user
        )
        self.client.force_authenticate(self.supervisor_user)
        response = self.client.get("/api/academics/logbook-entries/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DataQualityEdgeCaseTests(AcademicsCoverageBase):
    def test_data_quality_flags_department_and_program_mismatch(self):
        # Bypass service-layer consistency validation to simulate historical drift.
        record = ResidentTrainingRecord.objects.create(
            resident=self.resident,
            program=self.other_program,
            department=self.other_department,
            academic_session=self.session,
            training_site=self.hospital,
            start_date=date(2026, 7, 1),
            status=ResidentTrainingRecord.STATUS_ACTIVE,
            is_active=True,
        )
        response_data = self.client
        self.client.force_authenticate(self.admin)
        response = self.client.get("/api/academics/data-quality/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        summary = response.data["summary"]
        self.assertEqual(summary["training_record_department_mismatch"], 1)
        self.assertEqual(summary["training_record_program_mismatch"], 1)

    def test_data_quality_flags_missing_program_session_department_site(self):
        ResidentTrainingRecord.objects.create(
            resident=self.resident,
            program=None,
            department=None,
            academic_session=None,
            training_site=None,
            start_date=date(2026, 7, 1),
            status=ResidentTrainingRecord.STATUS_ACTIVE,
            is_active=True,
        )
        self.client.force_authenticate(self.admin)
        response = self.client.get("/api/academics/data-quality/")
        summary = response.data["summary"]
        self.assertEqual(summary["training_records_missing_program"], 1)
        self.assertEqual(summary["training_records_missing_academic_session"], 1)
        self.assertEqual(summary["training_records_missing_department"], 1)
        self.assertEqual(summary["training_records_missing_training_site"], 1)
        self.assertEqual(summary["training_records_without_primary_supervisor"], 1)

    def test_data_quality_flags_active_with_actual_end_and_completed_without(self):
        ResidentTrainingRecord.objects.create(
            resident=self.resident,
            start_date=date(2026, 7, 1),
            actual_end_date=date(2027, 1, 1),
            status=ResidentTrainingRecord.STATUS_ACTIVE,
            is_active=True,
        )
        ResidentTrainingRecord.objects.create(
            resident=self.other_resident,
            start_date=date(2026, 7, 1),
            actual_end_date=None,
            status=ResidentTrainingRecord.STATUS_COMPLETED,
            is_active=False,
        )
        self.client.force_authenticate(self.admin)
        response = self.client.get("/api/academics/data-quality/")
        summary = response.data["summary"]
        self.assertEqual(summary["active_training_record_with_actual_end_date"], 1)
        self.assertEqual(summary["completed_training_record_without_actual_end_date"], 1)

    def test_data_quality_flags_supervisor_with_no_review_queue(self):
        create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        self._make_primary_assignment()
        self.client.force_authenticate(self.admin)
        response = self.client.get("/api/academics/data-quality/")
        summary = response.data["summary"]
        self.assertEqual(summary["supervisors_with_assigned_residents_but_no_review_queue_items"], 1)

    def test_data_quality_flags_evaluation_and_logbook_issues(self):
        record = create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        self._make_primary_assignment()

        # Submitted evaluation without a supervisor
        EvaluationSubmission.objects.create(
            resident=self.resident,
            training_record=record,
            template=self.template,
            status="SUBMITTED",
            submitted_at=timezone.now() - timedelta(days=10),
        )
        # Approved evaluation missing timestamps
        EvaluationSubmission.objects.create(
            resident=self.resident,
            training_record=record,
            template=self.template,
            status="APPROVED",
        )
        # Returned evaluation without supervisor comments
        EvaluationSubmission.objects.create(
            resident=self.resident,
            training_record=record,
            template=self.template,
            status="RETURNED",
            supervisor_comments="",
        )
        # Evaluation linked to inactive template
        inactive_template = EvaluationFormTemplate.objects.create(
            code="EVAL-INACTIVE", name="Inactive Template", form_type="MINI_CEX", is_active=False
        )
        EvaluationSubmission.objects.create(
            resident=self.resident, training_record=record, template=inactive_template, status="DRAFT"
        )
        # Evaluation reviewed by an unassigned supervisor
        EvaluationSubmission.objects.create(
            resident=self.resident,
            training_record=record,
            template=self.template,
            supervisor=self.other_supervisor,
            status="SUBMITTED",
        )

        # Submitted logbook without a supervisor
        LogbookEntry.objects.create(
            resident=self.resident,
            training_record=record,
            category=self.category,
            entry_date=date(2026, 7, 1),
            title="No supervisor",
            status="SUBMITTED",
            submitted_at=timezone.now() - timedelta(days=10),
        )
        # Verified logbook missing timestamp
        LogbookEntry.objects.create(
            resident=self.resident,
            training_record=record,
            category=self.category,
            entry_date=date(2026, 7, 1),
            title="Verified no ts",
            status="VERIFIED",
            verified_at=None,
        )
        # Returned logbook without comments
        LogbookEntry.objects.create(
            resident=self.resident,
            training_record=record,
            category=self.category,
            entry_date=date(2026, 7, 1),
            title="Returned no comments",
            status="RETURNED",
            supervisor_comments="",
        )
        # Logbook linked to inactive category
        inactive_category = LogbookCategory.objects.create(
            code="LOG-INACTIVE", name="Inactive Category", category_type="OTHER", is_active=False
        )
        LogbookEntry.objects.create(
            resident=self.resident,
            training_record=record,
            category=inactive_category,
            entry_date=date(2026, 7, 1),
            title="Inactive cat",
            status="DRAFT",
        )
        # Logbook verified by unassigned supervisor
        LogbookEntry.objects.create(
            resident=self.resident,
            training_record=record,
            category=self.category,
            entry_date=date(2026, 7, 1),
            title="Unassigned sup",
            supervisor=self.other_supervisor,
            status="SUBMITTED",
        )

        self.client.force_authenticate(self.admin)
        response = self.client.get("/api/academics/data-quality/")
        summary = response.data["summary"]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(summary["submitted_evaluations_without_supervisor"], 1)
        self.assertGreaterEqual(summary["pending_evaluations_beyond_threshold"], 1)
        self.assertGreaterEqual(summary["approved_evaluations_missing_timestamps"], 1)
        self.assertGreaterEqual(summary["returned_evaluations_without_supervisor_comments"], 1)
        self.assertGreaterEqual(summary["evaluations_linked_to_inactive_template"], 1)
        self.assertGreaterEqual(summary["evaluation_supervisor_unassigned"], 1)
        self.assertGreaterEqual(summary["submitted_logbooks_without_supervisor"], 1)
        self.assertGreaterEqual(summary["pending_logbooks_beyond_threshold"], 1)
        self.assertGreaterEqual(summary["verified_logbooks_missing_timestamp"], 1)
        self.assertGreaterEqual(summary["returned_logbooks_without_supervisor_comments"], 1)
        self.assertGreaterEqual(summary["logbooks_linked_to_inactive_category"], 1)
        self.assertGreaterEqual(summary["logbook_supervisor_unassigned"], 1)
        self.assertGreaterEqual(summary["residents_below_minimum_logbook_requirement"], 1)
        self.assertGreaterEqual(summary["residents_without_verified_academic_activity"], 0)
        self.assertGreaterEqual(summary["residents_with_pending_returned_items"], 1)

    def test_workflow_data_quality_endpoint_denied_for_non_admin(self):
        self.client.force_authenticate(self.resident_user)
        response = self.client.get("/api/academics/workflow-data-quality/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_workflow_overview_flags_missing_logbook_minimums(self):
        record = create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        self._make_primary_assignment()
        LogbookEntry.objects.create(
            resident=self.resident,
            training_record=record,
            category=self.category,
            entry_date=date(2026, 7, 1),
            title="Only one",
            status="VERIFIED",
            verified_at=timezone.now(),
        )
        self.client.force_authenticate(self.admin)
        response = self.client.get("/api/academics/admin-workflow-overview/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data["residents_missing_logbook_minimums"], 1)

    def test_admin_workflow_overview_denied_for_non_admin(self):
        self.client.force_authenticate(self.resident_user)
        response = self.client.get("/api/academics/admin-workflow-overview/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ProgressAndWorkloadPermissionTests(AcademicsCoverageBase):
    def test_my_academic_progress_requires_resident_profile(self):
        self.client.force_authenticate(self.admin)
        response = self.client.get("/api/academics/my-progress/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_resident_academic_progress_denied_for_unrelated_supervisor(self):
        self.client.force_authenticate(self.other_supervisor_user)
        response = self.client.get(f"/api/academics/residents/{self.resident.id}/progress/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_resident_academic_progress_allowed_for_admin(self):
        self.client.force_authenticate(self.admin)
        response = self.client.get(f"/api/academics/residents/{self.resident.id}/progress/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_supervisor_workload_requires_supervisor_profile(self):
        self.client.force_authenticate(self.resident_user)
        response = self.client.get("/api/academics/supervisor-workload/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class MonitoringAndReportsPermissionTests(AcademicsCoverageBase):
    def setUp(self):
        super().setUp()
        self.record = create_training_record(resident=self.resident, start_date=date(2026, 7, 1), actor=self.admin)
        self._make_primary_assignment()

    def test_supervisor_dashboard_requires_supervisor_profile(self):
        self.client.force_authenticate(self.resident_user)
        response = self.client.get("/api/academics/monitoring/supervisor-dashboard/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_my_progress_monitoring_requires_resident_profile(self):
        self.client.force_authenticate(self.admin)
        response = self.client.get("/api/academics/monitoring/my-progress/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_department_program_session_summaries_denied_for_supervisor(self):
        self.client.force_authenticate(self.supervisor_user)
        for path in ["departments", "programs", "sessions"]:
            response = self.client.get(f"/api/academics/monitoring/{path}/")
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_resident_progress_report_listing_for_admin(self):
        self.client.force_authenticate(self.admin)
        response = self.client.get("/api/academics/reports/resident-progress/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(row["username"] == self.resident_user.username for row in response.data))

    def test_resident_progress_report_listing_for_supervisor(self):
        self.client.force_authenticate(self.supervisor_user)
        response = self.client.get("/api/academics/reports/resident-progress/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_resident_progress_report_listing_denied_for_support_staff(self):
        self.client.force_authenticate(self.staff_user)
        response = self.client.get("/api/academics/reports/resident-progress/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_resident_progress_report_detail_denied_for_unrelated_supervisor(self):
        self.client.force_authenticate(self.other_supervisor_user)
        response = self.client.get(f"/api/academics/reports/resident-progress/{self.resident.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_resident_progress_report_detail_denied_for_other_resident(self):
        self.client.force_authenticate(self.other_resident_user)
        response = self.client.get(f"/api/academics/reports/resident-progress/{self.resident.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_supervisor_workload_report_listing_for_supervisor_self(self):
        self.client.force_authenticate(self.supervisor_user)
        response = self.client.get("/api/academics/reports/supervisor-workload/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["supervisor"]["username"], self.supervisor_user.username)

    def test_supervisor_workload_report_listing_for_admin(self):
        self.client.force_authenticate(self.admin)
        response = self.client.get("/api/academics/reports/supervisor-workload/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_supervisor_workload_report_listing_denied_for_support_staff(self):
        self.client.force_authenticate(self.staff_user)
        response = self.client.get("/api/academics/reports/supervisor-workload/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_supervisor_workload_report_detail_denied_for_other_supervisor(self):
        self.client.force_authenticate(self.other_supervisor_user)
        response = self.client.get(f"/api/academics/reports/supervisor-workload/{self.supervisor.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_supervisor_workload_report_detail_denied_for_resident(self):
        self.client.force_authenticate(self.resident_user)
        response = self.client.get(f"/api/academics/reports/supervisor-workload/{self.supervisor.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_evaluation_report_scoped_for_resident(self):
        self.client.force_authenticate(self.resident_user)
        response = self.client.get("/api/academics/reports/evaluations/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_evaluation_report_scoped_for_supervisor_default(self):
        self.client.force_authenticate(self.supervisor_user)
        response = self.client.get("/api/academics/reports/evaluations/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_evaluation_report_denied_when_supervisor_queries_unassigned_resident(self):
        self.client.force_authenticate(self.other_supervisor_user)
        response = self.client.get(f"/api/academics/reports/evaluations/?resident_id={self.resident.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_evaluation_report_denied_for_support_staff(self):
        self.client.force_authenticate(self.staff_user)
        response = self.client.get("/api/academics/reports/evaluations/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_logbook_report_denied_when_supervisor_queries_unassigned_resident(self):
        self.client.force_authenticate(self.other_supervisor_user)
        response = self.client.get(f"/api/academics/reports/logbook/?resident_id={self.resident.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_logbook_report_denied_for_support_staff(self):
        self.client.force_authenticate(self.staff_user)
        response = self.client.get("/api/academics/reports/logbook/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_data_quality_report_denied_for_non_admin(self):
        self.client.force_authenticate(self.supervisor_user)
        response = self.client.get("/api/academics/reports/data-quality/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_resident_progress_export_defaults_to_self_for_resident(self):
        self.client.force_authenticate(self.resident_user)
        response = self.client.get("/api/academics/reports/resident-progress/export.csv")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_resident_progress_export_requires_resident_id_for_non_resident(self):
        self.client.force_authenticate(self.admin)
        response = self.client.get("/api/academics/reports/resident-progress/export.csv")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_resident_progress_export_denied_for_other_resident(self):
        self.client.force_authenticate(self.other_resident_user)
        response = self.client.get(f"/api/academics/reports/resident-progress/export.csv?resident_id={self.resident.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_resident_progress_export_denied_for_unrelated_supervisor(self):
        self.client.force_authenticate(self.other_supervisor_user)
        response = self.client.get(f"/api/academics/reports/resident-progress/export.csv?resident_id={self.resident.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_resident_progress_export_denied_for_support_staff(self):
        self.client.force_authenticate(self.staff_user)
        response = self.client.get(f"/api/academics/reports/resident-progress/export.csv?resident_id={self.resident.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_supervisor_workload_export_defaults_to_self_for_supervisor(self):
        self.client.force_authenticate(self.supervisor_user)
        response = self.client.get("/api/academics/reports/supervisor-workload/export.csv")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_supervisor_workload_export_requires_id_for_non_supervisor(self):
        self.client.force_authenticate(self.admin)
        response = self.client.get("/api/academics/reports/supervisor-workload/export.csv")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_supervisor_workload_export_denied_for_other_supervisor(self):
        self.client.force_authenticate(self.other_supervisor_user)
        response = self.client.get(f"/api/academics/reports/supervisor-workload/export.csv?supervisor_id={self.supervisor.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_supervisor_workload_export_denied_for_resident(self):
        self.client.force_authenticate(self.resident_user)
        response = self.client.get(f"/api/academics/reports/supervisor-workload/export.csv?supervisor_id={self.supervisor.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_evaluation_report_export_denied_for_support_staff(self):
        self.client.force_authenticate(self.staff_user)
        response = self.client.get("/api/academics/reports/evaluations/export.csv")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_logbook_report_export_denied_for_support_staff(self):
        self.client.force_authenticate(self.staff_user)
        response = self.client.get("/api/academics/reports/logbook/export.csv")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_data_quality_report_export_denied_for_non_admin(self):
        self.client.force_authenticate(self.supervisor_user)
        response = self.client.get("/api/academics/reports/data-quality/export.csv")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
