#!/usr/bin/env python
"""
Create a test logbook entry for review testing
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from sims.logbook.models import LogbookEntry
from django.utils import timezone

User = get_user_model()

def create_test_entry():
    """Create a test logbook entry for review"""
    print("=" * 50)
    print("CREATING TEST LOGBOOK ENTRY")
    print("=" * 50)
    
    # Get a supervisor and PG
    supervisor = User.objects.filter(role='supervisor').first()
    if not supervisor:
        print("❌ No supervisor found. Creating one...")
        supervisor = User.objects.create_user(
            username='test_supervisor',
            email='supervisor@test.com',
            password='test123',
            role='supervisor',
            first_name='Test',
            last_name='Supervisor'
        )
        print(f"✓ Created supervisor: {supervisor.username}")
    
    pg = supervisor.assigned_pgs.first()
    if not pg:
        print("❌ No PG assigned to supervisor. Creating one...")
        pg = User.objects.create_user(
            username='test_pg',
            email='pg@test.com',
            password='test123',
            role='pg',
            first_name='Test',
            last_name='PG',
            supervisor=supervisor
        )
        print(f"✓ Created PG: {pg.username} assigned to {supervisor.username}")
    
    print(f"✓ Using supervisor: {supervisor.username}")
    print(f"✓ Using PG: {pg.username}")
    
    # Create a test entry
    entry = LogbookEntry.objects.create(
        pg=pg,
        supervisor=supervisor,
        case_title="Test Case for Review",
        date=timezone.now().date(),
        location_of_activity="Test Ward",
        patient_history_summary="Test patient with test condition",
        management_action="Test management plan",
        topic_subtopic="Test Topic",
        status='pending',  # Set to pending for review
        submitted_to_supervisor_at=timezone.now(),
        created_by=pg
    )
    
    print(f"✓ Created test entry:")
    print(f"  - ID: {entry.id}")
    print(f"  - Title: {entry.case_title}")
    print(f"  - Status: {entry.status}")
    print(f"  - PG: {entry.pg.username}")
    print(f"  - Supervisor: {entry.supervisor.username}")
    print(f"  - Submitted: {entry.submitted_to_supervisor_at}")
    
    # Test URL
    review_url = f"http://127.0.0.1:8000/logbook/entry/{entry.id}/review/"
    print(f"\n🔗 Test review URL: {review_url}")
    
    print(f"\n📝 To test:")
    print(f"1. Login as supervisor: {supervisor.username} / test123")
    print(f"2. Visit: {review_url}")
    print(f"3. Should be able to review the entry")
    
    return entry

if __name__ == "__main__":
    try:
        create_test_entry()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
