from django.apps import AppConfig
from django.db import OperationalError, ProgrammingError


class RotationsConfig(AppConfig):
    """
    Configuration for the SIMS Rotations app.

    Created: 2025-05-29 16:27:47 UTC
    Author: SMIB2012
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "sims.rotations"
    verbose_name = "SIMS Rotations & Training"

    def ready(self):
        try:
            pass
        except (OperationalError, ProgrammingError):
            pass
        except ImportError:
            pass
