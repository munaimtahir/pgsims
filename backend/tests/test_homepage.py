#!/usr/bin/env python3
"""
Quick homepage verification script
Tests the new FMU-branded homepage functionality
"""

import requests
import sys
from urllib.parse import urljoin

def test_homepage():
    """Test the homepage functionality"""
    base_url = "http://127.0.0.1:8000"
    
    try:
        print("🔍 Testing SIMS Homepage...")
        print("-" * 50)
        
        # Test homepage
        response = requests.get(f"{base_url}/", timeout=10)
        print(f"📍 Homepage Status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            
            # Check for key content
            checks = [
                ("FMU Branding", "Faisalabad Medical University" in content),
                ("SIMS Title", "SIMS" in content),
                ("Login Button", "Sign In" in content),
                ("System Version", "v2.1.0" in content),
                ("Bootstrap CSS", "bootstrap" in content),
                ("Feature Cards", "Digital Logbook" in content),
                ("University Info", "leading institution" in content),
                ("Status Indicator", "System Online" in content or "System online" in content),
            ]
            
            print("\n✅ Content Verification:")
            for check_name, result in checks:
                status = "✓" if result else "✗"
                print(f"   {status} {check_name}")
            
            print(f"\n📊 Page size: {len(content):,} characters")
            
            # Test login page link
            if "login" in content.lower():
                login_response = requests.get(f"{base_url}/login/", timeout=10)
                print(f"🔗 Login page: {login_response.status_code}")
            
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
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Is Django running?")
        return False
    except Exception as e:
        print(f"❌ Error testing homepage: {e}")
        return False

if __name__ == "__main__":
    success = test_homepage()
    sys.exit(0 if success else 1)
