from __future__ import annotations

from rest_framework import serializers

from .models import ActivityLog, AuditReport


class ActivityLogSerializer(serializers.ModelSerializer):
    actor_display = serializers.CharField(source="actor.get_full_name", read_only=True)

    class Meta:
        model = ActivityLog
        fields = [
            "id",
            "actor",
            "actor_display",
            "action",
            "verb",
            "target_object_id",
            "target_repr",
            "metadata",
            "ip_address",
            "is_sensitive",
            "created_at",
        ]
        read_only_fields = fields


class AuditReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditReport
        fields = ["id", "start", "end", "generated_at", "payload", "created_by"]
        read_only_fields = ["generated_at", "payload", "created_by"]
