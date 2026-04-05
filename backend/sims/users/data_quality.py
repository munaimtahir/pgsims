from __future__ import annotations

from typing import Any

from django.contrib.auth import get_user_model
from django.db import transaction

from sims.training.models import ResidentTrainingRecord
from sims.users.models import DataCorrectionAudit, ResidentProfile, SupervisorResidentLink

User = get_user_model()

DEFAULT_DATE_STRINGS = {"2026-01-01"}


def _is_placeholder_email(email: str | None) -> bool:
    value = (email or "").strip().lower()
    return "placeholder" in value or value.endswith("@pilot-placeholder.local")


def scan_user_profile(user: User) -> list[str]:
    issues: list[str] = []
    email = (user.email or "").strip()
    if not email:
        issues.append("missing_email")
    elif _is_placeholder_email(email):
        issues.append("placeholder_email")

    if user.role in {"pg", "resident"}:
        if not (user.year or "").strip():
            issues.append("missing_year")
        profile = ResidentProfile.objects.filter(user=user).first()
        if not profile:
            issues.append("missing_resident_profile")
        else:
            if not profile.training_start:
                issues.append("missing_training_start")
            elif profile.training_start.isoformat() in DEFAULT_DATE_STRINGS:
                issues.append("default_training_start")
            if profile.training_end and profile.training_start and profile.training_end < profile.training_start:
                issues.append("invalid_training_end")
    return sorted(set(issues))


def scan_training_record(record: ResidentTrainingRecord) -> list[str]:
    issues: list[str] = []
    if not record.start_date:
        issues.append("missing_start_date")
    elif record.start_date.isoformat() in DEFAULT_DATE_STRINGS:
        issues.append("default_start_date")
    if record.expected_end_date and record.expected_end_date <= record.start_date:
        issues.append("invalid_expected_end_date")
    if not (record.current_level or "").strip():
        issues.append("missing_current_level")
    return sorted(set(issues))


@transaction.atomic
def recompute_flags_for_user(user: User) -> dict[str, Any]:
    user_issues = scan_user_profile(user)
    training_records = list(ResidentTrainingRecord.objects.filter(resident_user=user))
    training_issues = {record.id: scan_training_record(record) for record in training_records}
    has_training_issue = any(training_issues.values())

    for record in training_records:
        issues = training_issues.get(record.id, [])
        has_default_dates = any(code in {"default_start_date", "missing_start_date"} for code in issues)
        if record.has_default_dates != has_default_dates:
            record.has_default_dates = has_default_dates
            record.save(update_fields=["has_default_dates"])

    links = SupervisorResidentLink.objects.filter(resident_user=user)
    has_default_link_dates = False
    for link in links:
        has_default = (
            not bool(link.start_date) or (link.start_date and link.start_date.isoformat() in DEFAULT_DATE_STRINGS)
        )
        if has_default:
            has_default_link_dates = True
        if link.has_default_dates != has_default:
            link.has_default_dates = has_default
            link.save(update_fields=["has_default_dates"])

    if any(code in {"default_start_date", "missing_start_date"} for issues in training_issues.values() for code in issues):
        user_issues = sorted(set([*user_issues, "missing_training_dates"]))
    if has_default_link_dates:
        user_issues = sorted(set([*user_issues, "missing_supervision_dates"]))

    user.has_placeholder_email = "placeholder_email" in user_issues
    user.data_issues = user_issues
    user.is_complete_profile = not user_issues and not has_training_issue and not has_default_link_dates
    user.save(update_fields=["has_placeholder_email", "data_issues", "is_complete_profile"])

    return {
        "user_id": user.id,
        "issues": user_issues,
        "is_complete_profile": user.is_complete_profile,
        "training_record_count": len(training_records),
    }


def recompute_all() -> dict[str, int]:
    total = 0
    incomplete = 0
    placeholders = 0
    users_with_missing_dates = 0
    default_records = 0
    for user in User.objects.filter(role__in=["resident", "pg"]).iterator():
        total += 1
        result = recompute_flags_for_user(user)
        if not user.is_complete_profile:
            incomplete += 1
        if user.has_placeholder_email:
            placeholders += 1
        has_missing_dates = (
            "missing_training_dates" in (result.get("issues") or [])
            or "missing_supervision_dates" in (result.get("issues") or [])
        )
        if has_missing_dates:
            users_with_missing_dates += 1
        default_records += user.training_records.filter(has_default_dates=True).count()
    return {
        "total_users": total,
        "incomplete_profiles": incomplete,
        "users_with_placeholder_email": placeholders,
        "users_with_missing_dates": users_with_missing_dates,
        "records_with_default_dates": default_records,
        "complete_profiles": max(total - incomplete, 0),
    }


def log_data_correction(
    *,
    actor: User | None,
    entity_type: str,
    entity_id: str | int,
    field_name: str,
    old_value: Any,
    new_value: Any,
    metadata: dict[str, Any] | None = None,
) -> DataCorrectionAudit:
    return DataCorrectionAudit.objects.create(
        actor=actor,
        entity_type=entity_type,
        entity_id=str(entity_id),
        field_name=field_name,
        old_value="" if old_value is None else str(old_value),
        new_value="" if new_value is None else str(new_value),
        metadata=metadata or {},
    )
