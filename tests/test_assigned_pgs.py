#!/usr/bin/env python
"""
Minimal test to verify assigned_pgs relationship works
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')

try:
    import django
    django.setup()
    
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    
    print("=" * 40)
    print("TESTING ASSIGNED_PGS RELATIONSHIP")
    print("=" * 40)
    
    # Check if User model has the field
    user_fields = [f.name for f in User._meta.get_fields()]
    print(f"User model fields: {user_fields}")
    
    # Check for supervisor field
    if 'supervisor' in user_fields:
        print("✓ supervisor field exists in User model")
        
        # Get the related_name
        supervisor_field = User._meta.get_field('supervisor')
        print(f"✓ supervisor field related_name: {supervisor_field.related_query_name()}")
        
    else:
        print("✗ supervisor field missing in User model")
    
    # Test actual relationship
    supervisors = User.objects.filter(role='supervisor')
    print(f"Found {supervisors.count()} supervisors")
    
    if supervisors.exists():
        supervisor = supervisors.first()
        print(f"Testing with supervisor: {supervisor.username}")
        
        # Test the relationship
        assigned_pgs = supervisor.assigned_pgs.all()
        print(f"✓ assigned_pgs relationship works: {assigned_pgs.count()} PGs")
        
        for pg in assigned_pgs[:3]:
            print(f"  - {pg.username} ({pg.get_full_name()})")
            
        print("✓ All tests passed - assigned_pgs relationship is working!")
    else:
        print("No supervisors found in database")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
