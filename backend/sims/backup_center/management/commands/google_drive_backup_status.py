from django.core.management.base import BaseCommand

from sims.backup_center.models import BackupCloudConnection


class Command(BaseCommand):
    help = "Show Google Drive backup connection status"

    def handle(self, *args, **options):
        connection = BackupCloudConnection.objects.filter(provider="google_drive").first()
        if not connection:
            self.stdout.write("google_drive: not_connected (no connection record)")
            return
        self.stdout.write(
            f"google_drive: status={connection.status} account={connection.account_email or '-'} "
            f"folder_id={connection.backup_folder_id or '-'} folder_name={connection.backup_folder_name or '-'} "
            f"token_expiry={connection.token_expiry or '-'} last_error={connection.last_error or '-'}"
        )

