from __future__ import annotations

from datetime import timedelta

from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from sims.academics.models import Department
from sims.audit.models import ActivityLog, AuditReport
from sims.bulk.models import BulkOperation
from sims.notifications.models import Notification, NotificationPreference
from sims.rotations.models import Hospital, HospitalDepartment
from sims.training.eligibility import recompute_for_record
from sims.training.models import (
    DeputationPosting,
    LeaveRequest,
    LogbookEntry,
    LogbookReview,
    LogbookThresholdConfig,
    LogbookThresholdSnapshot,
    ProgramMilestone,
    ProgramMilestoneLogbookRequirement,
    ProgramMilestoneResearchRequirement,
    ProgramMilestoneWorkshopRequirement,
    ProgramPolicy,
    ProgramRotationRequirement,
    ProgramRotationTemplate,
    ResidentMilestoneEligibility,
    ResidentResearchProject,
    ResidentSubmission,
    ResidentThesis,
    ResidentTrainingRecord,
    ResidentWorkshopCompletion,
    RotationAssignment,
    RotationCompletion,
    RotationCertificate,
    SubmissionCertificate,
    SubmissionDocument,
    SubmissionRequirementTemplate,
    SubmissionReview,
    TrainingProgram,
    Workshop,
    WorkshopBlock,
    WorkshopRun,
)
from sims.users.models import (
    DataCorrectionAudit,
    DepartmentMembership,
    HospitalAssignment,
    ResidentProfile,
    SupervisorResidentLink,
    User,
    SupervisorProfile,
)

UserModel = get_user_model()


