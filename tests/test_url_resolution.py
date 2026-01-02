#!/usr/bin/env python
"""
Quick URL Resolution Test
Tests if the users:login URL resolves correctly
"""
import os
import sys
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

from django.urls import reverse, NoReverseMatch
from django.test import Client

def test_url_resolution():
    """Test URL resolution for login"""
    print("🔍 Testing URL Resolution...")
    print("=" * 40)
    
    try:
        # Test users:login URL resolution
        users_login_url = reverse('users:login')
        print(f"✅ users:login resolves to: {users_login_url}")
        
        # Test if old login URL exists
        try:
            old_login_url = reverse('login')
            print(f"⚠️  'login' still resolves to: {old_login_url}")
        except NoReverseMatch:
            print("✅ 'login' URL properly removed (NoReverseMatch)")
        
        return True
        
    except NoReverseMatch as e:
        print(f"❌ URL resolution error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_login_page():
    """Test login page accessibility"""
    print("\n🔍 Testing Login Page...")
    print("=" * 40)
    
    client = Client()
    
    try:
        # Test users login page
        response = client.get('/users/login/')
        print(f"✅ /users/login/ returns status: {response.status_code}")
        
        # Test homepage
        home_response = client.get('/')
        print(f"✅ Homepage returns status: {home_response.status_code}")
        
        return response.status_code == 200 and home_response.status_code == 200
        
    except Exception as e:
        print(f"❌ Page test error: {e}")
        return False

def main():
    """Run URL tests"""
    print("🚀 Quick URL Diagnostics")
    print("=" * 50)
    
    url_test = test_url_resolution()
    page_test = test_login_page()
    
    if url_test and page_test:
        print("\n✅ All tests passed!")
        print("URLs are resolving correctly.")
    else:
        print("\n❌ Some tests failed!")
        print("Check the output above for details.")

if __name__ == "__main__":
    main()
