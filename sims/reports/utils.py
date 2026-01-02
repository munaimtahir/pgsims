"""Utility helpers for reports."""

from __future__ import annotations

from django.db import OperationalError, ProgrammingError

from sims.reports.models import ReportTemplate


def ensure_default_templates() -> None:
    try:
        ReportTemplate.objects.get_or_create(
            slug="logbook-summary",
            defaults={
                "name": "Logbook Summary",
                "template_name": "reports/logbook_summary.html",
                "description": "Summary of logbook entries with filters.",
                "default_params": {"format": "pdf"},
            },
        )
    except (
        OperationalError,
        ProgrammingError,
    ):  # pragma: no cover - database not ready
        return


__all__ = ["ensure_default_templates"]
