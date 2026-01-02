"""Notification models for in-app and email delivery."""

from __future__ import annotations

from typing import Any, Dict, Optional

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class Notification(models.Model):
    """A notification delivered to a user via a specific channel."""

    CHANNEL_EMAIL = "email"
    CHANNEL_IN_APP = "in_app"
    CHANNEL_CHOICES = (
        (CHANNEL_EMAIL, "Email"),
        (CHANNEL_IN_APP, "In-App"),
    )

    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    actor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="notifications_sent",
    )
    verb = models.CharField(max_length=128)
    title = models.CharField(max_length=255)
    body = models.TextField()
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES, default=CHANNEL_IN_APP)
    metadata = models.JSONField(default=dict, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    scheduled_for = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["recipient", "created_at"]),
            models.Index(fields=["channel", "created_at"]),
            models.Index(fields=["read_at"]),
        ]

    def mark_read(self) -> None:
        if not self.read_at:
            self.read_at = timezone.now()
            self.save(update_fields=["read_at"])

    @property
    def is_read(self) -> bool:
        return self.read_at is not None


class NotificationPreference(models.Model):
    """User configurable notification preferences."""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="notification_preferences"
    )
    email_enabled = models.BooleanField(default=True)
    in_app_enabled = models.BooleanField(default=True)
    quiet_hours_start = models.TimeField(null=True, blank=True)
    quiet_hours_end = models.TimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Notification Preference"
        verbose_name_plural = "Notification Preferences"

    def __str__(self) -> str:
        return f"Preferences for {self.user}"  # pragma: no cover

    def allows_channel(self, channel: str, when: Optional[timezone.datetime] = None) -> bool:
        if channel == Notification.CHANNEL_EMAIL and not self.email_enabled:
            return False
        if channel == Notification.CHANNEL_IN_APP and not self.in_app_enabled:
            return False
        if when is None or not self.quiet_hours_start or not self.quiet_hours_end:
            return True
        start = self.quiet_hours_start
        end = self.quiet_hours_end
        current_time = (when or timezone.now()).time()
        if start == end:
            return False
        if start < end:
            return not (start <= current_time < end)
        # Quiet hours wrap around midnight
        return not (current_time >= start or current_time < end)

    @classmethod
    def for_user(cls, user: User) -> "NotificationPreference":
        preference, _ = cls.objects.get_or_create(user=user)
        return preference

    def to_dict(self) -> Dict[str, Any]:
        return {
            "email_enabled": self.email_enabled,
            "in_app_enabled": self.in_app_enabled,
            "quiet_hours_start": (
                self.quiet_hours_start.isoformat() if self.quiet_hours_start else None
            ),
            "quiet_hours_end": (self.quiet_hours_end.isoformat() if self.quiet_hours_end else None),
        }


__all__ = ["Notification", "NotificationPreference"]
