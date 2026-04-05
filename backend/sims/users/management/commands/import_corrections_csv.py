from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from sims.training.models import ResidentTrainingRecord
from sims.users.data_quality import log_data_correction, recompute_flags_for_user
from sims.users.models import ResidentProfile

User = get_user_model()

ALLOWED_FIELDS = {"email", "year", "training_start", "training_end", "training_level"}
ALLOWED_YEARS = {"1", "2", "3", "4", "5"}


def _parse_iso_date(value: str):
    value = (value or "").strip()
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise CommandError(f"Invalid ISO date: {value}") from exc


class Command(BaseCommand):
    help = "Import resident data corrections from CSV. Supports dry-run and apply with audit logging."

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="CSV path with columns: resident_email,field_name,new_value")
        parser.add_argument("--apply", action="store_true", help="Apply corrections. Default is dry-run.")
        parser.add_argument(
            "--confirm",
            action="store_true",
            help="Required together with --apply to prevent accidental overwrite.",
        )
        parser.add_argument("--actor-username", type=str, default="admin", help="Actor for audit logs.")

    def handle(self, *args, **options):
        csv_path = Path(options["csv_file"]).expanduser().resolve()
        if not csv_path.exists():
            raise CommandError(f"CSV file not found: {csv_path}")

        apply_mode = bool(options["apply"])
        if apply_mode and not options["confirm"]:
            raise CommandError("Apply mode requires --confirm.")

        actor = User.objects.filter(username=options["actor_username"]).first()
        if apply_mode and not actor:
            raise CommandError(f"Actor user not found: {options['actor_username']}")

        rows = []
        with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            expected = {"resident_email", "field_name", "new_value"}
            if set(reader.fieldnames or []) != expected:
                raise CommandError("CSV headers must be exactly: resident_email,field_name,new_value")
            for i, row in enumerate(reader, start=2):
                rows.append((i, (row.get("resident_email") or "").strip().lower(), (row.get("field_name") or "").strip(), (row.get("new_value") or "").strip()))

        updated = 0
        skipped = 0
        errors = 0
        email_to_user_id: dict[str, int] = {}

        for row_num, email, field_name, new_value in rows:
            if not email or not field_name:
                self.stdout.write(self.style.ERROR(f"row {row_num}: missing resident_email/field_name"))
                errors += 1
                continue
            if field_name not in ALLOWED_FIELDS:
                self.stdout.write(self.style.ERROR(f"row {row_num}: unsupported field '{field_name}'"))
                errors += 1
                continue

            user = None
            known_user_id = email_to_user_id.get(email)
            if known_user_id:
                user = User.objects.filter(id=known_user_id, role__in=["resident", "pg"]).first()
            if not user:
                user = User.objects.filter(email__iexact=email, role__in=["resident", "pg"]).first()
            if not user:
                self.stdout.write(self.style.ERROR(f"row {row_num}: resident '{email}' not found"))
                errors += 1
                continue
            email_to_user_id[email] = user.id

            try:
                if field_name == "email":
                    old_value = user.email
                    if new_value == old_value:
                        skipped += 1
                        continue
                    try:
                        validate_email(new_value)
                    except Exception as exc:
                        raise CommandError("email must be valid format") from exc
                    if not apply_mode:
                        self.stdout.write(f"row {row_num}: user.email {old_value} -> {new_value}")
                    else:
                        user.email = new_value
                        user.save(update_fields=["email"])
                        log_data_correction(
                            actor=actor,
                            entity_type="user",
                            entity_id=user.id,
                            field_name="email",
                            old_value=old_value,
                            new_value=new_value,
                            metadata={"source": "import_corrections_csv", "row": row_num},
                        )
                        recompute_flags_for_user(user)
                    email_to_user_id[new_value.strip().lower()] = user.id
                    updated += 1
                elif field_name == "year":
                    if new_value not in ALLOWED_YEARS:
                        raise CommandError(f"year must be one of {sorted(ALLOWED_YEARS)}")
                    old_value = user.year or ""
                    if new_value == old_value:
                        skipped += 1
                        continue
                    if not apply_mode:
                        self.stdout.write(f"row {row_num}: user.year {old_value} -> {new_value}")
                    else:
                        user.year = new_value
                        user.save(update_fields=["year"])
                        log_data_correction(
                            actor=actor,
                            entity_type="user",
                            entity_id=user.id,
                            field_name="year",
                            old_value=old_value,
                            new_value=new_value,
                            metadata={"source": "import_corrections_csv", "row": row_num},
                        )
                        recompute_flags_for_user(user)
                    updated += 1
                else:
                    profile = ResidentProfile.objects.filter(user=user).first()
                    if not profile:
                        self.stdout.write(self.style.ERROR(f"row {row_num}: resident profile missing for '{email}'"))
                        errors += 1
                        continue
                    old_value = getattr(profile, field_name, None)
                    if field_name in {"training_start", "training_end"}:
                        parsed = _parse_iso_date(new_value)
                        if field_name == "training_start" and not parsed:
                            raise CommandError("training_start cannot be empty")
                        new_cast = parsed
                    else:
                        new_cast = new_value
                    if str(old_value) == str(new_cast):
                        skipped += 1
                        continue
                    if not apply_mode:
                        self.stdout.write(f"row {row_num}: resident_profile.{field_name} {old_value} -> {new_cast}")
                    else:
                        with transaction.atomic():
                            setattr(profile, field_name, new_cast)
                            profile.save()
                            log_data_correction(
                                actor=actor,
                                entity_type="resident_profile",
                                entity_id=profile.id,
                                field_name=field_name,
                                old_value=old_value,
                                new_value=new_cast,
                                metadata={"source": "import_corrections_csv", "row": row_num},
                            )
                            for record in ResidentTrainingRecord.objects.filter(resident_user=user):
                                if field_name == "training_start":
                                    record.start_date = new_cast
                                    record.save(update_fields=["start_date"])
                            recompute_flags_for_user(user)
                    updated += 1
            except CommandError as exc:
                self.stdout.write(self.style.ERROR(f"row {row_num}: {exc}"))
                errors += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Mode={'APPLY' if apply_mode else 'DRY-RUN'} updated={updated} skipped={skipped} errors={errors}"
            )
        )
