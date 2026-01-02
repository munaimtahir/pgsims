#!/usr/bin/env python
"""
Final SIMS Deployment Verification Script
Verifies all fixes are working correctly for server deployment
"""

import os
import django
from pathlib import Path

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

def test_url_resolution():
    """Test that all URLs resolve correctly"""
    print("🔗 Testing URL Resolution...")
    from django.urls import reverse
    
    urls = [
        ('users:login', 'User Login'),
        ('users:logout', 'User Logout'),
        ('users:password_reset', 'Password Reset'),
        ('admin:index', 'Admin Panel'),
        ('home', 'Homepage')
    ]
    
    all_good = True
    for url_name, description in urls:
        try:
            url = reverse(url_name)
            print(f"   ✅ {description}: {url}")
        except Exception as e:
            print(f"   ❌ {description}: ERROR - {e}")
            all_good = False
    
    return all_good

def test_migration_loading():
    """Test that migrations load without errors"""
    print("\n📊 Testing Migration Files...")
    
    try:
        from django.core.management import call_command
        from io import StringIO
        
        # Capture output
        out = StringIO()
        call_command('showmigrations', stdout=out)
        
        print("   ✅ All migration files load successfully")
        return True
        
    except Exception as e:
        print(f"   ❌ Migration loading failed: {e}")
        return False

def test_static_files():
    """Test static files configuration"""
    print("\n📁 Testing Static Files Configuration...")
    
    from django.conf import settings
    
    checks = [
        ('STATIC_URL set', hasattr(settings, 'STATIC_URL') and settings.STATIC_URL),
        ('STATIC_ROOT set', hasattr(settings, 'STATIC_ROOT') and settings.STATIC_ROOT),
        ('static/ directory exists', Path('static').exists()),
        ('staticfiles/ directory exists', Path('staticfiles').exists())
    ]
    
    all_good = True
    for check_name, passed in checks:
        status = "✅" if passed else "❌"
        print(f"   {status} {check_name}")
        if not passed:
            all_good = False
    
    return all_good

def test_template_loading():
    """Test that key templates load correctly"""
    print("\n📄 Testing Template Loading...")
    
    from django.template.loader import get_template
    
    templates = [
        ('users/login.html', 'Login Template'),
        ('admin/base.html', 'Admin Base Template'),
        ('admin/login.html', 'Admin Login Template'),
        ('users/logged_out.html', 'Logout Template')
    ]
    
    all_good = True
    for template_name, description in templates:
        try:
            template = get_template(template_name)
            print(f"   ✅ {description}")
        except Exception as e:
            print(f"   ❌ {description}: {e}")
            all_good = False
    
    return all_good

def test_settings_configuration():
    """Test that settings are properly configured"""
    print("\n⚙️ Testing Settings Configuration...")
    
    from django.conf import settings
    
    checks = [
        ('SECRET_KEY configured', bool(settings.SECRET_KEY)),
        ('ALLOWED_HOSTS set', bool(settings.ALLOWED_HOSTS)),
        ('Database configured', bool(settings.DATABASES)),
        ('Apps installed', len(settings.INSTALLED_APPS) > 0),
        ('Middleware configured', len(settings.MIDDLEWARE) > 0)
    ]
    
    all_good = True
    for check_name, passed in checks:
        status = "✅" if passed else "❌"
        print(f"   {status} {check_name}")
        if not passed:
            all_good = False
    
    return all_good

def main():
    """Run all verification tests"""
    print("🚀 SIMS Deployment Verification")
    print("=" * 50)
    
    tests = [
        test_url_resolution,
        test_migration_loading,
        test_static_files,
        test_template_loading,
        test_settings_configuration
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"   ❌ Test failed with error: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📋 VERIFICATION RESULTS")
    
    if all(results):
        print("🎉 ALL TESTS PASSED!")
        print("\n✅ SIMS is ready for server deployment!")
        print("\n📝 Deployment Commands:")
        print("   1. python manage.py migrate")
        print("   2. python manage.py collectstatic --noinput")  
        print("   3. python manage.py createsuperuser")
        print("\n🌐 Access Points:")
        print("   - Homepage: http://your-server/")
        print("   - Login: http://your-server/users/login/")
        print("   - Admin: http://your-server/admin/")
        
    else:
        print("⚠️ Some tests failed. Please review the issues above.")
        print("Check the migration files and settings configuration.")
    
    print("\n📄 Documentation:")
    print("   - See SERVER_MIGRATION_FIX_REPORT.md for details")
    print("   - See AUTHENTICATION_SYSTEM_COMPLETION_REPORT.md for auth system")

if __name__ == '__main__':
    main()
