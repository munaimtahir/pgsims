from __future__ import annotations

from datetime import datetime
from typing import Optional

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords


class ActivityLog(models.Model):
    ACTION_CHOICES = (
        ("view", "View"),
        ("create", "Create"),
        ("update", "Update"),
        ("delete", "Delete"),
        ("export", "Export"),
        ("login", "Login"),
        ("logout", "Logout"),
    )

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="activity_logs",
    )
    action = models.CharField(max_length=32, choices=ACTION_CHOICES)
    verb = models.CharField(max_length=64)
    target_content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True)
    target_object_id = models.CharField(max_length=64, blank=True)
    target = GenericForeignKey("target_content_type", "target_object_id")
    target_repr = models.CharField(max_length=255, blank=True)
    metadata = models.JSONField(blank=True, default=dict)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    is_sensitive = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["action"]),
            models.Index(fields=["is_sensitive"]),
            models.Index(fields=["actor", "created_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.created_at:%Y-%m-%d %H:%M} {self.actor_id}:{self.action}:{self.verb}"

    @classmethod
    def log(
        cls,
        *,
        actor: Optional[models.Model],
        action: str,
        verb: str,
        target: Optional[models.Model] = None,
        metadata: Optional[dict] = None,
        ip_address: Optional[str] = None,
        is_sensitive: bool = False,
    ) -> "ActivityLog":
        metadata = metadata or {}
        target_ct = None
        target_pk: Optional[str] = None
        target_repr = ""
        if target is not None:
            target_ct = ContentType.objects.get_for_model(target, for_concrete_model=False)
            target_pk = str(target.pk)
            target_repr = str(target)
        return cls.objects.create(
            actor=actor,
            action=action,
            verb=verb,
            target_content_type=target_ct,
            target_object_id=target_pk or "",
            target_repr=target_repr,
            metadata=metadata,
            ip_address=ip_address,
            is_sensitive=is_sensitive,
        )


class AuditReport(models.Model):
    """Cached snapshot summarising activity logs for a timeframe."""

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_reports",
    )
    start = models.DateTimeField()
    end = models.DateTimeField()
    generated_at = models.DateTimeField(auto_now_add=True)
    payload = models.JSONField(default=dict)
    history = HistoricalRecords()

    class Meta:
        ordering = ["-generated_at"]
        unique_together = ("start", "end", "created_by")

    def __str__(self) -> str:
        return f"Audit report {self.start:%Y-%m-%d} - {self.end:%Y-%m-%d}"

    @classmethod
    def generate(
        cls,
        *,
        start: datetime,
        end: datetime,
        created_by: Optional[models.Model] = None,
        include_sensitive: bool = False,
    ) -> "AuditReport":
        queryset = ActivityLog.objects.filter(created_at__range=(start, end))
        if not include_sensitive:
            queryset = queryset.filter(is_sensitive=False)

        summary = {
            "total": queryset.count(),
            "by_action": {
                row["action"]: row["count"]
                for row in queryset.values("action")
                .order_by("action")
                .annotate(count=models.Count("id"))
            },
            "top_users": list(
                queryset.values("actor_id")
                .exclude(actor_id=None)
                .annotate(count=models.Count("id"))
                .order_by("-count")[:10]
            ),
        }
        report, created = cls.objects.get_or_create(
            start=start,
            end=end,
            created_by=created_by,
        )
        if created or report.payload != summary:
            report.payload = summary
            report.save()
        return report


def prune_activity_logs(older_than: datetime) -> int:
    """Delete activity logs older than provided cutoff."""

    qs = ActivityLog.objects.filter(created_at__lt=older_than)
    count = qs.count()
    qs.delete()
    return count
