"""
Quick verification that admin login is working
"""
print("🔍 Testing Admin Login Functionality")
print("=" * 50)

try:
    import os
    import django
    from django.test import Client
    from django.contrib.auth import get_user_model

    # Setup Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
    django.setup()

    print("1. Testing login page accessibility...")
    client = Client()
    response = client.get('/admin/login/')
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        print("   ✅ Login page is accessible")
        
        # Check for form
        content = response.content.decode()
        if 'login-form' in content:
            print("   ✅ Login form found")
        else:
            print("   ❌ Login form not found")
            
        print("\n2. Testing login credentials...")
        User = get_user_model()
        superuser = User.objects.filter(is_superuser=True).first()
        
        if superuser:
            print(f"   Superuser: {superuser.username}")
            
            # Test login
            response = client.post('/admin/login/', {
                'username': superuser.username,
                'password': 'admin123',
                'next': '/admin/'
            }, follow=True)
            
            print(f"   Login response status: {response.status_code}")
            
            if response.status_code == 200:
                final_url = response.wsgi_request.path if hasattr(response, 'wsgi_request') else 'unknown'
                print(f"   Final URL: {final_url}")
                
                content = response.content.decode()
                if 'Site administration' in content or 'Welcome' in content or 'Dashboard' in content:
                    print("   ✅ LOGIN SUCCESSFUL - Admin dashboard reached")
                elif 'errorlist' in content.lower() or 'error' in content.lower():
                    print("   ❌ Login failed - errors detected")
                else:
                    print("   ⚠️  Login status unclear")
            else:
                print(f"   ❌ Login failed with status {response.status_code}")
        else:
            print("   ❌ No superuser found")
    else:
        print("   ❌ Login page not accessible")

    print("\n3. Manual test instructions:")
    print("   1. Go to: http://127.0.0.1:8000/admin/")
    print("   2. Username: admin")
    print("   3. Password: admin123")
    print("   4. Click 'Log in'")
    
except Exception as e:
    print(f"❌ Error during testing: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 50)
print("Admin login verification complete!")
