"""
Django management command to import trainee data from Excel file.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from sims.bulk.services import BulkService

User = get_user_model()


class Command(BaseCommand):
    help = 'Import trainee data from Excel file'

    def add_arguments(self, parser):
        parser.add_argument(
            'file_path',
            type=str,
            help='Path to the Excel file containing trainee data'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Validate data without creating records',
        )
        parser.add_argument(
            '--allow-partial',
            action='store_true',
            help='Continue importing even if some rows fail',
        )
        parser.add_argument(
            '--admin-username',
            type=str,
            default='import_admin',
            help='Username of admin user to perform import (default: import_admin)',
        )

    def handle(self, *args, **options):
        file_path = options['file_path']
        dry_run = options['dry_run']
        allow_partial = options['allow_partial']
        admin_username = options['admin_username']

        # Get or create admin user
        try:
            admin_user = User.objects.get(username=admin_username, role='admin')
        except User.DoesNotExist:
            # Try to get any admin user
            admin_user = User.objects.filter(role='admin', is_active=True).first()
            if not admin_user:
                # Create a temporary admin user
                admin_user = User.objects.create(
                    username=admin_username,
                    email=f'{admin_username}@pmc.edu.pk',
                    first_name='Import',
                    last_name='Admin',
                    role='admin',
                    is_active=True,
                    is_staff=True,
                )
                admin_user.set_password('changeme123')
                admin_user.save()
                self.stdout.write(
                    self.style.WARNING(f'Created admin user: {admin_user.username}')
                )

        # Open and import file
        try:
            with open(file_path, 'rb') as f:
                service = BulkService(admin_user)
                
                self.stdout.write(
                    self.style.SUCCESS(f'\n{'='*60}')
                )
                self.stdout.write(f'Importing trainees from: {file_path}')
                self.stdout.write(f'Dry run: {dry_run}')
                self.stdout.write(f'Allow partial: {allow_partial}')
                self.stdout.write(f'{"="*60}\n')
                
                operation = service.import_trainees(
                    f,
                    dry_run=dry_run,
                    allow_partial=allow_partial
                )
                
                # Display results
                self.stdout.write(f'\n{"="*60}')
                self.stdout.write(self.style.SUCCESS('IMPORT RESULTS'))
                self.stdout.write(f'{'='*60}')
                self.stdout.write(f'Status: {operation.status}')
                self.stdout.write(f'Total items: {operation.total_items}')
                self.stdout.write(
                    self.style.SUCCESS(f'Success count: {operation.success_count}')
                )
                if operation.failure_count > 0:
                    self.stdout.write(
                        self.style.ERROR(f'Failure count: {operation.failure_count}')
                    )
                else:
                    self.stdout.write(f'Failure count: {operation.failure_count}')
                
                details = operation.details
                
                if details.get('created_supervisors'):
                    self.stdout.write(
                        f'\nCreated Supervisors ({len(details["created_supervisors"])}):'
                    )
                    for sup in details['created_supervisors']:
                        self.stdout.write(
                            f'  - {sup.get("name", "N/A")} ({sup.get("username", "N/A")})'
                        )
                
                if details.get('successes'):
                    self.stdout.write(
                        f'\nSuccessful Imports ({len(details["successes"])}):'
                    )
                    # Show first 10
                    for success in details['successes'][:10]:
                        self.stdout.write(
                            f'  Row {success.get("row", "N/A")}: '
                            f'{success.get("name", "N/A")} '
                            f'({success.get("username", "N/A")}) - '
                            f'Year {success.get("year", "N/A")}'
                        )
                    if len(details['successes']) > 10:
                        self.stdout.write(
                            f'  ... and {len(details["successes"]) - 10} more'
                        )
                
                if details.get('failures'):
                    self.stdout.write(
                        self.style.ERROR(
                            f'\nFailures ({len(details["failures"])}):'
                        )
                    )
                    # Show first 10
                    for failure in details['failures'][:10]:
                        error_msg = failure.get('error', 'Unknown error')
                        if isinstance(error_msg, dict):
                            error_msg = str(error_msg)
                        self.stdout.write(
                            self.style.ERROR(
                                f'  Row {failure.get("row", "N/A")}: {error_msg}'
                            )
                        )
                    if len(details['failures']) > 10:
                        self.stdout.write(
                            f'  ... and {len(details["failures"]) - 10} more'
                        )
                
                self.stdout.write(f'\n{"="*60}\n')
                
                if operation.status == 'completed' and operation.failure_count == 0:
                    self.stdout.write(
                        self.style.SUCCESS('✓ Import completed successfully!')
                    )
                elif operation.status == 'completed':
                    self.stdout.write(
                        self.style.WARNING('⚠ Import completed with some errors')
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR('✗ Import failed')
                    )
                    
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'Error: File not found: {file_path}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error: {str(e)}')
            )
            raise
