#!/usr/bin/env python
import os
import django
import json

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from sims.users.models import User

def test_admin_api():
    print("=== Testing Admin Stats API ===")
    
    # Create a test client
    client = Client()
    
    # Check if we have an admin user
    admin_users = User.objects.filter(is_staff=True)
    print(f"Found {admin_users.count()} staff users")
    
    if admin_users.count() == 0:
        print("Creating admin user...")
        admin = User.objects.create_user(
            username='testadmin',
            password='testpass123',
            is_staff=True,
            is_superuser=True,
            role='admin'
        )
        print(f"Created admin: {admin.username}")
    else:
        admin = admin_users.first()
        print(f"Using existing admin: {admin.username}")
    
    # Login as admin
    login_success = client.login(username=admin.username, password='testpass123' if admin.username == 'testadmin' else 'admin123')
    print(f"Login successful: {login_success}")
    
    if not login_success:
        # Try with different password
        admin.set_password('testpass123')
        admin.save()
        login_success = client.login(username=admin.username, password='testpass123')
        print(f"Login with new password: {login_success}")
    
    if login_success:
        # Test the API endpoint
        response = client.get('/users/api/admin/stats/')
        print(f"API Response Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = json.loads(response.content.decode())
                print("API Response Data:")
                print(json.dumps(data, indent=2))
                
                # Check if we have specialty data
                specialty_stats = data.get('specialty_stats', [])
                print(f"\nSpecialty Stats: {len(specialty_stats)} specialties found")
                for stat in specialty_stats:
                    print(f"  - {stat.get('specialty', 'Unknown')}: {stat.get('count', 0)} users")
                    
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
                print("Raw response:", response.content.decode())
        else:
            print(f"Error response: {response.content.decode()}")
    else:
        print("Could not login to test API")
    
    # Show user data
    print(f"\n=== Current User Data ===")
    users = User.objects.all()
    print(f"Total users: {users.count()}")
    
    for user in users:
        print(f"  {user.username} ({user.role}) - {user.specialty or 'No specialty'}")

if __name__ == "__main__":
    test_admin_api()
