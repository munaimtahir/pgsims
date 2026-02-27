"""Analytics data models."""

from __future__ import annotations

import uuid

from django.conf import settings
from django.db import models
from django.db.models import Q


class AnalyticsEvent(models.Model):
    """Immutable analytics event row."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    occurred_at = models.DateTimeField(db_index=True)
    event_type = models.CharField(max_length=120, db_index=True)
    actor_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="analytics_events",
    )
    actor_role = models.CharField(max_length=32, blank=True)
    department = models.ForeignKey(
        "academics.Department",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="analytics_events",
    )
    hospital = models.ForeignKey(
        "rotations.Hospital",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="analytics_events",
    )
    entity_type = models.CharField(max_length=64, null=True, blank=True)
    entity_id = models.CharField(max_length=64, null=True, blank=True)
    status_from = models.CharField(max_length=32, null=True, blank=True)
    status_to = models.CharField(max_length=32, null=True, blank=True)
    request_id = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    event_key = models.CharField(max_length=160, null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-occurred_at"]
        indexes = [
            models.Index(fields=["event_type", "occurred_at"]),
            models.Index(fields=["department", "occurred_at"]),
            models.Index(fields=["hospital", "occurred_at"]),
            models.Index(fields=["request_id", "event_type"]),
            models.Index(fields=["request_id", "event_type", "entity_id"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["request_id", "event_type", "event_key"],
                condition=Q(request_id__isnull=False) & Q(event_key__isnull=False),
                name="uniq_analytics_request_event_key",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.event_type} @ {self.occurred_at.isoformat()}"


class AnalyticsDailyRollup(models.Model):
    """Daily aggregates for fast dashboard reads."""

    day = models.DateField()
    event_type = models.CharField(max_length=120)
    department = models.ForeignKey(
        "academics.Department",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="analytics_daily_rollups",
    )
    hospital = models.ForeignKey(
        "rotations.Hospital",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="analytics_daily_rollups",
    )
    count = models.PositiveIntegerField(default=0)
    extra = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-day"]
        constraints = [
            models.UniqueConstraint(
                fields=["day", "event_type", "department", "hospital"],
                name="uniq_daily_rollup_scope",
            )
        ]
        indexes = [
            models.Index(fields=["day", "event_type"]),
            models.Index(fields=["department", "day"]),
            models.Index(fields=["hospital", "day"]),
        ]

    def __str__(self) -> str:
        return f"{self.day} {self.event_type}: {self.count}"


class AnalyticsValidationRejection(models.Model):
    """Stores analytics validation failures for governance reporting."""

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    source = models.CharField(max_length=32, default="track_event", db_index=True)
    event_type = models.CharField(max_length=120, blank=True)
    reason = models.CharField(max_length=200)
    actor_role = models.CharField(max_length=32, blank=True)
    department_id = models.IntegerField(null=True, blank=True)
    hospital_id = models.IntegerField(null=True, blank=True)
    metadata_keys = models.JSONField(default=list, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["event_type", "created_at"]),
            models.Index(fields=["reason", "created_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.source} {self.event_type or 'unknown'} ({self.reason})"
