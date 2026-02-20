#!/usr/bin/env python
"""
Django System Verification for SIMS
"""
import os
import sys
import traceback

def test_django_setup():
    """Test Django configuration and setup"""
    print("="*60)
    print("SIMS DJANGO SYSTEM VERIFICATION")
    print("="*60)
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
    
    try:
        import django
        print(f"✅ Django version: {django.get_version()}")
    except ImportError as e:
        print(f"❌ Django import failed: {e}")
        return False
    
    try:
        django.setup()
        print("✅ Django setup successful")
    except Exception as e:
        print(f"❌ Django setup failed: {e}")
        print(traceback.format_exc())
        return False
    
    return True

def test_models():
    """Test model imports and basic functionality"""
    print("\n" + "="*60)
    print("TESTING MODELS")
    print("="*60)
    
    try:
        from django.contrib.auth.models import User
        from sims.users.models import Profile
        print("✅ User and Profile models imported")
        
        # Test model counts
        user_count = User.objects.count()
        profile_count = Profile.objects.count()
        print(f"✅ Database accessible - Users: {user_count}, Profiles: {profile_count}")
        
        return True
    except Exception as e:
        print(f"❌ Model test failed: {e}")
        print(traceback.format_exc())
        return False

def test_views():
    """Test view imports"""
    print("\n" + "="*60)
    print("TESTING VIEWS")
    print("="*60)
    
    try:
        from sims.users.views import (
            AdminDashboardView, SupervisorDashboardView, PGDashboardView,
            UserListView, UserCreateView, SupervisorListView
        )
        print("✅ User dashboard views imported")
        
        from sims.logbook.views import LogbookAnalyticsView, LogbookDashboardView
        print("✅ Logbook views imported")
        
        from sims.certificates.views import CertificateDashboardView
        print("✅ Certificate views imported")
        
        from sims.rotations.views import RotationDashboardView
        print("✅ Rotation views imported")
        
        from sims.cases.views import CaseStatisticsView
        print("✅ Case views imported")
        
        return True
    except Exception as e:
        print(f"❌ Views test failed: {e}")
        print(traceback.format_exc())
        return False

def test_urls():
    """Test URL configuration"""
    print("\n" + "="*60)
    print("TESTING URL CONFIGURATION")
    print("="*60)
    
    try:
        from django.urls import reverse
        
        # Test main dashboard URLs
        urls_to_test = [
            'users:admin_dashboard',
            'users:supervisor_dashboard', 
            'users:pg_dashboard',
            'users:user_list',
            'users:user_create',
            'users:supervisor_list',
            'logbook:analytics',
            'logbook:dashboard',
            'certificates:dashboard',
            'rotations:dashboard',
        ]
        
        for url_name in urls_to_test:
            try:
                url = reverse(url_name)
                print(f"✅ {url_name}: {url}")
            except Exception as e:
                print(f"❌ {url_name}: {e}")
        
        return True
    except Exception as e:
        print(f"❌ URL test failed: {e}")
        print(traceback.format_exc())
        return False

def test_templates():
    """Test template existence"""
    print("\n" + "="*60)
    print("TESTING TEMPLATES")
    print("="*60)
    
    template_files = [
        'templates/users/admin_dashboard.html',
        'templates/users/supervisor_dashboard.html',
        'templates/users/pg_dashboard.html',
        'templates/users/user_list.html',
        'templates/users/user_create.html',
        'templates/users/supervisor_list.html',
        'templates/logbook/analytics.html',
        'templates/logbook/dashboard.html',
        'templates/certificates/dashboard.html',
        'templates/rotations/dashboard.html',
        'templates/registration/login.html',
        'templates/registration/password_reset_form.html',
        'templates/registration/password_reset_done.html',
        'templates/registration/password_reset_confirm.html',
        'templates/registration/password_reset_complete.html',
        'templates/registration/password_change_form.html',
        'templates/registration/password_change_done.html',
    ]
    
    template_count = 0
    for template_file in template_files:
        if os.path.exists(template_file):
            print(f"✅ {template_file}")
            template_count += 1
        else:
            print(f"❌ {template_file} (missing)")
    
    print(f"\n📊 Templates: {template_count}/{len(template_files)} found")
    return template_count == len(template_files)

def main():
    """Run all tests"""
    print(f"Working directory: {os.getcwd()}")
    print(f"Python version: {sys.version}")
    
    tests = [
        ("Django Setup", test_django_setup),
        ("Models", test_models),
        ("Views", test_views),
        ("URLs", test_urls),
        ("Templates", test_templates),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 ALL TESTS PASSED! SIMS system is ready.")
        return True
    else:
        print(f"\n⚠️  {len(results) - passed} tests failed. Please review the errors above.")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n💥 Test suite crashed: {e}")
        print(traceback.format_exc())
        sys.exit(1)
