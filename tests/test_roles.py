import os
import sys
import django
from django.conf import settings
from django.test import Client
from django.contrib.auth import get_user_model

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

User = get_user_model()

def test_pages_with_different_roles():
    client = Client()
    
    # Test with different user roles
    users = {
        'pg': User.objects.filter(role='pg').first(),
        'supervisor': User.objects.filter(role='supervisor').first(),
        'admin': User.objects.filter(role='admin').first(),
    }
    
    pages = [
        '/cases/',
        '/logbook/pg/entries/',
        '/certificates/create/',
        '/rotations/create/'
    ]
    
    for role, user in users.items():
        if not user:
            print(f"No {role} users found")
            continue
            
        user.set_password('testpass123')
        user.save()
        login_success = client.login(username=user.username, password='testpass123')
        print(f"\n=== Testing as {role} user: {user.username} (Login: {login_success}) ===")
        
        for page in pages:
            try:
                response = client.get(page)
                print(f"{page}: Status {response.status_code}")
                if response.status_code >= 400:
                    content = response.content.decode()[:500]
                    print(f"  Error: {content}...")
            except Exception as e:
                print(f"{page}: Exception - {str(e)}")
        
        client.logout()

if __name__ == '__main__':
    test_pages_with_different_roles()
