"""Serializers for analytics API responses."""

from __future__ import annotations

from rest_framework import serializers


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


__all__ = [
    "TrendPointSerializer",
    "TrendResponseSerializer",
    "ComparativeResponseSerializer",
    "PerformanceMetricsSerializer",
    "DashboardOverviewSerializer",
    "DashboardTrendsSerializer",
    "DashboardComplianceSerializer",
]
