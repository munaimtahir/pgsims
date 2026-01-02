import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Test basic functionality
print("Testing User model relationships...")

supervisors = User.objects.filter(role='supervisor')
print(f"Found {supervisors.count()} supervisors")

if supervisors.exists():
    supervisor = supervisors.first()
    print(f"Testing supervisor: {supervisor.username}")
    
    # Test the assigned_pgs relationship
    try:
        pgs = supervisor.assigned_pgs.all()
        print(f"assigned_pgs query successful: {pgs.count()} PGs found")
        for pg in pgs[:3]:  # Show first 3
            print(f"  - {pg.username}")
    except Exception as e:
        print(f"Error with assigned_pgs: {e}")
        
    # Test filtering
    try:
        active_pgs = supervisor.assigned_pgs.filter(is_active=True)
        print(f"Active assigned PGs: {active_pgs.count()}")
    except Exception as e:
        print(f"Error filtering assigned_pgs: {e}")

print("Test completed.")
