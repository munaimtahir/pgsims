"""Signal handlers for notifications."""

from __future__ import annotations

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from sims.logbook.models import LogbookEntry
from sims.notifications.services import NotificationService, ensure_preferences_exist
from sims.users.models import User


@receiver(pre_save, sender=LogbookEntry)
def store_previous_status(
    sender, instance: LogbookEntry, **kwargs
) -> None:  # pragma: no cover - simple signal
    if instance.pk:
        previous = sender.objects.filter(pk=instance.pk).values_list("status", flat=True).first()
        instance._previous_status = previous
    else:
        instance._previous_status = None


@receiver(post_save, sender=LogbookEntry)
def emit_logbook_notifications(sender, instance: LogbookEntry, created: bool, **kwargs) -> None:
    previous_status = getattr(instance, "_previous_status", None)
    service = NotificationService(actor=instance.supervisor or instance.pg)
    service.logbook_status_change(instance, previous_status)


@receiver(post_save, sender=User)
def ensure_user_preferences(sender, instance: User, created: bool, **kwargs) -> None:
    if created:
        ensure_preferences_exist(instance)
