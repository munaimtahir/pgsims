"""Models for tracking bulk operations."""

from __future__ import annotations

from typing import Any, Dict

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class BulkOperation(models.Model):
    """Audit trail for a bulk action executed by a user."""

    OP_REVIEW = "review"
    OP_ASSIGNMENT = "assignment"
    OP_IMPORT = "import"
    OPERATION_CHOICES = (
        (OP_REVIEW, "Bulk Review"),
        (OP_ASSIGNMENT, "Bulk Assignment"),
        (OP_IMPORT, "Bulk Import"),
    )

    STATUS_PENDING = "pending"
    STATUS_COMPLETED = "completed"
    STATUS_FAILED = "failed"
    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_FAILED, "Failed"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bulk_operations")
    operation = models.CharField(max_length=32, choices=OPERATION_CHOICES)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=STATUS_PENDING)
    total_items = models.PositiveIntegerField(default=0)
    success_count = models.PositiveIntegerField(default=0)
    failure_count = models.PositiveIntegerField(default=0)
    details = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "created_at"]),
            models.Index(fields=["operation", "created_at"]),
        ]

    def mark_completed(
        self, success_count: int, failure_count: int, details: Dict[str, Any]
    ) -> None:
        self.success_count = success_count
        self.failure_count = failure_count
        self.total_items = success_count + failure_count
        self.details = details
        self.status = self.STATUS_COMPLETED
        self.completed_at = timezone.now()
        self.save(
            update_fields=[
                "success_count",
                "failure_count",
                "total_items",
                "details",
                "status",
                "completed_at",
            ]
        )

    def mark_failed(self, details: Dict[str, Any]) -> None:
        self.status = self.STATUS_FAILED
        self.details = details
        self.completed_at = timezone.now()
        self.save(update_fields=["status", "details", "completed_at"])


__all__ = ["BulkOperation"]
