#!/usr/bin/env python
"""
Test the user creation form by simulating form submissions.
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
import json

User = get_user_model()

def test_user_creation_form():
    """Test the user creation form with different scenarios"""
    
    # Create client and admin user
    client = Client()
    
    # Create admin user for authentication
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
    
    # Login as admin
    login_success = client.login(username='admin', password='admin123')
    print(f"Admin login successful: {login_success}")
    
    if not login_success:
        print("Cannot proceed without admin login")
        return
    
    # Test 1: Create Admin User
    print("\n=== Test 1: Creating Admin User ===")
    form_data = {
        'username': 'testadmin1',
        'email': 'testadmin1@example.com',
        'first_name': 'Test',
        'last_name': 'Admin',
        'role': 'admin',
        'password1': 'testpass123',
        'password2': 'testpass123',
        'phone_number': '+1234567890',
        'registration_number': 'REG001',
        'is_active': True,
    }
    
    response = client.post(reverse('users:user_create'), form_data)
    print(f"Response status: {response.status_code}")
    if response.status_code == 302:
        print(f"Redirect to: {response.url}")
        # Check if user was created
        if User.objects.filter(username='testadmin1').exists():
            print("✅ Admin user created successfully")
        else:
            print("❌ Admin user was not created")
    else:
        print(f"Form submission failed: {response.content.decode()[:500]}")
    
    # Test 2: Create Supervisor User
    print("\n=== Test 2: Creating Supervisor User ===")
    form_data = {
        'username': 'testsupervisor1',
        'email': 'testsupervisor1@example.com',
        'first_name': 'Test',
        'last_name': 'Supervisor',
        'role': 'supervisor',
        'specialty': 'medicine',
        'password1': 'testpass123',
        'password2': 'testpass123',
        'phone_number': '+1234567891',
        'registration_number': 'REG002',
        'is_active': True,
    }
    
    response = client.post(reverse('users:user_create'), form_data)
    print(f"Response status: {response.status_code}")
    if response.status_code == 302:
        print(f"Redirect to: {response.url}")
        # Check if user was created
        if User.objects.filter(username='testsupervisor1').exists():
            print("✅ Supervisor user created successfully")
        else:
            print("❌ Supervisor user was not created")
    else:
        print(f"Form submission failed: {response.content.decode()[:500]}")
    
    # Test 3: Create PG User (need supervisor first)
    print("\n=== Test 3: Creating PG User ===")
    
    # Ensure we have a supervisor
    supervisor = User.objects.filter(role='supervisor', specialty='medicine').first()
    if not supervisor:
        print("No supervisor found, creating one...")
        supervisor = User.objects.create_user(
            username='supervisor_for_pg',
            email='supervisor_for_pg@example.com',
            password='testpass123',
            role='supervisor',
            specialty='medicine',
            first_name='Supervisor',
            last_name='ForPG'
        )
    
    form_data = {
        'username': 'testpg1',
        'email': 'testpg1@example.com',
        'first_name': 'Test',
        'last_name': 'PG',
        'role': 'pg',
        'specialty': 'medicine',
        'year': '1',
        'supervisor_choice': str(supervisor.id),  # This might be the issue
        'password1': 'testpass123',
        'password2': 'testpass123',
        'phone_number': '+1234567892',
        'registration_number': 'REG003',
        'is_active': True,
    }
    
    print(f"Using supervisor ID: {supervisor.id}")
    response = client.post(reverse('users:user_create'), form_data)
    print(f"Response status: {response.status_code}")
    if response.status_code == 302:
        print(f"Redirect to: {response.url}")
        # Check if user was created
        if User.objects.filter(username='testpg1').exists():
            pg_user = User.objects.get(username='testpg1')
            print(f"✅ PG user created successfully with supervisor: {pg_user.supervisor}")
        else:
            print("❌ PG user was not created")
    else:
        print(f"Form submission failed: {response.content.decode()[:500]}")
    
    # Test 4: Invalid form data
    print("\n=== Test 4: Testing validation ===")
    form_data = {
        'username': '',  # Missing username
        'email': 'invalid-email',  # Invalid email
        'first_name': 'Test',
        'last_name': 'Invalid',
        'role': 'pg',
        'specialty': '',  # Missing specialty for PG
        'password1': '123',  # Too short password
        'password2': '456',  # Mismatched passwords
    }
    
    response = client.post(reverse('users:user_create'), form_data)
    print(f"Response status: {response.status_code}")
    print("Expected validation errors should be shown")
    
    # Check current user count
    print(f"\n=== Current User Count ===")
    total_users = User.objects.count()
    admin_count = User.objects.filter(role='admin').count()
    supervisor_count = User.objects.filter(role='supervisor').count()
    pg_count = User.objects.filter(role='pg').count()
    
    print(f"Total users: {total_users}")
    print(f"Admins: {admin_count}")
    print(f"Supervisors: {supervisor_count}")
    print(f"PGs: {pg_count}")

if __name__ == '__main__':
    test_user_creation_form()
