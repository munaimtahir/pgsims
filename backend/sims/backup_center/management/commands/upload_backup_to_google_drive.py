from django.core.management.base import BaseCommand, CommandError

from sims.backup_center.google_drive import GoogleDriveBackupProvider
from sims.backup_center.models import BackupJob


class Command(BaseCommand):
    help = "Upload a BackupJob to Google Drive (encrypted) and record a BackupCloudCopy"

    def add_arguments(self, parser):
        parser.add_argument("--backup-id", type=int, required=True)

    def handle(self, *args, **options):
        backup_id = options["backup_id"]
        try:
            backup_job = BackupJob.objects.get(pk=backup_id)
        except BackupJob.DoesNotExist as e:
            raise CommandError(f"BackupJob {backup_id} not found") from e

        provider = GoogleDriveBackupProvider()
        cloud_copy = provider.upload_backup(backup_record=backup_job)
        self.stdout.write(f"uploaded cloud_copy_id={cloud_copy.id} remote_file_id={cloud_copy.remote_file_id}")

