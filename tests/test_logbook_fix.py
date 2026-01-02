#!/usr/bin/env python
"""
Test the logbook page fix for supervised_pgs error.
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

from django.contrib.auth import get_user_model
import requests

User = get_user_model()

def test_supervisor_relationships():
    """Test that supervisor relationships work correctly"""
    print("Testing supervisor relationships...")
    
    # Get a supervisor user
    supervisor = User.objects.filter(role='supervisor').first()
    if not supervisor:
        print("No supervisor found!")
        return False
    
    print(f"Testing with supervisor: {supervisor.username}")
    
    # Test assigned_pgs relationship
    try:
        pgs = supervisor.assigned_pgs.filter(is_active=True)
        print(f"Supervisor has {pgs.count()} assigned PGs")
        for pg in pgs:
            print(f"  - {pg.username} ({pg.first_name} {pg.last_name})")
        return True
    except Exception as e:
        print(f"Error accessing assigned_pgs: {e}")
        return False

def test_logbook_page():
    """Test the logbook page loads without error"""
    print("\nTesting logbook page...")
    
    supervisor = User.objects.filter(role='supervisor').first()
    if not supervisor:
        print("No supervisor found!")
        return False
    
    try:
        # Create a session and login
        session = requests.Session()
        
        # Get CSRF token
        csrf_response = session.get('http://127.0.0.1:8000/accounts/login/')
        if csrf_response.status_code != 200:
            print(f"Failed to get login page: {csrf_response.status_code}")
            return False
        
        csrf_token = csrf_response.text.split('csrfmiddlewaretoken')[1].split('value="')[1].split('"')[0]
        
        # Login
        login_data = {
            'username': supervisor.username,
            'password': 'sims2024',
            'csrfmiddlewaretoken': csrf_token
        }
        
        login_response = session.post('http://127.0.0.1:8000/accounts/login/', data=login_data)
        print(f"Login response status: {login_response.status_code}")
        
        if login_response.status_code != 200 and '/dashboard' not in login_response.url:
            print("Login failed")
            return False
        
        # Test logbook page
        logbook_response = session.get('http://127.0.0.1:8000/logbook/')
        print(f"Logbook page status: {logbook_response.status_code}")
        
        if logbook_response.status_code == 200:
            print("Logbook page loaded successfully!")
            if 'supervised_pgs' in logbook_response.text:
                print("WARNING: Still contains supervised_pgs reference")
                return False
            else:
                print("No supervised_pgs references found in response")
                return True
        else:
            print(f"Logbook page failed with status {logbook_response.status_code}")
            print("Response content preview:")
            print(logbook_response.text[:500])
            return False
            
    except Exception as e:
        print(f"Error testing logbook page: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("TESTING LOGBOOK SUPERVISED_PGS FIX")
    print("=" * 50)
    
    relationship_ok = test_supervisor_relationships()
    logbook_ok = test_logbook_page()
    
    print("\n" + "=" * 50)
    print("TEST RESULTS:")
    print(f"Supervisor relationships: {'PASS' if relationship_ok else 'FAIL'}")
    print(f"Logbook page loads: {'PASS' if logbook_ok else 'FAIL'}")
    print(f"Overall: {'PASS' if relationship_ok and logbook_ok else 'FAIL'}")
    print("=" * 50)
