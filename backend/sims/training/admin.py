from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import (
    TrainingProgram,
    ProgramRotationTemplate,
    ResidentTrainingRecord,
    RotationAssignment,
    LeaveRequest,
    DeputationPosting,
)


@admin.register(TrainingProgram)
class TrainingProgramAdmin(SimpleHistoryAdmin):
    list_display = ["name", "code", "duration_months", "active", "created_at"]
    list_filter = ["active"]
    search_fields = ["name", "code"]
    ordering = ["name"]


@admin.register(ProgramRotationTemplate)
class ProgramRotationTemplateAdmin(SimpleHistoryAdmin):
    list_display = ["name", "program", "department", "duration_weeks", "required", "sequence_order", "active"]
    list_filter = ["program", "required", "active"]
    search_fields = ["name", "program__name", "department__name"]
    filter_horizontal = ["allowed_hospitals"]
    ordering = ["program", "sequence_order"]


@admin.register(ResidentTrainingRecord)
class ResidentTrainingRecordAdmin(SimpleHistoryAdmin):
    list_display = ["resident_user", "program", "start_date", "expected_end_date", "current_level", "active"]
    list_filter = ["program", "active", "current_level"]
    search_fields = ["resident_user__username", "resident_user__first_name", "resident_user__last_name", "program__name"]
    raw_id_fields = ["resident_user", "created_by"]
    ordering = ["-start_date"]


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
