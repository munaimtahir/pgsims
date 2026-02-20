"""
Django management command to preview trainee data from Excel file.
This command analyzes the Excel file and generates lists of trainees and supervisors
without actually importing them into the database.
"""
import re
from datetime import date
from django.core.management.base import BaseCommand
from sims.bulk.services import _parse_trainee_rows, _parse_name, _parse_date, _infer_training_year


class Command(BaseCommand):
    help = 'Preview trainee data from Excel file (lists all trainees and supervisors)'

    def add_arguments(self, parser):
        parser.add_argument(
            'file_path',
            type=str,
            help='Path to the Excel file containing trainee data'
        )

    def handle(self, *args, **options):
        file_path = options['file_path']

        try:
            with open(file_path, 'rb') as f:
                # Parse rows from Excel file
                rows = list(_parse_trainee_rows(f))
                
                trainees = []
                supervisors_set = set()
                errors = []
                
                # Process each row
                for row in rows:
                    row_num = row.get("_row_number", "unknown")
                    name = row.get("name", "").strip()
                    date_joining = row.get("date_joining")
                    qualification = row.get("qualification", "").strip()
                    supervisor_name = row.get("supervisor_name", "").strip()
                    
                    # Validate required fields
                    if not name:
                        errors.append({
                            "row": row_num,
                            "error": "Missing 'Name of Trainee'"
                        })
                        continue
                    
                    # Parse name
                    try:
                        first_name, last_name = _parse_name(name)
                        if not first_name and not last_name:
                            errors.append({
                                "row": row_num,
                                "error": "Invalid name format",
                                "name": name
                            })
                            continue
                    except Exception as e:
                        errors.append({
                            "row": row_num,
                            "error": f"Error parsing name: {str(e)}",
                            "name": name
                        })
                        continue
                    
                    # Generate username (simplified version without DB check)
                    first_clean = re.sub(r"[^a-z0-9]", "", first_name.lower())
                    last_clean = re.sub(r"[^a-z0-9]", "", last_name.lower())
                    
                    if not first_clean and not last_clean:
                        base_username = "trainee"
                    elif not last_clean:
                        base_username = first_clean
                    elif not first_clean:
                        base_username = last_clean
                    else:
                        base_username = f"{first_clean}.{last_clean}"
                    
                    username = base_username
                    email = f"{username}.pgr@pmc.edu.pk"
                    
                    # Parse date and infer year
                    try:
                        date_joined = _parse_date(str(date_joining)) if date_joining else date.today()
                        year = _infer_training_year(date_joined)
                    except Exception as e:
                        date_joined = date.today()
                        year = "1"
                        errors.append({
                            "row": row_num,
                            "warning": f"Date parsing error, using today: {str(e)}"
                        })
                    
                    # Add supervisor to set
                    if supervisor_name:
                        supervisors_set.add(supervisor_name.strip())
                    
                    # Add trainee to list
                    trainees.append({
                        "row": row_num,
                        "full_name": name,
                        "first_name": first_name,
                        "last_name": last_name,
                        "username": username,
                        "email": email,
                        "date_joining": date_joined.strftime("%Y-%m-%d"),
                        "year": year,
                        "qualification": qualification,
                        "supervisor_name": supervisor_name,
                    })
                
                # Process supervisors to generate usernames
                supervisors_list = []
                for sup_name in sorted(supervisors_set):
                    if not sup_name:
                        continue
                    first_name, last_name = _parse_name(sup_name)
                    first_clean = re.sub(r"[^a-z0-9]", "", first_name.lower())
                    last_clean = re.sub(r"[^a-z0-9]", "", last_name.lower())
                    
                    if not first_clean and not last_clean:
                        base_username = "supervisor"
                    elif not last_clean:
                        base_username = first_clean
                    elif not first_clean:
                        base_username = last_clean
                    else:
                        base_username = f"{first_clean}.{last_clean}"
                    
                    username = base_username
                    email = f"{username}.supervisor@pmc.edu.pk"
                    
                    supervisors_list.append({
                        "full_name": sup_name,
                        "first_name": first_name,
                        "last_name": last_name,
                        "username": username,
                        "email": email,
                    })
                
                # Display results
                self.stdout.write(self.style.SUCCESS(f'\n{"="*80}'))
                self.stdout.write(self.style.SUCCESS('TRAINEE DATA PREVIEW'))
                self.stdout.write(self.style.SUCCESS(f'{"="*80}\n'))
                self.stdout.write(f'File: {file_path}')
                self.stdout.write(f'Total rows parsed: {len(rows)}')
                self.stdout.write(f'Valid trainees: {len(trainees)}')
                self.stdout.write(f'Unique supervisors: {len(supervisors_list)}')
                if errors:
                    self.stdout.write(self.style.WARNING(f'Warnings/Errors: {len(errors)}'))
                self.stdout.write(f'\n{"="*80}\n')
                
                # Display Supervisors
                self.stdout.write(self.style.SUCCESS('\nSUPERVISORS TO BE CREATED/USED:\n'))
                self.stdout.write(f'{"="*80}')
                self.stdout.write(f'{"#":<5} {"Full Name":<35} {"Username":<25} {"Email":<35}')
                self.stdout.write(f'{"-"*80}')
                for idx, sup in enumerate(supervisors_list, 1):
                    self.stdout.write(
                        f'{idx:<5} {sup["full_name"]:<35} {sup["username"]:<25} {sup["email"]:<35}'
                    )
                
                # Display Trainees
                self.stdout.write(self.style.SUCCESS('\n\nTRAINEES TO BE IMPORTED:\n'))
                self.stdout.write(f'{"="*80}')
                self.stdout.write(
                    f'{"#":<5} {"Full Name":<30} {"Username":<20} {"Email":<30} {"Year":<6} {"Supervisor":<25}'
                )
                self.stdout.write(f'{"-"*80}')
                for idx, trainee in enumerate(trainees, 1):
                    supervisor_display = trainee["supervisor_name"][:24] if trainee["supervisor_name"] else "N/A"
                    self.stdout.write(
                        f'{idx:<5} {trainee["full_name"]:<30} {trainee["username"]:<20} '
                        f'{trainee["email"]:<30} {trainee["year"]:<6} {supervisor_display:<25}'
                    )
                
                # Display errors/warnings if any
                if errors:
                    self.stdout.write(self.style.WARNING('\n\nWARNINGS/ERRORS:\n'))
                    self.stdout.write(f'{"="*80}')
                    for error in errors:
                        error_msg = error.get("error", "Unknown error")
                        row = error.get("row", "N/A")
                        self.stdout.write(self.style.WARNING(f'  Row {row}: {error_msg}'))
                
                self.stdout.write(f'\n{"="*80}\n')
                self.stdout.write(self.style.SUCCESS('Preview completed successfully!'))
                self.stdout.write(self.style.WARNING('\nNote: This is a preview only. No data has been imported.'))
                self.stdout.write('Run "python manage.py import_trainees <file> --dry-run" to validate the data.\n')
                
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'Error: File not found: {file_path}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error: {str(e)}')
            )
            import traceback
            traceback.print_exc()
            raise
