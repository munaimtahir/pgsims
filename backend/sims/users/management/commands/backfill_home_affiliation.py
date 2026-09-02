"""
Management command: backfill_home_affiliation

Reconciles User.home_hospital/home_department with the role-profile-level
hospital/department_ref fields (ResidentProfile, SupervisorProfile,
SupportStaffProfile) for users created before the write-path fix that keeps
them in sync (see sims/bulk/userbase_engine.py::_upsert_staff_user and
sims/users/services.py::create_user_with_profile).

Idempotent - safe to re-run. Only fills in User.home_hospital/home_department
when they're null and the corresponding profile field is set; never
overwrites an existing User.home_* value.

Usage:
    python manage.py backfill_home_affiliation
    python manage.py backfill_home_affiliation --dry-run
"""

from django.core.management.base import BaseCommand

from sims.users.models import ResidentProfile, SupervisorProfile, SupportStaffProfile, User


class Command(BaseCommand):
    help = "Backfill User.home_hospital/home_department from role-profile fields for pre-fix accounts."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Report what would change without saving.",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        updated = 0

        profile_querysets = [
            ("ResidentProfile", ResidentProfile.objects.select_related("user", "hospital", "department_ref")),
            ("SupervisorProfile", SupervisorProfile.objects.select_related("user", "hospital", "department_ref")),
            ("SupportStaffProfile", SupportStaffProfile.objects.select_related("user", "hospital", "department_ref")),
        ]

        for label, queryset in profile_querysets:
            for profile in queryset:
                user = profile.user
                needs_hospital = profile.hospital and not user.home_hospital
                needs_department = profile.department_ref and not user.home_department

                if not (needs_hospital or needs_department):
                    continue

                fields_to_update = []
                if needs_hospital:
                    user.home_hospital = profile.hospital
                    fields_to_update.append("home_hospital")
                if needs_department:
                    user.home_department = profile.department_ref
                    fields_to_update.append("home_department")

                self.stdout.write(
                    f"{'[dry-run] ' if dry_run else ''}{label} {user.username}: "
                    f"setting {', '.join(fields_to_update)}"
                )
                if not dry_run:
                    user.save(update_fields=fields_to_update)
                updated += 1

        verb = "Would update" if dry_run else "Updated"
        self.stdout.write(self.style.SUCCESS(f"{verb} {updated} user(s)."))
