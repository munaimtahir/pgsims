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

def test_single_page(page_url):
    client = Client()
    
    # Use an existing user
    user = User.objects.filter(role='pg').first()
    if not user:
        print("No PG users found")
        return
    
    # Login using existing user credentials if available
    login_success = client.login(username=user.username, password='testpass123')
    if not login_success:
        # Try another password
        login_success = client.login(username=user.username, password='password123')
    if not login_success:
        # Try setting a known password
        user.set_password('testpass123')
        user.save()
        login_success = client.login(username=user.username, password='testpass123')
        
    print(f"Login successful: {login_success} for user: {user.username}")
    
    try:
        response = client.get(page_url)
        print(f"{page_url}: Status {response.status_code}")
        if response.status_code >= 400:
            content = response.content.decode()
            print(f"Error content:\n{content[:1000]}")
    except Exception as e:
        print(f"{page_url}: Exception - {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    pages = [
        '/users/profile/edit/',
        '/logbook/pg/entries/',
        '/logbook/entry/create/',
        '/cases/create/',
        '/cases/statistics/'
    ]
    
    for page in pages:
        print(f"\n--- Testing {page} ---")
        test_single_page(page)
        print()
