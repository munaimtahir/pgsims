import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()

def test_specific_pages():
    client = Client()
    
    # Get a PG user and login
    user = User.objects.filter(role='pg').first()
    if not user:
        print("ERROR: No PG user found")
        return
    
    user.set_password('testpass123')
    user.save()
    login_ok = client.login(username=user.username, password='testpass123')
    print(f"Login: {'SUCCESS' if login_ok else 'FAILED'} for {user.username}")
    
    # Test specific pages
    pages = [
        '/logbook/pg/entries/',
        '/certificates/create/'
    ]
    
    for url in pages:
        print(f"\n--- Testing {url} ---")
        try:
            response = client.get(url)
            print(f"Status: {response.status_code}")
            
            if response.status_code >= 400:
                content = response.content.decode()
                if 'crispy' in content.lower():
                    print("ERROR: Crispy forms field error detected")
                    # Find the specific error
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if 'crispy' in line.lower() and 'error' in line.lower():
                            print(f"Error line: {line.strip()}")
                            break
                if 'templatetag' in content.lower():
                    print("ERROR: Template tag error detected")
                if response.status_code == 500:
                    print("ERROR: Internal server error")
                    
        except Exception as e:
            print(f"EXCEPTION: {str(e)}")

if __name__ == '__main__':
    test_specific_pages()
