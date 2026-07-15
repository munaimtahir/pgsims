from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from sims.academics.models import Department
from sims.rotations.models import Hospital
from sims.supervision.models import ResidentSupervisorAssignment
from sims.supervision.services import create_supervisor_assignment
from sims.training.models import ResidentTrainingRecord, TrainingProgram
from sims.users.models import DepartmentMembership, ResidentProfile, SupervisorProfile, User


class Command(BaseCommand):
    help = "Seed the minimal release-gated active surface baseline."

    @transaction.atomic
    def handle(self, *args, **options):
        today = timezone.now().date()

        department = Department.objects.filter(code="MED").first() or Department.objects.filter(active=True).first()
        hospital = Hospital.objects.filter(is_active=True).order_by("code").first()
        if department is None or hospital is None:
            self.stderr.write(
                self.style.ERROR("seed_org_data must run before seed_active_surface_baseline.")
            )
            return

        def upsert_user(username, password, **fields):
            user = User.objects.filter(username=username).first()
            if user is None:
                return User.objects.create_user(username=username, password=password, **fields)
            for key, value in fields.items():
                setattr(user, key, value)
            user.set_password(password)
            user.save()
            return user

        admin = upsert_user(
            "ADMIN",
            "admin123",
            email="admin@pgsims.local",
            role="ADMIN",
            first_name="Pilot",
            last_name="Admin",
            is_staff=True,
            is_superuser=True,
        )
        supervisor = upsert_user(
            "pilot_supervisor",
            "Pilot123!",
            email="pilot_supervisor@pgsims.local",
            role="SUPERVISOR",
            specialty="medicine",
            first_name="Pilot",
            last_name="Supervisor",
            home_hospital=hospital,
            home_department=department,
        )
        upsert_user(
            "pilot_utrmc_admin",
            "Pilot123!",
            email="pilot_utrmc_admin@pgsims.local",
            role="ADMIN",
            first_name="Pilot",
            last_name="UTRMC Admin",
        )
        upsert_user(
            "pilot_utrmc_user",
            "Pilot123!",
            email="pilot_utrmc_user@pgsims.local",
            role="SUPPORT_STAFF",
            first_name="Pilot",
            last_name="UTRMC User",
        )
        residents = [
            upsert_user(
                "pilot_pg",
                "Pilot123!",
                email="pilot_pg@pgsims.local",
                role="RESIDENT",
                specialty="medicine",
                year="1",
                supervisor=supervisor,
                first_name="Pilot",
                last_name="PG",
                home_hospital=hospital,
                home_department=department,
            ),
            upsert_user(
                "pilot_resident",
                "Pilot123!",
                email="pilot_resident@pgsims.local",
                role="RESIDENT",
                specialty="medicine",
                year="1",
                supervisor=supervisor,
                first_name="Pilot",
                last_name="Resident",
                home_hospital=hospital,
                home_department=department,
            ),
        ]

        DepartmentMembership.objects.update_or_create(
            user=supervisor,
            department=department,
            member_type=DepartmentMembership.MEMBER_SUPERVISOR,
            defaults={"active": True, "is_primary": True, "start_date": today, "created_by": admin},
        )
        supervisor_profile, _ = SupervisorProfile.objects.update_or_create(
            user=supervisor,
            defaults={"hospital": hospital, "department_ref": department},
        )

        program, _ = TrainingProgram.objects.update_or_create(
            code="ACTIVE-BASELINE",
            defaults={
                "name": "Active Surface Baseline Programme",
                "duration_months": 48,
                "degree_type": TrainingProgram.DEGREE_FCPS,
                "department": department,
                "description": "Minimal program used by release-gated active-surface verification.",
                "active": True,
            },
        )

        for resident in residents:
            DepartmentMembership.objects.update_or_create(
                user=resident,
                department=department,
                member_type=DepartmentMembership.MEMBER_RESIDENT,
                defaults={"active": True, "is_primary": True, "start_date": today, "created_by": admin},
            )
            resident_profile, _ = ResidentProfile.objects.update_or_create(
                user=resident,
                defaults={"hospital": hospital, "department_ref": department},
            )
            ResidentSupervisorAssignment.objects.filter(
                resident=resident_profile,
                supervisor=supervisor_profile,
                assignment_type=ResidentSupervisorAssignment.ASSIGNMENT_PRIMARY,
                is_active=True,
            ).first() or create_supervisor_assignment(
                resident=resident_profile,
                supervisor=supervisor_profile,
                assignment_type=ResidentSupervisorAssignment.ASSIGNMENT_PRIMARY,
                start_date=today,
                actor=admin,
            )
            ResidentTrainingRecord.objects.filter(resident_user=resident).exclude(program=program).update(active=False)
            ResidentTrainingRecord.objects.update_or_create(
                resident_user=resident,
                program=program,
                defaults={
                    "start_date": today - timedelta(days=120),
                    "expected_end_date": today + timedelta(days=365 * 3),
                    "current_level": "y1",
                    "status": ResidentTrainingRecord.STATUS_ACTIVE,
                    "active": True,
                    "has_default_dates": True,
                    "created_by": admin,
                },
            )

        self.stdout.write(self.style.SUCCESS("seed_active_surface_baseline completed successfully."))
