from django.contrib import admin
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


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["code", "name", "head", "active", "created_at"]
    list_filter = ["active", "created_at"]
    search_fields = ["name", "code", "description"]
    ordering = ["name"]


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ["code", "name", "active", "created_at"]
    list_filter = ["active", "created_at"]
    search_fields = ["name", "code", "description"]
    ordering = ["name"]


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ["code", "name", "active", "created_at"]
    list_filter = ["active", "created_at"]
    search_fields = ["name", "code", "description"]
    ordering = ["name"]


@admin.register(Designation)
class DesignationAdmin(admin.ModelAdmin):
    list_display = ["code", "name", "active", "created_at"]
    list_filter = ["active", "created_at"]
    search_fields = ["name", "code", "description"]
    ordering = ["name"]


@admin.register(AcademicSession)
class AcademicSessionAdmin(admin.ModelAdmin):
    list_display = ["code", "name", "active", "created_at"]
    list_filter = ["active", "created_at"]
    search_fields = ["name", "code", "description"]
    ordering = ["name"]


@admin.register(ResidentTrainingRecord)
class ResidentTrainingRecordAdmin(admin.ModelAdmin):
    list_display = ["resident", "program", "academic_session", "training_year", "status", "is_active"]
    list_filter = ["status", "is_active", "academic_session", "department"]
    search_fields = ["resident__user__username", "resident__user__first_name", "resident__user__last_name"]


@admin.register(AcademicPeriod)
class AcademicPeriodAdmin(admin.ModelAdmin):
    list_display = ["code", "name", "period_type", "academic_session", "start_date", "end_date", "is_active"]
    list_filter = ["period_type", "is_active", "academic_session"]
    search_fields = ["name", "code"]


@admin.register(RotationTemplate)
class RotationTemplateAdmin(admin.ModelAdmin):
    list_display = ["code", "name", "program", "department", "training_year", "is_required", "is_active"]
    list_filter = ["is_required", "is_active", "program", "department"]
    search_fields = ["name", "code"]


@admin.register(EvaluationFormTemplate)
class EvaluationFormTemplateAdmin(admin.ModelAdmin):
    list_display = ["code", "name", "form_type", "program", "department", "is_active"]
    list_filter = ["form_type", "is_active", "program", "department"]
    search_fields = ["name", "code"]


@admin.register(LogbookCategory)
class LogbookCategoryAdmin(admin.ModelAdmin):
    list_display = ["code", "name", "category_type", "program", "department", "is_active"]
    list_filter = ["category_type", "is_active", "program", "department"]
    search_fields = ["name", "code"]


@admin.register(SupervisorReviewQueueItem)
class SupervisorReviewQueueItemAdmin(admin.ModelAdmin):
    list_display = ["resident", "supervisor", "queue_type", "status", "due_date"]
    list_filter = ["queue_type", "status"]
    search_fields = [
        "resident__user__username",
        "resident__user__first_name",
        "resident__user__last_name",
        "supervisor__user__username",
    ]
