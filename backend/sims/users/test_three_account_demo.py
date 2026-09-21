"""Isolation, replay and real transition coverage for the three-account demo."""

import json
from datetime import timedelta
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase, override_settings
from django.utils import timezone

from sims.academics import services
from sims.academics.models import (
    Department,
    EvaluationSubmission,
    LogbookEntry,
    SupervisorReviewQueueItem,
)
from sims.audit.models import ActivityLog
from sims.rotations.models import Hospital, HospitalDepartment
from sims.supervision.services import create_supervisor_assignment
from sims.supervision.models import ResidentSupervisorAssignment
from sims.training.models import (
    LeaveRequest,
    ResidentTrainingRecord,
    RotationAssignment,
    TrainingProgram,
)
from sims.training.views import LeaveRequestViewSet, RotationAssignmentViewSet
from sims.users.management.commands.seed_three_account_demo import Command, DATASET, STATES
from sims.users.models import ResidentDocument, ResidentDocumentRequirement, User
from sims.users.services import create_user_with_profile
from sims.users.onboarding_api import ResidentDocumentViewSet


class ThreeAccountDemoTests(TestCase):
    def setUp(self):
        self.media = TemporaryDirectory(prefix="pgsims-demo-test-")
        self.addCleanup(self.media.cleanup)
        self.settings_override = override_settings(MEDIA_ROOT=self.media.name)
        self.settings_override.enable()
        self.addCleanup(self.settings_override.disable)
        self.department = Department.objects.create(name="Demo department", code="D3")
        self.hospital = Hospital.objects.create(name="Demo hospital", code="H3")
        HospitalDepartment.objects.create(hospital=self.hospital, department=self.department)
        self.program = TrainingProgram.objects.create(
            name="Demo programme", code="P3", duration_months=60
        )
        self.users = {}
        for name, role in [
            ("admin", "ADMIN"),
            ("supervisor", "SUPERVISOR"),
            ("resident", "RESIDENT"),
        ]:
            user = create_user_with_profile(username=name, role=role, full_name=f"Demo {name}")
            self.users[name] = user
        self.resident = self.users["resident"].resident_profile
        self.supervisor = self.users["supervisor"].supervisor_profile
        for profile in (self.resident, self.supervisor):
            profile.hospital = self.hospital
            profile.department_ref = self.department
            profile.save()
        self.today = timezone.localdate()
        self.training = ResidentTrainingRecord.objects.create(
            resident_user=self.users["resident"],
            program=self.program,
            start_date=self.today - timedelta(days=365),
            expected_end_date=self.today + timedelta(days=365),
            training_site=self.hospital,
            department=self.department,
        )
        self.assignment = create_supervisor_assignment(
            resident=self.resident,
            supervisor=self.supervisor,
            assignment_type="PRIMARY",
            start_date=self.training.start_date,
            actor=self.users["admin"],
        )

    def run_seed(self, mode="apply"):
        out = StringIO()
        call_command("seed_three_account_demo", **{mode: True}, stdout=out)
        return json.loads(out.getvalue())

    def test_preview_has_no_database_or_storage_writes(self):
        before = ActivityLog.objects.count()
        result = self.run_seed("dry_run")
        self.assertEqual(result["missing"], 20)
        self.assertEqual(ActivityLog.objects.count(), before)
        self.assertFalse(LogbookEntry.objects.exists())
        self.assertFalse(ResidentDocument.objects.exists())
        self.assertEqual(list(Path(self.media.name).rglob("*.png")), [])

    def test_apply_verify_and_replay_preserve_identities_and_states(self):
        before_users = list(User.objects.values())
        before_profiles = (
            list(type(self.resident).objects.values()),
            list(type(self.supervisor).objects.values()),
        )
        before_training = list(ResidentTrainingRecord.objects.values())
        before_requirements = list(ResidentDocumentRequirement.objects.values())
        first = self.run_seed()
        self.assertEqual(first["created"], 20)
        self.assertEqual(
            first["read_access_checks"], {"admin": 20, "supervisor": 20, "resident": 20}
        )
        for kind, states in STATES.items():
            self.assertEqual(
                [r["status"] for r in first["records"] if r["feature"] == kind], states
            )
        logbook = LogbookEntry.objects.get(extra_data__demo_key=Command.key("logbook", 1))
        services.verify_logbook_entry(
            entry=logbook, actor=self.users["supervisor"], supervisor_comments="Live rehearsal"
        )
        second = self.run_seed()
        self.assertEqual(second["created"], 0)
        self.assertEqual([r["id"] for r in first["records"]], [r["id"] for r in second["records"]])
        logbook.refresh_from_db()
        self.assertEqual(logbook.status, "VERIFIED")
        self.assertEqual(self.run_seed("verify")["missing"], 0)
        self.assertEqual(list(User.objects.values()), before_users)
        self.assertEqual(
            (
                list(type(self.resident).objects.values()),
                list(type(self.supervisor).objects.values()),
            ),
            before_profiles,
        )
        self.assertEqual(list(ResidentTrainingRecord.objects.values()), before_training)
        self.assertEqual(list(ResidentDocumentRequirement.objects.values()), before_requirements)
        self.assertEqual(ResidentSupervisorAssignment.objects.count(), 1)
        self.assertEqual(len(list(Path(self.media.name).rglob("*.png"))), 4)
        self.assertEqual(ActivityLog.objects.filter(verb="DEMO_RECORD_CREATED").count(), 20)

    def test_missing_profile_and_role_mismatch_fail_closed(self):
        self.users["admin"].admin_profile.delete()
        with self.assertRaises(CommandError):
            self.run_seed()
        self.assertFalse(LogbookEntry.objects.exists())

    def test_missing_account_fails_closed(self):
        User.objects.filter(username="admin").update(username="other-admin")
        with self.assertRaises(CommandError):
            self.run_seed()
        self.assertFalse(ResidentDocument.objects.exists())

    def test_wrong_role_fails_closed(self):
        User.objects.filter(username="supervisor").update(role="SUPPORT_STAFF")
        with self.assertRaises(CommandError):
            self.run_seed()

    def test_ambiguous_training_and_missing_assignment_fail(self):
        other_program = TrainingProgram.objects.create(
            name="Second programme", code="P4", duration_months=60
        )
        ResidentTrainingRecord.objects.create(
            resident_user=self.users["resident"],
            program=other_program,
            start_date=self.today,
            expected_end_date=self.today + timedelta(days=365),
        )
        with self.assertRaises(CommandError):
            self.run_seed()
        ResidentTrainingRecord.objects.exclude(pk=self.training.pk).delete()
        self.assignment.delete()
        with self.assertRaises(CommandError):
            self.run_seed()

    def test_late_failure_rolls_back_records_and_files(self):
        before = ActivityLog.objects.count()
        original = Command.create_example

        def fail_after_file(command, kind, index, state):
            original(command, kind, index, state)
            if kind == "document" and index == 2:
                raise CommandError("Synthetic failure after storage write")

        with (
            patch.object(Command, "create_example", fail_after_file),
            self.assertRaises(CommandError),
        ):
            self.run_seed()
        for model in (
            LogbookEntry,
            EvaluationSubmission,
            LeaveRequest,
            RotationAssignment,
            ResidentDocument,
        ):
            self.assertEqual(model.objects.count(), 0)
        self.assertEqual(ActivityLog.objects.count(), before)
        self.assertEqual(list(Path(self.media.name).rglob("*.png")), [])

    def test_existing_leave_is_preserved_and_dates_do_not_overlap(self):
        old = LeaveRequest.objects.create(
            resident_training=self.training,
            leave_type="STUDY",
            start_date=self.today + timedelta(days=2),
            end_date=self.today + timedelta(days=10),
            reason="Existing untouched leave",
        )
        original = LeaveRequest.objects.filter(pk=old.pk).values().get()
        result = self.run_seed()
        self.assertEqual(LeaveRequest.objects.filter(pk=old.pk).values().get(), original)
        spans = [
            (r["start_date"], r["end_date"])
            for r in result["records"]
            if r["feature"] in ("rotation", "leave")
        ]
        for i, (start, end) in enumerate(spans):
            for other_start, other_end in spans[i + 1 :]:
                self.assertFalse(start <= other_end and end >= other_start)

    def test_misowned_marker_is_rejected(self):
        self.run_seed()
        other = create_user_with_profile(
            username="unrelated", role="RESIDENT", full_name="Unrelated test identity"
        )
        ResidentDocument.objects.filter(extra_data__demo_key=Command.key("document", 1)).update(
            resident=other.resident_profile
        )
        with self.assertRaises(CommandError):
            self.run_seed()

    def test_actions_use_actual_handlers_and_role_permissions(self):
        self.run_seed()
        command = Command()
        command.users = self.users
        pending = list(LeaveRequest.objects.filter(status="SUBMITTED").order_by("pk"))
        with self.assertRaises(CommandError):
            command.request(LeaveRequestViewSet, "approve", "resident", pk=pending[0].pk)
        command.request(LeaveRequestViewSet, "approve", "supervisor", pk=pending[0].pk)
        command.request(
            LeaveRequestViewSet,
            "reject",
            "supervisor",
            {"reason": "Demo scheduling conflict"},
            pk=pending[1].pk,
        )
        draft = LeaveRequest.objects.get(status="DRAFT")
        command.request(LeaveRequestViewSet, "submit", "resident", pk=draft.pk)
        returned = LogbookEntry.objects.get(status="RETURNED")
        services.update_logbook_draft(
            entry=returned, resident_reflection="Added learning point", actor=self.users["resident"]
        )
        services.submit_logbook_entry(entry=returned, actor=self.users["resident"])
        evaluation = EvaluationSubmission.objects.filter(status="SUBMITTED").first()
        services.start_evaluation_review(submission=evaluation, actor=self.users["supervisor"])
        services.approve_evaluation(
            submission=evaluation,
            score=4,
            max_score=5,
            supervisor_comments="Reviewed",
            actor=self.users["supervisor"],
        )
        approved = RotationAssignment.objects.get(status="APPROVED")
        command.request(RotationAssignmentViewSet, "activate", "admin", pk=approved.pk)
        active = RotationAssignment.objects.get(
            notes__startswith=f"[{Command.key('rotation', 4)}] "
        )
        command.request(RotationAssignmentViewSet, "complete", "admin", pk=active.pk)
        document = ResidentDocument.objects.filter(status="PENDING_REVIEW").first()
        with self.assertRaises(CommandError):
            command.request(
                ResidentDocumentViewSet,
                "review",
                "supervisor",
                {"status": "VERIFIED"},
                pk=document.pk,
            )
        command.request(
            ResidentDocumentViewSet,
            "review",
            "admin",
            {"status": "VERIFIED", "remarks": "Demo review"},
            pk=document.pk,
        )
        self.assertTrue(
            SupervisorReviewQueueItem.objects.filter(
                resident=self.resident, supervisor=self.supervisor
            ).exists()
        )

    def test_verify_missing_is_read_only_failure(self):
        with self.assertRaises(CommandError):
            self.run_seed("verify")
        self.assertFalse(LogbookEntry.objects.exists())

    def test_missing_attachment_fails_verification(self):
        self.run_seed()
        document = ResidentDocument.objects.filter(extra_data__demo_dataset=DATASET).first()
        document.file.storage.delete(document.file.name)
        with self.assertRaises(CommandError):
            self.run_seed("verify")

    def test_schedule_failure_has_no_partial_records(self):
        self.training.expected_end_date = self.today + timedelta(days=3)
        self.training.save()
        with self.assertRaises(CommandError):
            self.run_seed()
        self.assertFalse(LogbookEntry.objects.exists())

    def test_import_samples_match_real_academic_session_contract(self):
        from sims.bulk.services import BulkService
        from sims.academics.models import AcademicSession
        from django.core.files.uploadedfile import SimpleUploadedFile

        root = Path(__file__).resolve().parents[3] / "demo_data/three_account_demo"
        before = AcademicSession.objects.count()
        service = BulkService(actor=self.users["admin"])
        for filename, successes, failures in [
            ("academic_sessions_valid.csv", 4, 0),
            ("academic_sessions_invalid.csv", 0, 2),
        ]:
            file = SimpleUploadedFile(
                filename, (root / filename).read_bytes(), content_type="text/csv"
            )
            operation = service.import_academic_sessions(file, dry_run=True)
            self.assertEqual(operation.success_count, successes)
            self.assertEqual(operation.failure_count, failures)
        self.assertEqual(AcademicSession.objects.count(), before)

    def test_outbound_transports_are_disabled_during_seed(self):
        from django.conf import settings

        original = Command.create_example

        def assert_settings(command, *args):
            self.assertFalse(settings.FCM_ENABLED)
            self.assertEqual(settings.EMAIL_BACKEND, "django.core.mail.backends.dummy.EmailBackend")
            return original(command, *args)

        with patch.object(Command, "create_example", assert_settings):
            self.run_seed()
