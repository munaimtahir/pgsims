from rest_framework import serializers
from django.db.models import Q
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
    LogbookThresholdConfig,
    LogbookEntry,
    LogbookReview,
    LogbookThresholdSnapshot,
    SubmissionRequirementTemplate,
    ResidentSubmission,
    SubmissionDocument,
    SubmissionReview,
    SubmissionCertificate,
    ProgramRotationRequirement,
    RotationCompletion,
    RotationCertificate,
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
        extra_kwargs = {"resident_training": {"required": True}}

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


class LogbookThresholdConfigSerializer(serializers.ModelSerializer):
    configured_by_name = serializers.SerializerMethodField()
    program_name = serializers.CharField(source="program.name", read_only=True)
    department_name = serializers.CharField(source="department.name", read_only=True)

    class Meta:
        model = LogbookThresholdConfig
        fields = [
            "id",
            "name",
            "mode",
            "min_approved_entries",
            "period_days",
            "program",
            "program_name",
            "department",
            "department_name",
            "is_active",
            "configured_by",
            "configured_by_name",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "configured_by", "created_at", "updated_at"]

    def get_configured_by_name(self, obj):
        if obj.configured_by:
            return obj.configured_by.get_full_name() or obj.configured_by.username
        return None


class LogbookReviewSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.SerializerMethodField()

    class Meta:
        model = LogbookReview
        fields = ["id", "entry", "reviewer", "reviewer_name", "action", "comments", "created_at"]
        read_only_fields = ["id", "reviewer", "created_at"]

    def get_reviewer_name(self, obj):
        if obj.reviewer:
            return obj.reviewer.get_full_name() or obj.reviewer.username
        return None


class LogbookEntrySerializer(serializers.ModelSerializer):
    resident_name = serializers.SerializerMethodField()
    feedback = serializers.CharField(source="supervisor_feedback", read_only=True)
    submitted_to_supervisor_at = serializers.DateTimeField(source="submitted_at", read_only=True)
    reviewed_by_name = serializers.SerializerMethodField()
    reviews = LogbookReviewSerializer(many=True, read_only=True)

    class Meta:
        model = LogbookEntry
        fields = [
            "id",
            "resident_training_record",
            "resident_name",
            "rotation_assignment",
            "patient_id_number",
            "patient_name",
            "age",
            "gender",
            "demographics",
            "disease_area",
            "diagnosis",
            "clinical_presentation",
            "management_plan",
            "resident_reflection",
            "patient_seen_at",
            "status",
            "supervisor_feedback",
            "feedback",
            "submitted_to_supervisor_at",
            "submitted_at",
            "returned_at",
            "approved_at",
            "reviewed_by",
            "reviewed_by_name",
            "created_by",
            "created_at",
            "updated_at",
            "reviews",
        ]
        read_only_fields = [
            "id",
            "resident_training_record",
            "status",
            "supervisor_feedback",
            "feedback",
            "submitted_to_supervisor_at",
            "submitted_at",
            "returned_at",
            "approved_at",
            "reviewed_by",
            "reviewed_by_name",
            "created_by",
            "created_at",
            "updated_at",
            "reviews",
        ]

    def get_resident_name(self, obj):
        user = obj.resident_training_record.resident_user
        return user.get_full_name() or user.username

    def get_reviewed_by_name(self, obj):
        if obj.reviewed_by:
            return obj.reviewed_by.get_full_name() or obj.reviewed_by.username
        return None


class LogbookThresholdSnapshotSerializer(serializers.ModelSerializer):
    threshold_name = serializers.CharField(source="threshold_config.name", read_only=True)

    class Meta:
        model = LogbookThresholdSnapshot
        fields = [
            "id",
            "resident_training_record",
            "threshold_config",
            "threshold_name",
            "rotation_assignment",
            "window_start",
            "window_end",
            "approved_entries",
            "required_entries",
            "is_met",
            "computed_at",
        ]
        read_only_fields = fields


