#!/usr/bin/env python
"""
Test script to verify login system is working properly
"""
import os
import sys
import django
from django.test import TestCase, Client
from django.urls import reverse, NoReverseMatch
from django.template import Context, Template

# Add project to path
sys.path.insert(0, 'd:\\PMC\\sims_project-1')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')

# Setup Django
django.setup()

def test_url_resolution():
    """Test that all URLs in login template can be resolved"""
    print("Testing URL resolution...")
    
    try:
        # Test home URL
        home_url = reverse('home')
        print(f"✅ home URL: {home_url}")
    except NoReverseMatch as e:
        print(f"❌ home URL error: {e}")
    
    try:
        # Test users:login URL
        login_url = reverse('users:login')
        print(f"✅ users:login URL: {login_url}")
    except NoReverseMatch as e:
        print(f"❌ users:login URL error: {e}")
    
    try:
        # Test users:password_reset URL
        reset_url = reverse('users:password_reset')
        print(f"✅ users:password_reset URL: {reset_url}")
    except NoReverseMatch as e:
        print(f"❌ users:password_reset URL error: {e}")
    
    try:
        # Test admin:index URL
        admin_url = reverse('admin:index')
        print(f"✅ admin:index URL: {admin_url}")
    except NoReverseMatch as e:
        print(f"❌ admin:index URL error: {e}")

def test_login_page_access():
    """Test accessing the login page"""
    print("\nTesting login page access...")
    
    client = Client()
    try:
        response = client.get('/users/login/')
        print(f"✅ Login page status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Login page loads successfully")
        else:
            print(f"❌ Login page returned status {response.status_code}")
    except Exception as e:
        print(f"❌ Login page error: {e}")

def test_template_rendering():
    """Test that login template renders without URL errors"""
    print("\nTesting template rendering...")
    
    from django.template.loader import get_template
    from django.template import Context, RequestContext
    from django.test import RequestFactory
    
    try:
        template = get_template('users/login.html')
        factory = RequestFactory()
        request = factory.get('/users/login/')
        context = RequestContext(request, {})
        
        rendered = template.render(context)
        print("✅ Login template renders successfully")
        return True
    except Exception as e:
        print(f"❌ Template rendering error: {e}")
        return False

if __name__ == '__main__':
    print("=== SIMS Login System Test ===")
    test_url_resolution()
    test_login_page_access()
    test_template_rendering()
    print("\n=== Test Complete ===")
