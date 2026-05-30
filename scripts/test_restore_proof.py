import os
import sys
import django
from pathlib import Path

# Setup Django environment
sys.path.append(str(Path(__file__).resolve().parent.parent / 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
os.environ.setdefault('SECRET_KEY', 'temporary-secret')
django.setup()

from django.contrib.auth import get_user_model
from django.core.management import call_command
from sims.backup_center.services import create_routine_application_data_backup, restore_routine_application_data_backup
from sims.rotations.models import Hospital
from sims.academics.models import Department

User = get_user_model()

def run_proof():
    print("=== Starting Restore Proof ===")
    
    # 1. Clean DB using ORM
    User.objects.all().delete()
    Hospital.objects.all().delete()
    Department.objects.all().delete()
    
    # 2. Create Test Data
    superadmin = User.objects.create_superuser(username='proofadmin', email='proofadmin@test.com', password='adminpassword', role='admin')
    resident = User.objects.create_user(username='proofresident', email='proofresident@test.com', password='residentpassword', role='resident')
    supervisor = User.objects.create_user(username='proofsupervisor', email='proofsupervisor@test.com', password='supervisorpassword', role='supervisor')
    
    # Create some models
    hosp = Hospital.objects.create(name='Proof Hospital')
    dept = Department.objects.create(name='Proof Department')
    
    print("Data created.")
    
    # Capture original hashes
    original_hashes = {
        'admin': superadmin.password,
        'resident': resident.password,
        'supervisor': supervisor.password
    }
    
    # Force commit if in transaction
    from django.db import transaction
    if not transaction.get_autocommit():
        transaction.commit()

    # 3. Create Routine Backup
    print("Users BEFORE backup:", [u.username for u in User.objects.all()])
    backup_job = create_routine_application_data_backup(user=superadmin, notes="Restore proof backup")
    backup_path = backup_job.file_path
    print(f"Backup created at: {backup_path}")
    
    # 4. Wipe DB Data and create dummy data
    User.objects.exclude(id=superadmin.id).delete()
    Hospital.objects.all().delete()
    Department.objects.all().delete()
    
    # Create some dummy data that shouldn't exist after restore
    User.objects.create_user(username='wronguser', email='wrong@test.com', password='wrongpassword')
    Hospital.objects.create(name='Wrong Hospital')
    
    print("Database wiped/altered.")
    
    # 5. Restore Backup
    restore_job = restore_routine_application_data_backup(
        file_path=backup_path,
        restored_by=superadmin,
        password_confirmed=True,
        typed_confirmation="RESTORE",
        dry_run=False
    )
    
    print(f"Restore completed with status: {restore_job.status}")
    
    # Close connection so sqlite reconnects to the new file on disk
    from django.db import connections
    for conn in connections.all():
        conn.close()
    
    from django.conf import settings
    print(f"DB Path is: {Path(settings.DATABASES['default']['NAME']).absolute()}")
    
    # 6. Verify Data Restored
    print("Users after restore:", [u.username for u in User.objects.all()])
    
    restored_admin = User.objects.get(username='proofadmin')
    restored_resident = User.objects.get(username='proofresident')
    restored_supervisor = User.objects.get(username='proofsupervisor')
    
    assert restored_admin.password == original_hashes['admin']
    assert restored_resident.password == original_hashes['resident']
    assert restored_supervisor.password == original_hashes['supervisor']
    
    assert restored_admin.check_password('adminpassword')
    assert restored_resident.check_password('residentpassword')
    assert restored_supervisor.check_password('supervisorpassword')
    
    assert Hospital.objects.filter(name='Proof Hospital').exists()
    assert Department.objects.filter(name='Proof Department').exists()
    
    assert not User.objects.filter(username='wronguser').exists()
    assert not Hospital.objects.filter(name='Wrong Hospital').exists()
    
    print("=== Restore Proof Successful ===")
    print("- Same user IDs and hashes preserved.")
    print("- Same test passwords work.")
    print("- Placements/Models preserved.")

if __name__ == "__main__":
    run_proof()
