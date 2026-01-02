from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "sims.notifications"

    def ready(self) -> None:  # pragma: no cover - import side effects
        from sims.notifications import signals  # noqa: F401
