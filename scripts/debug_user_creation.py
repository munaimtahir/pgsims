#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

from django.test import Client
from sims.users.models import User

client = Client()

print("🔧 DEBUGGING USER CREATION FORM")
print("=" * 50)

# Login as admin
client.login(username='admin', password='admin123')

# Test what happens with minimal data (similar to manual form filling)
print("1. 🧪 TESTING MINIMAL FORM DATA:")
minimal_data = {
    'role': 'supervisor',  # Note: not selectedRole, just role
    'username': 'debug_user',
    'email': 'debug@example.com',
    'first_name': 'Debug',
    'last_name': 'User',
    'specialty': 'surgery',
    'password1': 'debugpass123',
    'password2': 'debugpass123',
}

initial_count = User.objects.count()
response = client.post('/users/create/', minimal_data, follow=True)

print(f"   Response status: {response.status_code}")
print(f"   Initial count: {initial_count}")
print(f"   Final count: {User.objects.count()}")
print(f"   User created: {'✅ YES' if User.objects.filter(username='debug_user').exists() else '❌ NO'}")

# Check if redirected properly
final_url = response.request['PATH_INFO'] if hasattr(response, 'request') else 'Unknown'
print(f"   Final URL: {final_url}")

# Check for error messages in response
content = response.content.decode()
if 'error' in content.lower() or 'alert' in content.lower():
    print(f"   ⚠️  Response contains error messages")

# Test 2: Check what happens with missing required fields
print(f"\n2. 🧪 TESTING WITH MISSING FIELDS:")
incomplete_data = {
    'username': 'incomplete_user',
    'email': 'incomplete@example.com',
    # Missing role, names, passwords
}

response2 = client.post('/users/create/', incomplete_data)
print(f"   Status with incomplete data: {response2.status_code}")
print(f"   User created with incomplete data: {'❌ YES (BAD)' if User.objects.filter(username='incomplete_user').exists() else '✅ NO (GOOD)'}")

# Test 3: Check the UserCreateView directly
print(f"\n3. 🔍 ANALYZING VIEW LOGIC:")
# Let's check what the view expects vs what we're sending

print(f"   Testing exact field names from template...")

# Get the form page to see what fields are expected
form_response = client.get('/users/create/')
form_content = form_response.content.decode()

# Look for specific field names
required_fields = ['username', 'email', 'first_name', 'last_name', 'role', 'password1', 'password2']
for field in required_fields:
    if f'name="{field}"' in form_content:
        print(f"   ✅ {field} field found in form")
    else:
        print(f"   ❌ {field} field missing in form")

print(f"\n💡 DIAGNOSIS:")
successful_creation = User.objects.filter(username='debug_user').exists()
if successful_creation:
    print(f"   ✅ Form submission WORKS programmatically")
    print(f"   🔍 Issue is likely in browser JavaScript or UI")
    print(f"   🔧 Recommendations:")
    print(f"      - Check browser console for JavaScript errors")
    print(f"      - Check if validation alerts are blocking submission")
    print(f"      - Verify role selection is working")
    print(f"      - Check if loading modal is preventing completion")
else:
    print(f"   ❌ Form submission FAILS even programmatically")
    print(f"   🔍 Issue is in the Django view logic")

print(f"\n🧪 NEXT STEPS:")
print(f"   1. Test in browser with developer tools open")
print(f"   2. Check JavaScript console for errors")
print(f"   3. Verify all form fields are filled properly")
print(f"   4. Check if role selection works (click the role cards)")
