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
    
    # Use an existing user or create a simple one
    users = User.objects.filter(role='pg').first()
    if users:
        user = users
        print(f"Using existing user: {user.username}")
    else:
        print("No PG users found, creating one...")
        # Create supervisor first if needed
        supervisor = User.objects.filter(role='supervisor').first()
        if not supervisor:
            supervisor = User.objects.create_user(
                username='testsupervisor',
                email='testsupervisor@example.com',
                password='testpass123',
                role='supervisor',
                specialty='medicine'
            )
        
        user = User.objects.create_user(
            username='testpg',
            email='testpg@example.com',
            password='testpass123',
            role='pg',
            specialty='medicine',
            year='1',
            supervisor=supervisor
        )
    
    # Login
    login_success = client.login(username=user.username, password='testpass123')
    print(f"Login successful: {login_success}")
    
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
                content = response.content.decode()[:500]
                print(f"  Error content: {content}...")
        except Exception as e:
            print(f"{page}: Exception - {str(e)}")

if __name__ == '__main__':
    test_pages()
