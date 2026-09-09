"""Idempotent bootstrap/import for the approved Urology institutional demo workbook.

The workbook is intentionally supplied at runtime and is not committed because it contains
resident personal data.  Run with ``--dry-run`` before ``--apply``.
"""
from __future__ import annotations

import re
import unicodedata
from datetime import date, datetime
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from openpyxl import load_workbook


WORKSHOPS = {
    "communication skills": ("WS-COMM", "Communication Skills"),
    "research synopsis & thesis writing skills": ("WS-RESEARCH-WRITING", "Research Synopsis & Thesis Writing Skills"),
    "basic biostatistics & research methodology": ("WS-BIOSTATS", "Basic Biostatistics & Research Methodology"),
    "information technology skills": ("WS-IT", "Information Technology Skills"),
    "initial life support (ils)": ("WS-ILS", "Initial Life Support (ILS)"),
}
SUPERVISORS = {
    "dr muhammad irfan munir": "Dr. Muhammad Irfan Munir",
    "prof dr m tahir bashir malik": "Prof. Dr. M. Tahir Bashir Malik",
    "prof dr muhammad akmal": "Prof. Dr. Muhammad Akmal",
    "dr sheraz javed": "Dr. Sheraz Javed",
    "prof dr muhammad akram": "Prof. Dr. Muhammad Akram",
}
STAGES = {"not started", "topic selected", "synopsis submitted", "approved", "completed"}
WORKSHOP_COLUMN = "Which workshop(s) have you attended? (Select all that apply)"


def norm(value):
    value = unicodedata.normalize("NFKD", str(value or "")).encode("ascii", "ignore").decode()
    value = re.sub(r"[^a-z0-9]+", " ", value.lower())
    return re.sub(r"\s+", " ", value).strip()


def person_norm(value):
    return re.sub(r"\b(prof|dr|mr|mrs|ms|miss|sb|proff)\b", "", norm(value)).strip()


def clean(value):
    return str(value).strip() if value is not None else ""


def as_date(value):
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    return datetime.strptime(clean(value), "%Y-%m-%d").date() if value else None


def year_number(value):
    match = re.search(r"(\d+)", clean(value))
    return int(match.group(1)) if match else None


def split_name(name):
    parts = clean(name).split()
    return (parts[0] if parts else "Resident", " ".join(parts[1:]) if len(parts) > 1 else "")


