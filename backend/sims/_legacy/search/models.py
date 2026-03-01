from __future__ import annotations

from django.conf import settings
from django.db import models
from django.utils import timezone


class SearchQueryLog(models.Model):
    """Persist user search history for suggestions and audit."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="search_queries",
    )
    query = models.CharField(max_length=255)
    filters = models.JSONField(blank=True, default=dict)
    result_count = models.PositiveIntegerField(default=0)
    duration_ms = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["query"], name="search_query_idx"),
            models.Index(fields=["user", "created_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.user_id}:{self.query}"


class SavedSearchSuggestion(models.Model):
    """System curated or frequently used suggestions for typeahead."""

    label = models.CharField(max_length=255, unique=True)
    payload = models.JSONField(blank=True, default=dict)
    usage_count = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["label"]
        indexes = [models.Index(fields=["label"], name="search_suggestion_idx")]

    def __str__(self) -> str:
        return self.label
