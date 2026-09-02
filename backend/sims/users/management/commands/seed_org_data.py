"""Management command to seed canonical org data (hospitals, departments, matrix).

Usage:
    python manage.py seed_org_data          # idempotent upsert
    python manage.py seed_org_data --dry-run  # preview only
"""

from __future__ import annotations

from django.core.management.base import BaseCommand, CommandError

HOSPITALS = [
    {"code": "AH", "name": "Allied Hospital"},
    {"code": "DHQ", "name": "DHQ Hospital"},
    {"code": "GGH", "name": "Govt General Hospital Ghulam Muhammadabad"},
]

# Departments offered by each hospital (all major hospitals share most; GGH has core)
DEPARTMENTS_FULL = [
    {"code": "MED", "name": "General Medicine"},
    {"code": "SURG", "name": "General Surgery"},
    {"code": "PED", "name": "Paediatrics"},
    {"code": "OBG", "name": "Obstetrics & Gynaecology"},
    {"code": "ORTH", "name": "Orthopaedics"},
    {"code": "ENT", "name": "Ear, Nose & Throat"},
    {"code": "OPTH", "name": "Ophthalmology"},
    {"code": "DERM", "name": "Dermatology"},
    {"code": "PSY", "name": "Psychiatry"},
    {"code": "NEURO", "name": "Neurology"},
    {"code": "CARD", "name": "Cardiology"},
    {"code": "PULM", "name": "Pulmonology"},
    {"code": "GASTRO", "name": "Gastroenterology"},
    {"code": "NEPH", "name": "Nephrology"},
    {"code": "ONCO", "name": "Oncology"},
    {"code": "PATH", "name": "Pathology"},
    {"code": "RADIO", "name": "Radiology"},
    {"code": "ANAES", "name": "Anaesthesiology"},
    {"code": "EMERG", "name": "Emergency Medicine"},
    {"code": "ICU", "name": "Intensive Care Unit"},
]

# GGH (tehsil hospital) has core departments only
DEPARTMENTS_CORE = ["MED", "SURG", "PED", "OBG", "EMERG"]

# Matrix: which hospital hosts which departments
HOSPITAL_DEPT_MATRIX = {
    "AH": [d["code"] for d in DEPARTMENTS_FULL],   # full tertiary
    "DHQ": [d["code"] for d in DEPARTMENTS_FULL],  # full tertiary
    "GGH": DEPARTMENTS_CORE,                        # core only
}


class Command(BaseCommand):
    help = "Seed canonical org data: hospitals, departments, and hospital-department matrix."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            default=False,
            help="Preview what would be created without writing to DB.",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        try:
            from sims.rotations.models import Hospital, HospitalDepartment
            from sims.academics.models import Department
        except ImportError as exc:
            raise CommandError(f"Cannot import models: {exc}")

        mode = "DRY RUN" if dry_run else "APPLY"
        self.stdout.write(self.style.WARNING(f"=== seed_org_data ({mode}) ==="))

        # ----- Hospitals -----
        self.stdout.write("\n--- Hospitals ---")
        for h in HOSPITALS:
            if dry_run:
                exists = Hospital.objects.filter(code=h["code"]).exists()
                action = "EXISTS" if exists else "CREATE"
                self.stdout.write(f"  [{action}] {h['code']} — {h['name']}")
            else:
                obj, created = Hospital.objects.update_or_create(
                    code=h["code"],
                    defaults={"name": h["name"], "is_active": True},
                )
                self.stdout.write(
                    f"  [{'CREATED' if created else 'UPDATED'}] {obj.code} — {obj.name}"
                )

        # ----- Departments -----
        self.stdout.write("\n--- Departments ---")
        for d in DEPARTMENTS_FULL:
            if dry_run:
                exists = Department.objects.filter(code=d["code"]).exists()
                action = "EXISTS" if exists else "CREATE"
                self.stdout.write(f"  [{action}] {d['code']} — {d['name']}")
            else:
                obj, created = Department.objects.update_or_create(
                    code=d["code"],
                    defaults={"name": d["name"], "active": True},
                )
                self.stdout.write(
                    f"  [{'CREATED' if created else 'UPDATED'}] {obj.code} — {obj.name}"
                )

        if dry_run:
            self.stdout.write(
                self.style.SUCCESS("\nDry run complete. No changes were made.")
            )
            return

        # ----- Hospital-Department Matrix -----
        self.stdout.write("\n--- Hospital-Department Matrix ---")
        for hospital_code, dept_codes in HOSPITAL_DEPT_MATRIX.items():
            hospital = Hospital.objects.filter(code=hospital_code).first()
            if not hospital:
                self.stdout.write(self.style.ERROR(f"  Hospital {hospital_code} not found, skipping"))
                continue
            for dept_code in dept_codes:
                department = Department.objects.filter(code=dept_code).first()
                if not department:
                    self.stdout.write(
                        self.style.WARNING(f"  Department {dept_code} not found, skipping")
                    )
                    continue
                hd, created = HospitalDepartment.objects.update_or_create(
                    hospital=hospital,
                    department=department,
                    defaults={"is_active": True},
                )
                if created:
                    self.stdout.write(f"  [LINKED] {hospital_code} ↔ {dept_code}")

        total_hd = sum(len(v) for v in HOSPITAL_DEPT_MATRIX.values())
        self.stdout.write(
            self.style.SUCCESS(
                f"\nDone. {len(HOSPITALS)} hospitals, {len(DEPARTMENTS_FULL)} departments, "
                f"{total_hd} matrix entries seeded."
            )
        )
