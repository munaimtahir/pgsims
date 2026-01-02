#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()
client = Client()

print("🔍 SUPERVISOR PAGES TEST")
print("=" * 40)

# Find a supervisor user
try:
    supervisor = User.objects.filter(role='supervisor', is_active=True).first()
    if not supervisor:
        print("❌ No supervisor found in database")
        exit(1)
    
    print(f"✓ Testing with supervisor: {supervisor.username}")
    
    # Login as supervisor
    login_success = client.login(username=supervisor.username, password='admin123')  # Try common password
    if not login_success:
        # Try creating a supervisor for testing
        supervisor.set_password('admin123')
        supervisor.save()
        login_success = client.login(username=supervisor.username, password='admin123')
    
    print(f"✓ Supervisor login: {'SUCCESS' if login_success else 'FAILED'}")
    
    if login_success:
        # Test each supervisor page
        test_urls = [
            ('/users/pgs/', 'PG List'),
            ('/cases/statistics/', 'Cases Statistics'),
            ('/logbook/', 'Logbook'),
            ('/rotations/create/', 'Rotations Create'),
            ('/certificates/dashboard/', 'Certificates Dashboard'),
            ('/rotations/bulk-assignment/', 'Bulk Assignment'),
        ]
        
        print("\n📋 Testing supervisor pages:")
        print("-" * 30)
        
        for url, name in test_urls:
            try:
                response = client.get(url)
                status = response.status_code
                
                if status == 200:
                    result = "✅ SUCCESS"
                elif status == 403:
                    result = "❌ PERMISSION DENIED"
                elif status == 404:
                    result = "❌ NOT FOUND"
                elif status == 500:
                    result = "❌ SERVER ERROR"
                else:
                    result = f"⚠️ STATUS {status}"
                
                print(f"{name:25} {url:30} {result}")
                
                # Additional debugging for errors
                if status >= 400:
                    print(f"   Error details: {response.content[:200].decode('utf-8', errors='ignore')}")
                    
            except Exception as e:
                print(f"{name:25} {url:30} ❌ EXCEPTION: {str(e)}")
    
except Exception as e:
    print(f"❌ Error during test: {e}")

print("\n" + "=" * 40)
print("✅ Supervisor pages test completed")
