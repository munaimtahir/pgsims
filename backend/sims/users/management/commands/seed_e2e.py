from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from sims.academics.models import Department
from sims.rotations.models import Hospital, HospitalDepartment, Rotation
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
            department, _ = Department.objects.update_or_create(
                code=code,
                defaults={"name": name, "active": True},
            )
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

        rotation_specs = [
            # completed
            (departments[0], today - timedelta(days=90), today - timedelta(days=61), "completed"),
            # ongoing
            (departments[1], today - timedelta(days=20), today + timedelta(days=20), "ongoing"),
            # planned
            (departments[2], today + timedelta(days=30), today + timedelta(days=60), "planned"),
        ]
        for department, start_date, end_date, status in rotation_specs:
            Rotation.objects.update_or_create(
                pg=pg,
                department=department,
                start_date=start_date,
                end_date=end_date,
                defaults={
                    "hospital": hospital,
                    "supervisor": supervisor,
                    "status": status,
                },
            )

        self.stdout.write(self.style.SUCCESS("seed_e2e completed successfully."))
