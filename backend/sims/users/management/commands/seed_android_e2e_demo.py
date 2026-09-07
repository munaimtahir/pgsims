"""Seed a small, dedicated set of demo accounts for manual Android E2E testing.

Deliberately separate from `seed_demo_data` (that command's residents already have complete
profiles, for platform demos) and from any ad-hoc accounts created during live API verification
(`pgr001`/`pgr002`/`admin001`). The two residents here are created with a blank profile — no
hospital/department/program/supervisor pre-filled — so the Android onboarding wizard has real
required fields to walk through, matching the "resident has never used PGR SIMS" starting state.

Idempotent: safe to rerun. It is deliberately guarded to staging and obtains the
dedicated test password from the process environment, so test credentials never
become source code or command output.
"""

import os
from datetime import timedelta

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from sims.academics.models import Department
from sims.rotations.models import Hospital
from sims.supervision.models import ResidentSupervisorAssignment
from sims.supervision.services import create_supervisor_assignment
from sims.training.models import ResidentTrainingRecord, TrainingProgram
from sims.users.models import ResidentDocument, ResidentDocumentRequirement, SupervisorProfile, User
from sims.users.services import create_user_with_profile

PASSWORD_ENVIRONMENT_VARIABLE = "PGSIMS_STAGING_ANDROID_DEMO_PASSWORD"

ACCOUNTS = [
    {
        "username": "android.demo.admin",
        "role": "ADMIN",
        "full_name": "Android Demo Admin",
        "profile_payload": {"designation": "Institutional Reviewer"},
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
        environment = os.environ.get("PGSIMS_ENVIRONMENT", "").strip().lower()
        if environment != "staging":
            raise CommandError(
                "seed_android_e2e_demo refuses to run unless PGSIMS_ENVIRONMENT=staging."
            )
        demo_password = os.environ.get(PASSWORD_ENVIRONMENT_VARIABLE)
        if not demo_password or len(demo_password) < 12:
            raise CommandError(
                f"Set a 12+ character staging-only password in {PASSWORD_ENVIRONMENT_VARIABLE}."
            )

        with transaction.atomic():
            for spec in ACCOUNTS:
                user = User.objects.filter(username=spec["username"]).first()
                if user:
                    user.set_password(demo_password)
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
                    password=demo_password,
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

            ResidentDocumentRequirement.objects.get_or_create(
                document_type="CNIC",
                defaults={
                    "display_name": "CNIC Copy",
                    "stage": ResidentDocumentRequirement.STAGE_ONBOARDING,
                    "is_required": True,
                    "is_active": True,
                    "display_order": 1,
                },
            )
            ResidentDocumentRequirement.objects.get_or_create(
                document_type="PMDC_CERTIFICATE",
                defaults={
                    "display_name": "PMDC Registration Certificate",
                    "stage": ResidentDocumentRequirement.STAGE_ONBOARDING,
                    "is_required": True,
                    "is_active": True,
                    "display_order": 2,
                },
            )

        hospital = Hospital.objects.first()
        department = Department.objects.first()
        today = timezone.now().date()
        program, _ = TrainingProgram.objects.get_or_create(
            code="ANDROID-STAGING",
            defaults={
                "name": "Android Staging Residency Programme",
                "duration_months": 48,
                "degree_type": TrainingProgram.DEGREE_FCPS,
                "department": department,
                "description": "Staging-only programme for Android onboarding verification.",
                "active": True,
            },
        )
        supervisor_profile = SupervisorProfile.objects.filter(user__username="android.demo.supervisor").first()
        if supervisor_profile and (not supervisor_profile.hospital or not supervisor_profile.department_ref):
            supervisor_profile.hospital = hospital
            supervisor_profile.department_ref = department
            supervisor_profile.save(update_fields=["hospital", "department_ref", "updated_at"])

        admin_user = User.objects.get(username="android.demo.admin")
        resident_user = User.objects.get(username="android.demo.resident1")
        resident_profile = resident_user.resident_profile
        resident_profile.hospital = hospital
        resident_profile.department_ref = department
        resident_profile.program_ref = program
        resident_profile.save(update_fields=["hospital", "department_ref", "program_ref", "updated_at"])

        # Resident one is the assigned-supervisor/training fixture. It intentionally remains
        # incomplete (phone, email, session and specialty are blank) so the mobile profile
        # completion flow can still be tested against a real canonical record.
        resident_user.must_change_password = False
        resident_user.save(update_fields=["must_change_password"])
        ResidentTrainingRecord.objects.filter(resident_user=resident_user).exclude(program=program).update(active=False)
        ResidentTrainingRecord.objects.update_or_create(
            resident_user=resident_user,
            program=program,
            defaults={
                "start_date": today - timedelta(days=120),
                "expected_end_date": today + timedelta(days=365 * 3),
                "current_level": "y1",
                "status": ResidentTrainingRecord.STATUS_ACTIVE,
                "active": True,
                "has_default_dates": True,
                "training_site": hospital,
                "department": department,
                "created_by": admin_user,
            },
        )
        if supervisor_profile and not ResidentSupervisorAssignment.objects.filter(
            resident=resident_profile,
            assignment_type=ResidentSupervisorAssignment.ASSIGNMENT_PRIMARY,
            is_active=True,
        ).exists():
            create_supervisor_assignment(
                resident=resident_profile,
                supervisor=supervisor_profile,
                assignment_type=ResidentSupervisorAssignment.ASSIGNMENT_PRIMARY,
                start_date=today,
                actor=admin_user,
                notes="Staging-only Android E2E assignment.",
            )

        # Cover missing, approved and correction-required document states. The correction
        # requirement is intentionally file-less until the mobile resubmission test uploads it.
        training_letter, _ = ResidentDocumentRequirement.objects.get_or_create(
            document_type="TRAINING_LETTER",
            defaults={
                "display_name": "Training Letter",
                "stage": ResidentDocumentRequirement.STAGE_ONBOARDING,
                "is_required": True,
                "is_active": True,
                "display_order": 3,
            },
        )
        cnic = ResidentDocumentRequirement.objects.get(document_type="CNIC")
        pmdc = ResidentDocumentRequirement.objects.get(document_type="PMDC_CERTIFICATE")
        ResidentDocument.objects.update_or_create(
            resident=resident_profile,
            requirement=cnic,
            defaults={
                "document_type": cnic.document_type,
                "title": cnic.display_name,
                "status": ResidentDocument.STATUS_REUPLOAD_REQUIRED,
                "verification_remarks": "Staging review: upload a clear replacement copy.",
            },
        )
        ResidentDocument.objects.update_or_create(
            resident=resident_profile,
            requirement=pmdc,
            defaults={
                "document_type": pmdc.document_type,
                "title": pmdc.display_name,
                "status": ResidentDocument.STATUS_VERIFIED,
                "verification_remarks": "Staging review approved.",
            },
        )
        ResidentDocument.objects.get_or_create(
            resident=resident_profile,
            requirement=training_letter,
            defaults={"document_type": training_letter.document_type, "title": training_letter.display_name},
        )

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("Android E2E demo accounts ready:"))
        for spec in ACCOUNTS:
            self.stdout.write(f"  {spec['username']:28s}  ({spec['role']})")
        self.stdout.write(
            f"  Password source: environment variable {PASSWORD_ENVIRONMENT_VARIABLE} (not displayed)."
        )
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
