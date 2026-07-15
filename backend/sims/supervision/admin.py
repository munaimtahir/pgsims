from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import ResidentSupervisorAssignment


@admin.register(ResidentSupervisorAssignment)
class ResidentSupervisorAssignmentAdmin(SimpleHistoryAdmin):
    list_display = [
        "id",
        "resident",
        "supervisor",
        "assignment_type",
        "status",
        "start_date",
        "end_date",
        "is_active",
    ]
    list_filter = ["assignment_type", "status", "is_active", "start_date"]
    search_fields = [
        "resident__user__username",
        "resident__user__first_name",
        "resident__user__last_name",
        "supervisor__user__username",
        "supervisor__user__first_name",
        "supervisor__user__last_name",
    ]
    raw_id_fields = ["resident", "supervisor"]
