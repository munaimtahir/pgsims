#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

from django.test import Client
from sims.users.models import User

client = Client()

print("🔍 TESTING USER STATS API")
print("=" * 40)

# Get expected counts
total_users = User.objects.filter(is_archived=False).count()
active_users = User.objects.filter(is_active=True, is_archived=False).count()
pg_count = User.objects.filter(role='pg', is_archived=False).count()
supervisor_count = User.objects.filter(role='supervisor', is_archived=False).count()

print(f"📊 EXPECTED COUNTS:")
print(f"   Total users: {total_users}")
print(f"   Active users: {active_users}")
print(f"   PG users: {pg_count}")
print(f"   Supervisors: {supervisor_count}")

# Test the API
client.login(username='admin', password='admin123')
response = client.get('/users/api/stats/')

print(f"\n🌐 API TEST:")
print(f"   Status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    print(f"   ✅ API Response: {data}")
    
    # Check if all counts match
    checks = [
        ('total_users', data.get('total_users'), total_users),
        ('active_users', data.get('active_users'), active_users),
        ('pg_count', data.get('pg_count'), pg_count),
        ('supervisor_count', data.get('supervisor_count'), supervisor_count),
    ]
    
    all_correct = True
    for field, api_value, expected_value in checks:
        if api_value == expected_value:
            print(f"   ✅ {field}: {api_value} (correct)")
        else:
            print(f"   ❌ {field}: {api_value} (expected {expected_value})")
            all_correct = False
    
    if all_correct:
        print(f"\n🎉 ALL COUNTS ARE CORRECT!")
        print(f"   The user list page should now show the right numbers")
    else:
        print(f"\n❌ Some counts are incorrect")
        
else:
    print(f"   ❌ API failed: {response.status_code}")
    print(f"   Content: {response.content.decode()}")

print(f"\n🔗 Test the user list page: http://127.0.0.1:8000/users/list/")
