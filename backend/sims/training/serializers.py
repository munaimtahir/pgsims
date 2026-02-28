from rest_framework import serializers
from .models import (
    TrainingProgram,
    ProgramRotationTemplate,
    ResidentTrainingRecord,
    RotationAssignment,
    LeaveRequest,
    DeputationPosting,
)


class TrainingProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingProgram
        fields = [
            "id", "name", "code", "duration_months", "description", "active",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class ProgramRotationTemplateSerializer(serializers.ModelSerializer):
    program_name = serializers.CharField(source="program.name", read_only=True)
    department_name = serializers.CharField(source="department.name", read_only=True)
    allowed_hospital_names = serializers.SerializerMethodField()

    class Meta:
        model = ProgramRotationTemplate
        fields = [
            "id", "program", "program_name", "name", "department", "department_name",
            "duration_weeks", "required", "sequence_order", "allowed_hospitals",
            "allowed_hospital_names", "active", "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def get_allowed_hospital_names(self, obj):
        return [h.name for h in obj.allowed_hospitals.all()]


class ResidentTrainingRecordSerializer(serializers.ModelSerializer):
    resident_name = serializers.SerializerMethodField()
    program_name = serializers.CharField(source="program.name", read_only=True)
    program_code = serializers.CharField(source="program.code", read_only=True)

    class Meta:
        model = ResidentTrainingRecord
        fields = [
            "id", "resident_user", "resident_name", "program", "program_name", "program_code",
            "start_date", "expected_end_date", "current_level", "active",
            "created_by", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_by", "created_at", "updated_at"]

    def get_resident_name(self, obj):
        return obj.resident_user.get_full_name() or obj.resident_user.username

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)


class RotationAssignmentSerializer(serializers.ModelSerializer):
    resident_name = serializers.SerializerMethodField()
    program_name = serializers.SerializerMethodField()
    hospital_name = serializers.CharField(
        source="hospital_department.hospital.name", read_only=True
    )
    department_name = serializers.CharField(
        source="hospital_department.department.name", read_only=True
    )
    template_name = serializers.CharField(source="template.name", read_only=True)

    class Meta:
        model = RotationAssignment
        fields = [
            "id",
            "resident_training", "resident_name", "program_name",
            "hospital_department", "hospital_name", "department_name",
            "template", "template_name",
            "start_date", "end_date", "status", "notes",
            "return_reason", "reject_reason",
            "requested_by", "approved_by_hod", "approved_by_utrmc",
            "submitted_at", "approved_at", "completed_at",
            "created_at", "updated_at",
        ]
        read_only_fields = [
            "id", "status", "return_reason", "reject_reason",
            "requested_by", "approved_by_hod", "approved_by_utrmc",
            "submitted_at", "approved_at", "completed_at",
            "created_at", "updated_at",
        ]

    def get_resident_name(self, obj):
        user = obj.resident_training.resident_user
        return user.get_full_name() or user.username

    def get_program_name(self, obj):
        return obj.resident_training.program.name

    def validate(self, attrs):
        # Run model-level overlap check via clean()
        instance = RotationAssignment(**attrs)
        if self.instance:
            instance.pk = self.instance.pk
        instance.clean()
        return attrs


class LeaveRequestSerializer(serializers.ModelSerializer):
    resident_name = serializers.SerializerMethodField()

    class Meta:
        model = LeaveRequest
        fields = [
            "id", "resident_training", "resident_name",
            "leave_type", "start_date", "end_date", "reason", "status",
            "approved_by", "approved_at", "reject_reason",
            "created_at", "updated_at",
        ]
        read_only_fields = [
            "id", "status", "approved_by", "approved_at", "reject_reason",
            "created_at", "updated_at",
        ]

    def get_resident_name(self, obj):
        user = obj.resident_training.resident_user
        return user.get_full_name() or user.username


class DeputationPostingSerializer(serializers.ModelSerializer):
    resident_name = serializers.SerializerMethodField()

    class Meta:
        model = DeputationPosting
        fields = [
            "id", "resident_training", "resident_name",
            "posting_type", "institution_name", "city",
            "start_date", "end_date", "status", "notes",
            "approved_by", "approved_at", "reject_reason",
            "created_at", "updated_at",
        ]
        read_only_fields = [
            "id", "status", "approved_by", "approved_at", "reject_reason",
            "created_at", "updated_at",
        ]

    def get_resident_name(self, obj):
        user = obj.resident_training.resident_user
        return user.get_full_name() or user.username
