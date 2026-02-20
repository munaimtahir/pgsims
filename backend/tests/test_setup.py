#!/usr/bin/env python
import os
import sys

# Add the project directory to Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')

try:
    import django
    print(f"✓ Django imported successfully. Version: {django.get_version()}")
    
    django.setup()
    print("✓ Django setup completed")
    
    # Test database connection
    from django.db import connection
    cursor = connection.cursor()
    print("✓ Database connection successful")
    
    # Test user model
    from django.contrib.auth import get_user_model
    User = get_user_model()
    print(f"✓ User model loaded: {User}")
    
    # Create superuser if needed
    if not User.objects.filter(username='admin').exists():
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@sims.com',
            password='admin123',
            first_name='Admin',
            last_name='User',
            role='admin'
        )
        print("✓ Superuser 'admin' created successfully!")
        print("  Username: admin")
        print("  Password: admin123")
    else:
        print("✓ Superuser 'admin' already exists")
    
    # Test all apps
    from django.apps import apps
    installed_apps = apps.get_app_configs()
    sims_apps = [app for app in installed_apps if app.name.startswith('sims.')]
    print(f"✓ SIMS apps loaded: {[app.name for app in sims_apps]}")
    
    # Test models
    from sims.cases.models import ClinicalCase
    from sims.logbook.models import LogbookEntry
    from sims.certificates.models import Certificate
    from sims.rotations.models import Rotation
    print("✓ All models imported successfully")
    
    print("\n" + "="*50)
    print("🎉 DJANGO SETUP COMPLETE!")
    print("="*50)
    print("To start the server, run:")
    print("  py manage.py runserver")
    print("\nAdmin login:")
    print("  Username: admin")
    print("  Password: admin123")
    print("  URL: http://127.0.0.1:8000/admin")
    print("="*50)
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
