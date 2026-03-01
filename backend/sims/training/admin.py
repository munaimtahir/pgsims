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

