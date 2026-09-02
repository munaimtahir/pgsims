from __future__ import annotations

from django.dispatch import receiver
from simple_history.signals import post_create_historical_record

from .models import ActivityLog


@receiver(post_create_historical_record)
def mirror_history_to_activity(sender, instance, history_instance, **_: object) -> None:
    """Create an ActivityLog entry whenever a historical record is created."""

    history_type = getattr(history_instance, "history_type", "")
    action_map = {
        "+": "create",
        "~": "update",
        "-": "delete",
    }
    action = action_map.get(history_type)
    if not action:
        return

    history_date = getattr(history_instance, "history_date", None)
    if history_date is not None:
        history_date = history_date.isoformat()

    ActivityLog.log(
        actor=getattr(history_instance, "history_user", None),
        action=action,
        verb=f"{sender.__name__}:{history_instance.pk}",
        target=None,
        metadata={
            "history_id": getattr(history_instance, "history_id", None),
            "history_date": history_date,
            "object_repr": str(instance),
        },
        is_sensitive=False,
    )
