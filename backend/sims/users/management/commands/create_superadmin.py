"""
Create a superadmin user for local/testing access.

Usage:
  python manage.py create_superadmin
  python manage.py create_superadmin --reset-password   # reset password to admin123 if user exists

Default credentials: admin / admin123
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = "admin123"
DEFAULT_EMAIL = "admin@sims.com"


class Command(BaseCommand):
    help = "Create or ensure superadmin user (admin/admin123) for testing."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset-password",
            action="store_true",
            help="If admin user exists, reset password to admin123",
        )
        parser.add_argument(
            "--username",
            type=str,
            default=DEFAULT_USERNAME,
            help=f"Superadmin username (default: {DEFAULT_USERNAME})",
        )
        parser.add_argument(
            "--password",
            type=str,
            default=DEFAULT_PASSWORD,
            help="Superadmin password (default: admin123)",
        )

    def handle(self, *args, **options):
        username = options["username"]
        password = options["password"]
        reset_password = options["reset_password"]

        user = User.objects.filter(username=username).first()
        if user:
            if reset_password:
                user.set_password(password)
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Password reset for '{username}'. You can log in with {username} / {password}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Superadmin '{username}' already exists. Use --reset-password to set password to {password!r}."
                    )
                )
            return

        try:
            user = User.objects.create_superuser(
                username=username,
                email=DEFAULT_EMAIL,
                password=password,
                first_name="Admin",
                last_name="User",
                role="admin",
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"Superadmin created: {username} / {password}\n"
                    "You can log in at /admin/ or the app login page."
                )
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to create superadmin: {e}"))
