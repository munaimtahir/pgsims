from __future__ import annotations

from datetime import date
from typing import Optional

from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_not_future(value: Optional[date], field_name: str) -> None:
    if value and value > timezone.now().date():
        raise ValidationError({field_name: "Date cannot be in the future."})


def validate_chronology(
    start: Optional[date], end: Optional[date], start_field: str, end_field: str
) -> None:
    if start and end and end < start:
        raise ValidationError({end_field: "End date must be on or after the start date."})


def validate_same_supervisor(pg, supervisor) -> None:
    if (
        pg
        and supervisor
        and getattr(pg, "supervisor_id", None)
        and pg.supervisor_id != supervisor.pk
    ):
        raise ValidationError(
            {
                "supervisor": "Assigned supervisor must match the PG's registered supervisor.",
            }
        )


def sanitize_free_text(value: str) -> str:
    if not value:
        return ""
    disallowed = {"<script", "javascript:"}
    lower_value = value.lower()
    if any(token in lower_value for token in disallowed):
        raise ValidationError("Input contains disallowed scripting content.")
    return value.strip()
