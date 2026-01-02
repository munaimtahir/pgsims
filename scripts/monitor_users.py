#!/usr/bin/env python
"""
Monitor Django logs for user creation form submissions
"""
import os
import sys
import django

# Setup Django
sys.path.append('d:/PMC/sims_project-2')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

from django.contrib.auth import get_user_model
import time

User = get_user_model()

def monitor_users():
    """Monitor user creation"""
    print("=== User Creation Monitor ===")
    print("Current users:")
    
    users = User.objects.all().order_by('-date_joined')
    for user in users[:10]:  # Show last 10 users
        print(f"  {user.username} ({user.role}) - Created: {user.date_joined}")
    
    print(f"\nTotal users: {User.objects.count()}")
    print("\nMonitoring for new users... (Check back after creating a user)")
    
    # Wait and check again
    time.sleep(1)
    
    print("\n=== After potential creation ===")
    new_users = User.objects.all().order_by('-date_joined')
    for user in new_users[:5]:  # Show last 5 users
        print(f"  {user.username} ({user.role}) - Created: {user.date_joined}")
    
    print(f"Total users now: {User.objects.count()}")

if __name__ == '__main__':
    monitor_users()
