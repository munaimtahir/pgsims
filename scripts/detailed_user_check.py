#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

from django.test import Client
from sims.users.models import User

client = Client()

print("🔍 DETAILED USER LIST ANALYSIS")
print("=" * 50)

# Check user counts
print("📊 CURRENT USER COUNTS:")
total_users = User.objects.count()
active_users = User.objects.filter(is_archived=False).count()
print(f"   Total: {total_users}")
print(f"   Active (not archived): {active_users}")

# Test user list page with content analysis
client.login(username='admin', password='admin123')
response = client.get('/users/list/')

if response.status_code == 200:
    content = response.content.decode()
    print(f"\n✅ Page loads successfully")
    
    # Look for the count in the HTML
    import re
    
    # Search for the total users count
    total_pattern = r'<h3[^>]*id="total-users"[^>]*>(\d+)</h3>'
    total_match = re.search(total_pattern, content)
    
    if total_match:
        displayed_count = total_match.group(1)
        print(f"📋 DISPLAYED COUNT: {displayed_count}")
        print(f"📋 EXPECTED COUNT: {active_users}")
        
        if int(displayed_count) == active_users:
            print("✅ Count is CORRECT!")
        else:
            print("❌ Count is INCORRECT!")
            
    else:
        print("❌ Could not find count in HTML")
        
    # Also check the header count
    header_pattern = r'Users \((\d+) total\)'
    header_match = re.search(header_pattern, content)
    
    if header_match:
        header_count = header_match.group(1)
        print(f"📋 HEADER COUNT: {header_count}")
    
    # Check if all expected users are listed
    user_list = User.objects.filter(is_archived=False)
    print(f"\n👥 CHECKING USER VISIBILITY:")
    for user in user_list:
        if user.username in content:
            print(f"   ✅ {user.username} is visible")
        else:
            print(f"   ❌ {user.username} is MISSING")
            
else:
    print(f"❌ Page failed to load: {response.status_code}")

print(f"\n💡 SUMMARY:")
print(f"   Expected users to show: {active_users}")
print(f"   All users are active (non-archived)")
print(f"   User list should display all {active_users} users")
