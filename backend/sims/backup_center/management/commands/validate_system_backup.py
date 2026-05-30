from django.core.management.base import BaseCommand
from sims.backup_center.services import validate_backup_file
import json

class Command(BaseCommand):
    help = 'Validates a PGSIMS backup file (.pgsimsbak or .pgsimsdr)'

    def add_arguments(self, parser):
        parser.add_argument(
            'file_path',
            type=str,
            help='Path to the backup file to validate',
        )

    def handle(self, *args, **options):
        file_path = options['file_path']
        self.stdout.write(self.style.NOTICE(f'Validating: {file_path}'))
        
        result = validate_backup_file(file_path)
        
        self.stdout.write(f"Kind: {result['backup_kind']}")
        
        if result['valid']:
            self.stdout.write(self.style.SUCCESS('STATUS: VALID'))
            if result['manifest']:
                self.stdout.write(self.style.NOTICE('--- Manifest Summary ---'))
                self.stdout.write(json.dumps(result['manifest'], indent=2))
            
            if result['table_counts']:
                self.stdout.write(self.style.NOTICE('--- Table Counts ---'))
                self.stdout.write(json.dumps(result['table_counts'], indent=2))
                
            if result['warnings']:
                for warn in result['warnings']:
                    self.stdout.write(self.style.WARNING(f'WARNING: {warn}'))
        else:
            self.stdout.write(self.style.ERROR('STATUS: INVALID'))
            for err in result['errors']:
                self.stdout.write(self.style.ERROR(f'ERROR: {err}'))
