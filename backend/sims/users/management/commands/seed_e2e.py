from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from sims.academics.models import Department
from sims.rotations.models import Hospital, HospitalDepartment
from sims.training.models import (
    ProgramMilestone,
    ProgramMilestoneResearchRequirement,
    ResidentResearchProject,
    ResidentTrainingRecord,
    TrainingProgram,
)
from sims.users.models import SupervisorResidentLink, User


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

        upsert_user(
            username="e2e_admin",
            password="Admin123!",
            email="e2e_admin@pgsims.local",
            role="admin",
            first_name="E2E",
            last_name="Admin",
        )

        upsert_user(
            username="e2e_utrmc_user",
            password="Utrmc123!",
            email="e2e_utrmc_user@pgsims.local",
            role="utrmc_user",
            first_name="E2E",
            last_name="UTRMC User",
        )

        upsert_user(
            username="e2e_utrmc_admin",
            password="UtrmcAdmin123!",
            email="e2e_utrmc_admin@pgsims.local",
            role="utrmc_admin",
            first_name="E2E",
            last_name="UTRMC Admin",
        )

        supervisor = upsert_user(
            username="e2e_supervisor",
            password="Supervisor123!",
            email="e2e_supervisor@pgsims.local",
            role="supervisor",
            specialty="surgery",
            first_name="E2E",
            last_name="Supervisor",
        )

        pg = upsert_user(
            username="e2e_pg",
            password="Pg123456!",
            email="e2e_pg@pgsims.local",
            role="pg",
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

        ResidentResearchProject.objects.update_or_create(
            resident_training_record=rtr,
            defaults={
                "title": "E2E Baseline Research Project",
                "topic_area": "Clinical Education",
                "supervisor": supervisor,
                "status": ResidentResearchProject.STATUS_SUBMITTED_SUPERVISOR,
                "supervisor_feedback": "",
                "submitted_to_supervisor_at": timezone.now(),
                "synopsis_approved_at": None,
                "submitted_to_university_at": None,
                "accepted_at": None,
                "university_submission_ref": "",
            },
        )

        from sims.training.eligibility import recompute_for_record

        recompute_for_record(rtr)

        self.stdout.write(self.style.SUCCESS("seed_e2e completed successfully."))
