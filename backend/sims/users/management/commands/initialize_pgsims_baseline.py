from __future__ import annotations

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand
from django.db import transaction

from sims.academics.models import Department
from sims.rotations.models import Hospital

User = get_user_model()

HOSPITALS = [
    {"code": "AH", "name": "Allied Hospital"},
    {"code": "DHQ", "name": "DHQ Hospital"},
    {"code": "GGH", "name": "Govt General Hospital Ghulam Muhammadabad"},
    {"code": "UTRMC", "name": "UTRMC Teaching Hospital"},
]

DEPARTMENTS = [
    {"code": "ANAES", "name": "Anaesthesia"},
    {"code": "CARD", "name": "Cardiology"},
    {"code": "DERM", "name": "Dermatology"},
    {"code": "ENT", "name": "Ear, Nose & Throat"},
    {"code": "EMERG", "name": "Emergency Medicine"},
    {"code": "GASTRO", "name": "Gastroenterology"},
    {"code": "OBG", "name": "Gynecology & Obstetrics"},
    {"code": "ICU", "name": "Intensive Care Unit"},
    {"code": "MED", "name": "Medicine"},
    {"code": "NEPH", "name": "Nephrology"},
    {"code": "NEURO", "name": "Neurology"},
    {"code": "ONCO", "name": "Oncology"},
    {"code": "OPTH", "name": "Ophthalmology"},
    {"code": "ORTH", "name": "Orthopedics"},
    {"code": "PATH", "name": "Pathology"},
    {"code": "PED", "name": "Pediatrics"},
    {"code": "PSY", "name": "Psychiatry"},
    {"code": "PULM", "name": "Pulmonology"},
    {"code": "RADIO", "name": "Radiology"},
    {"code": "SURG", "name": "Surgery"},
]

ROLE_GROUPS = ["ADMIN", "RESIDENT", "SUPERVISOR", "SUPPORT_STAFF"]


class Command(BaseCommand):
    help = "Initialize the minimal real baseline: canonical org records, role groups, and admin access."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            default=False,
            help="Preview the baseline changes without writing to the database.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        dry_run = bool(options["dry_run"])
        self.stdout.write(self.style.WARNING(f"initialize_pgsims_baseline ({'DRY-RUN' if dry_run else 'APPLY'})"))

        created_groups = []
        for group_name in ROLE_GROUPS:
            if dry_run:
                created_groups.append(group_name)
                continue
            Group.objects.get_or_create(name=group_name)

        if not dry_run:
            admin_group = Group.objects.get(name="ADMIN")
            admin_group.permissions.set(Permission.objects.all())

        created_hospitals = []
        for spec in HOSPITALS:
            if dry_run:
                created_hospitals.append(spec["code"])
                continue
            Hospital.objects.update_or_create(
                code=spec["code"],
                defaults={"name": spec["name"], "is_active": True},
            )

        created_departments = []
        for spec in DEPARTMENTS:
            if dry_run:
                created_departments.append(spec["code"])
                continue
            Department.objects.update_or_create(
                code=spec["code"],
                defaults={"name": spec["name"], "active": True},
            )

        admin_user = None
        if not dry_run:
            admin_user, _ = User.objects.update_or_create(
                username="ADMIN",
                defaults={
                    "email": "admin@pgsims.local",
                    "first_name": "Pilot",
                    "last_name": "Admin",
                    "role": "ADMIN",
                    "is_staff": True,
                    "is_superuser": True,
                    "is_active": True,
                },
            )
            admin_user.set_password("admin123")
            admin_user.save()
            admin_user.groups.add(Group.objects.get(name="ADMIN"))

        self.stdout.write(f"Groups: {', '.join(ROLE_GROUPS)}")
        self.stdout.write(f"Hospitals: {', '.join(spec['code'] for spec in HOSPITALS)}")
        self.stdout.write(f"Departments: {', '.join(spec['code'] for spec in DEPARTMENTS)}")
        self.stdout.write("Hospital-department matrix: intentionally left empty for manual correction.")
        if admin_user is not None:
            self.stdout.write(f"Admin user ensured: {admin_user.username} <{admin_user.email}>")

        if dry_run:
            self.stdout.write(self.style.SUCCESS("Dry-run complete. No changes were made."))
            return

        self.stdout.write(self.style.SUCCESS("initialize_pgsims_baseline completed successfully."))
