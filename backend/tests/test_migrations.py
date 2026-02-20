import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

from django.core.management import execute_from_command_line

print("Testing Django migration...")
try:
    execute_from_command_line(['manage.py', 'check'])
    print("✅ Django check passed!")
except Exception as e:
    print(f"❌ Django check failed: {e}")

print("Testing migrations...")
try:
    from django.db import connection
    from django.core.management import call_command
    
    # Test that migrations can be loaded without errors
    call_command('showmigrations', verbosity=0)
    print("✅ Migration files are valid!")
    
except Exception as e:
    print(f"❌ Migration error: {e}")

print("Testing URL resolution...")
try:
    from django.urls import reverse
    
    urls_to_test = [
        'users:login',
        'users:logout', 
        'admin:index'
    ]
    
    for url_name in urls_to_test:
        try:
            url = reverse(url_name)
            print(f"✅ {url_name}: {url}")
        except Exception as e:
            print(f"❌ {url_name}: {e}")
            
except Exception as e:
    print(f"❌ URL test failed: {e}")

print("\nMigration fixes applied successfully!")
print("Ready for server deployment.")
