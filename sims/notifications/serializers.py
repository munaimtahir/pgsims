"""Serializers for notification APIs."""

from __future__ import annotations

from rest_framework import serializers

from sims.notifications.models import Notification, NotificationPreference


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            "id",
            "verb",
            "title",
            "body",
            "channel",
            "metadata",
            "is_read",
            "created_at",
        ]


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationPreference
        fields = [
            "email_enabled",
            "in_app_enabled",
            "quiet_hours_start",
            "quiet_hours_end",
        ]


class NotificationMarkReadSerializer(serializers.Serializer):
    notification_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1), allow_empty=False
    )


__all__ = [
    "NotificationSerializer",
    "NotificationPreferenceSerializer",
    "NotificationMarkReadSerializer",
]
