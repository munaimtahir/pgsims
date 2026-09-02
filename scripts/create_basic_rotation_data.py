#!/usr/bin/env python3
"""
Script to create basic departments and hospitals for rotation creation.

Created: 2025-01-27
Author: GitHub Copilot
"""

import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

from sims.rotations.models import Hospital
from sims.academics.models import Department


def create_basic_data():
    """Create basic departments and hospitals if they don't exist"""
    print("=== Creating Basic Rotation Data ===")

    # Create hospitals if they don't exist
    hospitals_data = [
        {"name": "Main Teaching Hospital", "address": "Main Street, City", "code": "MTH"},
        {"name": "City General Hospital", "address": "Central Avenue, City", "code": "CGH"},
        {"name": "Specialty Medical Center", "address": "Health Complex, City", "code": "SMC"},
    ]

    for hospital_data in hospitals_data:
        hospital, created = Hospital.objects.get_or_create(
            name=hospital_data["name"],
            defaults={
                "address": hospital_data["address"],
                "code": hospital_data["code"],
            }
        )
        if created:
            print(f"✓ Created hospital: {hospital.name}")
        else:
            print(f"- Hospital already exists: {hospital.name}")

    # Create departments if they don't exist
    departments_data = [
        {"name": "Internal Medicine", "code": "MED", "description": "General internal medicine rotation"},
        {"name": "Surgery", "code": "SURG", "description": "General surgery rotation"},
        {"name": "Pediatrics", "code": "PEDS", "description": "Pediatric medicine rotation"},
        {"name": "Emergency Medicine", "code": "ER", "description": "Emergency department rotation"},
        {"name": "Cardiology", "code": "CARD", "description": "Cardiovascular medicine rotation"},
        {"name": "Radiology", "code": "RAD", "description": "Medical imaging rotation"},
        {"name": "Anesthesiology", "code": "ANES", "description": "Anesthesiology rotation"},
        {"name": "Psychiatry", "code": "PSYCH", "description": "Mental health rotation"},
    ]

    for dept_data in departments_data:
        department, created = Department.objects.get_or_create(
            name=dept_data["name"],
            defaults={
                "code": dept_data["code"],
                "description": dept_data["description"],
            }
        )
        if created:
            print(f"✓ Created department: {department.name}")
        else:
            print(f"- Department already exists: {department.name}")

    print(f"\nTotal hospitals: {Hospital.objects.count()}")
    print(f"Total departments: {Department.objects.count()}")


if __name__ == "__main__":
    create_basic_data()
