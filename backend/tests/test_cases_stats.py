#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

def test_cases_statistics():
    """Test the cases statistics page"""
    User = get_user_model()
    client = Client()
    
    print("🔍 TESTING CASES STATISTICS PAGE")
    print("=" * 40)
    
    try:
        # Find a supervisor
        supervisor = User.objects.filter(role='supervisor', is_active=True).first()
        if supervisor:
            supervisor.set_password('admin123')
            supervisor.save()
            
            login_success = client.login(username=supervisor.username, password='admin123')
            print(f"✓ Supervisor login: {'SUCCESS' if login_success else 'FAILED'}")
            
            if login_success:
                # Test cases statistics page
                response = client.get('/cases/statistics/')
                print(f"✓ Status Code: {response.status_code}")
                
                if response.status_code == 200:
                    print("✅ Cases statistics page loads successfully")
                elif response.status_code == 500:
                    print("❌ Server error occurred")
                    print("Error content:", response.content[:500].decode('utf-8', errors='ignore'))
                else:
                    print(f"⚠️ Unexpected status: {response.status_code}")
                    print("Response content:", response.content[:300].decode('utf-8', errors='ignore'))
        else:
            print("❌ No supervisor found")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_cases_statistics()
