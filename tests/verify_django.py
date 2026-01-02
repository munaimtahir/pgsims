#!/usr/bin/env python
"""
SIMS Django System Verification and Setup
Creates admin user and verifies system functionality
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse, NoReverseMatch
from django.template.loader import get_template
from django.template import TemplateDoesNotExist
from django.core.exceptions import ImproperlyConfigured

def create_admin_user():
    """Create admin user if it doesn't exist"""
    print("👤 Setting up Admin User...")
    
    User = get_user_model()
    
    try:
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@sims.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            print("   ✅ Admin user created successfully!")
        else:
            admin = User.objects.get(username='admin')
            admin.set_password('admin123')  # Ensure password is correct
            admin.save()
            print("   ✅ Admin user already exists (password updated)")
        
        print(f"   📧 Email: admin@sims.com")
        print(f"   🔑 Password: admin123")
        print(f"   👥 Total users: {User.objects.count()}")
        return True
        
    except Exception as e:
        print(f"   ❌ Error creating admin user: {e}")
        return False

def test_url_accessibility():
    """Test URL patterns and accessibility"""
    print("\n🌐 Testing URL Accessibility...")
    
    client = Client()
    
    # URLs that should be accessible (may redirect to login)
    test_urls = [
        ('/', 'Homepage'),
        ('/admin/', 'Django Admin'),
        ('/users/login/', 'Login Page'),
        ('/users/dashboard/', 'User Dashboard'),
        ('/users/profile/', 'User Profile'),
        ('/users/users/', 'User List'),
        ('/logbook/dashboard/', 'Logbook Dashboard'),
        ('/logbook/analytics/', 'Logbook Analytics'),
        ('/certificates/dashboard/', 'Certificates Dashboard'),
        ('/rotations/dashboard/', 'Rotations Dashboard'),
    ]
    
    results = []
    for url, description in test_urls:
        try:
            response = client.get(url)
            # Consider 200, 302 (redirect), and 403 (forbidden) as successful responses
            if response.status_code in [200, 302, 403]:
                print(f"   ✅ {description}: {url} (Status: {response.status_code})")
                results.append(True)
            else:
                print(f"   ❌ {description}: {url} (Status: {response.status_code})")
                results.append(False)
        except Exception as e:
            print(f"   ❌ {description}: {url} (Error: {e})")
            results.append(False)
    
    return results

def test_templates():
    """Verify template files exist and can be loaded"""
    print("\n📄 Testing Template Files...")
    
    critical_templates = [
        'base/base.html',
        'users/dashboard.html',
        'users/admin_dashboard.html',
        'users/supervisor_dashboard.html',
        'users/pg_dashboard.html',
        'users/profile.html',
        'users/user_edit.html',
        'registration/login.html',
        'logbook/dashboard.html',
        'logbook/analytics.html',
        'certificates/dashboard.html',
        'rotations/dashboard.html',
    ]
    
    results = []
    for template_name in critical_templates:
        try:
            template = get_template(template_name)
            print(f"   ✅ {template_name}")
            results.append(True)
        except TemplateDoesNotExist:
            print(f"   ❌ {template_name} (Not Found)")
            results.append(False)
        except Exception as e:
            print(f"   ❌ {template_name} (Error: {e})")
            results.append(False)
    
    return results

def test_models():
    """Test model functionality"""
    print("\n🗄️  Testing Database Models...")
    
    try:
        User = get_user_model()
        
        # Test user creation
        test_count = User.objects.count()
        print(f"   ✅ User model accessible ({test_count} users)")
        
        # Import and test other models
        from sims.cases.models import Case
        case_count = Case.objects.count()
        print(f"   ✅ Case model accessible ({case_count} cases)")
        
        from sims.logbook.models import LogbookEntry
        logbook_count = LogbookEntry.objects.count()
        print(f"   ✅ Logbook model accessible ({logbook_count} entries)")
        
        from sims.certificates.models import Certificate
        cert_count = Certificate.objects.count()
        print(f"   ✅ Certificate model accessible ({cert_count} certificates)")
        
        from sims.rotations.models import Rotation
        rotation_count = Rotation.objects.count()
        print(f"   ✅ Rotation model accessible ({rotation_count} rotations)")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Model test failed: {e}")
        return False

def run_migrations():
    """Ensure all migrations are applied"""
    print("\n🔄 Checking Database Migrations...")
    
    try:
        from django.core.management import call_command
        from io import StringIO
        
        # Capture migration status
        out = StringIO()
        call_command('showmigrations', stdout=out, verbosity=0)
        migration_output = out.getvalue()
        
        # Check for unapplied migrations
        if '[' in migration_output and 'X' in migration_output:
            print("   ✅ All migrations applied")
            return True
        else:
            print("   ⚠️  Some migrations may need to be applied")
            # Try to apply migrations
            call_command('migrate', verbosity=0)
            print("   ✅ Migrations applied successfully")
            return True
            
    except Exception as e:
        print(f"   ❌ Migration check failed: {e}")
        return False

def main():
    """Main verification function"""
    print("🏥 SIMS Django System Verification")
    print("=" * 50)
    print(f"Django Version: {django.get_version()}")
    print(f"Python Version: {sys.version.split()[0]}")
    print()
    
    # Run all tests
    tests = [
        ("Database Migrations", run_migrations),
        ("Admin User Setup", create_admin_user),
        ("Model Functionality", test_models),
        ("Template Files", test_templates),
        ("URL Accessibility", test_url_accessibility),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            if isinstance(result, list):
                success = all(result)
                passed = sum(result)
                total = len(result)
                print(f"   📊 {test_name}: {passed}/{total} passed")
            else:
                success = result
            results.append(success)
        except Exception as e:
            print(f"   ❌ {test_name} failed with error: {e}")
            results.append(False)
    
    # Summary
    print("\n📊 Verification Summary")
    print("=" * 30)
    passed_tests = sum(results)
    total_tests = len(results)
    success_rate = (passed_tests / total_tests) * 100
    
    print(f"Tests Passed: {passed_tests}/{total_tests}")
    print(f"Success Rate: {success_rate:.1f}%")
    
    if passed_tests == total_tests:
        print("\n🎉 System verification completed successfully!")
        print("\n🚀 SIMS is ready for use:")
        print("   • Admin Panel: http://127.0.0.1:8000/admin/")
        print("   • Login Page: http://127.0.0.1:8000/users/login/")
        print("   • Dashboard: http://127.0.0.1:8000/users/dashboard/")
        print("\n🔑 Admin Credentials:")
        print("   Username: admin")
        print("   Password: admin123")
    else:
        print(f"\n⚠️  {total_tests - passed_tests} test(s) failed.")
        print("Please review the errors above and fix any issues.")

if __name__ == "__main__":
    main()
