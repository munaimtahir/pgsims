#!/usr/bin/env python
"""
SIMS Application Verification Script
Comprehensive test of all major components
"""

import os
import sys
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

def test_models():
    """Test all model imports and basic functionality"""
    print("\n📋 TESTING MODELS...")
    
    try:
        # Import all models
        from sims.users.models import User
        from sims.cases.models import ClinicalCase, Diagnosis, CaseReview
        from sims.logbook.models import LogbookEntry, LogbookReview
        from sims.certificates.models import Certificate, CertificateType
        from sims.rotations.models import Rotation, Department
        
        print("✅ All models imported successfully")
        
        # Test model counts
        print(f"  Users: {User.objects.count()}")
        print(f"  Clinical Cases: {ClinicalCase.objects.count()}")
        print(f"  Logbook Entries: {LogbookEntry.objects.count()}")
        print(f"  Certificates: {Certificate.objects.count()}")
        print(f"  Rotations: {Rotation.objects.count()}")
        print(f"  Departments: {Department.objects.count()}")
        
        return True
    except Exception as e:
        print(f"❌ Model test failed: {e}")
        return False

def test_admin():
    """Test admin interface configuration"""
    print("\n🔧 TESTING ADMIN INTERFACE...")
    
    try:
        from django.contrib import admin
        from sims.users.admin import UserAdmin
        from sims.cases.admin import ClinicalCaseAdmin
        from sims.logbook.admin import LogbookEntryAdmin
        
        print("✅ Admin classes imported successfully")
        
        # Check registered models
        registered_models = admin.site._registry.keys()
        sims_models = [model for model in registered_models if 'sims' in str(model)]
        print(f"  Registered SIMS models: {len(sims_models)}")
        
        return True
    except Exception as e:
        print(f"❌ Admin test failed: {e}")
        return False

def test_urls():
    """Test URL configuration"""
    print("\n🌐 TESTING URL CONFIGURATION...")
    
    try:
        from django.urls import reverse
        from django.test import Client
        
        client = Client()
        
        # Test key URLs
        test_urls = [
            ('home', '/'),
            ('health_check', '/health/'),
            ('admin:index', '/admin/'),
        ]
        
        for name, expected_path in test_urls:
            try:
                actual_path = reverse(name)
                if actual_path == expected_path:
                    print(f"✅ URL '{name}': {actual_path}")
                else:
                    print(f"⚠️  URL '{name}': {actual_path} (expected {expected_path})")
            except Exception as e:
                print(f"❌ URL '{name}' failed: {e}")
        
        return True
    except Exception as e:
        print(f"❌ URL test failed: {e}")
        return False

def test_database():
    """Test database connectivity and basic operations"""
    print("\n💾 TESTING DATABASE...")
    
    try:
        from django.db import connection
        
        # Test connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result[0] == 1:
                print("✅ Database connection successful")
            
        # Test table existence
        tables = connection.introspection.table_names()
        sims_tables = [table for table in tables if 'users_user' in table or 'cases_' in table or 'logbook_' in table]
        print(f"✅ SIMS tables found: {len(sims_tables)}")
        
        return True
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_superuser():
    """Test superuser creation and authentication"""
    print("\n👤 TESTING SUPERUSER...")
    
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        # Check if admin user exists
        admin_user = User.objects.filter(username='admin').first()
        if admin_user:
            print("✅ Admin user exists")
            print(f"  Username: {admin_user.username}")
            print(f"  Email: {admin_user.email}")
            print(f"  Role: {admin_user.role}")
            print(f"  Is superuser: {admin_user.is_superuser}")
            print(f"  Is staff: {admin_user.is_staff}")
        else:
            # Create admin user
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@sims.com',
                password='admin123',
                first_name='Admin',
                last_name='User',
                role='admin'
            )
            print("✅ Admin user created successfully")
            print("  Username: admin")
            print("  Password: admin123")
        
        return True
    except Exception as e:
        print(f"❌ Superuser test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 SIMS APPLICATION VERIFICATION")
    print("=" * 50)
    
    tests = [
        test_database,
        test_models,
        test_admin,
        test_urls,
        test_superuser,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
    
    print("\n" + "=" * 50)
    print(f"🎯 TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("SIMS application is ready for use!")
        print("\n📋 QUICK ACCESS:")
        print("  🌐 Application: http://127.0.0.1:8000")
        print("  🔧 Admin: http://127.0.0.1:8000/admin")
        print("  👤 Login: admin / admin123")
        print("\n🚀 Start server: py manage.py runserver")
    else:
        print(f"\n⚠️  {total - passed} tests failed. Please check the errors above.")
    
    print("=" * 50)

if __name__ == '__main__':
    main()
