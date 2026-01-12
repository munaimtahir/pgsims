#!/usr/bin/env python
"""
Script to import trainee data while bypassing logging file permission issues.
"""
import os
import sys
import tempfile
import shutil
from pathlib import Path

# Setup Django environment
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

# Force SQLite database by unsetting DATABASE_URL and setting DB_ENGINE
# IMPORTANT: Remove DB_NAME as settings.py will force PostgreSQL if DB_NAME is set (line 541)
# Remove all DB-related env vars that might point to PostgreSQL
for key in list(os.environ.keys()):
    if key.startswith("DATABASE") or key.startswith("DB_"):
        os.environ.pop(key, None)
# Do NOT set DB_NAME - let Django use the default SQLite path from settings
os.environ["DB_ENGINE"] = "django.db.backends.sqlite3"

# Set required environment variables (usually from .env but we removed it)
if "SECRET_KEY" not in os.environ:
    os.environ["SECRET_KEY"] = "django-insecure-temp-key-for-import-only-change-in-production"
if "DEBUG" not in os.environ:
    os.environ["DEBUG"] = "True"

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sims_project.settings")

# Temporarily rename .env file to prevent it from loading PostgreSQL config
env_path = project_root / ".env"
env_backup_path = project_root / ".env.bak_import"
env_file_moved = False
if env_path.exists():
    env_path.rename(env_backup_path)
    env_file_moved = True

# Temporarily modify settings to use a writable log file location
settings_path = project_root / "sims_project" / "settings.py"
backup_path = settings_path.with_suffix('.py.bak')

# Create a temporary log file in /tmp
temp_log = tempfile.NamedTemporaryFile(mode='w', suffix='.log', delete=False)
temp_log_path = temp_log.name
temp_log.close()

try:
    # Backup original settings
    shutil.copy2(settings_path, backup_path)
    
    # Read settings
    with open(settings_path, 'r') as f:
        settings_content = f.read()
    
    # Replace log file path with temp file
    modified_content = settings_content.replace(
        'BASE_DIR / "logs" / "sims_error.log"',
        f'"{temp_log_path}"'
    )
    
    # Force SQLite by replacing DATABASE_URL line and if condition
    modified_content = modified_content.replace(
        'DATABASE_URL = os.environ.get("DATABASE_URL")',
        'DATABASE_URL = None  # Force SQLite'
    )
    modified_content = modified_content.replace(
        'if DATABASE_URL:',
        'if False:  # Force SQLite'
    )
    
    # Write modified settings
    with open(settings_path, 'w') as f:
        f.write(modified_content)
    
    # Now setup Django
    import django
    django.setup()
    
    # Override database settings to use SQLite after Django setup
    from django.conf import settings
    from django.db import connections
    settings.DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": str(project_root / "db.sqlite3"),
        }
    }
    # Close any existing connections and force reconnection with new settings
    connections.close_all()
    
finally:
    # Restore original settings
    if backup_path.exists():
        shutil.move(backup_path, settings_path)
    # Restore .env file
    if env_file_moved and env_backup_path.exists():
        env_backup_path.rename(env_path)

# Now import and run
from django.contrib.auth import get_user_model
from sims.bulk.services import BulkService

User = get_user_model()

