#!/usr/bin/env python
"""
Basic SIMS system verification script
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from django.test import Client
from django.urls import reverse, NoReverseMatch

def test_basic_setup():
    """Test basic Django setup"""
    print("🔧 Testing Basic Setup...")
    
    try:
        # Test database connection
        User = get_user_model()
        user_count = User.objects.count()
        print(f"   ✅ Database connected - {user_count} users")
        
        # Test settings
        from django.conf import settings
        print(f"   ✅ Settings loaded - DEBUG: {settings.DEBUG}")
        
        return True
    except Exception as e:
        print(f"   ❌ Basic setup failed: {e}")
        return False

def test_user_creation():
    """Test user creation and authentication"""
    print("\n👤 Testing User Management...")
    
    try:
        User = get_user_model()
        
        # Create test superuser if doesn't exist
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@sims.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            print("   ✅ Admin user created")
        else:
            admin = User.objects.get(username='admin')
            print("   ✅ Admin user exists")
        
        # Create test regular user
        if not User.objects.filter(username='testuser').exists():
            test_user = User.objects.create_user(
                username='testuser',
                email='test@sims.com',
                password='test123',
                first_name='Test',
                last_name='User'
            )
            print("   ✅ Test user created")
        else:
            print("   ✅ Test user exists")
        
        print(f"   📊 Total users: {User.objects.count()}")
        return True
        
    except Exception as e:
        print(f"   ❌ User creation failed: {e}")
        return False

def test_url_patterns():
    """Test URL patterns and views"""
    print("\n🌐 Testing URL Patterns...")
    
    urls_to_test = [
        ('admin:index', 'Admin interface'),
        ('users:login', 'Login page'),
        ('users:dashboard', 'User dashboard'),
        ('users:profile', 'User profile'),
        ('users:user_list', 'User list'),
    ]
    
    client = Client()
    
    for url_name, description in urls_to_test:
        try:
            url = reverse(url_name)
            response = client.get(url)
            status = "✅" if response.status_code in [200, 302, 403] else "❌"
            print(f"   {status} {description}: {url} (Status: {response.status_code})")
        except NoReverseMatch:
            print(f"   ❌ {description}: URL pattern '{url_name}' not found")
        except Exception as e:
            print(f"   ❌ {description}: Error - {e}")

def test_templates():
    """Test template rendering"""
    print("\n📄 Testing Templates...")
    
    from django.template.loader import get_template
    from django.template import TemplateDoesNotExist
    
    templates_to_test = [
        'base.html',
        'users/dashboard.html',
        'users/admin_dashboard.html',
        'users/profile.html',
        'registration/login.html',
    ]
    
    for template_name in templates_to_test:
        try:
            template = get_template(template_name)
            print(f"   ✅ {template_name}: Found")
        except TemplateDoesNotExist:
            print(f"   ❌ {template_name}: Not found")
        except Exception as e:
            print(f"   ❌ {template_name}: Error - {e}")

def main():
    print("🏥 SIMS System Verification")
    print("=" * 50)
    
    tests = [
        test_basic_setup,
        test_user_creation,
        test_url_patterns,
        test_templates,
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n📊 Summary:")
    print("=" * 30)
    passed = sum(results)
    total = len(results)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! System is ready.")
        print("\n🚀 Next steps:")
        print("   1. Access admin at: http://127.0.0.1:8000/admin/")
        print("   2. Login with: admin / admin123")
        print("   3. Test user dashboard: http://127.0.0.1:8000/users/dashboard/")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main()
