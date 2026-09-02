from django.core.management.base import BaseCommand
from sims.backup_center.services import create_routine_application_data_backup, create_disaster_recovery_backup

class Command(BaseCommand):
    help = 'Creates a PGSIMS system backup'

    def add_arguments(self, parser):
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument(
            '--routine',
            action='store_true',
            help='Create a routine application data backup (.pgsimsbak)',
        )
        group.add_argument(
            '--disaster',
            action='store_true',
            help='Create a full disaster recovery backup (.pgsimsdr)',
        )
        parser.add_argument(
            '--notes',
            type=str,
            help='Optional notes for the backup job',
        )

    def handle(self, *args, **options):
        notes = options.get('notes')
        
        if options['routine']:
            self.stdout.write(self.style.NOTICE('Starting routine application data backup...'))
            try:
                job = create_routine_application_data_backup(user=None, notes=notes)
                self.stdout.write(self.style.SUCCESS(f'Routine backup completed: {job.file_name}'))
                self.stdout.write(f"Path: {job.file_path}")
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Routine backup failed: {e}'))
        
        elif options['disaster']:
            self.stdout.write(self.style.NOTICE('Starting disaster recovery backup...'))
            try:
                job = create_disaster_recovery_backup(user=None, notes=notes)
                self.stdout.write(self.style.SUCCESS(f'Disaster backup completed: {job.file_name}'))
                self.stdout.write(f"Path: {job.file_path}")
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Disaster backup failed: {e}'))
