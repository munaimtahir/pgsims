from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    Configuration for the SIMS Users app.

    This app manages user roles and authentication for the SIMS platform:
    - Admin: Full system access, user management, analytics
    - Supervisor: Manages assigned PGs, reviews documents
    - PG (Postgraduate): Uploads documents, views own progress

    Created: 2025-05-29
    Author: SMIB2012
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "sims.users"
    verbose_name = "SIMS Users & Roles"

    def ready(self):
        """
        Called when Django starts.
        Import any signal handlers or perform app initialization.
        """
        try:
            # Import signals if you have any (e.g., for notifications)
            # import sims.users.signals
            pass
        except ImportError:
            pass
