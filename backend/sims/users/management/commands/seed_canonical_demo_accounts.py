"""Idempotently create/verify the four canonical demonstration login accounts.

Creates one ADMIN, one RESIDENT, one SUPERVISOR and one SUPPORT_STAFF login (usernames
``admin``, ``resident``, ``supervisor``, ``staff``) with an empty profile if they do not
already exist. Existing accounts and profiles are left untouched (get_or_create semantics)
so this is safe to re-run, including after `reconcile_urology_supervisor_profiles` has
re-pointed the resident/supervisor profiles onto real institutional identities.

Passwords are read from environment variables and are never hardcoded or logged:
ADMIN_DEMO_PASSWORD, RESIDENT_DEMO_PASSWORD, SUPERVISOR_DEMO_PASSWORD, STAFF_DEMO_PASSWORD.
If unset for an account being newly created, Command uses the platform default temporary
password (see `sims.users.services.create_user_with_profile`) and that account is left with
`must_change_password=True`.
"""
import os

from django.core.management.base import BaseCommand

from sims.users.services import create_user_with_profile
from sims.users.models import User, SupportStaffProfile
from sims.academics.models import Department

ACCOUNTS = [
    ("admin", "ADMIN", "ADMIN_DEMO_PASSWORD", "Demo Admin"),
    ("resident", "RESIDENT", "RESIDENT_DEMO_PASSWORD", "Demo Resident"),
    ("supervisor", "SUPERVISOR", "SUPERVISOR_DEMO_PASSWORD", "Demo Supervisor"),
    ("staff", "SUPPORT_STAFF", "STAFF_DEMO_PASSWORD", "Demo Support Staff"),
]

STAFF_DEMO_DEPARTMENT = "Urology Department"


class Command(BaseCommand):
    help = "Create the canonical admin/resident/supervisor/staff demo login accounts if missing."

    def handle(self, *args, **options):
        for username, role, password_env, full_name in ACCOUNTS:
            existing = User.objects.filter(username=username).first()
            if existing:
                self.stdout.write(self.style.SUCCESS(f"{username} already exists (role={existing.role})."))
                continue

            password = os.environ.get(password_env)
            user = create_user_with_profile(
                role=role,
                username=username,
                password=password,
                full_name=full_name,
                source="canonical_demo_seed",
            )
            # Canonical demo logins use fixed, known credentials meant for repeated live
            # demonstration use, not a real onboarding flow — skip the forced first-login
            # password change every other freshly-created account goes through.
            user.must_change_password = False
            user.save(update_fields=["must_change_password"])
            self.stdout.write(self.style.SUCCESS(f"Created canonical login '{username}' (role={role})."))

        self._ensure_staff_department_scope()

    def _ensure_staff_department_scope(self):
        staff_user = User.objects.filter(username="staff", role="SUPPORT_STAFF").first()
        if not staff_user:
            return
        profile = SupportStaffProfile.objects.filter(user=staff_user).first()
        if not profile or profile.department_ref_id:
            return
        department = Department.objects.filter(name=STAFF_DEMO_DEPARTMENT).first()
        if not department:
            self.stdout.write(self.style.WARNING(
                f"'{STAFF_DEMO_DEPARTMENT}' not found; leaving staff.department_ref unset."
            ))
            return
        profile.department_ref = department
        profile.designation = profile.designation or "Support Staff"
        profile.save(update_fields=["department_ref", "designation"])
        self.stdout.write(self.style.SUCCESS(f"Linked 'staff' to department '{department.name}'."))
