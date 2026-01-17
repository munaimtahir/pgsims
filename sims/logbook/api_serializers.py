"""Serializers for logbook API endpoints."""

from rest_framework import serializers

from sims.logbook.models import LogbookEntry


class PGLogbookEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = LogbookEntry
        fields = [
            "id",
            "case_title",
            "date",
            "location_of_activity",
            "patient_history_summary",
            "management_action",
            "topic_subtopic",
            "status",
            "created_at",
            "updated_at",
            "submitted_to_supervisor_at",
        ]
        read_only_fields = [
            "id",
            "status",
            "created_at",
            "updated_at",
            "submitted_to_supervisor_at",
        ]


class PGLogbookEntryWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogbookEntry
        fields = [
            "case_title",
            "date",
            "location_of_activity",
            "patient_history_summary",
            "management_action",
            "topic_subtopic",
        ]
