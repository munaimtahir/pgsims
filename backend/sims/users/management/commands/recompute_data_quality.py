"""
Management command: recompute_data_quality

Recomputes data quality flags for all users.

Usage:
    python manage.py recompute_data_quality
    python manage.py recompute_data_quality --user-id 42  # single user
"""

from django.core.management.base import BaseCommand

from sims.users.data_quality import recompute_all, recompute_flags_for_user
from sims.users.models import User


class Command(BaseCommand):
    help = "Recompute data quality flags for all users or a specific user"

    def add_arguments(self, parser):
        parser.add_argument(
            "--user-id",
            type=int,
            help="If provided, only recompute for the given User ID.",
        )

    def handle(self, *args, **options):
        user_id = options.get("user_id")

        if user_id:
            try:
                user = User.objects.get(id=user_id)
                self.stdout.write(f"Recomputing flags for user {user.id} ({user})...")
                result = recompute_flags_for_user(user)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✓ User {user.id}: "
                        f"is_complete_profile={result['is_complete_profile']}, "
                        f"issues={result['issues']}"
                    )
                )
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"✗ User with ID {user_id} not found"))
                return

        else:
            self.stdout.write("Recomputing data quality flags for all users...")
            stats = recompute_all()
            self.stdout.write(self.style.SUCCESS("✓ Recompute complete"))
            self.stdout.write(f"  Total users processed: {stats['total_users']}")
            self.stdout.write(f"  Complete profiles: {stats['complete_profiles']}")
            self.stdout.write(f"  Incomplete profiles: {stats['incomplete_profiles']}")
            self.stdout.write(f"  Users with placeholder email: {stats['users_with_placeholder_email']}")
            self.stdout.write(f"  Users with missing dates: {stats['users_with_missing_dates']}")
            self.stdout.write(f"  Records with default dates: {stats['records_with_default_dates']}")
