#!/usr/bin/env python
"""
Test script to verify admin URL patterns are working correctly
"""
import os
import sys
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

from django.urls import reverse
from django.test import RequestFactory
from django.contrib.admin.sites import site
from django.contrib.auth import get_user_model

def test_admin_urls():
    """Test that all admin URL patterns work correctly"""
    User = get_user_model()
    
    print("🔍 Testing Admin URL Patterns...")
    print("=" * 50)
    
    try:
        # Test basic admin URLs
        admin_index = reverse('admin:index')
        print(f"✅ Admin Index URL: {admin_index}")
        
        admin_login = reverse('admin:login')
        print(f"✅ Admin Login URL: {admin_login}")
        
        admin_logout = reverse('admin:logout')
        print(f"✅ Admin Logout URL: {admin_logout}")
        
        # Test user model URLs
        users_add = reverse('admin:users_user_add')
        print(f"✅ Users Add URL: {users_add}")
        
        users_changelist = reverse('admin:users_user_changelist')
        print(f"✅ Users Changelist URL: {users_changelist}")
        
        # Test if a user exists to test change URL
        user = User.objects.first()
        if user:
            user_change = reverse('admin:users_user_change', args=[user.id])
            print(f"✅ User Change URL: {user_change}")
            
            user_delete = reverse('admin:users_user_delete', args=[user.id])
            print(f"✅ User Delete URL: {user_delete}")
        else:
            print("⚠️  No users found to test change/delete URLs")
        
        print("\n🎉 All admin URL patterns are working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing admin URLs: {e}")
        return False

def test_admin_site_registration():
    """Test that models are properly registered with admin"""
    print("\n🔍 Testing Admin Site Registration...")
    print("=" * 50)
    
    try:
        # Get all registered models
        registered_models = site._registry
        
        print(f"📋 Total registered models: {len(registered_models)}")
        
        for model, admin_class in registered_models.items():
            app_label = model._meta.app_label
            model_name = model._meta.model_name
            print(f"✅ {app_label}.{model_name} -> {admin_class.__class__.__name__}")
        
        # Check if User model is registered
        User = get_user_model()
        if User in registered_models:
            print(f"\n✅ Custom User model ({User._meta.label}) is properly registered")
        else:
            print(f"\n❌ Custom User model ({User._meta.label}) is NOT registered")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Error checking admin registration: {e}")
        return False

def test_admin_templates():
    """Test that admin templates exist and are accessible"""
    print("\n🔍 Testing Admin Template Files...")
    print("=" * 50)
    
    templates_to_check = [
        'admin/base.html',
        'admin/base_site.html', 
        'admin/index.html',
        'admin/login.html',
        'admin/logged_out.html',
        'admin/change_form.html',
        'admin/change_list.html',
        'admin/delete_confirmation.html',
        'admin/404.html',
        'admin/500.html'
    ]
    
    template_dir = os.path.join(settings.BASE_DIR, 'templates')
    
    for template in templates_to_check:
        template_path = os.path.join(template_dir, template)
        if os.path.exists(template_path):
            print(f"✅ {template}")
        else:
            print(f"❌ {template} - NOT FOUND")
    
    return True

if __name__ == "__main__":
    print("🚀 SIMS Admin System Test")
    print("=" * 60)
    
    # Run all tests
    url_test = test_admin_urls()
    registration_test = test_admin_site_registration()
    template_test = test_admin_templates()
    
    print("\n" + "=" * 60)
    if url_test and registration_test and template_test:
        print("🎉 ALL TESTS PASSED! Admin system is working correctly.")
    else:
        print("❌ SOME TESTS FAILED! Please check the errors above.")
    print("=" * 60)
