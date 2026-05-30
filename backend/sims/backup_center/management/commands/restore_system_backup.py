from django.core.management.base import BaseCommand
from sims.backup_center.services import restore_full_backup
from sims.backup_center.models import RestoreJob
from django.contrib.auth import get_user_model
import sys

User = get_user_model()

class Command(BaseCommand):
    help = 'Restores a full system backup (database and media)'

    def add_arguments(self, parser):
        parser.add_argument(
            'file_path',
            type=str,
            help='Path to the backup zip file to restore',
        )
        parser.add_argument(
            '--super-admin-email',
            type=str,
            required=True,
            help='Email of a superadmin authorizing this restore',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Bypass interactive prompt (requires typed confirmation argument)',
        )
        parser.add_argument(
            '--typed-confirmation',
            type=str,
            help='Typed confirmation (must be "RESTORE") if using --force',
        )

    def handle(self, *args, **options):
        file_path = options['file_path']
        email = options['super_admin_email']
        
        try:
            user = User.objects.get(email=email, is_superuser=True)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Superadmin with email {email} not found.'))
            sys.exit(1)
            
        restore_job = RestoreJob.objects.create(
            status='running',
            file_path=file_path,
            started_by=user,
        )
            
        if options['force']:
            typed = options.get('typed_confirmation', '')
            if typed != 'RESTORE':
                self.stdout.write(self.style.ERROR('Must provide --typed-confirmation RESTORE when using --force'))
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
            # We assume password confirmed for CLI if they passed the prompt/force
            restore_full_backup(
                restore_job=restore_job,
                file_path=file_path,
                user=user,
                password_confirmed=True,
                typed_confirmation="RESTORE"
            )
            self.stdout.write(self.style.SUCCESS('Restore completed successfully!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Restore failed: {str(e)}'))
            sys.exit(1)
