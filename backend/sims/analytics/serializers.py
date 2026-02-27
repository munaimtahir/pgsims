"""Serializers for analytics API responses."""

from __future__ import annotations

from rest_framework import serializers

from sims.analytics.services import normalize_ui_event_type


class TrendPointSerializer(serializers.Serializer):
    date = serializers.DateField()
    count = serializers.IntegerField()
    approved = serializers.IntegerField()
    avg_score = serializers.FloatField(allow_null=True)
    moving_average = serializers.FloatField(allow_null=True)


class TrendResponseSerializer(serializers.Serializer):
    metric = serializers.CharField()
    window = serializers.IntegerField()
    series = TrendPointSerializer(many=True)


class ComparativeGroupSerializer(serializers.Serializer):
    value = serializers.FloatField()
    total_entries = serializers.IntegerField()
    approved = serializers.IntegerField()
    average_score = serializers.FloatField()


class ComparativeResponseSerializer(serializers.Serializer):
    primary = ComparativeGroupSerializer()
    secondary = ComparativeGroupSerializer()


class PerformanceMetricsSerializer(serializers.Serializer):
    total_entries = serializers.FloatField()
    pending = serializers.FloatField()
    approved = serializers.FloatField()
    approval_rate = serializers.FloatField()
    rejection_rate = serializers.FloatField()
    pending_rate = serializers.FloatField()
    average_review_hours = serializers.FloatField()


class DashboardOverviewSerializer(serializers.Serializer):
    """Serializer for dashboard overview data."""

    total_residents = serializers.IntegerField()
    active_rotations = serializers.IntegerField()
    pending_certificates = serializers.IntegerField()
    last_30d_logs = serializers.IntegerField()
    last_30d_cases = serializers.IntegerField()
    unverified_logs = serializers.IntegerField()


class MonthlyTrendSerializer(serializers.Serializer):
    """Serializer for monthly trend data."""

    month = serializers.CharField()
    department = serializers.CharField()
    case_count = serializers.IntegerField()
    log_count = serializers.IntegerField()


class DashboardTrendsSerializer(serializers.Serializer):
    """Serializer for dashboard trends (last 12 months)."""

    trends = MonthlyTrendSerializer(many=True)


class ComplianceDataSerializer(serializers.Serializer):
    """Serializer for compliance data by rotation."""

    rotation_name = serializers.CharField()
    total_logs = serializers.IntegerField()
    verified_logs = serializers.IntegerField()
    verification_percentage = serializers.FloatField()


class DashboardComplianceSerializer(serializers.Serializer):
    """Serializer for dashboard compliance data."""

    compliance = ComplianceDataSerializer(many=True)


class AnalyticsFilterOptionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class AnalyticsFiltersSerializer(serializers.Serializer):
    roles = serializers.ListField(child=serializers.CharField())
    departments = AnalyticsFilterOptionSerializer(many=True)
    hospitals = AnalyticsFilterOptionSerializer(many=True)


class AnalyticsCardSerializer(serializers.Serializer):
    key = serializers.CharField()
    title = serializers.CharField()
    value = serializers.FloatField()


class AnalyticsTableSerializer(serializers.Serializer):
    columns = serializers.ListField(child=serializers.CharField())
    rows = serializers.ListField(child=serializers.DictField())


class AnalyticsTabPayloadSerializer(serializers.Serializer):
    title = serializers.CharField()
    date_range = serializers.DictField()
    cards = AnalyticsCardSerializer(many=True)
    table = AnalyticsTableSerializer()
    series = serializers.ListField(child=serializers.DictField())


class AnalyticsLivePayloadSerializer(serializers.Serializer):
    date_range = serializers.DictField()
    events = serializers.ListField(child=serializers.DictField())


class AnalyticsUIEventIngestSerializer(serializers.Serializer):
    event_type = serializers.CharField()
    metadata = serializers.DictField(required=False)
    department_id = serializers.IntegerField(required=False, allow_null=True)
    hospital_id = serializers.IntegerField(required=False, allow_null=True)
    entity_type = serializers.CharField(required=False, allow_blank=True)
    entity_id = serializers.CharField(required=False, allow_blank=True)
    event_key = serializers.CharField(required=False, allow_blank=True)
    occurred_at = serializers.DateTimeField(required=False)

    def validate_event_type(self, value):
        return normalize_ui_event_type(value)


__all__ = [
    "TrendPointSerializer",
    "TrendResponseSerializer",
    "ComparativeResponseSerializer",
    "PerformanceMetricsSerializer",
    "DashboardOverviewSerializer",
    "DashboardTrendsSerializer",
    "DashboardComplianceSerializer",
    "AnalyticsFiltersSerializer",
    "AnalyticsTabPayloadSerializer",
    "AnalyticsLivePayloadSerializer",
    "AnalyticsUIEventIngestSerializer",
]
