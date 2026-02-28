"""Serializers for rotations API endpoints."""

from typing import Optional

from rest_framework import serializers

from sims.rotations.models import Rotation


class DepartmentRefSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    code = serializers.CharField(allow_null=True, required=False)


class HospitalRefSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    code = serializers.CharField(allow_null=True, required=False)


class RotationSummarySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()
    hospital = serializers.SerializerMethodField()
    source_department = serializers.SerializerMethodField()
    source_hospital = serializers.SerializerMethodField()
    supervisor_name = serializers.SerializerMethodField()
    requires_utrmc_approval = serializers.SerializerMethodField()
    approved_by = serializers.SerializerMethodField()

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
            "source_department",
            "source_hospital",
            "requires_utrmc_approval",
            "override_reason",
            "approved_by",
            "approved_at",
            "utrmc_approved_by",
            "utrmc_approved_at",
        ]

    def _serialize_department(self, obj: Rotation):
        if not obj.department_id:
            return None
        return {
            "id": obj.department_id,
            "name": obj.department.name,
            "code": getattr(obj.department, "code", None),
        }

    def _serialize_hospital(self, hospital):
        if not hospital:
            return None
        return {"id": hospital.id, "name": hospital.name, "code": hospital.code}

    def get_name(self, obj: Rotation) -> str:
        return obj.get_department_name() if hasattr(obj, "get_department_name") else "Rotation"

    def get_department(self, obj: Rotation):
        return self._serialize_department(obj)

    def get_hospital(self, obj: Rotation):
        return self._serialize_hospital(obj.hospital)

    def get_source_department(self, obj: Rotation):
        if not obj.source_department_id:
            return None
        return {
            "id": obj.source_department_id,
            "name": obj.source_department.name,
            "code": obj.source_department.code,
        }

    def get_source_hospital(self, obj: Rotation):
        return self._serialize_hospital(obj.source_hospital)

    def get_supervisor_name(self, obj: Rotation) -> Optional[str]:
        if not obj.supervisor_id:
            return None
        return obj.supervisor.get_full_name() or obj.supervisor.username

    def get_requires_utrmc_approval(self, obj: Rotation) -> bool:
        return bool(getattr(obj, "requires_utrmc_approval", False))

    def get_approved_by(self, obj: Rotation):
        user = obj.approved_by
        if not user:
            return None
        return {"id": user.id, "username": user.username, "full_name": user.get_full_name()}