class SubmissionRequirementTemplateSerializer(serializers.ModelSerializer):
    program_name = serializers.CharField(source="program.name", read_only=True)
    department_name = serializers.CharField(source="department.name", read_only=True)
    created_by_name = serializers.SerializerMethodField()

    class Meta:
        model = SubmissionRequirementTemplate
        fields = [
            "id",
            "submission_type",
            "code",
            "title",
            "description",
            "is_required",
            "active",
            "sort_order",
            "program",
            "program_name",
            "department",
            "department_name",
            "created_by",
            "created_by_name",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_by", "created_at", "updated_at"]

    def get_created_by_name(self, obj):
        if obj.created_by:
            return obj.created_by.get_full_name() or obj.created_by.username
        return None


class SubmissionDocumentSerializer(serializers.ModelSerializer):
    requirement_title = serializers.CharField(source="requirement.title", read_only=True)
    uploaded_by_name = serializers.SerializerMethodField()

    class Meta:
        model = SubmissionDocument
        fields = [
            "id",
            "submission",
            "requirement",
            "requirement_title",
            "file",
            "original_filename",
            "uploaded_by",
            "uploaded_by_name",
            "uploaded_at",
            "is_active",
        ]
        read_only_fields = ["id", "uploaded_by", "uploaded_by_name", "uploaded_at"]

    def get_uploaded_by_name(self, obj):
        if obj.uploaded_by:
            return obj.uploaded_by.get_full_name() or obj.uploaded_by.username
        return None


class SubmissionReviewSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.SerializerMethodField()

    class Meta:
        model = SubmissionReview
        fields = ["id", "submission", "reviewer", "reviewer_name", "action", "comments", "created_at"]
        read_only_fields = ["id", "reviewer", "reviewer_name", "created_at"]

    def get_reviewer_name(self, obj):
        if obj.reviewer:
            return obj.reviewer.get_full_name() or obj.reviewer.username
        return None


class SubmissionCertificateSerializer(serializers.ModelSerializer):
    issued_by_name = serializers.SerializerMethodField()
    verified_by_name = serializers.SerializerMethodField()

    class Meta:
        model = SubmissionCertificate
        fields = [
            "id",
            "submission",
            "certificate_number",
            "status",
            "issued_by",
            "issued_by_name",
            "issued_at",
            "verified_by",
            "verified_by_name",
            "verified_at",
            "metadata",
        ]
        read_only_fields = [
            "id",
            "submission",
            "certificate_number",
            "status",
            "issued_by",
            "issued_by_name",
            "issued_at",
            "verified_by",
            "verified_by_name",
            "verified_at",
            "metadata",
        ]

    def get_issued_by_name(self, obj):
        if obj.issued_by:
            return obj.issued_by.get_full_name() or obj.issued_by.username
        return None

    def get_verified_by_name(self, obj):
        if obj.verified_by:
            return obj.verified_by.get_full_name() or obj.verified_by.username
        return None


class ResidentSubmissionSerializer(serializers.ModelSerializer):
    resident_name = serializers.SerializerMethodField()
    reviewed_by_name = serializers.SerializerMethodField()
    documents = SubmissionDocumentSerializer(many=True, read_only=True)
    reviews = SubmissionReviewSerializer(many=True, read_only=True)
    certificate = SubmissionCertificateSerializer(read_only=True)
    required_documents_count = serializers.SerializerMethodField()
    uploaded_required_count = serializers.SerializerMethodField()
    all_required_uploaded = serializers.SerializerMethodField()

    class Meta:
        model = ResidentSubmission
        fields = [
            "id",
            "resident_training_record",
            "resident_name",
            "submission_type",
            "status",
            "submitted_at",
            "under_review_at",
            "returned_at",
            "verified_at",
            "certificate_issued_at",
            "feedback",
            "reviewed_by",
            "reviewed_by_name",
            "required_documents_count",
            "uploaded_required_count",
            "all_required_uploaded",
            "documents",
            "reviews",
            "certificate",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "resident_name",
            "status",
            "submitted_at",
            "under_review_at",
            "returned_at",
            "verified_at",
            "certificate_issued_at",
            "reviewed_by",
            "reviewed_by_name",
            "required_documents_count",
            "uploaded_required_count",
            "all_required_uploaded",
            "documents",
            "reviews",
            "certificate",
            "created_at",
            "updated_at",
        ]

    def get_resident_name(self, obj):
        user = obj.resident_training_record.resident_user
        return user.get_full_name() or user.username

    def get_reviewed_by_name(self, obj):
        if obj.reviewed_by:
            return obj.reviewed_by.get_full_name() or obj.reviewed_by.username
        return None

    def _required_requirements_queryset(self, obj):
        user = obj.resident_training_record.resident_user
        return SubmissionRequirementTemplate.objects.filter(
            submission_type=obj.submission_type,
            active=True,
            is_required=True,
        ).filter(
            Q(program__isnull=True) | Q(program=obj.resident_training_record.program)
        ).filter(
            Q(department__isnull=True) | Q(department=user.home_department)
        )

    def get_required_documents_count(self, obj):
        return self._required_requirements_queryset(obj).count()

    def get_uploaded_required_count(self, obj):
        required_ids = list(self._required_requirements_queryset(obj).values_list("id", flat=True))
        if not required_ids:
            return 0
        return obj.documents.filter(is_active=True, requirement_id__in=required_ids).values(
            "requirement_id"
        ).distinct().count()

    def get_all_required_uploaded(self, obj):
        total = self.get_required_documents_count(obj)
        if total == 0:
            return True
        return self.get_uploaded_required_count(obj) >= total


class ProgramRotationRequirementSerializer(serializers.ModelSerializer):
    program_name = serializers.CharField(source="program.name", read_only=True)
    department_name = serializers.CharField(source="department.name", read_only=True)

    class Meta:
        model = ProgramRotationRequirement
        fields = [
            "id",
            "program",
            "program_name",
            "department",
            "department_name",
            "required_duration_weeks",
            "sequence_order",
            "is_mandatory",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class RotationCertificateSerializer(serializers.ModelSerializer):
    issued_by_name = serializers.SerializerMethodField()
    verified_by_name = serializers.SerializerMethodField()

    class Meta:
        model = RotationCertificate
        fields = [
            "id",
            "completion",
            "certificate_number",
            "status",
            "issued_by",
            "issued_by_name",
            "issued_at",
            "verified_by",
            "verified_by_name",
            "verified_at",
            "metadata",
        ]
        read_only_fields = fields

    def get_issued_by_name(self, obj):
        if obj.issued_by:
            return obj.issued_by.get_full_name() or obj.issued_by.username
        return None

    def get_verified_by_name(self, obj):
        if obj.verified_by:
            return obj.verified_by.get_full_name() or obj.verified_by.username
        return None


class RotationCompletionSerializer(serializers.ModelSerializer):
    resident_name = serializers.SerializerMethodField()
    confirmed_by_name = serializers.SerializerMethodField()
    verified_by_name = serializers.SerializerMethodField()
    certificate = RotationCertificateSerializer(read_only=True)

    class Meta:
        model = RotationCompletion
        fields = [
            "id",
            "rotation",
            "status",
            "resident_name",
            "confirmed_by",
            "confirmed_by_name",
            "confirmed_at",
            "verification_submitted_at",
            "verified_by",
            "verified_by_name",
            "verified_at",
            "notes",
            "certificate",
        ]
        read_only_fields = fields

    def get_resident_name(self, obj):
        user = obj.rotation.resident_training.resident_user
        return user.get_full_name() or user.username

    def get_confirmed_by_name(self, obj):
        if obj.confirmed_by:
            return obj.confirmed_by.get_full_name() or obj.confirmed_by.username
        return None

    def get_verified_by_name(self, obj):
        if obj.verified_by:
            return obj.verified_by.get_full_name() or obj.verified_by.username
        return None
