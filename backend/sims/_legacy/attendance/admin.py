"""Admin configuration for attendance app."""

from django.contrib import admin

from .models import AttendanceRecord, EligibilitySummary, Session


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    """Admin for attendance sessions."""

    list_display = ["title", "session_type", "date", "start_time", "status", "rotation"]
    list_filter = ["session_type", "status", "date"]
    search_fields = ["title", "module_name", "location"]
    date_hierarchy = "date"
    ordering = ["-date", "-start_time"]


@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    """Admin for attendance records."""

    list_display = ["user", "session", "status", "check_in_time", "recorded_by"]
    list_filter = ["status", "session__date", "session__session_type"]
    search_fields = ["user__username", "user__first_name", "user__last_name", "session__title"]
    date_hierarchy = "session__date"
    ordering = ["-session__date", "user__last_name"]


@admin.register(EligibilitySummary)
class EligibilitySummaryAdmin(admin.ModelAdmin):
    """Admin for eligibility summaries."""

    list_display = [
        "user",
        "period",
        "start_date",
        "end_date",
        "percentage_present",
        "is_eligible",
    ]
    list_filter = ["period", "is_eligible", "start_date"]
    search_fields = ["user__username", "user__first_name", "user__last_name"]
    date_hierarchy = "start_date"
    ordering = ["-start_date", "user__last_name"]
