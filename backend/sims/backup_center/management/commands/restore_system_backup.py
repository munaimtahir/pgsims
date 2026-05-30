from django.core.management.base import BaseCommand
from sims.backup_center.services import restore_routine_application_data_backup
from django.contrib.auth import get_user_model
import sys
import os

User = get_user_model()

class Command(BaseCommand):
    help = 'Restores a PGSIMS routine application data backup'

    def add_arguments(self, parser):
        parser.add_argument(
            'file_path',
            type=str,
            help='Path to the .pgsimsbak file to restore',
        )
        parser.add_argument(
            '--super-admin-email',
            type=str,
            required=True,
            help='Email of a superadmin authorizing this restore',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Validate and simulate restore without modifying data',
        )
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Bypass interactive prompt (requires --typed-confirmation)',
        )
        parser.add_argument(
            '--typed-confirmation',
            type=str,
            help='Must be "RESTORE"',
        )

    def handle(self, *args, **options):
        file_path = options['file_path']
        email = options['super_admin_email']
        dry_run = options['dry_run']
        
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"File not found: {file_path}"))
            sys.exit(1)

        try:
            user = User.objects.get(email=email, is_superuser=True)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Superadmin with email {email} not found.'))
            sys.exit(1)
            
        if dry_run:
            self.stdout.write(self.style.NOTICE('Running in DRY-RUN mode. No data will be changed.'))
        else:
            if options['confirm']:
                typed = options.get('typed_confirmation', '')
                if typed != 'RESTORE':
                    self.stdout.write(self.style.ERROR('Must provide --typed-confirmation RESTORE with --confirm'))
                    sys.exit(1)
            else:
                self.stdout.write(self.style.WARNING('!!! WARNING: RESTORE IS DESTRUCTIVE !!!'))
                self.stdout.write(self.style.WARNING('This will overwrite the current database and media files.'))
                self.stdout.write(self.style.WARNING(f'File: {file_path}'))
                typed = input('Type "RESTORE" to proceed: ')
                if typed != 'RESTORE':
                    self.stdout.write(self.style.ERROR('Aborted by user.'))
                    sys.exit(1)
                
        self.stdout.write(self.style.NOTICE('Starting restore process...'))
        
        try:
            job = restore_routine_application_data_backup(
                file_path=file_path,
                restored_by=user,
                password_confirmed=True, # CLI assumes confirmation if email is provided
                typed_confirmation="RESTORE",
                dry_run=dry_run
            )
            
            if job.status == 'restored':
                self.stdout.write(self.style.SUCCESS('Restore completed successfully!'))
                if job.safety_backup:
                    self.stdout.write(self.style.NOTICE(f"Safety backup created: {job.safety_backup.file_name}"))
            elif job.status == 'validation_passed' and dry_run:
                self.stdout.write(self.style.SUCCESS('Dry-run validation passed!'))
            else:
                self.stdout.write(self.style.ERROR(f"Restore failed with status: {job.status}"))
                if job.error_message:
                    self.stdout.write(self.style.ERROR(f"Error: {job.error_message}"))
                    
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Restore failed: {e}'))
            sys.exit(1)
