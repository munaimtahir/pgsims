from django.apps import AppConfig


class TrainingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "sims.training"
    verbose_name = "SIMS Training & Rotations"

    def ready(self):
        import sims.training.signals  # noqa: F401  – register signal handlers
