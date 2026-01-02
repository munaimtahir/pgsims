from django.contrib import admin
from .models import Department, Batch, StudentProfile


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["code", "name", "head", "active", "created_at"]
    list_filter = ["active", "created_at"]
    search_fields = ["name", "code", "description"]
    ordering = ["name"]


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ["name", "program", "department", "start_date", "end_date", "capacity", "active"]
    list_filter = ["program", "department", "active", "start_date"]
    search_fields = ["name", "department__name"]
    ordering = ["-start_date"]
    date_hierarchy = "start_date"


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ["roll_number", "user", "batch", "status", "admission_date", "cgpa"]
    list_filter = ["status", "batch__department", "batch", "admission_date"]
    search_fields = ["roll_number", "user__first_name", "user__last_name", "user__email"]
    ordering = ["roll_number"]
    date_hierarchy = "admission_date"
    readonly_fields = ["created_at", "updated_at", "status_updated_at"]

    fieldsets = (
        ("Basic Information", {"fields": ("user", "batch", "roll_number", "status")}),
        (
            "Academic Dates",
            {"fields": ("admission_date", "expected_graduation_date", "actual_graduation_date")},
        ),
        ("Performance", {"fields": ("cgpa",)}),
        (
            "Previous Education",
            {
                "fields": ("previous_institution", "previous_qualification"),
                "classes": ("collapse",),
            },
        ),
        (
            "Emergency Contact",
            {
                "fields": (
                    "emergency_contact_name",
                    "emergency_contact_phone",
                    "emergency_contact_relation",
                ),
                "classes": ("collapse",),
            },
        ),
        ("Additional", {"fields": ("remarks",)}),
        (
            "Timestamps",
            {"fields": ("status_updated_at", "created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )
