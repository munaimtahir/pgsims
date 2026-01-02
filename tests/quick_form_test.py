#!/usr/bin/env python
"""
Test user creation form with browser simulation
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

User = get_user_model()

def test_simple_user_creation():
    """Test creating a simple admin user"""
    
    client = Client()
    
    # Get or create admin user
    try:
        admin_user = User.objects.get(username='admin')
    except User.DoesNotExist:
        admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='admin123',
            role='admin',
            first_name='Admin',
            last_name='User'
        )
    
    # Login
    login_success = client.login(username='admin', password='admin123')
    if not login_success:
        print("Login failed")
        return
    
    print("Testing simple admin user creation...")
    
    # Count users before
    users_before = User.objects.count()
    print(f"Users before: {users_before}")
    
    # Create a unique username
    import time
    timestamp = int(time.time())
    username = f'testuser_{timestamp}'
    
    form_data = {
        'username': username,
        'email': f'{username}@example.com',
        'first_name': 'Test',
        'last_name': 'User',
        'role': 'admin',
        'password1': 'testpass123',
        'password2': 'testpass123',
        'is_active': 'on',  # Checkbox value
    }
    
    print(f"Submitting form data: {form_data}")
    
    response = client.post(reverse('users:user_create'), form_data, follow=True)
    
    print(f"Response status: {response.status_code}")
    print(f"Response redirect chain: {response.redirect_chain}")
    
    # Count users after
    users_after = User.objects.count()
    print(f"Users after: {users_after}")
    
    # Check if user was created
    if User.objects.filter(username=username).exists():
        print(f"✅ User {username} was created successfully!")
        created_user = User.objects.get(username=username)
        print(f"   - Email: {created_user.email}")
        print(f"   - Role: {created_user.role}")
        print(f"   - Active: {created_user.is_active}")
    else:
        print(f"❌ User {username} was NOT created")
        
        # Print any form errors from the response
        if hasattr(response, 'context') and response.context:
            print("Response context keys:", list(response.context.keys()) if response.context else "None")
        
        # Print response content (first 1000 chars)
        content = response.content.decode()[:1000]
        print(f"Response content preview: {content}")

if __name__ == '__main__':
    test_simple_user_creation()
