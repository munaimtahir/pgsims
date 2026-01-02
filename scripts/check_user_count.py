#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

from django.test import Client
from sims.users.models import User

client = Client()

print("🔍 CHECKING USER LIST COUNT")
print("=" * 40)

# Check actual user counts in database
total_users = User.objects.count()
active_users = User.objects.filter(is_archived=False).count()
archived_users = User.objects.filter(is_archived=True).count()

print(f"📊 DATABASE COUNTS:")
print(f"   Total users in DB: {total_users}")
print(f"   Active users (not archived): {active_users}")
print(f"   Archived users: {archived_users}")

print(f"\n👥 USER BREAKDOWN:")
for user in User.objects.all():
    status = "ARCHIVED" if user.is_archived else "ACTIVE"
    print(f"   {user.username} ({user.role}) - {status}")

# Test the user list view
print(f"\n🌐 TESTING USER LIST VIEW:")
login_result = client.login(username='admin', password='admin123')
print(f"   Admin login: {'SUCCESS' if login_result else 'FAILED'}")

if login_result:
    response = client.get('/users/list/')
    print(f"   User list page: {'SUCCESS' if response.status_code == 200 else f'ERROR {response.status_code}'}")
    
    if response.status_code == 200:
        # Check the context
        context = response.context
        users_queryset = context.get('users')
        if users_queryset:
            displayed_count = users_queryset.paginator.count
            print(f"   Users displayed: {displayed_count}")
            print(f"   Expected count: {active_users}")
            
            if displayed_count == active_users:
                print("   ✅ Count is CORRECT")
            else:
                print("   ❌ Count is WRONG")
                print(f"   Difference: {abs(displayed_count - active_users)}")
        else:
            print("   ❌ No users context found")

print(f"\n💡 EXPECTED BEHAVIOR:")
print(f"   User list should show: {active_users} users")
print(f"   (Only non-archived users should be displayed)")
