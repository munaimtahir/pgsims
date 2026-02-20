#!/usr/bin/env python3
"""
Comprehensive setup script for testing logbook review functionality.
This script ensures proper test data exists for the review form.

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
from sims.logbook.models import LogbookEntry, LogbookReview
from sims.rotations.models import Rotation
from datetime import date

User = get_user_model()

def setup_test_environment():
    """Set up complete test environment for review testing"""
    print("=== Setting Up Test Environment for Review ===")
    
    # 1. Check and create supervisor user
    supervisor = User.objects.filter(role='supervisor').first()
    if not supervisor:
        print("Creating supervisor user...")
        supervisor = User.objects.create_user(
            username='test_supervisor',
            email='supervisor@test.com',
            password='testpass123',
            first_name='Test',
            last_name='Supervisor',
            role='supervisor'
        )
    
    print(f"Supervisor: {supervisor.username} ({supervisor.id})")
    
    # 2. Check and create PG user
    pg = User.objects.filter(role='pg').first()
    if not pg:
        print("Creating PG user...")
        pg = User.objects.create_user(
            username='test_pg',
            email='pg@test.com',
            password='testpass123',
            first_name='Test',
            last_name='PG',
            role='pg'
        )
    
    # Assign supervisor to PG
    if not pg.supervisor:
        pg.supervisor = supervisor
        pg.save()
        print(f"Assigned supervisor {supervisor.username} to PG {pg.username}")
    
    print(f"PG: {pg.username} ({pg.id}) - Supervisor: {pg.supervisor}")
    
    # 3. Check and create rotation
    rotation = Rotation.objects.first()
    if not rotation:
        print("Creating test rotation...")
        rotation = Rotation.objects.create(
            name='Test Rotation',
            department='Test Department',
            duration_weeks=4,
            start_date=date.today(),
            end_date=date.today()
        )
    
    print(f"Rotation: {rotation.name} ({rotation.id})")
    
    # 4. Create or update logbook entry with ID 1
    entry = None
    if LogbookEntry.objects.filter(id=1).exists():
        entry = LogbookEntry.objects.get(id=1)
        print(f"Found existing entry 1: {entry.case_title} - Status: {entry.status}")
        
        # Update to ensure it's reviewable
        entry.pg = pg
        entry.supervisor = supervisor
        entry.status = 'pending'
        entry.save()
        print("Updated entry 1 to be reviewable")
        
    else:
        print("Creating new entry with ID 1...")
        # Delete any existing entry to create with specific ID
        LogbookEntry.objects.filter(id=1).delete()
        
        entry = LogbookEntry(
            id=1,
            pg=pg,
            supervisor=supervisor,
            date=date.today(),
            rotation=rotation,
            case_title="Test Case for Review",
            patient_age=45,
            patient_gender='M',
            patient_chief_complaint="Patient presents with chest pain",
            patient_history_summary="No significant past medical history",
            primary_diagnosis="Acute chest pain - rule out MI",
            clinical_reasoning="Given age and presentation, need to rule out cardiac causes",
            learning_points="Importance of rapid assessment in chest pain",
            self_assessment_score=7,
            status='pending'
        )
        entry.save()
        print(f"Created entry 1: {entry.case_title}")
    
    # 5. Clean up any existing reviews to allow new review
    existing_reviews = LogbookReview.objects.filter(
        logbook_entry=entry,
        reviewer=supervisor
    )
    if existing_reviews.exists():
        print(f"Removing {existing_reviews.count()} existing reviews to allow new review")
        existing_reviews.delete()
    
    print("\n=== Test Environment Ready ===")
    print(f"Entry URL: http://127.0.0.1:8000/logbook/entry/{entry.id}/review/")
    print(f"Entry can be reviewed by supervisor: {supervisor.username}")
    print(f"Entry status: {entry.status}")
    print(f"Entry PG: {entry.pg} (supervisor: {entry.pg.supervisor})")
    
    return entry, supervisor, pg

if __name__ == "__main__":
    setup_test_environment()
