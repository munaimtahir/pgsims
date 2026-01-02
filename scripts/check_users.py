#!/usr/bin/env python
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

from sims.users.models import User

print("=== SIMS USER DETAILS ===")
print(f"Total Users: {User.objects.count()}")
print("\nUser List:")
print("-" * 80)

for user in User.objects.all():
    print(f"Username: {user.username}")
    print(f"Full Name: {user.get_full_name() or 'Not provided'}")
    print(f"Email: {user.email or 'Not provided'}")
    print(f"Role: {user.get_role_display()}")
    print(f"Specialty: {user.get_specialty_display() if user.specialty else 'Not specified'}")
    print(f"Year: {user.year or 'Not specified'}")
    print(f"Supervisor: {user.supervisor.get_full_name() if user.supervisor else 'None'}")
    print(f"Active: {'Yes' if user.is_active else 'No'}")
    print(f"Staff: {'Yes' if user.is_staff else 'No'}")
    print(f"Superuser: {'Yes' if user.is_superuser else 'No'}")
    print(f"Date Joined: {user.date_joined.strftime('%Y-%m-%d %H:%M')}")
    print(f"Last Login: {user.last_login.strftime('%Y-%m-%d %H:%M') if user.last_login else 'Never'}")
    print("-" * 80)

if User.objects.count() == 0:
    print("No users found in the database.")
    print("\nTo create a superuser, run:")
    print("py manage.py createsuperuser")