class ResetDemoDataCommandTests(TestCase):
    def setUp(self):
        call_command("initialize_pgsims_baseline", verbosity=0)
        self.admin = UserModel.objects.get(username="ADMIN")

        self.hospital = Hospital.objects.create(
            code="H-1778624851512",
            name="Hospital e2e-1778624851512",
            is_active=True,
        )
        self.department = Department.objects.create(
            code="D-1778624851512",
            name="Department e2e-1778624851512",
            active=True,
        )
        self.matrix = HospitalDepartment.objects.create(
            hospital=self.hospital,
            department=self.department,
            is_active=True,
        )

        self.supervisor = UserModel.objects.create_user(
            username="supervisor_user",
            password="SupervisorUser123!",
            email="supervisor_user@pgsims.local",
            first_name="Feature",
            last_name="Supervisor",
            role="SUPERVISOR",
            specialty="medicine",
            home_hospital=self.hospital,
            home_department=self.department,
        )
        self.hod = UserModel.objects.create_user(
            username="hod_user",
            password="HodUser123!",
            email="hod_user@pgsims.local",
            first_name="Feature",
            last_name="HOD",
            role="SUPERVISOR",
            specialty="medicine",
            home_hospital=self.hospital,
            home_department=self.department,
        )
        self.resident = UserModel.objects.create_user(
            username="resident_user",
            password="ResidentUser123!",
            email="resident_user@pgsims.local",
            first_name="Feature",
            last_name="Resident",
            role="RESIDENT",
            specialty="medicine",
            year="1",
            supervisor=self.supervisor,
            home_hospital=self.hospital,
            home_department=self.department,
        )

        SupervisorProfile.objects.create(user=self.supervisor, designation_ref="Professor")
        ResidentProfile.objects.create(
            user=self.resident,
            registration_no="PGR-001",
        )

        DepartmentMembership.objects.create(
            user=self.supervisor,
            department=self.department,
            member_type=DepartmentMembership.MEMBER_SUPERVISOR,
            is_primary=True,
            active=True,
            start_date=timezone.now().date(),
            created_by=self.admin,
            updated_by=self.admin,
        )
        DepartmentMembership.objects.create(
            user=self.resident,
            department=self.department,
            member_type=DepartmentMembership.MEMBER_RESIDENT,
            is_primary=True,
            active=True,
            start_date=timezone.now().date(),
            created_by=self.admin,
            updated_by=self.admin,
        )
        HospitalAssignment.objects.create(
            user=self.resident,
            hospital_department=self.matrix,
            assignment_type=HospitalAssignment.ASSIGNMENT_PRIMARY_TRAINING,
            active=True,
            start_date=timezone.now().date(),
            created_by=self.admin,
            updated_by=self.admin,
        )
        SupervisorResidentLink.objects.create(
            supervisor_user=self.supervisor,
            resident_user=self.resident,
            department=self.department,
            active=True,
            start_date=timezone.now().date(),
            created_by=self.admin,
            updated_by=self.admin,
        )
        SupervisorProfile.objects.create(
            user=self.hod,
            designation_ref="HOD",
            department_ref=self.department,
        )

        self.program = TrainingProgram.objects.create(
            code="E2E-FCPS",
            name="E2E Baseline FCPS Program",
            duration_months=48,
            description="Demo program for cleanup validation",
            degree_type=TrainingProgram.DEGREE_FCPS,
            department=self.department,
            notes="Managed by seed_e2e",
            active=True,
        )
        ProgramPolicy.objects.create(program=self.program)
        self.milestone = ProgramMilestone.objects.create(
            program=self.program,
            code=ProgramMilestone.CODE_IMM,
            name="Intermediate Membership",
            recommended_month=24,
            is_active=True,
        )
        ProgramMilestoneResearchRequirement.objects.create(
            milestone=self.milestone,
            requires_synopsis_approved=True,
        )
        self.demo_workshop = Workshop.objects.create(
            name="Demo Workshop",
            code="DEMO-WS-1",
            description="Demo workshop",
            is_active=True,
        )
        ProgramMilestoneWorkshopRequirement.objects.create(
            milestone=self.milestone,
            workshop=self.demo_workshop,
            required_count=1,
        )
        ProgramMilestoneLogbookRequirement.objects.create(
            milestone=self.milestone,
            procedure_key="demo-procedure",
            category="Demo",
            min_entries=1,
        )
        ProgramRotationRequirement.objects.create(
            program=self.program,
            department=self.department,
            required_duration_weeks=4,
            sequence_order=1,
            is_mandatory=True,
        )
        self.rotation_template = ProgramRotationTemplate.objects.create(
            program=self.program,
            name="Demo Rotation Template",
            department=self.department,
            duration_weeks=4,
            required=True,
            sequence_order=1,
            active=True,
        )
        self.threshold_config = LogbookThresholdConfig.objects.create(
            name="Demo Threshold",
            mode=LogbookThresholdConfig.MODE_PER_ROTATION,
            min_approved_entries=1,
            program=self.program,
            department=self.department,
            is_active=True,
            configured_by=self.supervisor,
        )
        self.training_record = ResidentTrainingRecord.objects.create(
            resident_user=self.resident,
            program=self.program,
            start_date=timezone.now().date() - timedelta(days=120),
            expected_end_date=timezone.now().date() + timedelta(days=365),
            current_level="y1",
            status=ResidentTrainingRecord.STATUS_ACTIVE,
            active=True,
            created_by=self.supervisor,
        )
        self.rotation = RotationAssignment.objects.create(
            resident_training=self.training_record,
            hospital_department=self.matrix,
            template=self.rotation_template,
            start_date=timezone.now().date() - timedelta(days=7),
            end_date=timezone.now().date() + timedelta(days=7),
            status=RotationAssignment.STATUS_SUBMITTED,
            requested_by=self.supervisor,
        )
        self.rotation_completion = RotationCompletion.objects.create(
            rotation=self.rotation,
            status=RotationCompletion.STATUS_CONFIRMED_BY_DEPARTMENT,
            confirmed_by=self.supervisor,
        )
        RotationCertificate.objects.create(
            completion=self.rotation_completion,
            certificate_number="RC-1778624851512",
            issued_by=self.supervisor,
        )
        LeaveRequest.objects.create(
            resident_training=self.training_record,
            leave_type=LeaveRequest.TYPE_ANNUAL,
            start_date=timezone.now().date() + timedelta(days=10),
            end_date=timezone.now().date() + timedelta(days=12),
            reason="Workflow test",
            status=LeaveRequest.STATUS_SUBMITTED,
            approved_by=self.supervisor,
        )
        DeputationPosting.objects.create(
            resident_training=self.training_record,
            posting_type=DeputationPosting.TYPE_DEPUTATION,
            institution_name="Test Hospital WF-1778624779089",
            city="Faisalabad",
            start_date=timezone.now().date() + timedelta(days=20),
            end_date=timezone.now().date() + timedelta(days=30),
            status=DeputationPosting.STATUS_SUBMITTED,
            approved_by=self.supervisor,
        )
        self.research_project = ResidentResearchProject.objects.create(
            resident_training_record=self.training_record,
            title="Demo research",
            topic_area="Clinical education",
            supervisor=self.supervisor,
            status=ResidentResearchProject.STATUS_SUBMITTED_SUPERVISOR,
        )
        self.thesis = ResidentThesis.objects.create(
            resident_training_record=self.training_record,
            status=ResidentThesis.STATUS_IN_PROGRESS,
        )
        ResidentWorkshopCompletion.objects.create(
            resident_training_record=self.training_record,
            workshop=self.demo_workshop,
            completed_at=timezone.now().date(),
        )
        self.submission_template = SubmissionRequirementTemplate.objects.create(
            submission_type=SubmissionRequirementTemplate.TYPE_SYNOPSIS,
            program=self.program,
            department=self.department,
            code="SYN-DEMO",
            title="Demo Synopsis",
            description="Demo requirement",
            is_required=True,
            active=True,
            sort_order=1,
            created_by=self.admin,
        )
        self.submission = ResidentSubmission.objects.create(
            resident_training_record=self.training_record,
            submission_type=ResidentSubmission.TYPE_SYNOPSIS,
            status=ResidentSubmission.STATUS_SUBMITTED,
            submitted_at=timezone.now(),
            reviewed_by=self.supervisor,
        )
        SubmissionDocument.objects.create(
            submission=self.submission,
            requirement=self.submission_template,
            file=SimpleUploadedFile("demo.txt", b"demo"),
            original_filename="demo.txt",
            uploaded_by=self.supervisor,
        )
        SubmissionReview.objects.create(
            submission=self.submission,
            reviewer=self.supervisor,
            action=SubmissionReview.ACTION_RETURNED,
            comments="Demo returned",
        )
        SubmissionCertificate.objects.create(
            submission=self.submission,
            certificate_number="SC-1778624851512",
            issued_by=self.supervisor,
        )
        self.logbook_entry = LogbookEntry.objects.create(
            resident_training_record=self.training_record,
            patient_id_number="P-1778624851512",
            patient_name="Demo Patient",
            disease_area="Demo",
            patient_seen_at=timezone.now(),
            status=LogbookEntry.STATUS_SUBMITTED,
            reviewed_by=self.supervisor,
            created_by=self.supervisor,
        )
        LogbookReview.objects.create(
            entry=self.logbook_entry,
            reviewer=self.supervisor,
            action=LogbookReview.ACTION_RETURNED,
            comments="Demo returned",
        )
        LogbookThresholdSnapshot.objects.create(
            resident_training_record=self.training_record,
            threshold_config=self.threshold_config,
            rotation_assignment=self.rotation,
            approved_entries=0,
            required_entries=1,
            is_met=False,
        )
        recompute_for_record(self.training_record)
        NotificationPreference.for_user(self.resident)
        Notification.objects.create(
            recipient=self.resident,
            actor=self.supervisor,
            verb="demo-seeded",
            title="Demo notification",
            body="Seeded by seed_demo_data",
            metadata={"seed_source": "seed_demo_data"},
        )
        BulkOperation.objects.create(
            user=self.supervisor,
            operation=BulkOperation.OP_IMPORT,
            status=BulkOperation.STATUS_COMPLETED,
            details={"seed_source": "seed_demo_data"},
        )
        DataCorrectionAudit.objects.create(
            actor=self.supervisor,
            entity_type="User",
            entity_id=str(self.resident.id),
            field_name="email",
            old_value="old@test.com",
            new_value="new@test.com",
            metadata={"seed": "demo"},
        )
        ActivityLog.objects.create(
            actor=self.supervisor,
            action="create",
            verb="demo-seeded",
            target_repr="Demo target",
            metadata={"seed_source": "seed_demo_data"},
        )
        AuditReport.objects.create(
            created_by=self.supervisor,
            start=timezone.now() - timedelta(days=1),
            end=timezone.now(),
            payload={"seed_source": "seed_demo_data"},
        )

    def test_dry_run_does_not_delete_anything(self):
        before = self._snapshot_counts()
        call_command("reset_demo_data", verbosity=0)
        after = self._snapshot_counts()
        self.assertEqual(before, after)

    def test_confirm_removes_fake_graph_and_preserves_canonical_data(self):
        call_command("reset_demo_data", verbosity=0, confirm=True)

        self.assertTrue(UserModel.objects.filter(username="ADMIN").exists())
        self.assertTrue(UserModel.objects.get(username="ADMIN").is_superuser)
        self.assertTrue(UserModel.objects.get(username="ADMIN").check_password("admin123"))

        self.assertTrue(Hospital.objects.filter(code__in=["AH", "DHQ", "GGH", "UTRMC"]).count() >= 4)
        self.assertEqual(Hospital.objects.filter(name__icontains="e2e").count(), 0)
        self.assertEqual(Department.objects.filter(name__icontains="e2e").count(), 0)

        self.assertEqual(UserModel.objects.filter(username__in=["supervisor_user", "hod_user", "resident_user"]).count(), 0)
        self.assertEqual(HospitalDepartment.objects.filter(hospital=self.hospital).count(), 0)
        self.assertEqual(DepartmentMembership.objects.filter(department=self.department).count(), 0)
        self.assertEqual(HospitalAssignment.objects.filter(hospital_department__hospital=self.hospital).count(), 0)
        self.assertEqual(SupervisorResidentLink.objects.filter(department=self.department).count(), 0)
        self.assertEqual(SupervisorProfile.objects.filter(department_ref=self.department).count(), 0)
        self.assertEqual(TrainingProgram.objects.filter(code="E2E-FCPS").count(), 0)
        self.assertEqual(ProgramPolicy.objects.filter(program=self.program).count(), 0)
        self.assertEqual(ProgramMilestone.objects.filter(program=self.program).count(), 0)
        self.assertEqual(ProgramRotationRequirement.objects.filter(program=self.program).count(), 0)
        self.assertEqual(ProgramRotationTemplate.objects.filter(program=self.program).count(), 0)
        self.assertEqual(LogbookThresholdConfig.objects.filter(program=self.program).count(), 0)
        self.assertEqual(ResidentTrainingRecord.objects.filter(resident_user=self.resident).count(), 0)
        self.assertEqual(RotationAssignment.objects.filter(resident_training=self.training_record).count(), 0)
        self.assertEqual(RotationCompletion.objects.filter(rotation=self.rotation).count(), 0)
        self.assertEqual(RotationCertificate.objects.filter(completion=self.rotation_completion).count(), 0)
        self.assertEqual(LeaveRequest.objects.filter(resident_training=self.training_record).count(), 0)
        self.assertEqual(DeputationPosting.objects.filter(resident_training=self.training_record).count(), 0)
        self.assertEqual(ResidentMilestoneEligibility.objects.filter(resident_training_record=self.training_record).count(), 0)
        self.assertEqual(LogbookEntry.objects.filter(resident_training_record=self.training_record).count(), 0)
        self.assertEqual(LogbookReview.objects.filter(entry=self.logbook_entry).count(), 0)
        self.assertEqual(LogbookThresholdSnapshot.objects.filter(resident_training_record=self.training_record).count(), 0)
        self.assertEqual(ResidentSubmission.objects.filter(resident_training_record=self.training_record).count(), 0)
        self.assertEqual(SubmissionDocument.objects.filter(submission=self.submission).count(), 0)
        self.assertEqual(SubmissionReview.objects.filter(submission=self.submission).count(), 0)
        self.assertEqual(SubmissionCertificate.objects.filter(submission=self.submission).count(), 0)
        self.assertEqual(ResidentWorkshopCompletion.objects.filter(resident_training_record=self.training_record).count(), 0)
        self.assertEqual(NotificationPreference.objects.filter(user=self.resident).count(), 0)
        self.assertEqual(Notification.objects.filter(recipient=self.resident).count(), 0)
        self.assertEqual(BulkOperation.objects.filter(user=self.supervisor).count(), 0)
        self.assertEqual(ActivityLog.objects.filter(actor=self.supervisor).count(), 0)
        self.assertEqual(AuditReport.objects.filter(created_by=self.supervisor).count(), 0)

    def _snapshot_counts(self):
        return {
            "users": UserModel.objects.count(),
            "hospitals": Hospital.objects.count(),
            "departments": Department.objects.count(),
            "matrix": HospitalDepartment.objects.count(),
            "training_programs": TrainingProgram.objects.count(),
            "training_records": ResidentTrainingRecord.objects.count(),
            "rotations": RotationAssignment.objects.count(),
            "leaves": LeaveRequest.objects.count(),
            "eligibility": ResidentMilestoneEligibility.objects.count(),
            "logbook_entries": LogbookEntry.objects.count(),
            "submissions": ResidentSubmission.objects.count(),
        }


