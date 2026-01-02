#!/usr/bin/env python
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

from sims.users.models import User

def check_users():
    print("=== User Database Analysis ===")
    
    # Check total users
    total_users = User.objects.all().count()
    print(f"Total users: {total_users}")
    
    if total_users == 0:
        print("No users found. Creating sample users...")
        
        # Create admin user
        admin = User.objects.create_user(
            username='admin',
            password='admin123',
            email='admin@example.com',
            first_name='System',
            last_name='Administrator',
            role='admin',
            is_staff=True,
            is_superuser=True
        )
        print(f"Created admin user: {admin.username}")
        
        # Create sample PGs with specialties
        specialties = [
            'Internal Medicine', 'Surgery', 'Pediatrics', 
            'Obstetrics & Gynecology', 'Psychiatry', 'Radiology'
        ]
        
        for i, specialty in enumerate(specialties):
            pg = User.objects.create_user(
                username=f'pg{i+1}',
                password='pg123',
                email=f'pg{i+1}@example.com',
                first_name=f'PG{i+1}',
                last_name='Doctor',
                role='pg',
                specialty=specialty
            )
            print(f"Created PG: {pg.username} - {specialty}")
        
        # Create some supervisors
        supervisor_specialties = ['Internal Medicine', 'Surgery', 'Pediatrics']
        for i, specialty in enumerate(supervisor_specialties):
            supervisor = User.objects.create_user(
                username=f'supervisor{i+1}',
                password='supervisor123',
                email=f'supervisor{i+1}@example.com',
                first_name=f'Dr. Supervisor{i+1}',
                last_name='Doctor',
                role='supervisor',
                specialty=specialty,
                is_staff=True
            )
            print(f"Created Supervisor: {supervisor.username} - {specialty}")
        
        print(f"\nCreated {User.objects.count()} users total")
    
    else:
        print("\nExisting users:")
        for user in User.objects.all()[:10]:  # Show first 10 users
            print(f"  {user.username} ({user.role}) - {user.specialty or 'No specialty'}")
        
        if total_users > 10:
            print(f"  ... and {total_users - 10} more users")
    
    # Check specialty distribution
    print("\n=== Specialty Distribution ===")
    from django.db.models import Count
    specialty_stats = User.objects.values('specialty').annotate(count=Count('id')).order_by('-count')
    
    for stat in specialty_stats:
        specialty = stat['specialty'] or 'Unspecified'
        count = stat['count']
        print(f"  {specialty}: {count} users")
    
    print(f"\nTotal specialties: {len(specialty_stats)}")

if __name__ == "__main__":
    check_users()
