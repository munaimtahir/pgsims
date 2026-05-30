from django.core.management.base import BaseCommand
from sims.backup_center.services import create_full_backup

class Command(BaseCommand):
    help = 'Creates a full system backup (database and media)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--notes',
            type=str,
            help='Optional notes for the backup job',
        )

    def handle(self, *args, **options):
        notes = options.get('notes')
        self.stdout.write(self.style.NOTICE('Starting full system backup...'))
        
        try:
            job = create_full_backup(user=None, notes=notes)
            self.stdout.write(self.style.SUCCESS(f'Backup completed successfully. File: {job.file_name}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Backup failed: {str(e)}'))
