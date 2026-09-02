import os
import tempfile

from django.core.files import File
from django.core.management.base import BaseCommand, CommandError

from sims.backup_center.google_drive import GoogleDriveBackupProvider
from sims.backup_center.models import BackupCloudCopy, RestoreJob


class Command(BaseCommand):
    help = "Download a Google Drive cloud copy, decrypt it locally, and store it as a RestoreJob upload"

    def add_arguments(self, parser):
        parser.add_argument("--cloud-copy-id", type=int, required=True)

    def handle(self, *args, **options):
        cloud_copy_id = options["cloud_copy_id"]
        try:
            cloud_copy = BackupCloudCopy.objects.get(pk=cloud_copy_id, provider="google_drive")
        except BackupCloudCopy.DoesNotExist as e:
            raise CommandError(f"BackupCloudCopy {cloud_copy_id} not found") from e

        if cloud_copy.verification_status != "verified":
            raise CommandError("Cloud copy is not verified; refusing to download for restore")

        provider = GoogleDriveBackupProvider()
        tmp_dir = tempfile.mkdtemp(prefix="pgsims-drive-restore-cmd-")
        file_name = cloud_copy.remote_file_name or f"backup-{cloud_copy.backup_record_id}.pgsimsbak"
        dest_path = os.path.join(tmp_dir, file_name.replace(".enc", ""))
        try:
            provider.download_backup(cloud_copy=cloud_copy, destination_path=dest_path)

            restore_job = RestoreJob.objects.create(
                uploaded_file_name=os.path.basename(dest_path),
                status="pending",
                restored_by=cloud_copy.connection.connected_by_user,
            )
            with open(dest_path, "rb") as f:
                restore_job.uploaded_file.save(os.path.basename(dest_path), File(f), save=True)

            cloud_copy.download_status = "restore_ready"
            cloud_copy.save(update_fields=["download_status", "updated_at"])

            self.stdout.write(f"restore_ready restore_job_id={restore_job.id} cloud_copy_id={cloud_copy.id}")
        finally:
            try:
                if os.path.exists(dest_path):
                    os.remove(dest_path)
                if os.path.exists(tmp_dir):
                    os.rmdir(tmp_dir)
            except Exception:
                pass

