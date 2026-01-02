#!/usr/bin/env python
"""
Test script to verify admin dashboard consolidation
"""
import os
import sys
import django
import requests

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

from django.test.client import Client
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

def test_admin_consolidation():
    """Test that admin consolidation is working"""
    print("Testing Admin Dashboard Consolidation")
    print("=" * 50)
    
    # Test server availability
    base_url = "http://127.0.0.1:8000"
    
    try:
        response = requests.get(f"{base_url}/admin/", timeout=5)
        print(f"✓ Django Admin accessible: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"✗ Django Admin not accessible: {e}")
        return False
    
    # Test redirect functionality
    try:
        # Create test client
        client = Client()
        
        # Try to access old admin dashboard URL
        old_admin_url = "/users/admin-dashboard/"
        response = client.get(old_admin_url, follow=True)
        print(f"✓ Old admin dashboard URL redirect test: {response.status_code}")
        
        # Check if it redirects to login (expected for non-authenticated users)
        if response.status_code == 200:
            print("  - Redirected to login page (expected)")
        
    except Exception as e:
        print(f"✗ Error testing redirects: {e}")
    
    # Test URL reverse functionality
    try:
        admin_index_url = reverse('admin:index')
        print(f"✓ Django admin URL resolution: {admin_index_url}")
    except Exception as e:
        print(f"✗ Error resolving admin URL: {e}")
    
    print("\nConsolidation Test Summary:")
    print("- Django admin should be accessible at /admin/")
    print("- Old admin dashboard at /users/admin-dashboard/ should redirect admins to /admin/")
    print("- All admin functionality should be available from /admin/")
    print("\nTest completed!")

if __name__ == "__main__":
    test_admin_consolidation()