class Command(BaseCommand):
    help = "Bootstrap canonical institutional masters and import the approved Urology demo workbook."

    def add_arguments(self, parser):
        parser.add_argument("workbook", type=Path)
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, **options):
        path = options["workbook"]
        if not path.exists():
            raise CommandError(f"Workbook not found: {path}")
        wb = load_workbook(path, data_only=True, read_only=True)
        if "PGSIMS Resident Master" not in wb.sheetnames:
            raise CommandError("Workbook is missing the PGSIMS Resident Master sheet")
        ws = wb["PGSIMS Resident Master"]
        headers = [clean(x) for x in next(ws.iter_rows(values_only=True))]
        rows = [dict(zip(headers, row)) for row in ws.iter_rows(min_row=2, values_only=True)
                if clean(row[0]) and "APPROVED" in clean(row[1]).upper()]
        if len(rows) != 28:
            raise CommandError(f"Expected 28 approved residents, found {len(rows)}")
        if options["dry_run"]:
            self.stdout.write(self.style.SUCCESS("DRY RUN OK: 28 approved residents, 5 workshops, 5 research stages"))
            return

        from sims.academics.models import Department, Institution
        from sims.rotations.models import Hospital, HospitalDepartment
        from sims.training.models import ResidentResearchProject, ResidentTrainingRecord, ResidentWorkshopCompletion, Workshop
        from sims.supervision.models import ResidentSupervisorAssignment
        from sims.users.models import ResidentProfile, SupervisorProfile, User

        with transaction.atomic():
            institution, _ = Institution.objects.get_or_create(code="FMU", defaults={"name": "Faisalabad Medical University"})
            institution.name, institution.active = "Faisalabad Medical University", True
            institution.save(update_fields=["name", "active", "updated_at"])
            hospital = Hospital.objects.filter(code__in=["AHF-I", "AHF", "AHF-1"]).first()
            if not hospital:
                hospital = Hospital.objects.filter(name__iregex=r"allied hospital").first()
            if not hospital:
                hospital = Hospital(code="AHF-I", name="Allied Hospital-I Faisalabad")
            hospital.code, hospital.name, hospital.institution_id, hospital.is_active = "AHF-I", "Allied Hospital-I Faisalabad", institution.id, True
            hospital.save()
            department, _ = Department.objects.get_or_create(code="UROLOGY", defaults={"name": "Urology Department"})
            department.name, department.active = "Urology Department", True
            department.save(update_fields=["name", "active", "updated_at"])
            HospitalDepartment.objects.update_or_create(hospital=hospital, department=department, defaults={"is_active": True})
            programs = {}
            for code, name, degree in (("MS-URO", "MS Urology", "MS"), ("FCPS-URO", "FCPS Urology", "FCPS")):
                from sims.training.models import TrainingProgram
                program, _ = TrainingProgram.objects.get_or_create(code=code, defaults={"name": name, "degree_type": degree, "duration_months": 60, "department": department})
                program.name, program.degree_type, program.department_id, program.active = name, degree, department.id, True
                program.save()
                programs[name] = program
            supervisors = {}
            for canonical in SUPERVISORS.values():
                user = next((u for u in User.objects.filter(role="SUPERVISOR").order_by("id") if person_norm(u.get_full_name()) == person_norm(canonical)), None)
                if not user:
                    first, last = split_name(canonical.replace("Prof. ", "").replace("Dr. ", ""))
                    base = "sup" + re.sub(r"[^a-z]", "", (first + last).lower())[:18]
                    username, suffix = base, 1
                    while User.objects.filter(username=username).exists():
                        suffix += 1; username = f"{base}{suffix}"
                    user = User(username=username, first_name=first, last_name=last, role="SUPERVISOR", is_active=True, must_change_password=True)
                    user.set_password("pgfmu123"); user.save()
                profile, _ = SupervisorProfile.objects.get_or_create(user=user)
                profile.hospital_id, profile.department_ref_id, profile.specialty_ref_id = hospital.id, department.id, "urology"
                profile.save()
                supervisors[person_norm(canonical)] = profile
            workshop_map = {}
            for code, name in WORKSHOPS.values():
                workshop, _ = Workshop.objects.update_or_create(code=code, defaults={"name": name, "is_active": True})
                workshop_map[norm(name)] = workshop
            admin = User.objects.filter(role="ADMIN", is_active=True).order_by("id").first()
            for row in rows:
                name, first, last = clean(row["Resident Master Name"]), *split_name(row["Resident Master Name"])
                email = clean(row.get("Email address(Gmail/other provivder)")) or clean(row.get("Email Address"))
                user = next((u for u in User.objects.filter(role="RESIDENT") if norm(u.get_full_name()) in {norm(name), norm(clean(row.get("Full name (as per official record)")))}), None)
                if not user:
                    base = "pgr" + re.sub(r"[^a-z]", "", (first + last).lower())[:18]
                    username, suffix = base, 1
                    while User.objects.filter(username=username).exists():
                        suffix += 1; username = f"{base}{suffix}"
                    user = User(username=username, first_name=first, last_name=last, role="RESIDENT", email=email, is_active=True, must_change_password=True)
                    user.set_password("pgfmu123"); user.save()
                profile, _ = ResidentProfile.objects.get_or_create(user=user)
                program = programs[clean(row["Program"])]
                profile.hospital_id, profile.department_ref_id, profile.program_ref_id, profile.specialty_ref_id = hospital.id, department.id, program.id, "urology"
                profile.email, profile.phone, profile.cnic, profile.registration_no = email, clean(row.get("WhatsApp number")), clean(row.get("CNIC / National ID number(Without dashes)")), clean(row.get("PMDC number")) or clean(row.get("Registration ID"))
                profile.save()
                start, end, yr = as_date(row.get("Date of induction")), as_date(row.get("Expected completion date")), year_number(row.get("Year of training"))
                record, _ = ResidentTrainingRecord.objects.update_or_create(resident_user=user, program=program, defaults={"start_date": start, "expected_end_date": end, "training_year": yr, "current_level": f"y{yr}", "training_site": hospital, "department": department, "active": True, "status": ResidentTrainingRecord.STATUS_ACTIVE, "created_by": admin})
                supervisor = supervisors.get(person_norm(row.get("Current Supervisor")))
                if not supervisor:
                    raise CommandError(f"Unresolved supervisor for {name}: {row.get('Current Supervisor')}")
                assignment = ResidentSupervisorAssignment.objects.filter(
                    resident=profile, assignment_type="PRIMARY", is_active=True
                ).first()
                if assignment is None:
                    assignment = ResidentSupervisorAssignment(
                        resident=profile, assignment_type="PRIMARY", created_by=admin
                    )
                assignment.supervisor = supervisor
                assignment.start_date = start or date.today()
                assignment.status = "ACTIVE"
                assignment.is_active = True
                assignment.updated_by = admin
                assignment.save()
                for raw in clean(row.get(WORKSHOP_COLUMN)).split(","):
                    key = norm(re.sub(r"^\s*\d+\.\s*", "", raw))
                    if key in WORKSHOPS:
                        workshop = workshop_map[key]
                        ResidentWorkshopCompletion.objects.update_or_create(resident_training_record=record, workshop=workshop, defaults={"completed_at": start or date.today(), "source": "SYSTEM_GENERATED", "notes": "Imported from approved institutional demo workbook."})
                stage = clean(row.get("Synopsis status")).lower()
                if stage not in STAGES:
                    raise CommandError(f"Unsupported research stage for {name}: {stage}")
                extra = record.extra_data or {}; extra["demo_research_stage"] = stage; record.extra_data = extra; record.save(update_fields=["extra_data", "updated_at"])
                title = clean(row.get("Title of synopsis / thesis (if selected)"))
                if title:
                    status = {"topic selected": "DRAFT", "synopsis submitted": "SUBMITTED_TO_SUPERVISOR", "approved": "APPROVED_BY_SUPERVISOR", "completed": "ACCEPTED_UNIVERSITY", "not started": "DRAFT"}[stage]
                    ResidentResearchProject.objects.update_or_create(resident_training_record=record, defaults={"title": title, "supervisor_id": supervisor.user_id, "status": status})
        self.stdout.write(self.style.SUCCESS(f"Imported {len(rows)} approved Urology residents idempotently."))
