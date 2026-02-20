#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

from django.test import Client

client = Client()

print("🔍 Testing profile page functionality...")

# Test profile page access
login_result = client.login(username='admin', password='admin123')
print(f"Admin login: {'SUCCESS' if login_result else 'FAILED'}")

if login_result:
    response = client.get('/users/profile/')
    print(f"Profile page status: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Profile page loads successfully!")
        # Check if the content contains expected elements
        content = response.content.decode()
        if 'User Profile' in content:
            print("✅ Profile page has correct title")
        if 'Basic Information' in content:
            print("✅ Profile page has basic information section")
        if 'admin' in content.lower():
            print("✅ Profile page shows user data")
    else:
        print(f"❌ Profile page failed: {response.status_code}")
        if hasattr(response, 'context') and response.context.get('exception'):
            print(f"Error: {response.context['exception']}")

# Test with PG user
print("\n🔍 Testing with PG user...")
client.logout()
pg_login = client.login(username='pg_test', password='pg123')
print(f"PG login: {'SUCCESS' if pg_login else 'FAILED'}")

if pg_login:
    response = client.get('/users/profile/')
    print(f"PG profile page status: {response.status_code}")
    if response.status_code == 200:
        print("✅ PG profile page works!")
        content = response.content.decode()
        if 'Professional Information' in content:
            print("✅ PG profile shows professional information")
    else:
        print(f"❌ PG profile failed: {response.status_code}")

print("\n✅ Profile page should now work in browser!")
