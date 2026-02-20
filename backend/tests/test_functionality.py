#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

# Create a test client
client = Client()

print("=== Testing Logout Functionality ===")
# Get the admin user
admin_user = User.objects.get(username='admin')
print(f"Admin user found: {admin_user.username}")

# Login as admin
login_success = client.login(username='admin', password='admin123')
print(f"Login successful: {login_success}")

if login_success:
    # Test logout
    logout_response = client.get('/users/logout/')
    print(f"Logout response status: {logout_response.status_code}")
    print(f"Logout successful: {logout_response.status_code == 200}")
else:
    print("Could not test logout - login failed")

print("\n=== Testing Supervisor API ===")
# Login again for API testing
client.login(username='admin', password='admin123')

# Test the supervisor API
api_response = client.get('/users/api/supervisors/specialty/cardiology/')
print(f"API response status: {api_response.status_code}")

if api_response.status_code == 200:
    data = api_response.json()
    print(f"API response: {data}")
    if 'supervisors' in data and len(data['supervisors']) > 0:
        print("✅ Supervisor API working correctly!")
    else:
        print("⚠️  API working but no supervisors found")
else:
    print(f"❌ API error: {api_response.content.decode()}")

print("\n=== Testing User Creation Permission ===")
# Test if admin can access user creation page
create_response = client.get('/users/create/')
print(f"User creation page status: {create_response.status_code}")
print(f"User creation accessible: {create_response.status_code == 200}")

print("\n=== Testing New User Login ===")
# Test if the created PG user can login
client.logout()
pg_login = client.login(username='pg_test', password='pg123')
print(f"PG user login successful: {pg_login}")

if pg_login:
    # Test PG dashboard access
    dashboard_response = client.get('/users/dashboard/')
    print(f"PG dashboard access status: {dashboard_response.status_code}")
    print(f"PG dashboard accessible: {dashboard_response.status_code in [200, 302]}")  # 302 for redirect
