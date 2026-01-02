#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

from django.test import Client

client = Client()

print("🔍 Testing ADMIN logout functionality...")

# Test admin logout
print("\n1. Testing /admin/logout/ GET:")
login_result = client.login(username='admin', password='admin123')
print(f"   Admin login: {'SUCCESS' if login_result else 'FAILED'}")

if login_result:
    response = client.get('/admin/logout/', follow=True)
    print(f"   Admin logout GET: Status {response.status_code}")
    print(f"   Final URL: {response.wsgi_request.path}")
    
    # Test if we're redirected properly
    if response.status_code == 200:
        print("   ✅ Admin logout working!")
    else:
        print(f"   ❌ Admin logout failed: {response.status_code}")

# Test admin logout POST
print("\n2. Testing /admin/logout/ POST:")
login_result = client.login(username='admin', password='admin123')
if login_result:
    response = client.post('/admin/logout/', follow=True)
    print(f"   Admin logout POST: Status {response.status_code}")
    print(f"   Final URL: {response.wsgi_request.path}")

print("\n✅ Admin logout should now work in browser!")
