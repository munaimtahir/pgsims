#!/usr/bin/env python3
"""
Test script to check rotation creation issues.

Created: 2025-01-27
Author: GitHub Copilot
"""

import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from sims.rotations.models import Rotation, Department, Hospital
from sims.rotations.forms import RotationCreateForm

User = get_user_model()

def test_rotation_create_setup():
    """Test rotation creation setup and requirements"""
    print("=== Testing Rotation Creation Setup ===")
    
    # Check users
    admin_users = User.objects.filter(role='admin')
    supervisor_users = User.objects.filter(role='supervisor')
    pg_users = User.objects.filter(role='pg')
    
    print(f"Admin users: {admin_users.count()}")
    print(f"Supervisor users: {supervisor_users.count()}")
    print(f"PG users: {pg_users.count()}")
    
    # Check if we have departments and hospitals
    departments = Department.objects.all()
    hospitals = Hospital.objects.all()
    
    print(f"Departments: {departments.count()}")
    for dept in departments[:3]:
        print(f"  - {dept.name}")
    
    print(f"Hospitals: {hospitals.count()}")
    for hospital in hospitals[:3]:
        print(f"  - {hospital.name}")
    
    # Test form creation with different user types
    test_users = [
        admin_users.first(),
        supervisor_users.first(),
        pg_users.first()
    ]
    
    for user in test_users:
        if user:
            print(f"\n--- Testing form for {user.role}: {user.username} ---")
            try:
                form = RotationCreateForm(user=user)
                print(f"✓ Form created successfully")
                print(f"  PG choices: {form.fields['pg'].queryset.count()}")
                print(f"  Department choices: {form.fields['department'].queryset.count()}")
                print(f"  Hospital choices: {form.fields['hospital'].queryset.count()}")
                print(f"  Supervisor choices: {form.fields['supervisor'].queryset.count()}")
            except Exception as e:
                print(f"❌ Error creating form: {e}")
                import traceback
                traceback.print_exc()
    
    # Check existing rotations
    rotations = Rotation.objects.all()
    print(f"\nExisting rotations: {rotations.count()}")
    for rotation in rotations[:3]:
        print(f"  - {rotation.pg} in {rotation.department} ({rotation.start_date} to {rotation.end_date})")

if __name__ == "__main__":
    test_rotation_create_setup()
