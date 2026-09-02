from django.apps import AppConfig


class SearchConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "sims.search"
    verbose_name = "Global Search"

    def ready(self):
        # Import signals so search history cleanup and activity logging are registered.
        from . import signals  # noqa: F401
