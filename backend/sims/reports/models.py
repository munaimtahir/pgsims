"""Models for templated reporting and scheduling."""

from __future__ import annotations

from datetime import timedelta
from typing import Any, Dict

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class ReportTemplate(models.Model):
    """Reusable report templates stored in the database."""

    slug = models.SlugField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    template_name = models.CharField(max_length=255)
    default_params = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:  # pragma: no cover - repr helper
        return self.name


class ScheduledReport(models.Model):
    """Represents a scheduled report to be generated periodically."""

    template = models.ForeignKey(ReportTemplate, on_delete=models.CASCADE, related_name="schedules")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="scheduled_reports")
    email_to = models.CharField(max_length=500, help_text="Comma separated list of recipients")
    params = models.JSONField(default=dict, blank=True)
    cron = models.CharField(max_length=64, help_text="Simplified cron expression like '0 6 * * *'")
    last_run_at = models.DateTimeField(null=True, blank=True)
    next_run_at = models.DateTimeField(null=True, blank=True)
    last_result = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["is_active", "next_run_at"]),
        ]

    def schedule_next_run(self, when: timezone.datetime | None = None) -> None:
        self.next_run_at = when or timezone.now()
        self.save(update_fields=["next_run_at"])

    def record_run(self, success: bool, details: Dict[str, Any]) -> None:
        self.last_run_at = timezone.now()
        self.last_result = {"success": success, **details}
        if success:
            self.next_run_at = timezone.now() + timedelta(days=1)
        self.save(update_fields=["last_run_at", "last_result", "next_run_at"])


__all__ = ["ReportTemplate", "ScheduledReport"]
