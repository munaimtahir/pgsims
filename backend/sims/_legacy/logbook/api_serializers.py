"""Serializers for logbook API endpoints."""

from rest_framework import serializers

from sims.logbook.models import LogbookEntry


class PGLogbookEntrySerializer(serializers.ModelSerializer):
    feedback = serializers.CharField(source="supervisor_feedback", read_only=True)
    submitted_at = serializers.DateTimeField(source="submitted_to_supervisor_at", read_only=True)

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
            "supervisor_feedback",
            "feedback",
            "submitted_to_supervisor_at",
            "submitted_at",
            "verified_at",
        ]
        read_only_fields = [
            "id",
            "status",
            "created_at",
            "updated_at",
            "supervisor_feedback",
            "feedback",
            "submitted_to_supervisor_at",
            "submitted_at",
            "verified_at",
        ]


class PGLogbookEntryWriteSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if self.instance and not self.instance.can_be_edited():
            raise serializers.ValidationError(
                "Entry cannot be edited after submission/verification."
            )
        return super().validate(attrs)

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