class InitializeBaselineCommandTests(TestCase):
    def test_initialize_is_idempotent(self):
        call_command("initialize_pgsims_baseline", verbosity=0)
        initial_snapshot = self._snapshot()

        call_command("initialize_pgsims_baseline", verbosity=0)
        self.assertEqual(self._snapshot(), initial_snapshot)

        self.assertTrue(UserModel.objects.filter(username="ADMIN", is_superuser=True).exists())
        self.assertEqual(UserModel.objects.filter(username="ADMIN").count(), 1)
        self.assertEqual(
            Group.objects.filter(name__in=["ADMIN", "RESIDENT", "SUPERVISOR", "SUPPORT_STAFF"]).count(),
            4,
        )

    def test_baseline_creates_canonical_org_data(self):
        call_command("initialize_pgsims_baseline", verbosity=0)

        self.assertEqual(Hospital.objects.count(), 4)
        self.assertEqual(Department.objects.count(), 20)
        self.assertTrue(Hospital.objects.filter(code="UTRMC", name="UTRMC Teaching Hospital").exists())
        self.assertTrue(Department.objects.filter(code="ANAES", name="Anaesthesia").exists())
        self.assertTrue(Department.objects.filter(code="SURG", name="Surgery").exists())

    def _snapshot(self):
        return {
            "groups": Group.objects.count(),
            "permissions": Permission.objects.count(),
            "hospitals": Hospital.objects.count(),
            "departments": Department.objects.count(),
            "users": UserModel.objects.count(),
        }
