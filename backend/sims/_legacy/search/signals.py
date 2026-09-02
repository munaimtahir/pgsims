from __future__ import annotations

from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import SavedSearchSuggestion, SearchQueryLog


@receiver(post_save, sender=SearchQueryLog)
def update_suggestions(sender, instance: SearchQueryLog, created: bool, **_: object) -> None:
    """Keep suggestion table warm with most used queries."""

    if not created or not instance.query:
        return

    suggestion, created = SavedSearchSuggestion.objects.get_or_create(label=instance.query)
    if created:
        return

    SavedSearchSuggestion.objects.filter(pk=suggestion.pk).update(
        usage_count=F("usage_count") + 1,
        updated_at=timezone.now(),
    )
