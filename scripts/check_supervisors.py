#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

from sims.users.models import User

print("=== ALL USERS ===")
users = User.objects.all()
for user in users:
    print(f"Username: {user.username}, Role: {user.role}, Specialty: {user.specialty}")

print("\n=== SUPERVISORS ===")
supervisors = User.objects.filter(role='supervisor')
print(f"Total supervisors: {supervisors.count()}")
for supervisor in supervisors:
    print(f"Username: {supervisor.username}, Specialty: {supervisor.specialty}")

print("\n=== SPECIALTIES ===")
specialties = User.objects.filter(role='supervisor').values_list('specialty', flat=True).distinct()
print(f"Available specialties: {list(specialties)}")
