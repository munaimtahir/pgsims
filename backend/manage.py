#!/usr/bin/env python
import os
import sys

def main():
    """Run administrative tasks."""
    default_settings = "sims_project.settings"
    if "test" in sys.argv and "DJANGO_SETTINGS_MODULE" not in os.environ:
        # Use test settings by default for `manage.py test` to avoid
        # manifest/staticfiles and other production-only settings issues.
        default_settings = "sims_project.settings_test"
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", default_settings)
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()
