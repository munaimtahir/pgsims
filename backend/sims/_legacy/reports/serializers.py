"""Serializers for report generation APIs."""

from __future__ import annotations

from rest_framework import serializers

from sims.reports.models import ReportTemplate, ScheduledReport


class ReportTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportTemplate
        fields = ["slug", "name", "description", "template_name", "default_params"]


class ReportRequestSerializer(serializers.Serializer):
    template_slug = serializers.SlugField()
    format = serializers.ChoiceField(choices=["pdf", "xlsx"])
    params = serializers.DictField(child=serializers.CharField(), required=False)


class ScheduledReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledReport
        fields = [
            "id",
            "template",
            "email_to",
            "params",
            "cron",
            "last_run_at",
            "next_run_at",
            "is_active",
        ]
        read_only_fields = ["last_run_at", "next_run_at"]


__all__ = [
    "ReportTemplateSerializer",
    "ReportRequestSerializer",
    "ScheduledReportSerializer",
]
