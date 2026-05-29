import json
import re
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.db import transaction

from sims.academics.models import Department
from sims.rotations.models import Hospital, HospitalDepartment
from sims.users.models import (
    ResidentProfile, StaffProfile, DepartmentMembership,
    HospitalAssignment, SupervisorResidentLink, HODAssignment
)
from sims.training.models import (
    ResidentTrainingRecord, RotationAssignment, LeaveRequest,
    DeputationPosting, LogbookEntry, LogbookReview,
    ResidentResearchProject, ResidentThesis, ResidentWorkshopCompletion,
    ResidentMilestoneEligibility, LogbookThresholdSnapshot,
    ResidentSubmission, SubmissionDocument, SubmissionReview,
    SubmissionCertificate, RotationCompletion, RotationCertificate
)
from sims.notifications.models import Notification, NotificationPreference
from sims.audit.models import ActivityLog, AuditReport
from sims.bulk.models import BulkOperation

User = get_user_model()

class Command(BaseCommand):
    help = "Idempotent safe reset command for clearing all pilot/demo test data before real data entry."

    def add_arguments(self, parser):
        parser.add_argument(
            "--confirm",
            action="store_true",
            help="Execute the actual database deletion. Without this, the command runs in dry-run mode.",
        )

    def handle(self, *args, **options):
        confirm = options.get("confirm", False)
        
        self.stdout.write(self.style.WARNING("=== PGSIMS Pilot Data Reset ==="))
        self.stdout.write(f"Mode: {'APPLY' if confirm else 'DRY-RUN (Pass --confirm to apply)'}")
        self.stdout.write("")

        # 1. Identify users to delete
        # Preserve superadmin/admin accounts, delete all test/demo/E2E accounts.
        # We preserve any superusers or users with username 'admin' or 'pilot_admin'.
        preserved_usernames = {"admin", "pilot_admin"}
        all_users = User.objects.all()
        users_to_delete = []
        users_to_keep = []

        for user in all_users:
            if user.is_superuser or user.username.lower() in preserved_usernames or user.role == "admin":
                users_to_keep.append(user)
            else:
                users_to_delete.append(user)

        # 2. Count records for deletion
        # All transactional rows are deleted
        deletions = {
            "ActivityLog": ActivityLog.objects.all(),
            "AuditReport": AuditReport.objects.all(),
            "BulkOperation": BulkOperation.objects.all(),
            "Notification": Notification.objects.all(),
            "NotificationPreference": NotificationPreference.objects.all(),
            "RotationCertificate": RotationCertificate.objects.all(),
            "RotationCompletion": RotationCompletion.objects.all(),
            "RotationAssignment": RotationAssignment.objects.all(),
            "LeaveRequest": LeaveRequest.objects.all(),
            "DeputationPosting": DeputationPosting.objects.all(),
            "LogbookReview": LogbookReview.objects.all(),
            "LogbookEntry": LogbookEntry.objects.all(),
            "LogbookThresholdSnapshot": LogbookThresholdSnapshot.objects.all(),
            "ResidentMilestoneEligibility": ResidentMilestoneEligibility.objects.all(),
            "ResidentWorkshopCompletion": ResidentWorkshopCompletion.objects.all(),
            "ResidentThesis": ResidentThesis.objects.all(),
            "ResidentResearchProject": ResidentResearchProject.objects.all(),
            "SubmissionCertificate": SubmissionCertificate.objects.all(),
            "SubmissionReview": SubmissionReview.objects.all(),
            "SubmissionDocument": SubmissionDocument.objects.all(),
            "ResidentSubmission": ResidentSubmission.objects.all(),
            "ResidentTrainingRecord": ResidentTrainingRecord.objects.all(),
            "SupervisorResidentLink": SupervisorResidentLink.objects.all(),
            "HODAssignment": HODAssignment.objects.all(),
            "HospitalAssignment": HospitalAssignment.objects.all(),
            "DepartmentMembership": DepartmentMembership.objects.all(),
            "StaffProfile": StaffProfile.objects.all(),
            "ResidentProfile": ResidentProfile.objects.all(),
            "User": User.objects.filter(id__in=[u.id for u in users_to_delete]),
        }

        # Print plan
        total_deletions = 0
        for label, queryset in deletions.items():
            count = queryset.count()
            total_deletions += count
            self.stdout.write(f"Plan to delete {count} records from {label}")

        self.stdout.write(f"Preserving {len(users_to_keep)} admin/superuser accounts:")
        for u in users_to_keep:
            self.stdout.write(f"  - {u.username} ({u.role})")

        self.stdout.write("")
        self.stdout.write(f"Total planned deletions: {total_deletions}")

        if not confirm:
            self.stdout.write(self.style.SUCCESS("Dry-run check completed. No database mutations occurred. Run with --confirm to apply changes."))
            return

        # Perform deletion inside a transaction
        with transaction.atomic():
            for label, queryset in deletions.items():
                count = queryset.count()
                if count > 0:
                    # Clear history tables if simple-history is installed and tracked on model
                    model_class = queryset.model
                    if hasattr(model_class, "history"):
                        model_class.history.all().delete()
                        self.stdout.write(f"  Cleared history for {label}")
                    
                    queryset.delete()
                    self.stdout.write(self.style.SUCCESS(f"  Deleted {count} records from {label}"))
            
        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("=== PGSIMS database reset completed successfully ==="))
