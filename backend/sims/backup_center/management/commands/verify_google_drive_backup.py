from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from sims.backup_center.google_drive import GoogleDriveBackupProvider
from sims.backup_center.models import BackupCloudCopy, BackupJob


class Command(BaseCommand):
    help = "Verify the latest Google Drive cloud copy for a given BackupJob"

    def add_arguments(self, parser):
        parser.add_argument("--backup-id", type=int, required=True)

    def handle(self, *args, **options):
        backup_id = options["backup_id"]
        try:
            backup_job = BackupJob.objects.get(pk=backup_id)
        except BackupJob.DoesNotExist as e:
            raise CommandError(f"BackupJob {backup_id} not found") from e

        cloud_copy = (
            BackupCloudCopy.objects.filter(backup_record=backup_job, provider="google_drive")
            .exclude(remote_file_id__isnull=True)
            .order_by("-created_at")
            .first()
        )
        if not cloud_copy:
            raise CommandError("No Google Drive cloud copy found for this backup")

        provider = GoogleDriveBackupProvider()
        provider.verify_uploaded_file(
            connection=cloud_copy.connection,
            drive_file_id=cloud_copy.remote_file_id,
            expected_size=cloud_copy.remote_size,
            expected_md5=cloud_copy.remote_checksum,
        )
        cloud_copy.verification_status = "verified"
        cloud_copy.verified_at = timezone.now()
        cloud_copy.save(update_fields=["verification_status", "verified_at", "updated_at"])
        self.stdout.write(f"verified cloud_copy_id={cloud_copy.id}")

