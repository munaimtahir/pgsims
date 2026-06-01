from django.core.management.base import BaseCommand, CommandError

from sims.backup_center.google_drive import GoogleDriveBackupProvider
from sims.backup_center.models import BackupCloudConnection


class Command(BaseCommand):
    help = "Run a Google Drive API health check using the stored connection"

    def handle(self, *args, **options):
        connection = BackupCloudConnection.objects.filter(provider="google_drive").first()
        if not connection or connection.status != "connected":
            raise CommandError("Google Drive is not connected")
        provider = GoogleDriveBackupProvider()
        result = provider.health_check(connection)
        self.stdout.write(str(result))

