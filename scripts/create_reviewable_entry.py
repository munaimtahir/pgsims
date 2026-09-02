#!/usr/bin/env python3
"""
Script to create a test logbook entry for review testing if none exists.

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
from sims.logbook.models import LogbookEntry
from sims.rotations.models import Rotation
from datetime import date

User = get_user_model()

def create_test_entry():
    """Create a test logbook entry for review testing"""
    print("=== Creating Test Logbook Entry ===")
    
    # Check what entries exist
    entries = LogbookEntry.objects.all()
    print(f"Current entries: {entries.count()}")
    for entry in entries[:5]:
        print(f"  Entry {entry.id}: {entry.case_title} - Status: {entry.status} - PG: {entry.pg}")
    
    # Check users
    users = User.objects.all()
    print(f"\nUsers: {users.count()}")
    
    pgs = User.objects.filter(role='pg')
    supervisors = User.objects.filter(role='supervisor')
    
    print(f"PGs: {pgs.count()}")
    for pg in pgs[:3]:
        print(f"  PG: {pg.username} - Supervisor: {getattr(pg, 'supervisor', 'None')}")
    
    print(f"Supervisors: {supervisors.count()}")
    for supervisor in supervisors[:3]:
        assigned_pgs = getattr(supervisor, 'assigned_pgs', None)
        if assigned_pgs:
            print(f"  Supervisor: {supervisor.username} - Assigned PGs: {assigned_pgs.count()}")
        else:
            print(f"  Supervisor: {supervisor.username} - No assigned PGs")
    
    # Create a test entry if needed
    if LogbookEntry.objects.filter(id=1).exists():
        entry = LogbookEntry.objects.get(id=1)
        print(f"\nEntry 1 exists: {entry.case_title} - Status: {entry.status}")
        
        # Make sure it's in pending status for review
        if entry.status not in ['pending', 'submitted']:
            print(f"Updating entry status from {entry.status} to pending")
            entry.status = 'pending'
            entry.save()
            
    else:
        print("\nCreating new entry with ID 1...")
        # Get a PG and supervisor pair
        pg = pgs.first()
        if not pg:
            print("No PG users found. Cannot create test entry.")
            return
            
        supervisor = getattr(pg, 'supervisor', None)
        if not supervisor:
            supervisor = supervisors.first()
            if supervisor:
                print(f"Assigning supervisor {supervisor.username} to PG {pg.username}")
                pg.supervisor = supervisor
                pg.save()
        
        if not supervisor:
            print("No supervisor available. Cannot create test entry.")
            return
            
        # Get a rotation
        rotation = Rotation.objects.first()
        
        # Create the entry
        entry = LogbookEntry.objects.create(
            pg=pg,
            supervisor=supervisor,
            date=date.today(),
            rotation=rotation,
            case_title="Test Case for Review",
            patient_age=45,
            patient_gender='M',
            patient_chief_complaint="Test complaint",
            primary_diagnosis="Test diagnosis",
            clinical_reasoning="Test reasoning",
            learning_points="Test learning",
            self_assessment_score=7,
            status='pending'
        )
        print(f"Created entry {entry.id}: {entry.case_title}")

if __name__ == "__main__":
    create_test_entry()
