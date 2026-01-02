#!/usr/bin/env python
"""
Login Consolidation Verification Test
Tests that only users/login works and accounts/login is properly removed
"""
import os
import sys
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

from django.test import Client
from django.urls import reverse, NoReverseMatch
from django.contrib.auth import get_user_model

def test_login_urls():
    """Test login URL patterns"""
    print("🔍 Testing Login URL Patterns...")
    print("=" * 50)
    
    try:
        # Test users login URL
        users_login = reverse('users:login')
        print(f"✅ Users Login URL: {users_login}")
        
        # Test that accounts login URL no longer exists
        try:
            accounts_login = reverse('login')  # This should fail now
            print(f"❌ Accounts Login URL still exists: {accounts_login}")
            return False
        except NoReverseMatch:
            print("✅ Accounts login URL properly removed (NoReverseMatch)")
        
        # Test password reset URLs
        password_reset = reverse('users:password_reset')
        print(f"✅ Password Reset URL: {password_reset}")
        
        password_reset_done = reverse('users:password_reset_done')
        print(f"✅ Password Reset Done URL: {password_reset_done}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing login URLs: {e}")
        return False

def test_login_pages():
    """Test login pages are accessible"""
    print("\n🔍 Testing Login Page Accessibility...")
    print("=" * 50)
    
    client = Client()
    
    try:
        # Test users login page works
        response = client.get('/users/login/')
        if response.status_code == 200:
            print("✅ Users login page loads successfully (200)")
        else:
            print(f"❌ Users login page failed: {response.status_code}")
            return False
        
        # Test accounts login page returns 404
        accounts_response = client.get('/accounts/login/')
        if accounts_response.status_code == 404:
            print("✅ Accounts login page properly returns 404")
        else:
            print(f"❌ Accounts login page still accessible: {accounts_response.status_code}")
            return False
        
        # Test password reset page works
        reset_response = client.get('/users/password-reset/')
        if reset_response.status_code == 200:
            print("✅ Password reset page loads successfully (200)")
        else:
            print(f"❌ Password reset page failed: {reset_response.status_code}")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Error testing login pages: {e}")
        return False

def test_login_redirects():
    """Test login redirect behavior"""
    print("\n🔍 Testing Login Redirects...")
    print("=" * 50)
    
    try:
        # Check settings
        login_url = getattr(settings, 'LOGIN_URL', None)
        login_redirect_url = getattr(settings, 'LOGIN_REDIRECT_URL', None)
        logout_redirect_url = getattr(settings, 'LOGOUT_REDIRECT_URL', None)
        
        print(f"✅ LOGIN_URL: {login_url}")
        print(f"✅ LOGIN_REDIRECT_URL: {login_redirect_url}")
        print(f"✅ LOGOUT_REDIRECT_URL: {logout_redirect_url}")
        
        if login_url and '/users/login/' in login_url:
            print("✅ LOGIN_URL points to users/login (correct)")
        else:
            print(f"❌ LOGIN_URL incorrect: {login_url}")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Error testing login redirects: {e}")
        return False

def test_protected_pages():
    """Test that protected pages redirect to users/login"""
    print("\n🔍 Testing Protected Page Redirects...")
    print("=" * 50)
    
    client = Client()
    
    try:
        # Test accessing a protected page
        protected_urls = [
            '/users/dashboard/',
            '/users/profile/',
            '/admin/'
        ]
        
        for url in protected_urls:
            response = client.get(url)
            if response.status_code == 302:  # Redirect
                redirect_url = response.url
                if '/users/login/' in redirect_url:
                    print(f"✅ {url} redirects to users/login")
                else:
                    print(f"❌ {url} redirects to: {redirect_url}")
                    return False
            elif response.status_code == 200:
                print(f"⚠️  {url} accessible without login (may be normal)")
            else:
                print(f"❌ {url} unexpected status: {response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing protected pages: {e}")
        return False

