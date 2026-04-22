from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from sims.academics.models import Department
from sims.rotations.models import Hospital
from sims.training.models import ResidentTrainingRecord, TrainingProgram
from sims.users.models import DepartmentMembership, SupervisorResidentLink, User


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
            "admin",
            "admin123",
            email="admin@pgsims.local",
            role="admin",
            first_name="Pilot",
            last_name="Admin",
            is_staff=True,
            is_superuser=True,
        )
        supervisor = upsert_user(
            "pilot_supervisor",
            "Pilot123!",
            email="pilot_supervisor@pgsims.local",
            role="supervisor",
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
            role="utrmc_admin",
            first_name="Pilot",
            last_name="UTRMC Admin",
        )
        upsert_user(
            "pilot_utrmc_user",
            "Pilot123!",
            email="pilot_utrmc_user@pgsims.local",
            role="utrmc_user",
            first_name="Pilot",
            last_name="UTRMC User",
        )
        residents = [
            upsert_user(
                "pilot_pg",
                "Pilot123!",
                email="pilot_pg@pgsims.local",
                role="pg",
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
                role="resident",
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

        program, _ = TrainingProgram.objects.update_or_create(
            code="ACTIVE-BASELINE",
            defaults={
                "name": "Active Surface Baseline Programme",
                "duration_months": 48,
                "degree_type": TrainingProgram.DEGREE_FCPS,
                "department": department,
                "description": "Minimal programme used by release-gated active-surface verification.",
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
            SupervisorResidentLink.objects.update_or_create(
                supervisor_user=supervisor,
                resident_user=resident,
                defaults={
                    "active": True,
                    "start_date": today,
                    "department": department,
                    "created_by": admin,
                    "updated_by": admin,
                },
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
