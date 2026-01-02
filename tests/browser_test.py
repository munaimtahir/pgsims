#!/usr/bin/env python
"""
Test user creation by mimicking browser form submission exactly
"""
import os
import sys
import django

# Setup Django
sys.path.append('d:/PMC/sims_project-2')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test.utils import override_settings
import time

User = get_user_model()

def test_form_like_browser():
    """Test form submission exactly like a browser would"""
    
    client = Client()
    
    # Login as admin
    admin_login = client.login(username='admin', password='admin123')
    if not admin_login:
        print("Login failed")
        return
    
    print("=== Testing form submission like browser ===")
    
    # First, get the form page to ensure CSRF token
    form_response = client.get(reverse('users:user_create'))
    print(f"Form page status: {form_response.status_code}")
    
    # Extract CSRF token
    csrf_token = None
    if hasattr(form_response, 'context') and form_response.context:
        csrf_token = form_response.context.get('csrf_token')
    
    # Count current users
    initial_count = User.objects.count()
    print(f"Initial user count: {initial_count}")
    
    # Create unique username
    timestamp = int(time.time())
    username = f'browsertest_{timestamp}'
    
    # Form data exactly as browser would send (including checkboxes as 'on')
    form_data = {
        'username': username,
        'email': f'{username}@example.com',
        'first_name': 'Browser',
        'last_name': 'Test',
        'role': 'admin',  # Simple admin role first
        'password1': 'browsertest123',
        'password2': 'browsertest123',
        'phone_number': '+1234567890',
        'registration_number': 'BT001',
        'is_active': 'on',  # This is how checkboxes are sent
        'send_welcome_email': 'on',
        'force_password_change': 'on',
    }
    
    if csrf_token:
        form_data['csrfmiddlewaretoken'] = csrf_token
    
    print(f"Submitting form data: {form_data}")
    
    # Submit form
    response = client.post(reverse('users:user_create'), form_data, follow=True)
    
    print(f"Response status: {response.status_code}")
    print(f"Final URL: {response.request['PATH_INFO'] if response.request else 'Unknown'}")
    
    # Check user count after
    final_count = User.objects.count()
    print(f"Final user count: {final_count}")
    
    # Check if user was created
    if User.objects.filter(username=username).exists():
        created_user = User.objects.get(username=username)
        print(f"✅ SUCCESS: User {username} created!")
        print(f"   - Role: {created_user.role}")
        print(f"   - Active: {created_user.is_active}")
        print(f"   - Email: {created_user.email}")
    else:
        print(f"❌ FAILED: User {username} was not created")
        
        # Print response content if there's an error
        if response.status_code != 302:  # Not a redirect
            content = response.content.decode()
            if 'error' in content.lower() or 'invalid' in content.lower():
                print("Error content found in response:")
                print(content[:1000])

if __name__ == '__main__':
    test_form_like_browser()
