from __future__ import annotations

from rest_framework import serializers

from .models import SearchQueryLog


class SearchResultSerializer(serializers.Serializer):
    module = serializers.CharField()
    object_id = serializers.IntegerField()
    title = serializers.CharField()
    summary = serializers.CharField()
    url = serializers.CharField(allow_blank=True)
    score = serializers.FloatField()


class SearchQueryLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchQueryLog
        fields = ["id", "query", "filters", "result_count", "duration_ms", "created_at"]
        read_only_fields = fields
