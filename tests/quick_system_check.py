#!/usr/bin/env python
"""
Quick SIMS System Check - Focused on immediate issues
"""
import os
import sys

def main():
    print("="*60)
    print("QUICK SIMS SYSTEM CHECK")
    print("="*60)
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
    
    try:
        import django
        print(f"✅ Django version: {django.get_version()}")
        django.setup()
        print("✅ Django setup successful")
    except Exception as e:
        print(f"❌ Django setup failed: {e}")
        return False
    
    # Test database connection
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✅ Database connection successful")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
    
    # Test model imports
    print("\n📋 Testing Model Imports:")
    models_to_test = [
        ('sims.users.models', 'Profile'),
        ('sims.cases.models', 'ClinicalCase'),
        ('sims.cases.models', 'CaseCategory'),
        ('sims.logbook.models', 'LogbookEntry'),
        ('sims.certificates.models', 'Certificate'),
        ('sims.rotations.models', 'Rotation'),
    ]
    
    for module_name, model_name in models_to_test:
        try:
            module = __import__(module_name, fromlist=[model_name])
            model = getattr(module, model_name)
            count = model.objects.count()
            print(f"✅ {model_name}: {count} records")
        except Exception as e:
            print(f"❌ {model_name}: {e}")
    
    # Test URL resolution
    print("\n🔗 Testing URL Resolution:")
    from django.urls import reverse
    from django.core.exceptions import NoReverseMatch
    
    urls_to_test = [
        'users:admin_dashboard',
        'users:user_list',
        'cases:case_list',
        'logbook:dashboard',
        'certificates:dashboard',
        'rotations:dashboard',
    ]
    
    for url_name in urls_to_test:
        try:
            url = reverse(url_name)
            print(f"✅ {url_name}: {url}")
        except NoReverseMatch as e:
            print(f"❌ {url_name}: URL not found")
        except Exception as e:
            print(f"❌ {url_name}: {e}")
    
    # Check template existence
    print("\n📄 Testing Template Existence:")
    import os
    template_dirs = [
        'templates/base/base.html',
        'templates/home/index.html',
        'templates/users/admin_dashboard.html',
        'templates/cases/case_list.html',
        'templates/logbook/logbook_list.html',
        'templates/certificates/certificate_list.html',
        'templates/rotations/rotation_list.html',
    ]
    
    for template_path in template_dirs:
        full_path = os.path.join(os.getcwd(), template_path)
        if os.path.exists(full_path):
            print(f"✅ {template_path}")
        else:
            print(f"❌ {template_path} - NOT FOUND")
    
    print("\n" + "="*60)
    print("QUICK CHECK COMPLETE")
    print("="*60)

if __name__ == '__main__':
    main()
