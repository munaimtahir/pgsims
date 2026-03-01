from django.apps import AppConfig


class ReportsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "sims.reports"

    def ready(self) -> None:  # pragma: no cover - import side effects
        from sims.reports.utils import ensure_default_templates

        ensure_default_templates()
