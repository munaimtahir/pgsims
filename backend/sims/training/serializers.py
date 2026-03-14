from rest_framework import serializers
from .models import (
    TrainingProgram,
    ProgramPolicy,
    ProgramMilestone,
    ProgramMilestoneResearchRequirement,
    ProgramMilestoneWorkshopRequirement,
    ProgramMilestoneLogbookRequirement,
    ProgramRotationTemplate,
    ResidentTrainingRecord,
    ResidentResearchProject,
    ResidentThesis,
    Workshop,
    WorkshopBlock,
    WorkshopRun,
    ResidentWorkshopCompletion,
    ResidentMilestoneEligibility,
    RotationAssignment,
    LeaveRequest,
    DeputationPosting,
)


class TrainingProgramSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source="department.name", read_only=True)
    is_active = serializers.BooleanField(source="active", read_only=True)

    class Meta:
        model = TrainingProgram
        fields = [
            "id", "name", "code", "duration_months", "description",
            "degree_type", "department", "department_name", "notes",
            "active", "is_active",
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


# ---------------------------------------------------------------------------
# Program Policy
# ---------------------------------------------------------------------------

class ProgramPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramPolicy
        fields = [
            "id", "program",
            "allow_program_change", "program_change_requires_restart",
            "min_active_months_before_imm", "imm_allowed_from_month",
            "final_allowed_from_month", "exception_rules_text",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


# ---------------------------------------------------------------------------
# Program Milestones + Requirements
# ---------------------------------------------------------------------------

class ProgramMilestoneResearchRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramMilestoneResearchRequirement
        fields = [
            "id", "milestone",
            "requires_synopsis_approved",
            "requires_synopsis_submitted_to_university",
            "requires_thesis_submitted",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class ProgramMilestoneWorkshopRequirementSerializer(serializers.ModelSerializer):
    workshop_name = serializers.CharField(source="workshop.name", read_only=True)

    class Meta:
        model = ProgramMilestoneWorkshopRequirement
        fields = ["id", "milestone", "workshop", "workshop_name", "required_count", "created_at"]
        read_only_fields = ["id", "created_at"]


class ProgramMilestoneLogbookRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramMilestoneLogbookRequirement
        fields = ["id", "milestone", "procedure_key", "category", "min_entries", "created_at"]
        read_only_fields = ["id", "created_at"]


class ProgramMilestoneSerializer(serializers.ModelSerializer):
    program_code = serializers.CharField(source="program.code", read_only=True)
    code_display = serializers.CharField(source="get_code_display", read_only=True)
    research_requirement = ProgramMilestoneResearchRequirementSerializer(read_only=True)
    workshop_requirements = ProgramMilestoneWorkshopRequirementSerializer(many=True, read_only=True)
    logbook_requirements = ProgramMilestoneLogbookRequirementSerializer(many=True, read_only=True)

    class Meta:
        model = ProgramMilestone
        fields = [
            "id", "program", "program_code", "code", "code_display", "name",
            "recommended_month", "is_active",
            "research_requirement", "workshop_requirements", "logbook_requirements",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


# ---------------------------------------------------------------------------
# Research Project + Thesis
# ---------------------------------------------------------------------------

class ResidentResearchProjectSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    supervisor_name = serializers.SerializerMethodField()
    resident_name = serializers.SerializerMethodField()

    class Meta:
        model = ResidentResearchProject
        fields = [
            "id", "resident_training_record",
            "resident_name", "title", "topic_area",
            "supervisor", "supervisor_name",
            "status", "status_display",
            "synopsis_file", "synopsis_approved_at",
            "supervisor_feedback", "university_submission_ref",
            "submitted_to_supervisor_at", "submitted_to_university_at",
            "accepted_at", "created_at", "updated_at",
        ]
        read_only_fields = [
            "id", "resident_training_record", "status", "synopsis_approved_at",
            "submitted_to_supervisor_at", "submitted_to_university_at",
            "accepted_at", "created_at", "updated_at",
        ]

    def get_supervisor_name(self, obj):
        if obj.supervisor:
            return obj.supervisor.get_full_name() or obj.supervisor.username
        return None

    def get_resident_name(self, obj):
        user = obj.resident_training_record.resident_user
        return user.get_full_name() or user.username


class ResidentThesisSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = ResidentThesis
        fields = [
            "id", "resident_training_record",
            "status", "status_display",
            "thesis_file", "submitted_at", "final_submission_ref", "notes",
            "created_at", "updated_at",
        ]
        read_only_fields = [
            "id", "status", "submitted_at", "created_at", "updated_at",
        ]


# ---------------------------------------------------------------------------
# Workshops
# ---------------------------------------------------------------------------

class WorkshopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workshop
        fields = ["id", "name", "code", "description", "is_active", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class WorkshopBlockSerializer(serializers.ModelSerializer):
    workshop_name = serializers.CharField(source="workshop.name", read_only=True)

    class Meta:
        model = WorkshopBlock
        fields = ["id", "workshop", "workshop_name", "name", "capacity", "created_at"]
        read_only_fields = ["id", "created_at"]


class WorkshopRunSerializer(serializers.ModelSerializer):
    block_name = serializers.CharField(source="block.name", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = WorkshopRun
        fields = [
            "id", "block", "block_name", "run_date", "facilitator",
            "status", "status_display", "notes", "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class ResidentWorkshopCompletionSerializer(serializers.ModelSerializer):
    workshop_name = serializers.CharField(source="workshop.name", read_only=True)
    source_display = serializers.CharField(source="get_source_display", read_only=True)

    class Meta:
        model = ResidentWorkshopCompletion
        fields = [
            "id", "resident_training_record",
            "workshop", "workshop_name",
            "workshop_run",
            "completed_at", "certificate_file",
            "source", "source_display", "notes",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "resident_training_record", "source", "created_at", "updated_at"]

    def create(self, validated_data):
        validated_data["source"] = ResidentWorkshopCompletion.SOURCE_MANUAL
        return super().create(validated_data)


# ---------------------------------------------------------------------------
# Eligibility snapshot
# ---------------------------------------------------------------------------

class ResidentMilestoneEligibilitySerializer(serializers.ModelSerializer):
    milestone_code = serializers.CharField(source="milestone.code", read_only=True)
    milestone_name = serializers.CharField(source="milestone.name", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    resident_name = serializers.SerializerMethodField()
    reasons = serializers.ListField(source="reasons_json", child=serializers.CharField(), read_only=True)

    class Meta:
        model = ResidentMilestoneEligibility
        fields = [
            "id", "resident_training_record", "resident_name",
            "milestone", "milestone_code", "milestone_name",
            "status", "status_display",
            "reasons", "computed_at",
        ]
        read_only_fields = ["id", "status", "reasons", "computed_at"]

    def get_resident_name(self, obj):
        user = obj.resident_training_record.resident_user
        return user.get_full_name() or user.username
