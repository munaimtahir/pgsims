"""Serializers for rotations API endpoints."""

from typing import Optional

from rest_framework import serializers

from sims.rotations.models import Rotation


class RotationSummarySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    department = serializers.CharField(source="department.name", read_only=True)
    hospital = serializers.CharField(source="hospital.name", read_only=True)
    supervisor_name = serializers.SerializerMethodField()

    class Meta:
        model = Rotation
        fields = [
            "id",
            "name",
            "department",
            "hospital",
            "start_date",
            "end_date",
            "status",
            "supervisor_name",
        ]

    def get_name(self, obj: Rotation) -> str:
        if obj.department_id:
            return obj.department.name
        return "Rotation"

    def get_supervisor_name(self, obj: Rotation) -> Optional[str]:
        if not obj.supervisor_id:
            return None
        return obj.supervisor.get_full_name() or obj.supervisor.username
