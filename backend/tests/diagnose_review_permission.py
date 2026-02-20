#!/usr/bin/env python
"""
Diagnose logbook review permission issues
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from sims.logbook.models import LogbookEntry, LogbookReview

User = get_user_model()

def diagnose_review_permission():
    """Diagnose why review permission is failing"""
    print("=" * 60)
    print("DIAGNOSING LOGBOOK REVIEW PERMISSION ISSUE")
    print("=" * 60)
    
    # Check entry ID 1
    try:
        entry = LogbookEntry.objects.get(pk=1)
        print(f"✓ Found LogbookEntry ID 1:")
        print(f"  - Case Title: {entry.case_title}")
        print(f"  - Status: {entry.status} ({entry.get_status_display()})")
        print(f"  - PG: {entry.pg.username} ({entry.pg.get_full_name()})")
        print(f"  - PG Role: {entry.pg.role}")
        print(f"  - Supervisor: {entry.supervisor}")
        print(f"  - PG's Supervisor: {entry.pg.supervisor}")
        print(f"  - Created: {entry.created_at}")
        if entry.submitted_to_supervisor_at:
            print(f"  - Submitted: {entry.submitted_to_supervisor_at}")
        else:
            print(f"  - Submitted: Not submitted yet")
    except LogbookEntry.DoesNotExist:
        print("❌ LogbookEntry ID 1 does not exist")
        return
    
    print(f"\n" + "=" * 40)
    print("CHECKING USERS AND ROLES")
    print("=" * 40)
    
    # Check all users and their roles
    users = User.objects.all()
    for user in users:
        print(f"User: {user.username} ({user.get_full_name()})")
        print(f"  - Role: {user.role}")
        print(f"  - Active: {user.is_active}")
        if user.role == 'supervisor':
            assigned_pgs = user.assigned_pgs.all()
            print(f"  - Assigned PGs: {[pg.username for pg in assigned_pgs]}")
        elif user.role == 'pg':
            print(f"  - Supervisor: {user.supervisor}")
        print()
    
    print("=" * 40)
    print("PERMISSION CHECK SIMULATION")
    print("=" * 40)
    
    # Simulate permission checks for each user
    for user in users:
        print(f"\nTesting user: {user.username} (role: {user.role})")
        
        # Test 1: Role-based access
        if user.role == 'supervisor':
            if entry.pg.supervisor == user:
                print(f"  ✓ Supervisor check passed: User supervises {entry.pg.username}")
            else:
                print(f"  ❌ Supervisor check failed: User does not supervise {entry.pg.username}")
                print(f"     Entry PG's supervisor: {entry.pg.supervisor}")
        elif user.role == 'admin':
            print(f"  ✓ Admin access: Should have permission")
        else:
            print(f"  ❌ Role check failed: Role '{user.role}' cannot review entries")
        
        # Test 2: Entry status check
        if entry.status == 'submitted':
            print(f"  ✓ Status check passed: Entry is submitted")
        else:
            print(f"  ❌ Status check failed: Entry status is '{entry.status}', not 'submitted'")
        
        # Test 3: Already reviewed check
        existing_review = LogbookReview.objects.filter(
            logbook_entry=entry,
            reviewer=user
        ).first()
        if existing_review:
            print(f"  ❌ Already reviewed: User has already reviewed this entry")
        else:
            print(f"  ✓ No existing review: User has not reviewed this entry yet")
    
    print(f"\n" + "=" * 40)
    print("RECOMMENDATIONS")
    print("=" * 40)
    
    # Provide recommendations based on findings
    if entry.status != 'submitted':
        print(f"❗ Entry status is '{entry.status}' but needs to be 'submitted' for review")
        print(f"   - You may need to update the entry status to 'submitted' or 'pending'")
    
    if not entry.pg.supervisor:
        print(f"❗ Entry's PG ({entry.pg.username}) has no assigned supervisor")
        print(f"   - Assign a supervisor to the PG or update the entry's supervisor field")
    
    supervisors = User.objects.filter(role='supervisor')
    if not supervisors.exists():
        print(f"❗ No supervisors found in the system")
        print(f"   - Create supervisor users or update existing user roles")
    
    print(f"\n✅ Diagnosis completed!")

if __name__ == "__main__":
    try:
        diagnose_review_permission()
    except Exception as e:
        print(f"❌ Error during diagnosis: {e}")
        import traceback
        traceback.print_exc()
