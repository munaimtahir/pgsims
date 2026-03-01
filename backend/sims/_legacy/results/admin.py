from django.contrib import admin
from .models import Exam, Score


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ["title", "exam_type", "date", "max_marks", "passing_marks", "status"]
    list_filter = ["exam_type", "status", "date", "requires_eligibility"]
    search_fields = ["title", "module_name"]
    ordering = ["-date"]
    date_hierarchy = "date"

    fieldsets = (
        ("Basic Information", {"fields": ("title", "exam_type", "rotation", "module_name")}),
        ("Schedule", {"fields": ("date", "start_time", "duration_minutes", "status")}),
        ("Marks", {"fields": ("max_marks", "passing_marks")}),
        ("Eligibility", {"fields": ("requires_eligibility",)}),
        ("Additional", {"fields": ("conducted_by", "instructions", "remarks")}),
    )


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = [
        "student",
        "exam",
        "marks_obtained",
        "percentage",
        "grade",
        "is_passing",
        "is_eligible",
    ]
    list_filter = ["exam__exam_type", "is_passing", "is_eligible", "grade", "exam__date"]
    search_fields = ["student__first_name", "student__last_name", "exam__title"]
    ordering = ["-exam__date", "student__last_name"]
    readonly_fields = ["percentage", "grade", "is_passing", "created_at", "updated_at"]

    fieldsets = (
        ("Exam Information", {"fields": ("exam", "student")}),
        ("Score", {"fields": ("marks_obtained", "percentage", "grade", "is_passing")}),
        ("Eligibility", {"fields": ("is_eligible", "ineligibility_reason")}),
        ("Additional", {"fields": ("remarks", "entered_by")}),
        ("Timestamps", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )
