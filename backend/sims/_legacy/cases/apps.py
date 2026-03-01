from django.apps import AppConfig


class CasesConfig(AppConfig):
    """Configuration for the cases app"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "sims.cases"
    verbose_name = "Clinical Cases"

    def ready(self):
        """Import signals when the app is ready"""
        try:
            pass
        except ImportError:
            pass
