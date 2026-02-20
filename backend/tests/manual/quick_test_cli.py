#!/usr/bin/env python
"""
Simple test script to check page status
Run in background and write results to test_results_final.txt
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

def main():
    results = []
    
    try:
        User = get_user_model()
        client = Client()
        
        # Get a PG user
        user = User.objects.filter(role='pg').first()
        if not user:
            results.append("ERROR: No PG user found")
            return
        
        # Set password and login
        user.set_password('testpass123')
        user.save()
        login_ok = client.login(username=user.username, password='testpass123')
        
        results.append(f"Login: {'SUCCESS' if login_ok else 'FAILED'} (User: {user.username})")
        results.append("-" * 50)
        
        # Test pages
        pages = [
            ('/cases/', 'Cases List'),
            ('/logbook/pg/entries/', 'PG Logbook'),
            ('/certificates/create/', 'Create Certificate'),
            ('/rotations/create/', 'Create Rotation'),
            ('/cases/create/', 'Create Case'),
            ('/cases/statistics/', 'Case Statistics'),
            ('/users/profile/edit/', 'Edit Profile')
        ]
        
        for url, name in pages:
            try:
                response = client.get(url)
                if response.status_code == 200:
                    status = "✓ PASS"
                elif response.status_code == 403:
                    status = "⚠ FORBIDDEN"
                else:
                    status = f"✗ ERROR {response.status_code}"
                    
                results.append(f"{status:12} | {url:25} | {name}")
                
                # Check for specific errors
                if response.status_code >= 400 and response.status_code != 403:
                    content = response.content.decode()
                    if 'crispy' in content.lower():
                        results.append(f"             └─ Crispy forms error detected")
                    if 'basename' in content.lower():
                        results.append(f"             └─ Basename filter error detected")
                        
            except Exception as e:
                results.append(f"EXCEPTION    | {url:25} | {name} - {str(e)}")
        
    except Exception as e:
        results.append(f"FATAL ERROR: {str(e)}")
    
    # Write results
    with open('test_results_final.txt', 'w') as f:
        f.write("SIMS Page Test Results\n")
        f.write("======================\n\n")
        f.write("\n".join(results))
        f.write("\n\nTest completed.\n")
    
    print("Test completed. Results written to test_results_final.txt")

if __name__ == '__main__':
    main()
