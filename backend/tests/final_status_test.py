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

def test_pages_final():
    client = Client()
    
    # Use an existing user
    user = User.objects.filter(role='pg').first()
    if not user:
        with open('final_status_report.txt', 'w') as f:
            f.write("ERROR: No PG users found\n")
        return
    
    # Login
    user.set_password('testpass123')
    user.save()
    login_success = client.login(username=user.username, password='testpass123')
    
    pages = [
        ('/cases/', 'Cases List'),
        ('/logbook/pg/entries/', 'PG Logbook Entries'),
        ('/certificates/create/', 'Create Certificate'),
        ('/rotations/create/', 'Create Rotation'),
        ('/cases/create/', 'Create Case'),
        ('/cases/statistics/', 'Case Statistics'),
        ('/users/profile/edit/', 'Edit Profile')
    ]
    
    results = []
    results.append(f"SIMS Final Page Status Report")
    results.append(f"=============================")
    results.append(f"Login successful: {login_success} for user: {user.username}")
    results.append("")
    
    for page_url, page_name in pages:
        try:
            response = client.get(page_url)
            status_text = "PASS" if response.status_code == 200 else "FORBIDDEN" if response.status_code == 403 else "FAIL"
            results.append(f"{status_text:10} | {page_url:25} | {page_name}")
            
            if response.status_code >= 400 and response.status_code != 403:
                content = response.content.decode()
                if 'basename' in content:
                    results.append(f"           └─ ERROR: basename filter issue still present")
                elif 'Internal Server Error' in content:
                    results.append(f"           └─ ERROR: Internal Server Error")
                    
        except Exception as e:
            results.append(f"EXCEPTION  | {page_url:25} | {page_name} - {str(e)}")
    
    results.append("")
    results.append("Legend:")
    results.append("  PASS      - Page loads successfully (HTTP 200)")
    results.append("  FORBIDDEN - Access denied for current user role (HTTP 403)")  
    results.append("  FAIL      - Page has errors or issues")
    results.append("  EXCEPTION - Python/Django exception occurred")
    
    with open('final_status_report.txt', 'w') as f:
        f.write('\n'.join(results))
    
    # Also print to console
    for line in results:
        print(line)

if __name__ == '__main__':
    test_pages_final()
