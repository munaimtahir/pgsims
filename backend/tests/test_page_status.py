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
    
    # Create or get a supervisor user first
    try:
        supervisor = User.objects.get(username='supervisor')
    except User.DoesNotExist:
        supervisor = User.objects.create_user(
            username='supervisor',
            email='supervisor@example.com',
            password='supervisorpass123',
            first_name='Super',
            last_name='Visor',
            role='supervisor',
            specialty='medicine'
        )
    
    # Create or get a test user
    try:
        user = User.objects.get(username='testuser')
    except User.DoesNotExist:
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
            role='pg',
            specialty='medicine',
            year='1',
            supervisor=supervisor
        )
    
    # Login
    client.login(username='testuser', password='testpass123')
    
    pages = [
        '/users/profile/edit/',
        '/logbook/pg/entries/',
        '/logbook/entry/create/',
        '/cases/create/',
        '/cases/statistics/'
    ]
    
    for page in pages:
        try:
            response = client.get(page)
            print(f"{page}: Status {response.status_code}")
            if response.status_code >= 400:
                print(f"  Error content: {response.content.decode()[:200]}...")
        except Exception as e:
            print(f"{page}: Exception - {str(e)}")

if __name__ == '__main__':
    test_pages()
