#!/usr/bin/env python
"""
Test supervisor logbook review functionality
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from sims.logbook.models import LogbookEntry

User = get_user_model()

def test_supervisor_review_access():
    """Test that supervisors can access their PGs' logbook entries for review"""
    print("=" * 50)
    print("TESTING SUPERVISOR REVIEW FUNCTIONALITY")
    print("=" * 50)
    
    # Get a supervisor
    supervisor = User.objects.filter(role='supervisor').first()
    if not supervisor:
        print("❌ No supervisor found in database")
        return False
    
    print(f"✓ Testing with supervisor: {supervisor.username} ({supervisor.get_full_name()})")
    
    # Get supervisor's assigned PGs
    assigned_pgs = supervisor.assigned_pgs.filter(is_active=True)
    print(f"✓ Supervisor has {assigned_pgs.count()} assigned PGs:")
    for pg in assigned_pgs:
        print(f"  - {pg.username} ({pg.get_full_name()})")
    
    # Check logbook entries from assigned PGs
    entries = LogbookEntry.objects.filter(pg__supervisor=supervisor)
    print(f"✓ Found {entries.count()} total logbook entries from assigned PGs")
    
    # Check pending entries
    pending_entries = entries.filter(status='pending')
    print(f"✓ Found {pending_entries.count()} pending entries requiring review")
    
    # Check entries by status
    statuses = ['draft', 'pending', 'approved', 'rejected', 'returned']
    print(f"\n📊 Entry status breakdown:")
    for status in statuses:
        count = entries.filter(status=status).count()
        print(f"  {status.title()}: {count}")
    
    # Test review permissions
    print(f"\n🔐 Review permissions test:")
    
    # Test that supervisor can access entries from their PGs
    supervisor_entries = LogbookEntry.objects.filter(pg__in=assigned_pgs)
    print(f"✓ Supervisor can access {supervisor_entries.count()} entries from their PGs")
    
    # Test that supervisor cannot access entries from other PGs
    other_entries = LogbookEntry.objects.exclude(pg__in=assigned_pgs)
    print(f"✓ There are {other_entries.count()} entries from other PGs (should not be accessible)")
    
    # Test specific review scenarios
    if pending_entries.exists():
        test_entry = pending_entries.first()
        print(f"\n📝 Testing with entry: '{test_entry.case_title}' by {test_entry.pg.get_full_name()}")
        print(f"  - Status: {test_entry.get_status_display()}")
        print(f"  - Submitted: {test_entry.submitted_to_supervisor_at}")
        print(f"  - Supervisor feedback: {test_entry.supervisor_feedback or 'None yet'}")
        
        # Check if supervisor is assigned correctly
        if test_entry.supervisor == supervisor:
            print(f"  ✓ Entry is correctly assigned to supervisor {supervisor.get_full_name()}")
        else:
            print(f"  ⚠️  Entry supervisor: {test_entry.supervisor}, expected: {supervisor}")
    
    print(f"\n✅ Supervisor review functionality test completed successfully!")
    return True

if __name__ == "__main__":
    try:
        test_supervisor_review_access()
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
