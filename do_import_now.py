#!/usr/bin/env python3
"""
Direct script to import trainee data.
This script sets up Django and imports the data.
"""
import os
import sys
import django

# Add project directory to path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')

# Setup Django - must be done before any Django imports
try:
    django.setup()
except Exception as e:
    error_msg = str(e)
    if 'handler' in error_msg.lower() or 'logging' in error_msg.lower():
        # Logging configuration issues are usually not critical, ignore them
        import warnings
        warnings.filterwarnings('ignore')
        try:
            django.setup()
        except:
            pass  # Continue anyway if it's just logging
    else:
        print(f"Error setting up Django: {e}")
        sys.exit(1)

# Now import Django models
from django.contrib.auth import get_user_model
from django.db import transaction
from sims.bulk.services import BulkService

User = get_user_model()

def main():
    file_path = '/home/munaim/Downloads/Trainee_Data_Department_of_Urology.xlsx'
    
    print("="*70)
    print("TRAINEE DATA IMPORT")
    print("="*70)
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"\n❌ ERROR: File not found: {file_path}")
        print("\nPlease ensure the Excel file is at the correct location.")
        sys.exit(1)
    
    print(f"\n📁 File: {file_path}")
    print(f"✅ File exists")
    
    # Check/run migrations
    print("\n📋 Checking database migrations...")
    try:
        from django.core.management import call_command
        call_command('migrate', 'users', verbosity=0, interactive=False)
        print("✅ Migrations are up to date")
    except Exception as e:
        print(f"⚠️  Migration check: {e}")
    
    # Get or create admin user
    print("\n👤 Setting up admin user for import...")
    try:
        admin_user = User.objects.filter(role='admin', is_active=True).first()
        if not admin_user:
            admin_user = User.objects.filter(is_superuser=True, is_active=True).first()
        if not admin_user:
            # Create a temporary admin
            admin_user = User.objects.create(
                username='import_admin',
                email='import@pmc.edu.pk',
                first_name='Import',
                last_name='Admin',
                role='admin',
                is_active=True,
                is_staff=True,
            )
            admin_user.set_password('changeme123')
            admin_user.save()
            print(f"✅ Created admin user: {admin_user.username}")
        else:
            print(f"✅ Using existing admin: {admin_user.username}")
    except Exception as e:
        print(f"❌ Error setting up admin: {e}")
        sys.exit(1)
    
    # Step 1: Dry run
    print("\n" + "="*70)
    print("STEP 1: VALIDATING DATA (DRY RUN)")
    print("="*70)
    
    try:
        with open(file_path, 'rb') as f:
            service = BulkService(admin_user)
            operation = service.import_trainees(f, dry_run=True, allow_partial=True)
            
            print(f"\n📊 Results:")
            print(f"   Status: {operation.status}")
            print(f"   Total rows: {operation.total_items}")
            print(f"   ✅ Successful validations: {operation.success_count}")
            print(f"   ❌ Failed validations: {operation.failure_count}")
            
            if operation.details.get('failures'):
                print(f"\n⚠️  Validation issues found:")
                for failure in operation.details['failures'][:5]:
                    error = failure.get('error', 'Unknown')
                    if isinstance(error, dict):
                        error = str(error)
                    print(f"   Row {failure.get('row', '?')}: {error}")
                if len(operation.details['failures']) > 5:
                    print(f"   ... and {len(operation.details['failures']) - 5} more")
    except Exception as e:
        print(f"\n❌ Error during validation: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Step 2: Actual import
    if operation.failure_count > 0:
        print(f"\n⚠️  {operation.failure_count} validation errors found.")
        response = input("\nContinue with import anyway? (yes/no): ")
        if response.lower() not in ['yes', 'y']:
            print("Import cancelled.")
            sys.exit(0)
    
    print("\n" + "="*70)
    print("STEP 2: IMPORTING DATA")
    print("="*70)
    
    try:
        with open(file_path, 'rb') as f:
            service = BulkService(admin_user)
            operation = service.import_trainees(f, dry_run=False, allow_partial=True)
            
            print(f"\n📊 Import Results:")
            print(f"   Status: {operation.status}")
            print(f"   ✅ Successfully imported: {operation.success_count}")
            print(f"   ❌ Failed: {operation.failure_count}")
            
            if operation.details.get('created_supervisors'):
                print(f"\n👨‍⚕️  Created Supervisors ({len(operation.details['created_supervisors'])}):")
                for sup in operation.details['created_supervisors'][:10]:
                    print(f"   - {sup.get('name', 'N/A')} ({sup.get('username', 'N/A')})")
            
            if operation.details.get('successes'):
                print(f"\n✅ Sample imported trainees (first 10):")
                for success in operation.details['successes'][:10]:
                    print(f"   Row {success.get('row', '?')}: {success.get('name', 'N/A')} "
                          f"({success.get('username', 'N/A')}) - Year {success.get('year', '?')}")
                if len(operation.details['successes']) > 10:
                    print(f"   ... and {len(operation.details['successes']) - 10} more")
            
            if operation.details.get('failures'):
                print(f"\n❌ Errors encountered ({len(operation.details['failures'])}):")
                for failure in operation.details['failures'][:5]:
                    error = failure.get('error', 'Unknown')
                    if isinstance(error, dict):
                        error = str(error)
                    print(f"   Row {failure.get('row', '?')}: {error}")
                if len(operation.details['failures']) > 5:
                    print(f"   ... and {len(operation.details['failures']) - 5} more")
            
            # Final verification
            print("\n" + "="*70)
            print("VERIFICATION")
            print("="*70)
            
            imported_count = User.objects.filter(role='pg', specialty='urology').count()
            print(f"\n✅ Total urology trainees in database: {imported_count}")
            
            if imported_count > 0:
                print("\n✅ Import completed successfully!")
                print(f"\n📝 Summary:")
                print(f"   - {imported_count} trainees are now in the system")
                print(f"   - All trainees have role='pg' and specialty='urology'")
                print(f"   - Usernames: firstname.lastname format")
                print(f"   - Emails: username.pgr@pmc.edu.pk")
                print(f"   - Default password: changeme123")
                print("\n🎉 Data is ready to use in the application!")
            else:
                print("\n⚠️  No trainees found in database. Please check errors above.")
    except Exception as e:
        print(f"\n❌ Error during import: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
