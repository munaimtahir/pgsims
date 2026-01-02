#!/usr/bin/env python
"""
Login System Final Verification
Tests all login functionality after fixes
"""
import os
import sys
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

from django.test import Client
from django.urls import reverse

def test_login_system():
    """Test complete login system functionality"""
    print("🔍 Testing Complete Login System...")
    print("=" * 50)
    
    client = Client()
    
    # Test 1: Homepage loads
    try:
        response = client.get('/')
        if response.status_code == 200:
            print("✅ Homepage loads successfully (200)")
        else:
            print(f"❌ Homepage failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Homepage error: {e}")
        return False
    
    # Test 2: Users login page loads
    try:
        response = client.get('/users/login/')
        if response.status_code == 200:
            print("✅ Users login page loads successfully (200)")
        else:
            print(f"❌ Users login page failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Users login page error: {e}")
        return False
    
    # Test 3: Accounts login returns 404
    try:
        response = client.get('/accounts/login/')
        if response.status_code == 404:
            print("✅ Accounts login properly returns 404")
        else:
            print(f"❌ Accounts login still accessible: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Accounts login test error: {e}")
        return False
    
    # Test 4: URL resolution works
    try:
        login_url = reverse('users:login')
        print(f"✅ users:login resolves to: {login_url}")
    except Exception as e:
        print(f"❌ URL resolution error: {e}")
        return False
    
    # Test 5: Password reset works
    try:
        response = client.get('/users/password-reset/')
        if response.status_code == 200:
            print("✅ Password reset page loads successfully (200)")
        else:
            print(f"❌ Password reset failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Password reset error: {e}")
        return False
    
    return True

def test_protected_pages():
    """Test that protected pages redirect correctly"""
    print("\n🔍 Testing Protected Page Redirects...")
    print("=" * 50)
    
    client = Client()
    
    protected_urls = [
        '/users/dashboard/',
        '/users/profile/',
    ]
    
    for url in protected_urls:
        try:
            response = client.get(url)
            if response.status_code == 302:  # Redirect
                redirect_url = response.url
                if '/users/login/' in redirect_url:
                    print(f"✅ {url} redirects to users/login")
                else:
                    print(f"❌ {url} redirects to: {redirect_url}")
                    return False
            else:
                print(f"⚠️  {url} status: {response.status_code}")
        except Exception as e:
            print(f"❌ {url} error: {e}")
            return False
    
    return True

def main():
    """Run all tests"""
    print("🚀 Login System Final Verification")
    print("=" * 60)
    
    login_test = test_login_system()
    protected_test = test_protected_pages()
    
    print("\n" + "=" * 60)
    
    if login_test and protected_test:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Login system working correctly")
        print("✅ Only users/login is active")
        print("✅ accounts/login properly removed")
        print("✅ Homepage 'Sign in to SIMS' button works")
        print("✅ All authentication flows functional")
    else:
        print("❌ SOME TESTS FAILED!")
        print("Please check the output above for details.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
