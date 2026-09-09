"""Repair the canonical demo-login accounts' identity linkage.

The Urology institutional bootstrap created real profiles (SupervisorProfile /
ResidentProfile, with hospital, department, ResidentSupervisorAssignment, and
ResidentTrainingRecord rows) under dedicated usernames such as `supmtahirbashirmalik` and
`pgrdrjawadsaifullah`, while the canonical demo-login accounts `supervisor` and `resident`
were left with their own separate, empty profiles. This command re-points the real
profile (and, for residents, the real ResidentTrainingRecord) onto the login account so it
authenticates as the real identity, instead of creating a duplicate user/profile. The
now-redundant real-identity login is deactivated (data preserved, never used to log in).

Idempotent: safe to re-run. On a second run it finds nothing left to repair.
"""
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from sims.audit.models import ActivityLog
from sims.users.models import SupervisorProfile, ResidentProfile
from sims.training.models import ResidentTrainingRecord

User = get_user_model()

# (canonical demo-login username, username holding the real identity/data, role)
RECONCILIATIONS = [
    ("supervisor", "supmtahirbashirmalik", "SUPERVISOR"),
    ("resident", "pgrdrjawadsaifullah", "RESIDENT"),
]

PROFILE_MODEL = {
    "SUPERVISOR": SupervisorProfile,
    "RESIDENT": ResidentProfile,
}


class Command(BaseCommand):
    help = (
        "Re-point real SupervisorProfile/ResidentProfile records (and, for residents, "
        "ResidentTrainingRecord) onto their canonical demo-login accounts without creating "
        "duplicate users, profiles, or assignments."
    )

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true", help="Report planned changes without writing them.")

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        users_reused = 0
        profiles_repointed = 0
        training_records_repointed = 0
        links_repaired = 0
        already_correct = 0

        for login_username, real_username, role in RECONCILIATIONS:
            ProfileModel = PROFILE_MODEL[role]
            login_user = User.objects.filter(username=login_username).first()
            real_user = User.objects.filter(username=real_username).first()

            if not login_user or not real_user:
                self.stdout.write(self.style.WARNING(
                    f"Skipping {login_username} <-> {real_username}: one or both users not found."
                ))
                continue

            real_profile = ProfileModel.objects.filter(user=real_user).first()
            login_profile = ProfileModel.objects.filter(user=login_user).first()

            if not real_profile:
                self.stdout.write(self.style.WARNING(
                    f"Skipping {login_username}: {real_username} has no {ProfileModel.__name__} to link."
                ))
                continue

            if login_profile and login_profile.pk == real_profile.pk:
                self.stdout.write(self.style.SUCCESS(f"{login_username} already linked to {real_username}'s profile."))
                already_correct += 1
                continue

            self.stdout.write(
                f"Plan: move {ProfileModel.__name__}#{real_profile.pk} ({real_user.get_full_name()}) "
                f"from user={real_user.username} -> user={login_user.username}; "
                f"rename {login_user.username}'s identity to match; "
                f"deactivate {real_user.username} (data preserved, login retired)."
            )

            if dry_run:
                continue

            with transaction.atomic():
                real_full_name = real_user.get_full_name()
                real_first, real_last = real_user.first_name, real_user.last_name
                real_email = real_user.email

                # Vacate the login account's own empty profile first (OneToOne can't collide).
                if login_profile:
                    ProfileModel.objects.filter(pk=login_profile.pk).update(user=real_user)
                    profiles_repointed += 1

                ProfileModel.objects.filter(pk=real_profile.pk).update(user=login_user)
                profiles_repointed += 1

                if role == "RESIDENT":
                    login_tr = ResidentTrainingRecord.objects.filter(resident_user=login_user).first()
                    real_tr = ResidentTrainingRecord.objects.filter(resident_user=real_user).first()
                    if login_tr:
                        ResidentTrainingRecord.objects.filter(pk=login_tr.pk).update(resident_user=real_user)
                        training_records_repointed += 1
                    if real_tr:
                        ResidentTrainingRecord.objects.filter(pk=real_tr.pk).update(resident_user=login_user)
                        training_records_repointed += 1

                login_user.first_name = real_first
                login_user.last_name = real_last
                if real_email:
                    login_user.email = real_email
                login_user.save(update_fields=["first_name", "last_name", "email"])
                users_reused += 1

                real_user.is_active = False
                real_user.save(update_fields=["is_active"])

                links_repaired += 1

                ActivityLog.objects.create(
                    actor=None,
                    action="update",
                    verb="reconcile_demo_identity",
                    target_repr=f"{login_user.username} -> {real_full_name}",
                    metadata={
                        "login_username": login_user.username,
                        "real_username": real_user.username,
                        "role": role,
                        "profile_id": real_profile.pk,
                        "vacated_profile_id": login_profile.pk if login_profile else None,
                        "command": "reconcile_urology_supervisor_profiles",
                    },
                    is_sensitive=True,
                )

        self.stdout.write(self.style.SUCCESS(
            f"users reused: {users_reused}, profiles repointed: {profiles_repointed}, "
            f"training records repointed: {training_records_repointed}, "
            f"links repaired: {links_repaired}, already correct: {already_correct}"
        ))
