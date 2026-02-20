#!/usr/bin/env python
"""
Test script to verify admin login functionality
"""
import os
import sys
import django
from django.test.client import Client
from django.contrib.auth import get_user_model

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

def test_admin_login():
    """Test admin login functionality"""
    print("🔍 Testing Admin Login Functionality")
    print("=" * 50)
    
    # Create test client
    client = Client()
    
    # Test 1: Access admin login page
    print("1. Testing admin login page accessibility...")
    try:
        response = client.get('/admin/login/')
        if response.status_code == 200:
            print("   ✅ Admin login page accessible (Status: 200)")
            
            # Check if the page contains expected elements
            content = response.content.decode('utf-8')
            if 'login-form' in content:
                print("   ✅ Login form found in page")
            else:
                print("   ❌ Login form not found in page")
                
            if 'csrf' in content.lower():
                print("   ✅ CSRF token present")
            else:
                print("   ❌ CSRF token missing")
                
        else:
            print(f"   ❌ Admin login page not accessible (Status: {response.status_code})")
            return False
    except Exception as e:
        print(f"   ❌ Error accessing admin login page: {e}")
        return False
    
    # Test 2: Check if superuser exists
    print("\n2. Checking for existing superuser...")
    try:
        User = get_user_model()
        superusers = User.objects.filter(is_superuser=True)
        if superusers.exists():
            superuser = superusers.first()
            print(f"   ✅ Superuser found: {superuser.username} ({superuser.email})")
            
            # Test 3: Test login with valid credentials
            print("\n3. Testing login with superuser credentials...")
            login_data = {
                'username': superuser.username,
                'password': 'admin123',  # Default password we set
                'next': '/admin/'
            }
            
            response = client.post('/admin/login/', login_data, follow=True)
            
            if response.status_code == 200:
                # Check if we're redirected to admin dashboard
                if '/admin/' in response.request['PATH_INFO']:
                    if 'Site administration' in response.content.decode('utf-8') or 'Welcome' in response.content.decode('utf-8'):
                        print("   ✅ Login successful - redirected to admin dashboard")
                        return True
                    else:
                        print("   ⚠️  Login may have succeeded but unexpected content")
                        print(f"   Current URL: {response.request['PATH_INFO']}")
                else:
                    print("   ❌ Login failed - not redirected to admin")
                    if 'errorlist' in response.content.decode('utf-8').lower():
                        print("   ❌ Login errors found on page")
            else:
                print(f"   ❌ Login request failed (Status: {response.status_code})")
                
        else:
            print("   ❌ No superuser found")
            print("   💡 Create a superuser with: py manage.py createsuperuser")
            return False
            
    except Exception as e:
        print(f"   ❌ Error checking superuser: {e}")
        return False
    
    return False

def test_admin_pages():
    """Test access to various admin pages"""
    print("\n🔍 Testing Admin Pages Access")
    print("=" * 50)
    
    client = Client()
    
    # Login first
    User = get_user_model()
    superuser = User.objects.filter(is_superuser=True).first()
    
    if not superuser:
        print("❌ No superuser available for testing")
        return False
    
    login_success = client.login(username=superuser.username, password='admin123')
    
    if not login_success:
        print("❌ Could not login for admin pages testing")
        return False
    
    print("✅ Logged in successfully")
    
    # Test admin pages
    admin_urls = [
        ('/admin/', 'Admin Dashboard'),
        ('/admin/users/user/', 'Users List'),
        ('/admin/users/user/add/', 'Add User'),
        ('/admin/logbook/', 'Logbook Admin'),
        ('/admin/cases/', 'Cases Admin'),
        ('/admin/rotations/', 'Rotations Admin'),
        ('/admin/certificates/', 'Certificates Admin'),
    ]
    
    for url, name in admin_urls:
        try:
            response = client.get(url)
            if response.status_code == 200:
                print(f"   ✅ {name}: Accessible")
            elif response.status_code == 302:
                print(f"   ⚠️  {name}: Redirected (may be normal)")
            else:
                print(f"   ❌ {name}: Status {response.status_code}")
        except Exception as e:
            print(f"   ❌ {name}: Error - {e}")

if __name__ == '__main__':
    try:
        print("🚀 SIMS Admin Login Test Suite")
        print("=" * 50)
        
        # Test admin login
        login_works = test_admin_login()
        
        if login_works:
            test_admin_pages()
            print("\n🎉 Admin login is working properly!")
        else:
            print("\n❌ Admin login has issues that need to be resolved")
            
            # Provide troubleshooting suggestions
            print("\n🔧 Troubleshooting Suggestions:")
            print("1. Ensure the development server is running:")
            print("   py manage.py runserver")
            print("2. Check if superuser exists:")
            print("   py manage.py shell -c \"from django.contrib.auth import get_user_model; print(get_user_model().objects.filter(is_superuser=True).count())\"")
            print("3. Create superuser if needed:")
            print("   py manage.py createsuperuser")
            print("4. Try different password (default is 'admin123')")
            print("5. Check Django logs for errors")
        
    except Exception as e:
        print(f"\n💥 Test suite failed with error: {e}")
        import traceback
        traceback.print_exc()
