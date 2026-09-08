"""Prepare only the dedicated Android synthetic fixture for production E2E.

This command is intentionally more restrictive than normal seed commands. It can run only when
the deployment explicitly declares ``PGSIMS_ENVIRONMENT=production`` and it refuses to address any
account outside the fixed android.demo namespace. It creates no schema and no real-user records.
"""

import os
from datetime import timedelta

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from sims.rotations.models import HospitalDepartment
from sims.training.models import ResidentTrainingRecord, RotationAssignment
from sims.users.models import User


PASSWORD_ENVIRONMENT_VARIABLE = "PGSIMS_PRODUCTION_ANDROID_TEST_PASSWORD"
RESIDENT_USERNAME = "android.demo.resident1"
ADMIN_USERNAME = "android.demo.admin"


class Command(BaseCommand):
    help = "Prepare the fixed synthetic Android production E2E resident and rotation fixture."

    def handle(self, *args, **options):
        if os.environ.get("PGSIMS_ENVIRONMENT", "").strip().lower() != "production":
            raise CommandError("This fixture command refuses to run outside PGSIMS_ENVIRONMENT=production.")
        password = os.environ.get(PASSWORD_ENVIRONMENT_VARIABLE, "")
        if len(password) < 16:
            raise CommandError(f"Set a 16+ character password in {PASSWORD_ENVIRONMENT_VARIABLE}.")

        with transaction.atomic():
            resident = User.objects.filter(username=RESIDENT_USERNAME, role="RESIDENT").first()
            admin = User.objects.filter(username=ADMIN_USERNAME, role="ADMIN").first()
            if not resident or not admin:
                raise CommandError("Required android.demo synthetic accounts are missing; refusing to create substitutes.")
            record = ResidentTrainingRecord.objects.filter(resident_user=resident, active=True).first()
            if not record:
                raise CommandError("The synthetic resident has no active canonical training record.")

            hospital_department = HospitalDepartment.objects.filter(
                hospital=record.training_site, department=record.department
            ).first() or HospitalDepartment.objects.first()
            if not hospital_department:
                raise CommandError("No canonical hospital/department placement exists for a synthetic rotation.")

            resident.set_password(password)
            resident.must_change_password = False
            resident.is_active = True
            resident.save(update_fields=["password", "must_change_password", "is_active"])

            today = timezone.localdate()
            fixtures = (
                ("android-production-e2e-previous", today - timedelta(days=75), today - timedelta(days=15), RotationAssignment.STATUS_COMPLETED),
                ("android-production-e2e-current", today - timedelta(days=14), today + timedelta(days=14), RotationAssignment.STATUS_ACTIVE),
                ("android-production-e2e-upcoming", today + timedelta(days=15), today + timedelta(days=45), RotationAssignment.STATUS_APPROVED),
            )
            for marker, start_date, end_date, status in fixtures:
                RotationAssignment.objects.update_or_create(
                    resident_training=record,
                    notes=marker,
                    defaults={
                        "hospital_department": hospital_department,
                        "start_date": start_date,
                        "end_date": end_date,
                        "status": status,
                        "requested_by": admin,
                    },
                )

        self.stdout.write(self.style.SUCCESS("Synthetic Android production E2E fixture is ready."))
