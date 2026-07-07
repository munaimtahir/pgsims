"""
Create a superadmin user for local/testing access.

Usage:
  python manage.py create_superadmin
  python manage.py create_superadmin --reset-password   # reset password to admin123 if user exists

Default credentials: admin / admin123
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from sims.users.models import AdminProfile

User = get_user_model()

DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = "admin123"
DEFAULT_EMAIL = "admin@fmu.edu.pk"


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
            changed_fields = []
            if user.role != "ADMIN":
                user.role = "ADMIN"
                changed_fields.append("role")
            if not user.is_staff:
                user.is_staff = True
                changed_fields.append("is_staff")
            if not user.is_superuser:
                user.is_superuser = True
                changed_fields.append("is_superuser")
            if not user.is_active:
                user.is_active = True
                changed_fields.append("is_active")
            if user.must_change_password:
                user.must_change_password = False
                changed_fields.append("must_change_password")
            if not user.email:
                user.email = DEFAULT_EMAIL
                changed_fields.append("email")
            if reset_password:
                user.set_password(password)
            user.save()
            AdminProfile.objects.get_or_create(
                user=user,
                defaults={
                    "designation": "Super Admin",
                    "email": user.email or DEFAULT_EMAIL,
                    "profile_status": "COMPLETE",
                    "completed_schema_version": 1,
                },
            )
            message = f"Superadmin ensured: {username}"
            if reset_password:
                message += f" / {password}"
            elif changed_fields:
                message += f" ({', '.join(changed_fields)} updated)"
            self.stdout.write(self.style.SUCCESS(message))
            return

        try:
            user = User.objects.create_superuser(
                username=username,
                email=DEFAULT_EMAIL,
                password=password,
                first_name="Admin",
                last_name="User",
                role="ADMIN",
            )
            user.must_change_password = False
            user.is_profile_complete = True
            user.is_complete_profile = True
            user.save()
            AdminProfile.objects.create(
                user=user,
                designation="Super Admin",
                email=user.email or DEFAULT_EMAIL,
                profile_status="COMPLETE",
                completed_schema_version=1,
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"Superadmin created: {username} / {password}\n"
                    "You can log in at /admin/ or the app login page."
                )
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to create superadmin: {e}"))
