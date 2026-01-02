from django.apps import AppConfig
from django.db import OperationalError, ProgrammingError


class RotationsConfig(AppConfig):
    """
    Configuration for the SIMS Rotations app.

    This app manages rotation scheduling and tracking for the SIMS platform:
    - Rotation assignments and scheduling
    - Hospital and department management
    - Rotation evaluations and assessments
    - Progress tracking and completion certificates
    - Supervisor-PG rotation relationships

    Created: 2025-05-29 16:27:47 UTC
    Author: SMIB2012
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "sims.rotations"
    verbose_name = "SIMS Rotations & Training"

    def ready(self):
        """
        Called when Django starts.
        Import any signal handlers or perform app initialization.
        """
        try:
            # Import signals for rotation management
            pass

            # Register any custom model permissions
            from django.contrib.auth.models import Permission
            from django.contrib.contenttypes.models import ContentType

            from .models import Rotation, RotationEvaluation

            # Create custom permissions if they don't exist
            rotation_ct = ContentType.objects.get_for_model(Rotation)
            evaluation_ct = ContentType.objects.get_for_model(RotationEvaluation)

            custom_permissions = [
                ("can_approve_rotations", "Can approve rotations", rotation_ct),
                ("can_schedule_rotations", "Can schedule rotations for PGs", rotation_ct),
                ("can_view_all_rotations", "Can view all rotations", rotation_ct),
                ("can_evaluate_rotations", "Can evaluate rotations", evaluation_ct),
                ("can_view_evaluations", "Can view rotation evaluations", evaluation_ct),
            ]

            for codename, name, content_type in custom_permissions:
                Permission.objects.get_or_create(
                    codename=codename, name=name, content_type=content_type
                )

        except (OperationalError, ProgrammingError):
            # Database not ready (migrations not applied). Skip DB-dependent initialization.
            pass
        except ImportError:
            pass
        except Exception as e:
            # Log the error but don't prevent app from loading
            import logging

            logger = logging.getLogger("sims.rotations")
            logger.warning(f"Error in rotations app ready(): {e}")
