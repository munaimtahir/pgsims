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

def test_all_target_pages():
    client = Client()
    
    # Use an existing user
    user = User.objects.filter(role='pg').first()
    if not user:
        print("No PG users found")
        return
    
    # Login
    user.set_password('testpass123')
    user.save()
    login_success = client.login(username=user.username, password='testpass123')
    print(f"Login successful: {login_success} for user: {user.username}")
    
    pages = [
        '/cases/',
        '/logbook/pg/entries/',
        '/certificates/create/',
        '/rotations/create/',
        '/cases/create/',
        '/cases/statistics/',
        '/users/profile/edit/'
    ]
    
    for page in pages:
        try:
            response = client.get(page)
            status_icon = "✓" if response.status_code == 200 else "✗" if response.status_code == 403 else "⚠"
            print(f"{status_icon} {page}: Status {response.status_code}")
            if response.status_code >= 400 and response.status_code != 403:
                # For 403, it's expected for some roles
                content = response.content.decode()
                error_line = [line for line in content.split('\n') if 'error' in line.lower() or 'exception' in line.lower()]
                if error_line:
                    print(f"   Error: {error_line[0][:100]}...")
        except Exception as e:
            print(f"✗ {page}: Exception - {str(e)}")

if __name__ == '__main__':
    test_all_target_pages()
