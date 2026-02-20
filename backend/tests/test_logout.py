#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

from django.test import Client

client = Client()

print("Testing logout functionality...")

# Login first
login_result = client.login(username='admin', password='admin123')
print(f"Login successful: {login_result}")

if login_result:
    # Test GET request to logout
    response_get = client.get('/users/logout/')
    print(f"Logout GET response: {response_get.status_code}")
    
    # Login again for POST test
    client.login(username='admin', password='admin123')
    
    # Test POST request to logout
    response_post = client.post('/users/logout/')
    print(f"Logout POST response: {response_post.status_code}")
    
    if response_get.status_code == 200:
        print("✅ Logout working with GET")
    elif response_post.status_code == 200:
        print("✅ Logout working with POST")
    else:
        print("❌ Logout not working properly")
        print(f"GET content: {response_get.content[:200]}")
        print(f"POST content: {response_post.content[:200]}")
else:
    print("❌ Could not test logout - login failed")