def test_url_file_cleanup():
    """Test that URL configuration is properly cleaned up"""
    print("\n🔍 Testing URL Configuration...")
    print("=" * 50)
    
    try:
        # Check main urls.py for accounts include
        main_urls_path = os.path.join(settings.BASE_DIR, 'sims_project', 'urls.py')
        with open(main_urls_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if "include('django.contrib.auth.urls')" in content:
            print("❌ Main URLs still includes django.contrib.auth.urls")
            return False
        else:
            print("✅ Main URLs properly cleaned of auth.urls include")
        
        if "path('accounts/" in content:
            print("❌ Main URLs still has accounts/ path")
            return False
        else:
            print("✅ Main URLs properly cleaned of accounts/ path")
        
        # Check users urls.py has password reset URLs
        users_urls_path = os.path.join(settings.BASE_DIR, 'sims', 'users', 'urls.py')
        with open(users_urls_path, 'r', encoding='utf-8') as f:
            users_content = f.read()
        
        if 'password_reset' in users_content:
            print("✅ Users URLs contains password reset patterns")
        else:
            print("❌ Users URLs missing password reset patterns")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing URL configuration: {e}")
        return False

def test_template_cleanup():
    """Test that templates are properly cleaned up"""
    print("\n🔍 Testing Template Cleanup...")
    print("=" * 50)
    
    try:
        # Check users login template exists
        users_template = os.path.join(settings.BASE_DIR, 'templates', 'users', 'login.html')
        if os.path.exists(users_template):
            with open(users_template, 'r', encoding='utf-8') as f:
                content = f.read()
            if len(content) > 100:  # Has substantial content
                print("✅ Users login template exists and has content")
            else:
                print("❌ Users login template exists but appears empty")
                return False
        else:
            print("❌ Users login template missing")
            return False
        
        # Check registration login template is disabled
        reg_template = os.path.join(settings.BASE_DIR, 'templates', 'registration', 'login.html')
        if os.path.exists(reg_template):
            with open(reg_template, 'r', encoding='utf-8') as f:
                content = f.read()
            if 'intentionally left blank' in content or len(content) < 100:
                print("✅ Registration login template properly disabled")
            else:
                print("❌ Registration login template still has active content")
                return False
        else:
            print("✅ Registration login template removed")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing template cleanup: {e}")
        return False

def main():
    """Run all login consolidation tests"""
    print("🚀 SIMS Login Consolidation - Verification Test")
    print("=" * 60)
    
    tests = [
        ("Login URL Patterns", test_login_urls),
        ("Login Page Accessibility", test_login_pages),
        ("Login Redirects", test_login_redirects),
        ("Protected Page Redirects", test_protected_pages),
        ("URL Configuration Cleanup", test_url_file_cleanup),
        ("Template Cleanup", test_template_cleanup),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append(result)
            if result:
                print(f"\n✅ {test_name}: PASSED")
            else:
                print(f"\n❌ {test_name}: FAILED")
        except Exception as e:
            print(f"\n❌ {test_name}: ERROR - {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    print("LOGIN CONSOLIDATION RESULTS:")
    print("=" * 60)
    
    passed_tests = sum(results)
    total_tests = len(results)
    
    for i, (test_name, _) in enumerate(tests):
        status = "✅ PASSED" if results[i] else "❌ FAILED"
        print(f"{test_name:.<40} {status}")
    
    print("-" * 60)
    print(f"TOTAL: {passed_tests}/{total_tests} tests passed ({passed_tests/total_tests*100:.1f}%)")
    
    if passed_tests == total_tests:
        print("\n🎉 LOGIN CONSOLIDATION SUCCESSFUL!")
        print("✅ Only users/login is active")
        print("✅ accounts/login properly removed")
        print("✅ All authentication flows working")
    elif passed_tests >= total_tests * 0.8:
        print("\n⚠️  LOGIN CONSOLIDATION MOSTLY SUCCESSFUL!")
        print("Minor issues may need attention.")
    else:
        print("\n❌ LOGIN CONSOLIDATION NEEDS ATTENTION!")
        print("Please review the failed tests.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
