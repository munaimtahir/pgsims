from django.core.management.base import BaseCommand
from sims.backup_center.services import validate_backup_file
import json

class Command(BaseCommand):
    help = 'Validates a given system backup file'

    def add_arguments(self, parser):
        parser.add_argument(
            'file_path',
            type=str,
            help='Path to the backup zip file to validate',
        )

    def handle(self, *args, **options):
        file_path = options['file_path']
        self.stdout.write(self.style.NOTICE(f'Validating backup file: {file_path}'))
        
        result = validate_backup_file(file_path)
        
        if result['valid']:
            self.stdout.write(self.style.SUCCESS('Validation passed! The backup is valid.'))
            if result['warnings']:
                self.stdout.write(self.style.WARNING(f'Warnings: {json.dumps(result["warnings"], indent=2)}'))
        else:
            self.stdout.write(self.style.ERROR('Validation failed!'))
            self.stdout.write(self.style.ERROR(f'Errors: {json.dumps(result["errors"], indent=2)}'))
