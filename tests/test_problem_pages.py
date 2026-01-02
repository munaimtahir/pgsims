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

def test_pages():
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
        '/rotations/create/'
    ]
    
    for page in pages:
        try:
            response = client.get(page)
            print(f"\n{page}: Status {response.status_code}")
            if response.status_code >= 400:
                content = response.content.decode()
                print(f"Error content:\n{content[:1000]}...")
        except Exception as e:
            print(f"\n{page}: Exception - {str(e)}")

if __name__ == '__main__':
    test_pages()
