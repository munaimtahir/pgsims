#!/usr/bin/env python
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

from sims.users.models import User
from django.http import JsonResponse
from django.db.models import Count

def simple_test():
    print("=== Simple User Data Test ===")
    
    # Get all users
    users = User.objects.all()
    print(f"Total users in database: {users.count()}")
    
    if users.count() == 0:
        print("Creating sample users...")
        
        # Create admin
        admin = User.objects.create_user(
            username='admin',
            password='admin123',
            role='admin',
            is_staff=True,
            is_superuser=True,
            first_name='Admin',
            last_name='User'
        )
        
        # Create PGs with specialties
        specialties = ['Internal Medicine', 'Surgery', 'Pediatrics', 'Cardiology']
        for i, specialty in enumerate(specialties):
            User.objects.create_user(
                username=f'pg{i+1}',
                password='pg123',
                role='pg',
                specialty=specialty,
                first_name=f'PG{i+1}',
                last_name='Doctor'
            )
        
        print(f"Created {User.objects.count()} users")
    
    # Test specialty distribution
    specialty_stats_qs = User.objects.values('specialty').annotate(
        count=Count('id')
    ).order_by('-count')
    
    specialty_stats = []
    total_count = User.objects.count()
    
    print("\nSpecialty Distribution:")
    for item in specialty_stats_qs:
        specialty_name = item['specialty'] or 'Unspecified'
        count = item['count']
        percentage = round((count / total_count * 100), 1) if total_count > 0 else 0
        
        specialty_stats.append({
            'specialty': specialty_name,
            'count': count,
            'percentage': percentage
        })
        
        print(f"  {specialty_name}: {count} users ({percentage}%)")
    
    # Mock the API response
    response_data = {
        'total_users': User.objects.count(),
        'total_pgs': User.objects.filter(role='pg').count(),
        'total_supervisors': User.objects.filter(role='supervisor').count(),
        'new_users_this_month': 0,
        'recent_users': [],
        'specialty_stats': specialty_stats,
        'filter_applied': {
            'role': 'all',
            'period': 'all',
            'total_filtered': total_count
        },
        'summary': {
            'total_specialties': len(specialty_stats),
            'most_popular': specialty_stats[0]['specialty'] if specialty_stats else 'None',
            'average_per_specialty': round(total_count / len(specialty_stats), 1) if len(specialty_stats) > 0 else 0,
            'unspecified_count': sum(1 for item in specialty_stats if item['specialty'] == 'Unspecified')
        },
        'status': 'success'
    }
    
    print(f"\nMock API Response:")
    import json
    print(json.dumps(response_data, indent=2))
    
    return response_data

if __name__ == "__main__":
    simple_test()
