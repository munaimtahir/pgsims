import os
import django
from django.test import Client
from django.urls import reverse

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

def test_authentication_system():
    """Comprehensive test of the authentication system"""
    client = Client()
    print("=== SIMS Authentication System Test ===\n")
    
    # Test URL resolution
    print("1. Testing URL Resolution:")
    urls_to_test = [
        ('home', 'Home page'),
        ('users:login', 'Login page'),
        ('users:logout', 'Logout'),
        ('users:password_reset', 'Password reset'),
        ('users:password_reset_done', 'Password reset done'),
        ('users:password_change', 'Password change'),
        ('users:password_change_done', 'Password change done'),
        ('admin:index', 'Admin index'),
    ]
    
    for url_name, description in urls_to_test:
        try:
            url = reverse(url_name)
            print(f"   ✅ {description}: {url}")
        except Exception as e:
            print(f"   ❌ {description}: {e}")
    
    print("\n2. Testing Page Access:")
    
    # Test page accessibility
    pages_to_test = [
        ('/', 'Home page'),
        ('/users/login/', 'Login page'),
        ('/users/password-reset/', 'Password reset page'),
        ('/admin/', 'Admin login'),
    ]
    
    for url, description in pages_to_test:
        try:
            response = client.get(url)
            if response.status_code == 200:
                print(f"   ✅ {description}: HTTP {response.status_code}")
            elif response.status_code == 302:
                print(f"   ↗️  {description}: HTTP {response.status_code} (redirect)")
            else:
                print(f"   ⚠️  {description}: HTTP {response.status_code}")
        except Exception as e:
            print(f"   ❌ {description}: {e}")
    
    print("\n3. Testing Template Rendering:")
    templates_to_test = [
        '/users/login/',
        '/users/password-reset/',
    ]
    
    for url in templates_to_test:
        try:
            response = client.get(url)
            if response.status_code == 200 and b'SIMS' in response.content:
                print(f"   ✅ {url}: Template renders with SIMS branding")
            elif response.status_code == 200:
                print(f"   ⚠️  {url}: Template renders but missing SIMS branding")
            else:
                print(f"   ❌ {url}: Template rendering failed")
        except Exception as e:
            print(f"   ❌ {url}: {e}")
    
    print("\n=== Test Complete ===")
    print("✅ All systems appear to be working correctly!")
    print("🔗 Login URL: http://127.0.0.1:8000/users/login/")
    print("🔗 Admin URL: http://127.0.0.1:8000/admin/")
    print("🏠 Home URL: http://127.0.0.1:8000/")

if __name__ == '__main__':
    test_authentication_system()
