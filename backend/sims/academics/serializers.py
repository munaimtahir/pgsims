from rest_framework import serializers
from .models import (
    AcademicPeriod,
    AcademicSession,
    Department,
    Designation,
    EvaluationFormTemplate,
    Institution,
    LogbookCategory,
    ResidentTrainingRecord,
    RotationTemplate,
    Specialty,
    SupervisorReviewQueueItem,
)
from sims.rotations.models import Hospital
from sims.training.models import TrainingProgram
from sims.users.models import ResidentProfile, SupervisorProfile


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = ["id", "name", "code", "description", "active", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at"]


class DepartmentSerializer(serializers.ModelSerializer):
    head_name = serializers.CharField(source="head.get_full_name", read_only=True)

    class Meta:
        model = Department
        fields = [
            "id",
            "name",
            "code",
            "description",
            "head",
            "head_name",
            "active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]


class HospitalSerializer(serializers.ModelSerializer):
    institution_name = serializers.CharField(source="institution.name", read_only=True)

    class Meta:
        model = Hospital
        fields = [
            "id",
            "name",
            "code",
            "address",
            "phone",
            "email",
            "website",
            "description",
            "facilities",
            "institution",
            "institution_name",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]


class TrainingProgramSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source="department.name", read_only=True)

    class Meta:
        model = TrainingProgram
        fields = [
            "id",
            "name",
            "code",
            "duration_months",
            "description",
            "degree_type",
            "department",
            "department_name",
            "notes",
            "active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]


class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ["id", "name", "code", "description", "active", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at"]


class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = ["id", "name", "code", "description", "active", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at"]


class AcademicSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicSession
        fields = ["id", "name", "code", "description", "active", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at"]


class ResidentTrainingRecordSerializer(serializers.ModelSerializer):
    resident_name = serializers.CharField(source="resident.user.get_full_name", read_only=True)
    resident_username = serializers.CharField(source="resident.user.username", read_only=True)
    program_name = serializers.CharField(source="program.name", read_only=True)
    academic_session_name = serializers.CharField(source="academic_session.name", read_only=True)
    training_site_name = serializers.CharField(source="training_site.name", read_only=True)
    department_name = serializers.CharField(source="department.name", read_only=True)

    class Meta:
        model = ResidentTrainingRecord
        fields = [
            "id",
            "resident",
            "resident_name",
            "resident_username",
            "program",
            "program_name",
            "academic_session",
            "academic_session_name",
            "training_site",
            "training_site_name",
            "department",
            "department_name",
            "start_date",
            "expected_end_date",
            "actual_end_date",
            "training_year",
            "status",
            "is_active",
            "notes",
            "extra_data",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_by", "updated_by", "created_at", "updated_at"]


class AcademicPeriodSerializer(serializers.ModelSerializer):
    academic_session_name = serializers.CharField(source="academic_session.name", read_only=True)

    class Meta:
        model = AcademicPeriod
        fields = [
            "id",
            "name",
            "code",
            "academic_session",
            "academic_session_name",
            "start_date",
            "end_date",
            "period_type",
            "is_active",
            "sort_order",
            "description",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_by", "updated_by", "created_at", "updated_at"]


class RotationTemplateSerializer(serializers.ModelSerializer):
    program_name = serializers.CharField(source="program.name", read_only=True)
    department_name = serializers.CharField(source="department.name", read_only=True)

    class Meta:
        model = RotationTemplate
        fields = [
            "id",
            "name",
            "code",
            "program",
            "program_name",
            "department",
            "department_name",
            "training_year",
            "duration_weeks",
            "is_required",
            "is_active",
            "description",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_by", "updated_by", "created_at", "updated_at"]


class EvaluationFormTemplateSerializer(serializers.ModelSerializer):
    program_name = serializers.CharField(source="program.name", read_only=True)
    department_name = serializers.CharField(source="department.name", read_only=True)

    class Meta:
        model = EvaluationFormTemplate
        fields = [
            "id",
            "name",
            "code",
            "program",
            "program_name",
            "department",
            "department_name",
            "form_type",
            "schema",
            "is_active",
            "description",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_by", "updated_by", "created_at", "updated_at"]


class LogbookCategorySerializer(serializers.ModelSerializer):
    program_name = serializers.CharField(source="program.name", read_only=True)
    department_name = serializers.CharField(source="department.name", read_only=True)

    class Meta:
        model = LogbookCategory
        fields = [
            "id",
            "name",
            "code",
            "program",
            "program_name",
            "department",
            "department_name",
            "category_type",
            "minimum_required",
            "is_active",
            "description",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_by", "updated_by", "created_at", "updated_at"]


class SupervisorReviewQueueItemSerializer(serializers.ModelSerializer):
    resident_name = serializers.CharField(source="resident.user.get_full_name", read_only=True)
    supervisor_name = serializers.CharField(source="supervisor.user.get_full_name", read_only=True)

    class Meta:
        model = SupervisorReviewQueueItem
        fields = [
            "id",
            "resident",
            "resident_name",
            "supervisor",
            "supervisor_name",
            "training_record",
            "queue_type",
            "status",
            "due_date",
            "notes",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_by", "updated_by", "created_at", "updated_at"]


class AcademicOptionsSerializer(serializers.Serializer):
    residents = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    supervisors = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    programs = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    academic_sessions = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    training_sites = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    departments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    periods = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
