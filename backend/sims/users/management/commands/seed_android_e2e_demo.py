"""Seed a small, dedicated set of demo accounts for manual Android E2E testing.

Deliberately separate from `seed_demo_data` (that command's residents already have complete
profiles, for platform demos) and from any ad-hoc accounts created during live API verification
(`pgr001`/`pgr002`/`admin001`). The two residents here are created with a blank profile — no
hospital/department/program/supervisor pre-filled — so the Android onboarding wizard has real
required fields to walk through, matching the "resident has never used PGR SIMS" starting state.

Idempotent: safe to rerun. Existing accounts have their password reset to the documented value
rather than being recreated, so credentials stay predictable across reseeds.
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from sims.academics.models import Department
from sims.rotations.models import Hospital
from sims.training.models import TrainingProgram
from sims.users.models import SupervisorProfile, User
from sims.users.services import create_user_with_profile

DEMO_PASSWORD = "AndroidDemo123!"

ACCOUNTS = [
    {
        "username": "android.demo.admin",
        "role": "ADMIN",
        "full_name": "Android Demo Admin",
        "profile_payload": {"designation": "UTRMC Reviewer"},
    },
    {
        "username": "android.demo.supervisor",
        "role": "SUPERVISOR",
        "full_name": "Ayesha Malik",
        "profile_payload": {},
    },
    {
        "username": "android.demo.resident1",
        "role": "RESIDENT",
        "full_name": "Android Demo Resident One",
        "profile_payload": {},
    },
    {
        "username": "android.demo.resident2",
        "role": "RESIDENT",
        "full_name": "Android Demo Resident Two",
        "profile_payload": {},
    },
]


class Command(BaseCommand):
    help = "Seed/reset the fixed demo-account set used by the Android emulator E2E test plan."

    def handle(self, *args, **options):
        with transaction.atomic():
            for spec in ACCOUNTS:
                user = User.objects.filter(username=spec["username"]).first()
                if user:
                    user.set_password(DEMO_PASSWORD)
                    user.is_active = True
                    update_fields = ["password", "is_active"]
                    # Only force-clear the password-change gate for admin/supervisor (they need
                    # to act immediately in tests). Leave RESIDENT's must_change_password alone on
                    # reruns - forcing it True would make an already-onboarded demo resident redo
                    # the change-password screen every reseed; forcing it False would make it
                    # impossible to ever test that screen against a truly fresh resident.
                    if spec["role"] != "RESIDENT":
                        user.must_change_password = False
                        update_fields.append("must_change_password")
                    user.save(update_fields=update_fields)
                    self.stdout.write(f"  reset password: {spec['username']}")
                    continue

                create_user_with_profile(
                    role=spec["role"],
                    username=spec["username"],
                    password=DEMO_PASSWORD,
                    full_name=spec["full_name"],
                    profile_payload=spec["profile_payload"],
                    source="android_e2e_seed",
                )
                # These are dedicated, disposable demo accounts for a QA walkthrough,
                # not first-login admin-created identities - skip the forced
                # must_change_password/onboarding-wizard gate for the admin/supervisor
                # so they can act immediately; the two residents deliberately KEEP the
                # gate + blank profile so the onboarding wizard has something to do.
                if spec["role"] != "RESIDENT":
                    u = User.objects.get(username=spec["username"])
                    u.must_change_password = False
                    u.save(update_fields=["must_change_password"])
                self.stdout.write(self.style.SUCCESS(f"  created: {spec['username']}"))

        hospital = Hospital.objects.first()
        department = Department.objects.first()
        program = TrainingProgram.objects.first()
        supervisor_profile = SupervisorProfile.objects.filter(user__username="android.demo.supervisor").first()

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("Android E2E demo accounts ready:"))
        for spec in ACCOUNTS:
            self.stdout.write(f"  {spec['username']:28s} / {DEMO_PASSWORD}  ({spec['role']})")
        self.stdout.write("")
        self.stdout.write("Suggested onboarding answers for android.demo.resident1/resident2:")
        self.stdout.write(f"  Hospital:   {hospital.name if hospital else '<none seeded - pick any>'}")
        self.stdout.write(f"  Department: {department.name if department else '<none seeded - pick any>'}")
        self.stdout.write(f"  Program:    {program.name if program else '<none seeded - pick any>'}")
        self.stdout.write(
            f"  Supervisor (resident1, 'select existing'): search \"Malik\" or \"Ayesha\" -> "
            f"{'found' if supervisor_profile else 'NOT FOUND - rerun this command'}"
        )
        self.stdout.write(
            "  Supervisor (resident2, 'not listed'): use any made-up name, e.g. "
            '"Dr. Test Notlisted", to exercise the PendingSupervisorAssignment path.'
        )
