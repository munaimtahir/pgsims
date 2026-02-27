"""Admin registrations for the analytics module."""

from django.contrib import admin

from sims.analytics.models import AnalyticsDailyRollup, AnalyticsEvent


@admin.register(AnalyticsEvent)
class AnalyticsEventAdmin(admin.ModelAdmin):
    list_display = ("occurred_at", "event_type", "actor_user", "actor_role", "department", "hospital")
    list_filter = ("event_type", "actor_role", "department", "hospital")
    search_fields = ("event_type", "request_id", "event_key", "entity_type", "entity_id")
    readonly_fields = (
        "id",
        "occurred_at",
        "event_type",
        "actor_user",
        "actor_role",
        "department",
        "hospital",
        "entity_type",
        "entity_id",
        "status_from",
        "status_to",
        "request_id",
        "event_key",
        "metadata",
    )
    ordering = ("-occurred_at",)

    def has_add_permission(self, request):
        return False


@admin.register(AnalyticsDailyRollup)
class AnalyticsDailyRollupAdmin(admin.ModelAdmin):
    list_display = ("day", "event_type", "department", "hospital", "count")
    list_filter = ("event_type", "department", "hospital")
    search_fields = ("event_type",)
