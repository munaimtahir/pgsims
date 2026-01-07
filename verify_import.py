#!/usr/bin/env python3
"""
Script to verify trainee data import.
Run this after importing to verify the data was imported correctly.
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

from sims.users.models import User

def verify_import():
    """Verify that trainee data was imported correctly."""
    print("="*60)
    print("VERIFYING TRAINEE DATA IMPORT")
    print("="*60)
    
    # Get all urology trainees
    trainees = User.objects.filter(role='pg', specialty='urology')
    total_count = trainees.count()
    
    print(f"\nTotal Urology Trainees: {total_count}")
    
    if total_count == 0:
        print("\n⚠ No trainees found. Please run the import first.")
        return
    
    # Statistics
    print("\n" + "="*60)
    print("STATISTICS")
    print("="*60)
    
    # By year
    year_counts = {}
    for trainee in trainees:
        year = trainee.year or "Unknown"
        year_counts[year] = year_counts.get(year, 0) + 1
    
    print("\nBy Training Year:")
    for year, count in sorted(year_counts.items()):
        print(f"  Year {year}: {count} trainees")
    
    # With supervisors
    with_supervisor = trainees.filter(supervisor__isnull=False).count()
    without_supervisor = total_count - with_supervisor
    
    print(f"\nSupervisor Assignment:")
    print(f"  With supervisor: {with_supervisor}")
    print(f"  Without supervisor: {without_supervisor}")
    
    # Email format check
    correct_email_format = trainees.filter(email__endswith='.pgr@pmc.edu.pk').count()
    print(f"\nEmail Format:")
    print(f"  Correct format (.pgr@pmc.edu.pk): {correct_email_format}")
    print(f"  Other formats: {total_count - correct_email_format}")
    
    # Sample data
    print("\n" + "="*60)
    print("SAMPLE DATA (First 10 trainees)")
    print("="*60)
    
    for trainee in trainees[:10]:
        supervisor_name = trainee.supervisor.get_full_name() if trainee.supervisor else "None"
        print(f"\n  Username: {trainee.username}")
        print(f"  Name: {trainee.get_full_name()}")
        print(f"  Email: {trainee.email}")
        print(f"  Year: {trainee.year}")
        print(f"  Supervisor: {supervisor_name}")
        print(f"  Date Joined: {trainee.date_joined}")
        if trainee.registration_number:
            print(f"  Qualification: {trainee.registration_number}")
    
    if total_count > 10:
        print(f"\n  ... and {total_count - 10} more trainees")
    
    # Check supervisors
    supervisors = User.objects.filter(role='supervisor', specialty='urology')
    print("\n" + "="*60)
    print(f"UROLOGY SUPERVISORS: {supervisors.count()}")
    print("="*60)
    
    for supervisor in supervisors[:10]:
        pg_count = supervisor.assigned_pgs.filter(specialty='urology').count()
        print(f"\n  {supervisor.get_full_name()} ({supervisor.username})")
        print(f"    Email: {supervisor.email}")
        print(f"    Assigned PGs: {pg_count}")
    
    print("\n" + "="*60)
    print("VERIFICATION COMPLETE")
    print("="*60)

if __name__ == '__main__':
    verify_import()
