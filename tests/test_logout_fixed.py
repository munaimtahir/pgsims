#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

from django.test import Client

client = Client()

print("🔍 Testing logout functionality after settings fix...")

# Test 1: Login and logout via GET
print("\n1. Testing GET logout:")
login_result = client.login(username='admin', password='admin123')
print(f"   Login: {'SUCCESS' if login_result else 'FAILED'}")

if login_result:
    response = client.get('/users/logout/', follow=True)
    print(f"   Logout GET: Status {response.status_code}")
    print(f"   Final URL: {response.request['PATH_INFO']}")
    print(f"   Response contains 'logged out': {'logged out' in response.content.decode().lower()}")

# Test 2: Login and logout via POST
print("\n2. Testing POST logout:")
login_result = client.login(username='admin', password='admin123')
print(f"   Login: {'SUCCESS' if login_result else 'FAILED'}")

if login_result:
    response = client.post('/users/logout/', follow=True)
    print(f"   Logout POST: Status {response.status_code}")
    print(f"   Final URL: {response.request['PATH_INFO']}")

# Test 3: Direct access to logout URL
print("\n3. Testing direct logout URL access:")
response = client.get('/users/logout/')
print(f"   Direct access: Status {response.status_code}")

print("\n✅ If all status codes are 200, logout should work in browser!")
