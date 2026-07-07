from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from sims.academics.models import Department
from sims.rotations.models import Hospital, HospitalDepartment
from sims.training.models import (
    LogbookThresholdConfig,
    ProgramRotationRequirement,
    ProgramMilestone,
    ProgramMilestoneResearchRequirement,
    ResidentSubmission,
    ResidentResearchProject,
    ResidentTrainingRecord,
    SubmissionRequirementTemplate,
    TrainingProgram,
)
from sims.users.models import DepartmentMembership, SupervisorResidentLink, User


class Command(BaseCommand):
    help = "Seed deterministic single-hospital E2E data."

    @transaction.atomic
    def handle(self, *args, **options):
        today = timezone.now().date()
        departments_seed = [
            ("SURG", "Surgery"),
            ("MED", "Medicine"),
            ("PED", "Pediatrics"),
            ("OBG", "Gynecology & Obstetrics"),
            ("ORTH", "Orthopedics"),
        ]

        # Single-hospital mode: only one active hospital, keep model/relations intact.
        Hospital.objects.exclude(code="UTRMC").update(is_active=False)
        hospital, _ = Hospital.objects.update_or_create(
            code="UTRMC",
            defaults={
                "name": "UTRMC Teaching Hospital",
                "is_active": True,
            },
        )

        departments = []
        for code, name in departments_seed:
            # Use code as the lookup key (unique); fall back to name-based lookup.
            department = Department.objects.filter(code=code).first()
            if department is None:
                department = Department.objects.filter(name=name).first()
            if department is not None:
                department.code = code
                department.name = name
                department.active = True
                department.save()
            else:
                department = Department.objects.create(code=code, name=name, active=True)
            departments.append(department)
            HospitalDepartment.objects.update_or_create(
                hospital=hospital,
                department=department,
                defaults={"is_active": True},
            )

        def upsert_user(*, username, password, **fields):
            user = User.objects.filter(username=username).first()
            if user is None:
                return User.objects.create_user(username=username, password=password, **fields)
            for key, value in fields.items():
                setattr(user, key, value)
            user.set_password(password)
            user.save()
            return user

        e2e_admin = upsert_user(
            username="e2e_admin",
            password="Admin123!",
            email="e2e_admin@pgsims.local",
            role="ADMIN",
            first_name="E2E",
            last_name="Admin",
        )

        upsert_user(
            username="e2e_utrmc_user",
            password="Utrmc123!",
            email="e2e_utrmc_user@pgsims.local",
            role="SUPPORT_STAFF",
            first_name="E2E",
            last_name="UTRMC User",
        )

        e2e_utrmc_admin = upsert_user(
            username="e2e_utrmc_admin",
            password="UtrmcAdmin123!",
            email="e2e_utrmc_admin@pgsims.local",
            role="ADMIN",
            first_name="E2E",
            last_name="UTRMC Admin",
        )

        supervisor = upsert_user(
            username="e2e_supervisor",
            password="Supervisor123!",
            email="e2e_supervisor@pgsims.local",
            role="SUPERVISOR",
            specialty="surgery",
            first_name="E2E",
            last_name="Supervisor",
        )

        pg = upsert_user(
            username="e2e_pg",
            password="Pg123456!",
            email="e2e_pg@pgsims.local",
            role="RESIDENT",
            specialty="surgery",
            year="1",
            supervisor=supervisor,
            home_hospital=hospital,
            home_department=departments[0],
            first_name="E2E",
            last_name="PG",
        )

        SupervisorResidentLink.objects.update_or_create(
            supervisor_user=supervisor,
            resident_user=pg,
            defaults={
                "active": True,
                "start_date": today,
                "department": departments[0],
            },
        )

        # Feature-layer explicit role fixtures for Playwright verification suite.
        supervisor_user = upsert_user(
            username="supervisor_user",
            password="SupervisorUser123!",
            email="supervisor_user@pgsims.local",
            role="SUPERVISOR",
            specialty="surgery",
            first_name="Feature",
            last_name="Supervisor",
            home_hospital=hospital,
            home_department=departments[0],
        )
        hod_user = upsert_user(
            username="hod_user",
            password="HodUser123!",
            email="hod_user@pgsims.local",
            role="SUPERVISOR",
            specialty="surgery",
            first_name="Feature",
            last_name="HOD",
            home_hospital=hospital,
            home_department=departments[0],
        )
        resident_user = upsert_user(
            username="resident_user",
            password="ResidentUser123!",
            email="resident_user@pgsims.local",
            role="RESIDENT",
            specialty="surgery",
            year="1",
            supervisor=supervisor_user,
            home_hospital=hospital,
            home_department=departments[0],
            first_name="Feature",
            last_name="Resident",
        )
        upsert_user(
            username="utrmc_admin_user",
            password="UtrmcAdminUser123!",
            email="utrmc_admin_user@pgsims.local",
            role="ADMIN",
            first_name="Feature",
            last_name="UTRMC Admin",
        )
        upsert_user(
            username="utrmc_staff_user",
            password="UtrmcStaffUser123!",
            email="utrmc_staff_user@pgsims.local",
            role="SUPPORT_STAFF",
            first_name="Feature",
            last_name="UTRMC Staff",
        )
        negative_role_user = upsert_user(
            username="negative_role_user",
            password="NegativeRole123!",
            email="negative_role_user@pgsims.local",
            role="RESIDENT",
            specialty="medicine",
            year="1",
            home_hospital=hospital,
            home_department=departments[1],
            first_name="Feature",
            last_name="Negative",
        )

        DepartmentMembership.objects.update_or_create(
            user=supervisor_user,
            department=departments[0],
            member_type=DepartmentMembership.MEMBER_SUPERVISOR,
            defaults={
                "is_primary": False,
                "active": True,
                "start_date": today,
                "created_by": e2e_admin,
            },
        )
        DepartmentMembership.objects.update_or_create(
            user=hod_user,
            department=departments[0],
            member_type=DepartmentMembership.MEMBER_SUPERVISOR,
            defaults={
                "is_primary": False,
                "active": True,
                "start_date": today,
                "created_by": e2e_admin,
            },
        )
        SupervisorResidentLink.objects.update_or_create(
            supervisor_user=supervisor_user,
            resident_user=resident_user,
            defaults={
                "active": True,
                "start_date": today,
                "department": departments[0],
            },
        )

        # Deterministic training baseline for workflow E2E
        program, _ = TrainingProgram.objects.update_or_create(
            code="E2E-FCPS",
            defaults={
                "name": "E2E Baseline FCPS Program",
                "duration_months": 48,
                "description": "Deterministic training baseline for Playwright workflow gate",
                "degree_type": TrainingProgram.DEGREE_FCPS,
                "department": departments[0],
                "notes": "Managed by seed_e2e",
                "active": True,
            },
        )

        imm, _ = ProgramMilestone.objects.update_or_create(
            program=program,
            code=ProgramMilestone.CODE_IMM,
            defaults={
                "name": "Intermediate Membership",
                "recommended_month": 24,
                "is_active": True,
            },
        )
        final, _ = ProgramMilestone.objects.update_or_create(
            program=program,
            code=ProgramMilestone.CODE_FINAL,
            defaults={
                "name": "Final Examination",
                "recommended_month": 48,
                "is_active": True,
            },
        )

        ProgramMilestoneResearchRequirement.objects.update_or_create(
            milestone=imm,
            defaults={
                "requires_synopsis_approved": True,
                "requires_synopsis_submitted_to_university": False,
                "requires_thesis_submitted": False,
            },
        )
        ProgramMilestoneResearchRequirement.objects.update_or_create(
            milestone=final,
            defaults={
                "requires_synopsis_approved": True,
                "requires_synopsis_submitted_to_university": False,
                "requires_thesis_submitted": True,
            },
        )
        # Keep eligibility reasons deterministic for gate assertions.
        imm.workshop_requirements.all().delete()
        imm.logbook_requirements.all().delete()
        final.workshop_requirements.all().delete()
        final.logbook_requirements.all().delete()

        ResidentTrainingRecord.objects.filter(resident_user=pg).exclude(program=program).update(active=False)
        rtr, _ = ResidentTrainingRecord.objects.update_or_create(
            resident_user=pg,
            program=program,
            defaults={
                "start_date": today - timedelta(days=365),
                "expected_end_date": today + timedelta(days=365 * 3),
                "current_level": "y2",
                "status": ResidentTrainingRecord.STATUS_ACTIVE,
                "locked_program": True,
                "restart_from_scratch_on_change": True,
                "active": True,
                "created_by": supervisor,
            },
        )
        ResidentTrainingRecord.objects.filter(resident_user=resident_user).exclude(program=program).update(
            active=False
        )
        resident_rtr, _ = ResidentTrainingRecord.objects.update_or_create(
            resident_user=resident_user,
            program=program,
            defaults={
                "start_date": today - timedelta(days=220),
                "expected_end_date": today + timedelta(days=365 * 3),
                "current_level": "y1",
                "status": ResidentTrainingRecord.STATUS_ACTIVE,
                "locked_program": True,
                "restart_from_scratch_on_change": True,
                "active": True,
                "created_by": supervisor_user,
            },
        )
        ResidentTrainingRecord.objects.filter(resident_user=negative_role_user).exclude(program=program).update(
            active=False
        )
        negative_rtr, _ = ResidentTrainingRecord.objects.update_or_create(
            resident_user=negative_role_user,
            program=program,
            defaults={
                "start_date": today - timedelta(days=140),
                "expected_end_date": today + timedelta(days=365 * 3),
                "current_level": "y1",
                "status": ResidentTrainingRecord.STATUS_ACTIVE,
                "locked_program": True,
                "restart_from_scratch_on_change": True,
                "active": True,
                "created_by": supervisor_user,
            },
        )

        # Keep feature-layer seeded resident deterministic between runs.
        resident_rtr.logbook_entries.all().delete()
        ResidentSubmission.objects.filter(resident_training_record=resident_rtr).delete()
        resident_rtr.rotation_assignments.all().delete()
        resident_rtr.logbook_threshold_snapshots.all().delete()
        ResidentResearchProject.objects.filter(resident_training_record=resident_rtr).delete()
        negative_rtr.logbook_entries.all().delete()
        ResidentSubmission.objects.filter(resident_training_record=negative_rtr).delete()
        negative_rtr.rotation_assignments.all().delete()
        negative_rtr.logbook_threshold_snapshots.all().delete()
        ResidentResearchProject.objects.filter(resident_training_record=negative_rtr).delete()

        ResidentResearchProject.objects.update_or_create(
            resident_training_record=rtr,
            defaults={
                "title": "E2E Baseline Research Project",
                "topic_area": "Clinical Education",
                "SUPERVISOR": supervisor,
                "status": ResidentResearchProject.STATUS_SUBMITTED_SUPERVISOR,
                "supervisor_feedback": "",
                "submitted_to_supervisor_at": timezone.now(),
                "synopsis_approved_at": None,
                "submitted_to_university_at": None,
                "accepted_at": None,
                "university_submission_ref": "",
            },
        )

        ProgramRotationRequirement.objects.update_or_create(
            program=program,
            department=departments[1],
            sequence_order=1,
            defaults={
                "required_duration_weeks": 4,
                "is_mandatory": True,
                "notes": "E2E phase-1 rotational requirement.",
            },
        )

        LogbookThresholdConfig.objects.update_or_create(
            name="E2E Logbook Threshold Per Rotation",
            mode=LogbookThresholdConfig.MODE_PER_ROTATION,
            program=program,
            department=departments[0],
            defaults={
                "min_approved_entries": 1,
                "period_days": None,
                "is_active": True,
                "configured_by": e2e_utrmc_admin,
            },
        )
        LogbookThresholdConfig.objects.update_or_create(
            name="E2E Logbook Threshold Per 30 Days",
            mode=LogbookThresholdConfig.MODE_PER_PERIOD,
            program=program,
            department=departments[0],
            defaults={
                "min_approved_entries": 1,
                "period_days": 30,
                "is_active": True,
                "configured_by": e2e_utrmc_admin,
            },
        )

        SubmissionRequirementTemplate.objects.update_or_create(
            submission_type=SubmissionRequirementTemplate.TYPE_SYNOPSIS,
            program=program,
            department=departments[0],
            code="SYN-PROPOSAL",
            defaults={
                "title": "Synopsis Proposal",
                "description": "Core synopsis proposal document.",
                "is_required": True,
                "active": True,
                "sort_order": 1,
                "created_by": e2e_admin,
            },
        )
        SubmissionRequirementTemplate.objects.update_or_create(
            submission_type=SubmissionRequirementTemplate.TYPE_SYNOPSIS,
            program=program,
            department=departments[0],
            code="SYN-ETHICS",
            defaults={
                "title": "Synopsis Ethics Sheet",
                "description": "Ethics and compliance attachment.",
                "is_required": True,
                "active": True,
                "sort_order": 2,
                "created_by": e2e_admin,
            },
        )
        SubmissionRequirementTemplate.objects.update_or_create(
            submission_type=SubmissionRequirementTemplate.TYPE_THESIS,
            program=program,
            department=departments[0],
            code="THS-MANUSCRIPT",
            defaults={
                "title": "Thesis Manuscript",
                "description": "Main thesis manuscript for completeness check.",
                "is_required": True,
                "active": True,
                "sort_order": 1,
                "created_by": e2e_admin,
            },
        )
        SubmissionRequirementTemplate.objects.update_or_create(
            submission_type=SubmissionRequirementTemplate.TYPE_THESIS,
            program=program,
            department=departments[0],
            code="THS-SIMILARITY",
            defaults={
                "title": "Similarity Report",
                "description": "Similarity/plagiarism report document.",
                "is_required": True,
                "active": True,
                "sort_order": 2,
                "created_by": e2e_admin,
            },
        )

        from sims.training.eligibility import recompute_for_record

        recompute_for_record(rtr)
        recompute_for_record(resident_rtr)

        self.stdout.write(self.style.SUCCESS("seed_e2e completed successfully."))
