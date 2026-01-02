#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

from sims.users.models import User
from django.contrib.auth.hashers import make_password

print("Creating sample supervisor users...")

# Create some supervisor users for different specialties
supervisors_data = [
    {
        'username': 'dr_cardiology',
        'email': 'cardiology@example.com',
        'first_name': 'Ahmed',
        'last_name': 'Hassan',
        'role': 'supervisor',
        'specialty': 'cardiology',
        'password': 'supervisor123'
    },
    {
        'username': 'dr_surgery',
        'email': 'surgery@example.com',
        'first_name': 'Sarah',
        'last_name': 'Khan',
        'role': 'supervisor',
        'specialty': 'surgery',
        'password': 'supervisor123'
    },
    {
        'username': 'dr_medicine',
        'email': 'medicine@example.com',
        'first_name': 'Mohammad',
        'last_name': 'Ali',
        'role': 'supervisor',
        'specialty': 'medicine',
        'password': 'supervisor123'
    },
    {
        'username': 'dr_pediatrics',
        'email': 'pediatrics@example.com',
        'first_name': 'Fatima',
        'last_name': 'Ahmed',
        'role': 'supervisor',
        'specialty': 'pediatrics',
        'password': 'supervisor123'
    }
]

created_count = 0
for sup_data in supervisors_data:
    username = sup_data['username']
    if not User.objects.filter(username=username).exists():
        password = sup_data.pop('password')
        user = User(**sup_data)
        user.set_password(password)
        user.save()
        print(f"Created supervisor: {username} ({sup_data['specialty']})")
        created_count += 1
    else:
        print(f"Supervisor {username} already exists")

print(f"\nCreated {created_count} new supervisors")

# Create a test PG user
pg_data = {
    'username': 'pg_test',
    'email': 'pg@example.com',
    'first_name': 'Test',
    'last_name': 'PG',
    'role': 'pg',
    'specialty': 'cardiology',
    'year': '1',
    'password': 'pg123'
}

if not User.objects.filter(username=pg_data['username']).exists():
    password = pg_data.pop('password')
    # Assign a supervisor (get the cardiology supervisor we just created)
    cardiology_supervisor = User.objects.filter(role='supervisor', specialty='cardiology').first()
    if cardiology_supervisor:
        pg_data['supervisor'] = cardiology_supervisor
    user = User(**pg_data)
    user.set_password(password)
    user.save()
    print(f"Created PG user: pg_test")
else:
    print(f"PG user pg_test already exists")

print("\n=== FINAL USER COUNT ===")
print(f"Total users: {User.objects.count()}")
print(f"Supervisors: {User.objects.filter(role='supervisor').count()}")
print(f"PG users: {User.objects.filter(role='pg').count()}")
print(f"Admin users: {User.objects.filter(role='admin').count()}")

print("\n=== AVAILABLE SPECIALTIES ===")
specialties = User.objects.filter(role='supervisor').values_list('specialty', flat=True).distinct()
for spec in specialties:
    print(f"- {spec}")
