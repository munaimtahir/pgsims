#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

from django.test import Client
from sims.users.models import User

client = Client()

print("🔍 TESTING USER CREATION FORM")
print("=" * 50)

# Login as admin
client.login(username='admin', password='admin123')

# Get the creation form first
print("1. 📋 TESTING FORM ACCESS:")
response = client.get('/users/create/')
print(f"   Form page status: {'✅ SUCCESS' if response.status_code == 200 else f'❌ ERROR {response.status_code}'}")

if response.status_code != 200:
    print(f"   Cannot access form: {response.status_code}")
    exit()

# Get current user count
initial_count = User.objects.count()
print(f"   Initial user count: {initial_count}")

# Test creating a new user
print(f"\n2. 🆕 TESTING USER CREATION:")
new_user_data = {
    'username': 'test_form_user',
    'email': 'testform@example.com',
    'first_name': 'Test',
    'last_name': 'Form',
    'role': 'pg',
    'specialty': 'medicine',
    'year': '2',
    'password1': 'testpass123',
    'password2': 'testpass123',
    'supervisor_choice': '4',  # dr_medicine supervisor
    'phone_number': '1234567890',
    'registration_number': 'REG123'
}

print(f"   Submitting form with data:")
for key, value in new_user_data.items():
    if 'password' not in key:
        print(f"     {key}: {value}")

# Submit the form
response = client.post('/users/create/', new_user_data, follow=True)
print(f"   Form submission status: {response.status_code}")

# Check if user was created
final_count = User.objects.count()
user_created = User.objects.filter(username='test_form_user').exists()

print(f"   Final user count: {final_count}")
print(f"   User created: {'✅ YES' if user_created else '❌ NO'}")
print(f"   Count increased: {'✅ YES' if final_count > initial_count else '❌ NO'}")

if response.status_code == 200:
    # Check if there are any form errors in the response
    content = response.content.decode()
    if 'error' in content.lower() or 'invalid' in content.lower():
        print(f"   ⚠️  Response may contain errors")
        # Look for specific error messages
        if 'already exists' in content.lower():
            print(f"   🔍 Username or email already exists")
        if 'required' in content.lower():
            print(f"   🔍 Required field missing")
        if 'password' in content.lower() and 'match' in content.lower():
            print(f"   🔍 Password mismatch")

# If creation failed, test with different data
if not user_created:
    print(f"\n3. 🔄 TESTING WITH DIFFERENT DATA:")
    different_data = {
        'username': 'test_form_user2',
        'email': 'testform2@example.com',
        'first_name': 'Test2',
        'last_name': 'Form2',
        'role': 'supervisor',
        'specialty': 'surgery',
        'password1': 'testpass123',
        'password2': 'testpass123',
        'phone_number': '9876543210',
    }
    
    response2 = client.post('/users/create/', different_data, follow=True)
    user_created2 = User.objects.filter(username='test_form_user2').exists()
    print(f"   Second attempt: {'✅ SUCCESS' if user_created2 else '❌ FAILED'}")

print(f"\n4. 📊 FINAL STATUS:")
print(f"   Total users now: {User.objects.count()}")
print(f"   Users created by test: {User.objects.filter(username__startswith='test_form_user').count()}")

if not user_created:
    print(f"\n❌ USER CREATION FAILED!")
    print(f"   Need to check the form processing logic")
else:
    print(f"\n✅ USER CREATION WORKING!")
    print(f"   Form successfully creates users")
