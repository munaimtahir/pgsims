#!/usr/bin/env python3
"""
Homepage verification using Django test client
Tests the new FMU-branded homepage functionality
"""

import os
import sys

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')

import django
django.setup()

from django.test import Client
from django.urls import reverse

def test_homepage():
    """Test the homepage functionality"""
    print("🔍 Testing SIMS Homepage...")
    print("-" * 50)
    
    try:
        client = Client()
        
        # Test homepage
        response = client.get('/')
        print(f"📍 Homepage Status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.content.decode()
            
            # Check for key content
            checks = [
                ("FMU Branding", "Faisalabad Medical University" in content),
                ("SIMS Title", "SIMS" in content),
                ("Login Button", "Sign In" in content or "login" in content.lower()),
                ("System Version", "v2.1.0" in content),
                ("Bootstrap CSS", "bootstrap" in content.lower()),
                ("Feature Cards", "Digital Logbook" in content or "logbook" in content.lower()),
                ("Medical Theme", "medical" in content.lower() or "training" in content.lower()),
                ("Professional Design", "gradient" in content.lower()),
            ]
            
            print("\n✅ Content Verification:")
            for check_name, result in checks:
                status = "✓" if result else "✗"
                print(f"   {status} {check_name}")
            
            print(f"\n📊 Page size: {len(content):,} characters")
            
            # Test login URL resolution
            try:
                login_url = reverse('login')
                print(f"🔗 Login URL resolves to: {login_url}")
                
                # Test login page
                login_response = client.get(login_url)
                print(f"🔗 Login page status: {login_response.status_code}")
            except Exception as e:
                print(f"⚠️  Login URL issue: {e}")
            
            all_passed = all(result for _, result in checks)
            if all_passed:
                print("\n🎉 All tests passed! Homepage is working correctly.")
                return True
            else:
                print("\n⚠️  Some checks failed. Please review the homepage.")
                return False
        else:
            print(f"❌ Homepage returned status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing homepage: {e}")
        return False

if __name__ == "__main__":
    success = test_homepage()
    print(f"\n{'='*50}")
    print(f"Test Result: {'✅ PASSED' if success else '❌ FAILED'}")
    sys.exit(0 if success else 1)
