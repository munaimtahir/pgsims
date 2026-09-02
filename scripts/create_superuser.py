#!/usr/bin/env python
"""
Create the SIMS superuser (admin) with the custom User model fields.

The SIMS User model extends AbstractUser with:
  - role (required): admin | supervisor | pg
  - specialty, year, supervisor (required only for pg; admins leave them null)
  - registration_number, phone_number, created_by, modified_by, etc. (optional)

For a superuser we create an admin-role user with is_staff=True, is_superuser=True.
Run when you need a superuser for testing or first-time setup.

Usage (from project root):
  python scripts/create_superuser.py
  python scripts/create_superuser.py --reset-password

Or via Django:
  python manage.py shell < scripts/create_superuser.py
"""

import os
import sys
from pathlib import Path

if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(project_root))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sims_project.settings")

    import django
    django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Default superuser credentials (admin role; no specialty/year/supervisor per model rules)
USERNAME = "admin"
PASSWORD = "admin123"
EMAIL = "admin@sims.com"
FIRST_NAME = "Admin"
LAST_NAME = "User"
ROLE = "admin"


def create_superuser(reset_password=False):
    """Create or update the superuser with the exact User model fields."""
    user = User.objects.filter(username=USERNAME).first()
    if user:
        if reset_password:
            user.set_password(PASSWORD)
            user.save()
            print(f"Password reset for '{USERNAME}'. Log in with: {USERNAME} / {PASSWORD}")
        else:
            print(f"Superuser '{USERNAME}' already exists. Use --reset-password to set password to {PASSWORD!r}.")
        return

    # create_superuser sets is_staff=True, is_superuser=True; we pass role and names.
    # For role=admin, specialty/year/supervisor must be omitted (model clean() allows null for admin).
    user = User.objects.create_superuser(
        username=USERNAME,
        email=EMAIL,
        password=PASSWORD,
        first_name=FIRST_NAME,
        last_name=LAST_NAME,
        role=ROLE,
    )
    print(f"Superuser created: {USERNAME} / {PASSWORD}")
    print("Log in at /admin/ or the app login page.")


if __name__ == "__main__":
    reset = "--reset-password" in sys.argv
    create_superuser(reset_password=reset)
