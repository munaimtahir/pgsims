#!/usr/bin/env python
"""
Supervisor Functionality Test
Tests all supervisor-facing pages and functionality
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

def test_supervisor_functionality():
    """Test all supervisor pages and functionality"""
    User = get_user_model()
    client = Client()
    
    print("🔍 SUPERVISOR FUNCTIONALITY TEST")
    print("=" * 50)
    
    # Find or create a test supervisor
    try:
        supervisor = User.objects.filter(role='supervisor', is_active=True).first()
        if not supervisor:
            print("❌ No supervisor found. Creating test supervisor...")
            supervisor = User.objects.create_user(
                username='test_supervisor',
                email='supervisor@test.com',
                password='admin123',
                role='supervisor',
                first_name='Test',
                last_name='Supervisor'
            )
            print(f"✅ Created supervisor: {supervisor.username}")
        else:
            # Ensure the supervisor has a password we can use
            supervisor.set_password('admin123')
            supervisor.save()
            print(f"✅ Using existing supervisor: {supervisor.username}")
        
        # Test login
        login_success = client.login(username=supervisor.username, password='admin123')
        
        if not login_success:
            print("❌ Failed to login as supervisor")
            return
        
        print("✅ Supervisor login successful")
        
        # Test all supervisor pages
        print("\n📋 Testing supervisor pages:")
        print("-" * 30)
        
        test_pages = [
            ('/users/pgs/', 'PG List'),
            ('/cases/statistics/', 'Cases Statistics'),
            ('/logbook/', 'Logbook'),
            ('/rotations/create/', 'Rotations Create'),
            ('/certificates/dashboard/', 'Certificates Dashboard'),
            ('/rotations/bulk-assignment/', 'Bulk Assignment'),
        ]
        
        success_count = 0
        total_pages = len(test_pages)
        
        for url, name in test_pages:
            try:
                response = client.get(url, follow=True)
                status = response.status_code
                
                if status == 200:
                    print(f"✅ {name:25} {url:30} SUCCESS")
                    success_count += 1
                elif status == 403:
                    print(f"❌ {name:25} {url:30} PERMISSION DENIED")
                elif status == 404:
                    print(f"❌ {name:25} {url:30} NOT FOUND")
                elif status == 500:
                    print(f"❌ {name:25} {url:30} SERVER ERROR")
                    print(f"   Error: {response.content[:200].decode('utf-8', errors='ignore')}")
                else:
                    print(f"⚠️  {name:25} {url:30} STATUS {status}")
                    
            except Exception as e:
                print(f"❌ {name:25} {url:30} EXCEPTION: {str(e)}")
        
        print("\n" + "=" * 50)
        print(f"📊 RESULTS: {success_count}/{total_pages} pages accessible")
        
        if success_count == total_pages:
            print("🎉 ALL SUPERVISOR PAGES WORKING CORRECTLY!")
        else:
            print("⚠️  Some issues detected. Please check the failures above.")
        
        # Test bulk assignment specifically
        print("\n🔧 Testing bulk assignment functionality:")
        print("-" * 40)
        
        # Check if bulk assignment form loads
        bulk_response = client.get('/rotations/bulk-assignment/')
        if bulk_response.status_code == 200:
            print("✅ Bulk assignment form loads successfully")
            
            # Check if form contains supervisor-specific elements
            content = bulk_response.content.decode('utf-8')
            if 'supervisor' in content.lower():
                print("✅ Supervisor field present in form")
            if 'postgraduate' in content.lower() or 'pg' in content.lower():
                print("✅ PG selection available")
            
        else:
            print(f"❌ Bulk assignment form failed to load: {bulk_response.status_code}")
        
        print("\n✅ Supervisor functionality test completed!")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_supervisor_functionality()
