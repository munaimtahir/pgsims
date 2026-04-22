from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import (
    TrainingProgram,
    ProgramRotationTemplate,
    ProgramPolicy,
    ProgramMilestone,
    ProgramMilestoneResearchRequirement,
    ProgramMilestoneWorkshopRequirement,
    ProgramMilestoneLogbookRequirement,
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


@admin.register(TrainingProgram)
class TrainingProgramAdmin(SimpleHistoryAdmin):
    list_display = ["name", "code", "degree_type", "department", "duration_months", "active", "created_at"]
    list_filter = ["active", "degree_type", "department"]
    search_fields = ["name", "code"]
    ordering = ["name"]


@admin.register(ProgramPolicy)
class ProgramPolicyAdmin(SimpleHistoryAdmin):
    list_display = ["program", "allow_program_change", "imm_allowed_from_month", "final_allowed_from_month"]
    search_fields = ["program__name", "program__code"]


class ProgramMilestoneResearchRequirementInline(admin.StackedInline):
    model = ProgramMilestoneResearchRequirement
    extra = 0


class ProgramMilestoneWorkshopRequirementInline(admin.TabularInline):
    model = ProgramMilestoneWorkshopRequirement
    extra = 0


class ProgramMilestoneLogbookRequirementInline(admin.TabularInline):
    model = ProgramMilestoneLogbookRequirement
    extra = 0


@admin.register(ProgramMilestone)
class ProgramMilestoneAdmin(SimpleHistoryAdmin):
    list_display = ["program", "code", "name", "recommended_month", "is_active"]
    list_filter = ["program", "code", "is_active"]
    search_fields = ["program__name", "code", "name"]
    inlines = [
        ProgramMilestoneResearchRequirementInline,
        ProgramMilestoneWorkshopRequirementInline,
        ProgramMilestoneLogbookRequirementInline,
    ]


@admin.register(ProgramRotationTemplate)
class ProgramRotationTemplateAdmin(SimpleHistoryAdmin):
    list_display = ["name", "program", "department", "year_index", "duration_weeks", "is_mandatory", "active"]
    list_filter = ["program", "is_mandatory", "active"]
    search_fields = ["name", "program__name", "department__name"]
    filter_horizontal = ["allowed_hospitals"]
    ordering = ["program", "sequence_order"]


@admin.register(Workshop)
class WorkshopAdmin(SimpleHistoryAdmin):
    list_display = ["name", "code", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["name", "code"]


class WorkshopRunInline(admin.TabularInline):
    model = WorkshopRun
    extra = 0


@admin.register(WorkshopBlock)
class WorkshopBlockAdmin(SimpleHistoryAdmin):
    list_display = ["workshop", "name", "capacity"]
    search_fields = ["workshop__name", "name"]
    inlines = [WorkshopRunInline]


@admin.register(ResidentTrainingRecord)
class ResidentTrainingRecordAdmin(SimpleHistoryAdmin):
    list_display = ["resident_user", "program", "start_date", "status", "locked_program", "active"]
    list_filter = ["program", "status", "active"]
    search_fields = ["resident_user__username", "resident_user__first_name", "resident_user__last_name"]
    raw_id_fields = ["resident_user", "created_by"]
    ordering = ["-start_date"]


@admin.register(ResidentResearchProject)
class ResidentResearchProjectAdmin(SimpleHistoryAdmin):
    list_display = ["resident_training_record", "title", "status", "supervisor", "created_at"]
    list_filter = ["status"]
    search_fields = ["title", "resident_training_record__resident_user__username"]
    raw_id_fields = ["supervisor"]


@admin.register(ResidentThesis)
class ResidentThesisAdmin(SimpleHistoryAdmin):
    list_display = ["resident_training_record", "status", "submitted_at"]
    list_filter = ["status"]


@admin.register(ResidentWorkshopCompletion)
class ResidentWorkshopCompletionAdmin(SimpleHistoryAdmin):
    list_display = ["resident_training_record", "workshop", "completed_at", "source"]
    list_filter = ["workshop", "source"]
    search_fields = ["resident_training_record__resident_user__username", "workshop__name"]
    date_hierarchy = "completed_at"


@admin.register(ResidentMilestoneEligibility)
class ResidentMilestoneEligibilityAdmin(admin.ModelAdmin):
    list_display = ["resident_training_record", "milestone", "status", "computed_at"]
    list_filter = ["status", "milestone__code", "milestone__program"]
    search_fields = ["resident_training_record__resident_user__username"]
    readonly_fields = ["computed_at", "reasons_json"]


@admin.register(LogbookThresholdConfig)
class LogbookThresholdConfigAdmin(SimpleHistoryAdmin):
    list_display = ["name", "mode", "min_approved_entries", "period_days", "program", "department", "is_active"]
    list_filter = ["mode", "is_active", "program", "department"]
    search_fields = ["name", "program__name", "department__name"]


@admin.register(LogbookEntry)
class LogbookEntryAdmin(SimpleHistoryAdmin):
    list_display = [
        "resident_training_record",
        "status",
        "patient_id_number",
        "patient_seen_at",
        "submitted_at",
        "approved_at",
    ]
    list_filter = ["status", "patient_seen_at"]
    search_fields = [
        "patient_id_number",
        "patient_name",
        "resident_training_record__resident_user__username",
    ]
    raw_id_fields = ["resident_training_record", "rotation_assignment", "reviewed_by", "created_by"]


@admin.register(LogbookReview)
class LogbookReviewAdmin(SimpleHistoryAdmin):
    list_display = ["entry", "action", "reviewer", "created_at"]
    list_filter = ["action"]
    search_fields = ["entry__patient_id_number", "reviewer__username"]
    raw_id_fields = ["entry", "reviewer"]


@admin.register(LogbookThresholdSnapshot)
class LogbookThresholdSnapshotAdmin(admin.ModelAdmin):
    list_display = [
        "resident_training_record",
        "threshold_config",
        "approved_entries",
        "required_entries",
        "is_met",
        "computed_at",
    ]
    list_filter = ["is_met", "threshold_config__mode"]
    search_fields = ["resident_training_record__resident_user__username", "threshold_config__name"]
    readonly_fields = ["computed_at"]


@admin.register(SubmissionRequirementTemplate)
class SubmissionRequirementTemplateAdmin(SimpleHistoryAdmin):
    list_display = ["submission_type", "code", "title", "is_required", "active", "program", "department", "sort_order"]
    list_filter = ["submission_type", "is_required", "active", "program", "department"]
    search_fields = ["code", "title", "description"]
    raw_id_fields = ["created_by"]


@admin.register(ResidentSubmission)
class ResidentSubmissionAdmin(SimpleHistoryAdmin):
    list_display = [
        "resident_training_record",
        "submission_type",
        "status",
        "submitted_at",
        "verified_at",
        "certificate_issued_at",
    ]
    list_filter = ["submission_type", "status"]
    search_fields = ["resident_training_record__resident_user__username", "feedback"]
    raw_id_fields = ["resident_training_record", "reviewed_by"]


@admin.register(SubmissionDocument)
class SubmissionDocumentAdmin(SimpleHistoryAdmin):
    list_display = ["submission", "requirement", "original_filename", "uploaded_by", "uploaded_at", "is_active"]
    list_filter = ["submission__submission_type", "is_active"]
    search_fields = ["original_filename", "submission__resident_training_record__resident_user__username"]
    raw_id_fields = ["submission", "requirement", "uploaded_by"]


@admin.register(SubmissionReview)
class SubmissionReviewAdmin(SimpleHistoryAdmin):
    list_display = ["submission", "action", "reviewer", "created_at"]
    list_filter = ["action"]
    search_fields = ["submission__resident_training_record__resident_user__username", "comments"]
    raw_id_fields = ["submission", "reviewer"]


@admin.register(SubmissionCertificate)
class SubmissionCertificateAdmin(SimpleHistoryAdmin):
    list_display = ["certificate_number", "submission", "status", "issued_by", "issued_at", "verified_by", "verified_at"]
    list_filter = ["status", "submission__submission_type"]
    search_fields = ["certificate_number", "submission__resident_training_record__resident_user__username"]
    raw_id_fields = ["submission", "issued_by", "verified_by"]


@admin.register(ProgramRotationRequirement)
class ProgramRotationRequirementAdmin(SimpleHistoryAdmin):
    list_display = ["program", "department", "required_duration_weeks", "sequence_order", "is_mandatory"]
    list_filter = ["program", "is_mandatory"]
    search_fields = ["program__name", "program__code", "department__name", "department__code"]


@admin.register(RotationCompletion)
class RotationCompletionAdmin(SimpleHistoryAdmin):
    list_display = ["rotation", "status", "confirmed_by", "confirmed_at", "verified_by", "verified_at"]
    list_filter = ["status"]
    search_fields = ["rotation__resident_training__resident_user__username"]
    raw_id_fields = ["rotation", "confirmed_by", "verified_by"]


@admin.register(RotationCertificate)
class RotationCertificateAdmin(SimpleHistoryAdmin):
    list_display = ["certificate_number", "completion", "status", "issued_by", "issued_at", "verified_by", "verified_at"]
    list_filter = ["status"]
    search_fields = ["certificate_number", "completion__rotation__resident_training__resident_user__username"]
    raw_id_fields = ["completion", "issued_by", "verified_by"]


@admin.register(RotationAssignment)
class RotationAssignmentAdmin(SimpleHistoryAdmin):
    list_display = [
        "resident_training", "hospital_department", "start_date", "end_date", "status",
        "approved_by_hod", "approved_by_utrmc", "submitted_at", "approved_at"
    ]
    list_filter = ["status", "hospital_department__hospital", "hospital_department__department"]
    search_fields = [
        "resident_training__resident_user__username",
        "resident_training__resident_user__first_name",
        "resident_training__resident_user__last_name",
    ]
    raw_id_fields = ["requested_by", "approved_by_hod", "approved_by_utrmc"]
    date_hierarchy = "start_date"
    ordering = ["-start_date"]


@admin.register(LeaveRequest)
class LeaveRequestAdmin(SimpleHistoryAdmin):
    list_display = [
        "resident_training", "leave_type", "start_date", "end_date", "status", "approved_by"
    ]
    list_filter = ["status", "leave_type"]
    search_fields = [
        "resident_training__resident_user__username",
        "resident_training__resident_user__first_name",
        "resident_training__resident_user__last_name",
    ]
    raw_id_fields = ["approved_by"]
    date_hierarchy = "start_date"
    ordering = ["-start_date"]


@admin.register(DeputationPosting)
class DeputationPostingAdmin(SimpleHistoryAdmin):
    list_display = [
        "resident_training", "posting_type", "institution_name", "city", "start_date", "end_date", "status"
    ]
    list_filter = ["status", "posting_type"]
    search_fields = [
        "institution_name", "city",
        "resident_training__resident_user__username",
        "resident_training__resident_user__first_name",
    ]
    raw_id_fields = ["approved_by"]
    date_hierarchy = "start_date"
    ordering = ["-start_date"]