def main():
    # Get file path from command line argument or use default
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = "/home/munaim/Downloads/Trainee_Data_Department_of_Urology.xlsx"
    
    if not os.path.exists(file_path):
        print(f"ERROR: File not found: {file_path}")
        print("\nPlease verify the file path. Searching for Excel files...")
        
        # Search more broadly
        search_paths = [
            "/home/munaim/Downloads",
            "/home/munaim/Desktop", 
            "/home/munaim/Documents",
            "/home/munaim",
            "/tmp",
            os.getcwd(),
        ]
        found_files = []
        for search_path in search_paths:
            if os.path.exists(search_path):
                try:
                    for root, dirs, files in os.walk(search_path, followlinks=False):
                        # Limit depth to avoid long searches
                        depth = root[len(search_path):].count(os.sep)
                        if depth > 2:
                            dirs[:] = []
                            continue
                        for file in files:
                            if file.endswith(('.xlsx', '.xls')):
                                full_path = os.path.join(root, file)
                                found_files.append(full_path)
                except PermissionError:
                    continue
            if len(found_files) > 20:  # Limit results
                break
        
        if found_files:
            print(f"\nFound {len(found_files)} Excel file(s):")
            for f in found_files[:10]:
                size = os.path.getsize(f) / 1024  # KB
                print(f"  - {f} ({size:.1f} KB)")
            if len(found_files) > 10:
                print(f"  ... and {len(found_files) - 10} more")
            print("\nIf your file is listed above, run:")
            print(f"  python run_import_now.py <correct_path>")
        else:
            print("\nNo Excel files found in common locations.")
            print("\nPlease provide the full path to your Excel file:")
            print("  python run_import_now.py /full/path/to/Trainee_Data_Department_of_Urology.xlsx")
        
        sys.exit(1)
    
    # Get or create admin user
    admin_username = 'import_admin'
    try:
        admin_user = User.objects.get(username=admin_username, role='admin')
    except User.DoesNotExist:
        admin_user = User.objects.filter(role='admin', is_active=True).first()
        if not admin_user:
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
            print(f'Created admin user: {admin_user.username}')
    
    # Open and import file
    print(f'\n{"="*60}')
    print(f'Importing trainees from: {file_path}')
    print(f'Allow partial: True')
    print(f'{"="*60}\n')
    
    try:
        with open(file_path, 'rb') as f:
            service = BulkService(admin_user)
            operation = service.import_trainees(
                f,
                dry_run=False,
                allow_partial=True
            )
            
            # Display results
            print(f'\n{"="*60}')
            print('IMPORT RESULTS')
            print(f'{"="*60}')
            print(f'Status: {operation.status}')
            print(f'Total items: {operation.total_items}')
            print(f'Success count: {operation.success_count}')
            print(f'Failure count: {operation.failure_count}')
            
            details = operation.details
            
            if details.get('created_supervisors'):
                print(f'\nCreated Supervisors ({len(details["created_supervisors"])}):')
                for sup in details['created_supervisors']:
                    print(f'  - {sup.get("name", "N/A")} ({sup.get("username", "N/A")})')
            
            if details.get('successes'):
                print(f'\nSuccessful Imports ({len(details["successes"])}):')
                for success in details['successes'][:10]:
                    print(
                        f'  Row {success.get("row", "N/A")}: '
                        f'{success.get("name", "N/A")} '
                        f'({success.get("username", "N/A")}) - '
                        f'Year {success.get("year", "N/A")}'
                    )
                if len(details['successes']) > 10:
                    print(f'  ... and {len(details["successes"]) - 10} more')
            
            if details.get('failures'):
                print(f'\nFailures ({len(details["failures"])}):')
                for failure in details['failures'][:10]:
                    error_msg = failure.get('error', 'Unknown error')
                    if isinstance(error_msg, dict):
                        error_msg = str(error_msg)
                    print(f'  Row {failure.get("row", "N/A")}: {error_msg}')
                if len(details['failures']) > 10:
                    print(f'  ... and {len(details["failures"]) - 10} more')
            
            print(f'\n{"="*60}\n')
            
            if operation.status == 'completed' and operation.failure_count == 0:
                print('✓ Import completed successfully!')
            elif operation.status == 'completed':
                print('⚠ Import completed with some errors')
            else:
                print('✗ Import failed')
                sys.exit(1)
                
    except FileNotFoundError:
        print(f'ERROR: File not found: {file_path}')
        sys.exit(1)
    except Exception as e:
        print(f'ERROR: {str(e)}')
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
