from __future__ import annotations

import csv
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from pathlib import Path
from typing import Iterable

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from django.utils.dateparse import parse_date, parse_datetime

from sims.academics.models import Department
from sims.logbook.models import LogbookEntry, Procedure
from sims.rotations.models import Hospital, HospitalDepartment, Rotation

User = get_user_model()

DEMO_EMAIL_DOMAIN = "@demo.local"
DEMO_DEPARTMENT_NAME = "Department of Urology & Renal Transplantation (DEMO)"
DEMO_CASE_PREFIX = "DEMO-URO-"
ROTATION_DEMO_SUFFIX = " (DEMO)"
DEMO_DEPT_CODE_BASE = "DEMO-URO-RT"

CSV_STATUS_MAP = {
    "submitted": "pending",
    "sent back": "returned",
    "verified": "approved",
}


@dataclass
class RowData:
    case_id: str
    trainee_name: str
    trainee_email: str
    supervisor_name: str
    supervisor_email: str
    rotation_name: str
    procedure_name: str
    patient_age: int | None
    patient_gender: str | None
    procedure_date: date
    source_status: str
    target_status: str
    sent_back_comment: str
    verified_at: datetime | None
    clinical_notes: str


class Command(BaseCommand):
    help = "Import demo logbook cases from CSV for screenshot-ready analytics."

    def add_arguments(self, parser):
        parser.add_argument("--file", required=True, help="Path to CSV file")
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete only demo entities created by this command before import.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        file_path = Path(options["file"]).expanduser().resolve()
        if not file_path.exists():
            raise CommandError(f"CSV file not found: {file_path}")

        self._print_phase_a_diagnostics()

        rows = self._load_rows(file_path)
        if not rows:
            self.stdout.write(self.style.WARNING("No rows found in CSV; nothing to import."))
            return

        before_non_demo = self._non_demo_snapshot()

        if options["reset"]:
            self._reset_demo_entities()

        department = self._ensure_demo_department()
        hospital = self._get_or_create_target_hospital()
        HospitalDepartment.objects.update_or_create(
            hospital=hospital,
            department=department,
            defaults={"is_active": True},
        )

        procedures = self._ensure_procedures(rows)
        users_by_email = self._ensure_users(rows, hospital, department)
        rotations = self._ensure_rotations(rows, users_by_email, hospital, department)

        imported, updated, status_counter = self._import_logbook_entries(
            rows=rows,
            users_by_email=users_by_email,
            rotations=rotations,
            procedures=procedures,
        )

        after_non_demo = self._non_demo_snapshot()

        self._print_phase_c_validation(
            imported=imported,
            updated=updated,
            status_counter=status_counter,
            before_non_demo=before_non_demo,
            after_non_demo=after_non_demo,
        )

    def _print_phase_a_diagnostics(self):
        models = [
            ("users.User", User),
            ("academics.Department", Department),
            ("rotations.Rotation", Rotation),
            ("logbook.LogbookEntry", LogbookEntry),
        ]

        self.stdout.write(self.style.MIGRATE_HEADING("PHASE A - SCHEMA DISCOVERY"))
        self.stdout.write(
            "Model | Required fields | Status enum values | Notes"
        )
        self.stdout.write("-" * 140)

        for label, model in models:
            required = self._required_fields(model)
            status_values = self._status_values(model)
            notes = self._model_notes(label)
            self.stdout.write(
                f"{label} | {', '.join(required) if required else '-'} | "
                f"{', '.join(status_values) if status_values else '-'} | {notes}"
            )

    def _required_fields(self, model) -> list[str]:
        fields: list[str] = []
        for field in model._meta.get_fields():
            if not getattr(field, "concrete", False):
                continue
            if getattr(field, "auto_created", False):
                continue
            if getattr(field, "many_to_many", False):
                continue
            if getattr(field, "primary_key", False):
                continue
            if getattr(field, "null", False):
                continue
            if getattr(field, "blank", False):
                continue
            if getattr(field, "has_default", lambda: False)():
                continue
            if getattr(field, "auto_now", False) or getattr(field, "auto_now_add", False):
                continue
            fields.append(field.name)
        return fields

    def _status_values(self, model) -> list[str]:
        status_choices = getattr(model, "STATUS_CHOICES", None)
        if status_choices:
            return [choice[0] for choice in status_choices]

        try:
            status_field = model._meta.get_field("status")
        except Exception:
            return []

        return [choice[0] for choice in (status_field.choices or [])]

    def _model_notes(self, label: str) -> str:
        notes_map = {
            "users.User": "Use get_user_model(); PG requires specialty+year+supervisor.",
            "academics.Department": "Canonical department model in academics app.",
            "rotations.Rotation": "Requires pg+department+hospital+start_date+end_date; dept must be in HospitalDepartment.",
            "logbook.LogbookEntry": "Verification fields: verified_by, verified_at; sent-back comment field: supervisor_feedback; no lock flag field present.",
        }
        return notes_map.get(label, "")

    def _load_rows(self, file_path: Path) -> list[RowData]:
        rows: list[RowData] = []
        with file_path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            required_columns = {
                "Case ID",
                "Trainee Name",
                "Trainee Email",
                "Supervisor Name",
                "Supervisor Email",
                "Rotation",
                "Procedure",
                "Patient Age",
                "Patient Gender",
                "Procedure Date",
                "Status",
            }
            missing = sorted(required_columns - set(reader.fieldnames or []))
            if missing:
                raise CommandError(f"CSV missing required columns: {', '.join(missing)}")

            for idx, raw in enumerate(reader, start=2):
                case_id = (raw.get("Case ID") or "").strip()
                if not case_id.startswith(DEMO_CASE_PREFIX):
                    continue

                status_src = (raw.get("Status") or "").strip()
                status_key = status_src.lower()
                if status_key not in CSV_STATUS_MAP:
                    raise CommandError(
                        f"Unsupported Status '{status_src}' at CSV line {idx}. "
                        f"Expected one of: Submitted, Sent Back, Verified"
                    )

                procedure_date = self._parse_date(raw.get("Procedure Date"), idx, "Procedure Date")

                patient_age = None
                age_raw = (raw.get("Patient Age") or "").strip()
                if age_raw:
                    try:
                        patient_age = int(age_raw)
                    except ValueError as exc:
                        raise CommandError(f"Invalid Patient Age '{age_raw}' at line {idx}") from exc

                rows.append(
                    RowData(
                        case_id=case_id,
                        trainee_name=(raw.get("Trainee Name") or "").strip(),
                        trainee_email=(raw.get("Trainee Email") or "").strip().lower(),
                        supervisor_name=(raw.get("Supervisor Name") or "").strip(),
                        supervisor_email=(raw.get("Supervisor Email") or "").strip().lower(),
                        rotation_name=(raw.get("Rotation") or "").strip(),
                        procedure_name=(raw.get("Procedure") or raw.get("Procedure Code") or "Procedure").strip(),
                        patient_age=patient_age,
                        patient_gender=self._map_gender(raw.get("Patient Gender")),
                        procedure_date=procedure_date,
                        source_status=status_src,
                        target_status=CSV_STATUS_MAP[status_key],
                        sent_back_comment=(raw.get("Sent Back Comment") or "").strip(),
                        verified_at=self._parse_datetime(raw.get("Verified At")),
                        clinical_notes=(raw.get("Clinical Notes") or "").strip(),
                    )
                )

        return rows

    def _parse_date(self, raw: str | None, line_no: int, label: str) -> date:
        value = (raw or "").strip()
        parsed = parse_date(value)
        if parsed is None:
            raise CommandError(f"Invalid {label} '{value}' at line {line_no}")
        return parsed

    def _parse_datetime(self, raw: str | None) -> datetime | None:
        value = (raw or "").strip()
        if not value:
            return None
        dt = parse_datetime(value)
        if dt is not None:
            if timezone.is_naive(dt):
                return timezone.make_aware(dt, timezone.get_current_timezone())
            return dt

        parsed_date = parse_date(value)
        if parsed_date is None:
            return None
        naive = datetime.combine(parsed_date, time(hour=12, minute=0, second=0))
        return timezone.make_aware(naive, timezone.get_current_timezone())

    def _map_gender(self, raw: str | None) -> str | None:
        value = (raw or "").strip().lower()
        mapping = {
            "male": "M",
            "m": "M",
            "female": "F",
            "f": "F",
            "other": "O",
            "o": "O",
            "unknown": "U",
            "u": "U",
            "": None,
        }
        return mapping.get(value, "U")

    def _non_demo_snapshot(self) -> dict[str, int]:
        return {
            "users": User.objects.exclude(email__iendswith=DEMO_EMAIL_DOMAIN).count(),
            "departments": Department.objects.exclude(name__icontains="(DEMO)").count(),
            "rotations": Rotation.objects.exclude(
                Q(pg__email__iendswith=DEMO_EMAIL_DOMAIN) | Q(notes__icontains="(DEMO)")
            ).count(),
            "logbook_entries": LogbookEntry.objects.exclude(
                Q(pg__email__iendswith=DEMO_EMAIL_DOMAIN) | Q(case_title__startswith=DEMO_CASE_PREFIX)
            ).count(),
        }

    def _reset_demo_entities(self):
        self.stdout.write(self.style.WARNING("Resetting demo entities only..."))

        demo_entries_deleted, _ = LogbookEntry.objects.filter(
            Q(pg__email__iendswith=DEMO_EMAIL_DOMAIN) | Q(case_title__startswith=DEMO_CASE_PREFIX)
        ).delete()

        demo_rotations_deleted, _ = Rotation.objects.filter(
            Q(pg__email__iendswith=DEMO_EMAIL_DOMAIN)
            | Q(notes__icontains="(DEMO)")
            | Q(department__name__icontains="(DEMO)")
        ).delete()

        demo_users_deleted, _ = User.objects.filter(email__iendswith=DEMO_EMAIL_DOMAIN).delete()

        demo_departments_deleted, _ = Department.objects.filter(name__icontains="(DEMO)").delete()

        self.stdout.write(
            f"Reset deleted: entries={demo_entries_deleted}, rotations={demo_rotations_deleted}, "
            f"users={demo_users_deleted}, departments={demo_departments_deleted}"
        )

    def _ensure_demo_department(self) -> Department:
        dept = Department.objects.filter(name=DEMO_DEPARTMENT_NAME).first()
        if dept:
            return dept

        code = DEMO_DEPT_CODE_BASE
        suffix = 1
        while Department.objects.filter(code=code).exists():
            suffix += 1
            code = f"{DEMO_DEPT_CODE_BASE[:16]}{suffix:02d}"

        dept = Department.objects.create(
            name=DEMO_DEPARTMENT_NAME,
            code=code,
            description="Demo department seeded by import_demo_cases command.",
            active=True,
        )
        return dept

    def _get_or_create_target_hospital(self) -> Hospital:
        hospital = Hospital.objects.filter(is_active=True).order_by("id").first()
        if hospital:
            return hospital

        hospital, _ = Hospital.objects.get_or_create(
            code="DEMO-UTRMC",
            defaults={
                "name": "UTRMC Teaching Hospital (DEMO)",
                "description": "Demo hospital for seeded screenshots.",
                "is_active": True,
            },
        )
        return hospital

    def _ensure_procedures(self, rows: Iterable[RowData]) -> dict[str, Procedure]:
        names = sorted({row.procedure_name for row in rows if row.procedure_name})
        existing = {p.name: p for p in Procedure.objects.filter(name__in=names)}

        for name in names:
            if name in existing:
                continue
            existing[name] = Procedure.objects.create(
                name=name,
                category="surgical",
                description="Demo procedure for imported screenshot dataset.",
                difficulty_level=2,
                cme_points=1,
                is_active=True,
            )

        return existing

    def _split_name(self, full_name: str) -> tuple[str, str]:
        cleaned = " ".join((full_name or "").strip().split())
        if not cleaned:
            return "Demo", "User"
        parts = cleaned.split(" ")
        if len(parts) == 1:
            return parts[0], "Demo"
        return " ".join(parts[:-1]), parts[-1]

    def _username_from_email(self, email: str, fallback_seed: str) -> str:
        local = (email.split("@", 1)[0] if "@" in email else fallback_seed).strip().lower()
        safe = "".join(ch if ch.isalnum() else "_" for ch in local) or "demo_user"
        username = safe[:150]
        candidate = username
        index = 1
        while User.objects.filter(username=candidate).exclude(email=email).exists():
            index += 1
            suffix = f"_{index}"
            candidate = f"{username[:150-len(suffix)]}{suffix}"
        return candidate

    def _ensure_user(
        self,
        *,
        email: str,
        full_name: str,
        role: str,
        specialty: str,
        year: str | None,
        supervisor: User | None,
        home_hospital: Hospital,
        home_department: Department,
    ) -> User:
        user = User.objects.filter(email__iexact=email).first()
        first_name, last_name = self._split_name(full_name)
        username = self._username_from_email(email=email, fallback_seed=full_name or role)

        if user is None:
            user = User(
                email=email,
                username=username,
                role=role,
            )

        user.first_name = first_name
        user.last_name = last_name
        user.role = role
        user.specialty = specialty
        user.home_hospital = home_hospital
        user.home_department = home_department
        user.supervisor = supervisor if role == "pg" else None
        user.year = year if role == "pg" else None
        user.is_active = True

        if not user.password or not user.has_usable_password():
            user.set_unusable_password()

        user.save()
        return user

    def _ensure_users(
        self,
        rows: Iterable[RowData],
        hospital: Hospital,
        department: Department,
    ) -> dict[str, User]:
        by_email: dict[str, User] = {}

        supervisors = {}
        for row in rows:
            if row.supervisor_email in supervisors:
                continue
            supervisors[row.supervisor_email] = self._ensure_user(
                email=row.supervisor_email,
                full_name=row.supervisor_name,
                role="supervisor",
                specialty="urology",
                year=None,
                supervisor=None,
                home_hospital=hospital,
                home_department=department,
            )

        by_email.update(supervisors)

        for row in rows:
            if row.trainee_email in by_email:
                continue
            supervisor = supervisors[row.supervisor_email]
            by_email[row.trainee_email] = self._ensure_user(
                email=row.trainee_email,
                full_name=row.trainee_name,
                role="pg",
                specialty="urology",
                year="2",
                supervisor=supervisor,
                home_hospital=hospital,
                home_department=department,
            )

        return by_email

    def _ensure_rotations(
        self,
        rows: Iterable[RowData],
        users_by_email: dict[str, User],
        hospital: Hospital,
        department: Department,
    ) -> dict[tuple[int, str], Rotation]:
        rows_by_rotation: dict[tuple[str, str], list[RowData]] = defaultdict(list)
        for row in rows:
            rows_by_rotation[(row.trainee_email, row.rotation_name)].append(row)

        result: dict[tuple[int, str], Rotation] = {}
        for (trainee_email, rotation_name), subset in rows_by_rotation.items():
            trainee = users_by_email[trainee_email]
            supervisor = users_by_email[subset[0].supervisor_email]
            start_date = min(item.procedure_date for item in subset)
            end_date = max(item.procedure_date for item in subset)
            if end_date <= start_date:
                end_date = start_date + timedelta(days=1)

            marked_name = rotation_name
            if ROTATION_DEMO_SUFFIX.strip() not in rotation_name:
                marked_name = f"{rotation_name}{ROTATION_DEMO_SUFFIX}"

            rotation, _ = Rotation.objects.update_or_create(
                pg=trainee,
                department=department,
                hospital=hospital,
                start_date=start_date,
                end_date=end_date,
                defaults={
                    "supervisor": supervisor,
                    "status": "completed",
                    "objectives": f"Demo rotation: {marked_name}",
                    "notes": f"Imported via import_demo_cases {ROTATION_DEMO_SUFFIX.strip()}",
                    "created_by": supervisor,
                    "source_hospital": hospital,
                    "source_department": department,
                },
            )
            result[(trainee.id, rotation_name)] = rotation

        return result

    def _build_case_title(self, row: RowData) -> str:
        return f"{row.case_id} | {row.procedure_name}"

    def _import_logbook_entries(
        self,
        *,
        rows: Iterable[RowData],
        users_by_email: dict[str, User],
        rotations: dict[tuple[int, str], Rotation],
        procedures: dict[str, Procedure],
    ) -> tuple[int, int, Counter]:
        imported = 0
        updated = 0
        status_counter: Counter = Counter()

        for row in rows:
            trainee = users_by_email[row.trainee_email]
            supervisor = users_by_email[row.supervisor_email]
            rotation = rotations[(trainee.id, row.rotation_name)]
            case_title = self._build_case_title(row)

            entry = LogbookEntry.objects.filter(case_title=case_title, pg=trainee).first()
            created = False
            if entry is None:
                entry = LogbookEntry(
                    pg=trainee,
                    supervisor=supervisor,
                    rotation=rotation,
                    case_title=case_title,
                    date=row.procedure_date,
                    location_of_activity=rotation.hospital.name,
                    patient_history_summary=row.clinical_notes or f"Demo case for {row.procedure_name}.",
                    management_action=(
                        f"{row.procedure_name} performed; imported from demo CSV {row.case_id}."
                    ),
                    topic_subtopic=f"Urology / {row.procedure_name}",
                    patient_age=row.patient_age,
                    patient_gender=row.patient_gender,
                    patient_chief_complaint=row.clinical_notes[:1000] if row.clinical_notes else "",
                    clinical_reasoning=row.clinical_notes[:2000] if row.clinical_notes else "",
                    learning_points="Imported demo learning point for screenshot dataset.",
                    status="draft",
                    created_by=trainee,
                )
                entry.save()
                created = True

            entry.supervisor = supervisor
            entry.rotation = rotation
            entry.date = row.procedure_date
            entry.location_of_activity = rotation.hospital.name
            entry.patient_age = row.patient_age
            entry.patient_gender = row.patient_gender
            entry.patient_history_summary = (
                row.clinical_notes or f"Demo case narrative for {row.procedure_name}."
            )
            entry.management_action = (
                f"{row.procedure_name} performed by trainee under supervision."
            )
            entry.topic_subtopic = f"Urology / {row.procedure_name}"
            entry.patient_chief_complaint = row.clinical_notes[:1000] if row.clinical_notes else ""
            entry.clinical_reasoning = row.clinical_notes[:2000] if row.clinical_notes else ""

            # Apply state transitions through model save hooks.
            if entry.status != "pending":
                entry.status = "pending"
                entry.save()

            if row.target_status == "returned":
                entry.supervisor_feedback = (
                    row.sent_back_comment or "Returned for refinement during demo workflow."
                )
                entry.status = "returned"
                entry.save()
            elif row.target_status == "approved":
                entry.supervisor_feedback = "Verified for demo presentation dataset."
                entry.status = "approved"
                entry.save()
                if row.verified_at is not None:
                    entry.verified_at = row.verified_at
                    entry.verified_by = supervisor
                    entry.save(update_fields=["verified_at", "verified_by", "updated_at"])
            else:
                entry.supervisor_feedback = ""
                entry.save(update_fields=["supervisor_feedback", "updated_at"])

            procedure = procedures.get(row.procedure_name)
            if procedure is not None:
                entry.procedures.set([procedure])

            status_counter[entry.status] += 1
            if created:
                imported += 1
            else:
                updated += 1

        return imported, updated, status_counter

    def _print_phase_c_validation(
        self,
        *,
        imported: int,
        updated: int,
        status_counter: Counter,
        before_non_demo: dict[str, int],
        after_non_demo: dict[str, int],
    ):
        demo_cases_qs = LogbookEntry.objects.filter(case_title__startswith=DEMO_CASE_PREFIX).select_related(
            "pg", "verified_by"
        )
        total_demo_cases = demo_cases_qs.count()

        lock_field_exists = any(f.name in {"is_locked", "locked"} for f in LogbookEntry._meta.get_fields())
        if lock_field_exists:
            locked_count = demo_cases_qs.filter(Q(is_locked=True) | Q(locked=True)).count()
        else:
            locked_count = demo_cases_qs.filter(status="approved", verified_by__isnull=False).count()

        self.stdout.write(self.style.MIGRATE_HEADING("PHASE C - VALIDATION"))
        self.stdout.write(f"Total cases imported (created): {imported}")
        self.stdout.write(f"Total cases updated (idempotent rerun): {updated}")
        self.stdout.write(f"Total demo cases present: {total_demo_cases}")
        self.stdout.write("Count by status:")
        for status_value in ["pending", "returned", "approved", "draft", "rejected", "archived"]:
            self.stdout.write(f"  {status_value}: {status_counter.get(status_value, 0)}")

        if lock_field_exists:
            self.stdout.write(f"Verified locked count: {locked_count}")
        else:
            self.stdout.write(
                "Verified locked count: lock field not present; using approved+verified_by proxy "
                f"count={locked_count}"
            )

        self.stdout.write("Sample 5 cases (id, resident, status, verified_by):")
        sample = demo_cases_qs.order_by("id")[:5]
        for entry in sample:
            resident = entry.pg.get_full_name() or entry.pg.username
            verifier = (
                (entry.verified_by.get_full_name() or entry.verified_by.username)
                if entry.verified_by
                else "-"
            )
            self.stdout.write(
                f"  id={entry.id}, resident={resident}, status={entry.status}, verified_by={verifier}"
            )

        untouched = before_non_demo == after_non_demo
        self.stdout.write(
            "Non-demo data integrity check: "
            + (self.style.SUCCESS("UNCHANGED") if untouched else self.style.ERROR("CHANGED"))
        )
        self.stdout.write(f"  before: {before_non_demo}")
        self.stdout.write(f"  after : {after_non_demo}")
