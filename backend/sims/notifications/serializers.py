"""Serializers for notification APIs."""

from __future__ import annotations

from rest_framework import serializers

from sims.notifications.models import Notification, NotificationPreference


class NotificationTargetSerializer(serializers.Serializer):
    """The only notification metadata Android may turn into a native route."""

    kind = serializers.ChoiceField(
        choices=("leave", "evaluation", "logbook", "rotation", "research", "resident_progress")
    )
    id = serializers.IntegerField(min_value=1, required=False)


class NotificationSerializer(serializers.ModelSerializer):
    target = serializers.SerializerMethodField()

    def get_target(self, instance):
        candidate = (instance.metadata or {}).get("target")
        serializer = NotificationTargetSerializer(data=candidate)
        return serializer.initial_data if serializer.is_valid() else None

    class Meta:
        model = Notification
        fields = [
            "id",
            "verb",
            "title",
            "body",
            "channel",
            "metadata",
            "target",
            "is_read",
            "created_at",
        ]


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationPreference
        fields = [
            "email_enabled",
            "in_app_enabled",
            "push_enabled",
            "quiet_hours_start",
            "quiet_hours_end",
        ]


class NotificationMarkReadSerializer(serializers.Serializer):
    notification_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1), allow_empty=False
    )


class MobileDeviceSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=4096)
    platform = serializers.ChoiceField(choices=("android",), default="android")


__all__ = [
    "NotificationSerializer",
    "NotificationTargetSerializer",
    "NotificationPreferenceSerializer",
    "NotificationMarkReadSerializer",
    "MobileDeviceSerializer",
]
