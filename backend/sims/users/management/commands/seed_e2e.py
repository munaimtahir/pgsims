from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from sims.academics.models import Department
from sims.rotations.models import Hospital, HospitalDepartment
from sims.users.models import User


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

        self.stdout.write(self.style.SUCCESS("seed_e2e completed successfully."))
