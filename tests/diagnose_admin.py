"""
Quick test to diagnose admin page issues
"""
import os
import django
from django.test import Client
from django.contrib.auth import get_user_model

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

print("🔍 Diagnosing Admin Page Issues")
print("=" * 50)

try:
    client = Client()
    
    # Test 1: Root admin URL
    print("1. Testing /admin/ (should redirect to login)")
    response = client.get('/admin/')
    print(f"   Status: {response.status_code}")
    print(f"   Location: {response.get('Location', 'No redirect')}")
    
    # Test 2: Admin login URL
    print("\n2. Testing /admin/login/")
    response = client.get('/admin/login/')
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        content = response.content.decode()
        print(f"   Content length: {len(content)} characters")
        print(f"   Has form: {'login-form' in content}")
        print(f"   Has title: {'Admin Login' in content}")
    else:
        print(f"   Error: {response.content.decode()[:200]}...")
    
    # Test 3: Try accessing admin after login
    print("\n3. Testing admin access with login")
    User = get_user_model()
    superuser = User.objects.filter(is_superuser=True).first()
    
    if superuser:
        login_success = client.login(username=superuser.username, password='admin123')
        print(f"   Login successful: {login_success}")
        
        if login_success:
            response = client.get('/admin/')
            print(f"   Admin dashboard status: {response.status_code}")
            if response.status_code == 200:
                content = response.content.decode()
                print(f"   Dashboard content length: {len(content)} characters")
                print(f"   Has admin content: {'Site administration' in content or 'Dashboard' in content}")
            else:
                print(f"   Dashboard error: {response.content.decode()[:200]}...")
    else:
        print("   No superuser found for testing")
    
    # Test 4: Check template loading
    print("\n4. Testing template loading")
    from django.template.loader import get_template
    try:
        admin_base = get_template('admin/base.html')
        print("   ✅ admin/base.html loads")
    except Exception as e:
        print(f"   ❌ admin/base.html error: {e}")
    
    try:
        admin_login = get_template('admin/login.html')
        print("   ✅ admin/login.html loads")
    except Exception as e:
        print(f"   ❌ admin/login.html error: {e}")
    
    print("\n" + "=" * 50)
    print("Diagnosis complete!")
    
except Exception as e:
    print(f"❌ Error during diagnosis: {e}")
    import traceback
    traceback.print_exc()
