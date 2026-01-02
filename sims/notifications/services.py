"""Notification service layer handling channel dispatch and triggers."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import timedelta
from typing import Iterable, Optional

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

from sims.logbook.models import LogbookEntry
from sims.notifications.models import Notification, NotificationPreference
from sims.rotations.models import Rotation
from sims.users.models import User

logger = logging.getLogger(__name__)


@dataclass
class NotificationResult:
    channel: str
    delivered: bool
    error: Optional[str] = None


class NotificationService:
    """Encapsulates the delivery logic for notifications."""

    def __init__(self, actor: Optional[User] = None):
        self.actor = actor

    def send(
        self,
        recipient: User,
        verb: str,
        title: str,
        template: str,
        context: Optional[dict] = None,
        channels: Optional[Iterable[str]] = None,
    ) -> Iterable[NotificationResult]:
        channels = channels or (Notification.CHANNEL_IN_APP, Notification.CHANNEL_EMAIL)
        context = {"recipient": recipient, **(context or {})}
        preference = NotificationPreference.for_user(recipient)
        results: list[NotificationResult] = []
        for channel in channels:
            if not preference.allows_channel(channel, timezone.now()):
                results.append(
                    NotificationResult(channel=channel, delivered=False, error="channel-disabled")
                )
                continue
            try:
                if channel == Notification.CHANNEL_IN_APP:
                    self._create_in_app(recipient, verb, title, template, context)
                elif channel == Notification.CHANNEL_EMAIL:
                    self._send_email(recipient, title, template, context)
                results.append(NotificationResult(channel=channel, delivered=True))
            except Exception as exc:  # pragma: no cover - defensive logging
                logger.exception("Notification delivery failed", exc_info=exc)
                results.append(NotificationResult(channel=channel, delivered=False, error=str(exc)))
        return results

    def _create_in_app(
        self, recipient: User, verb: str, title: str, template: str, context: dict
    ) -> None:
        body = render_to_string(f"notifications/{template}.txt", context)
        Notification.objects.create(
            recipient=recipient,
            actor=self.actor,
            verb=verb,
            title=title,
            body=body,
            channel=Notification.CHANNEL_IN_APP,
            metadata=self._serialise_metadata(context),
        )

    def _send_email(self, recipient: User, title: str, template: str, context: dict) -> None:
        subject = title
        text_body = render_to_string(f"notifications/{template}.txt", context)
        html_body = render_to_string(f"notifications/{template}.html", context)
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@example.com"),
            to=[recipient.email],
        )
        email.attach_alternative(html_body, "text/html")
        email.send(fail_silently=False)

    def _serialise_metadata(self, context: dict) -> dict:
        serialised: dict[str, object] = {}
        for key, value in context.items():
            if isinstance(value, (str, int, float, bool)) or value is None:
                serialised[key] = value
            elif hasattr(value, "pk"):
                serialised[f"{key}_id"] = getattr(value, "pk", None)
            elif hasattr(value, "isoformat"):
                serialised[key] = value.isoformat()
            else:
                serialised[key] = str(value)
        return serialised

    # Trigger helpers -------------------------------------------------

    def logbook_status_change(self, entry: LogbookEntry, previous_status: Optional[str]) -> None:
        if entry.status == previous_status:
            return
        context = {"entry": entry, "previous_status": previous_status}
        if entry.status == "pending" and entry.supervisor:
            self.send(
                recipient=entry.supervisor,
                verb="logbook-submitted",
                title=f"Logbook entry submitted by {entry.pg.get_full_name()}",
                template="emails/logbook_pending",
                context=context,
            )
        elif entry.status == "approved":
            self.send(
                recipient=entry.pg,
                verb="logbook-approved",
                title=f"Logbook entry '{entry.case_title}' approved",
                template="emails/logbook_approved",
                context=context,
            )

    def upcoming_rotation_deadlines(self, days: int = 3) -> int:
        today = timezone.now().date()
        threshold = today + timedelta(days=days)
        rotations = Rotation.objects.filter(
            status__in=["ongoing", "planned"],
            end_date__range=(today, threshold),
        ).select_related("pg", "supervisor")
        count = 0
        for rotation in rotations:
            context = {"rotation": rotation, "days": (rotation.end_date - today).days}
            self.send(
                recipient=rotation.pg,
                verb="rotation-ending",
                title=f"Rotation ending on {rotation.end_date:%d %b %Y}",
                template="emails/rotation_deadline",
                context=context,
                channels=(Notification.CHANNEL_IN_APP,),
            )
            if rotation.supervisor:
                self.send(
                    recipient=rotation.supervisor,
                    verb="rotation-ending",
                    title=f"Rotation for {rotation.pg.get_full_name()} ending soon",
                    template="emails/rotation_deadline",
                    context=context,
                    channels=(Notification.CHANNEL_IN_APP,),
                )
            count += 1
        return count


def ensure_preferences_exist(user: User) -> NotificationPreference:
    return NotificationPreference.for_user(user)


__all__ = ["NotificationService", "NotificationResult", "ensure_preferences_exist"]
