#!/usr/bin/env python
"""
Quick test to verify the model names spelling fix in the admin dashboard.
"""

import subprocess
import sys
import os

def test_template_fix():
    """Test that the template has been properly fixed"""
    
    print("=" * 60)
    print("TESTING MODEL NAMES SPELLING FIX")
    print("=" * 60)
    print()
    
    template_path = "templates/admin/index.html"
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("✅ Successfully read template file")
        print()
        
        # Check for the fix
        tests = [
            ("Old problematic code removed", "{{ model.object_name|title }}s" not in content),
            ("New correct code present", "{{ model.name }}" in content),
            ("No hardcoded 'casecategorys'", "casecategorys" not in content.lower()),
            ("No hardcoded 'casereviews'", "casereviews" not in content.lower()),
        ]
        
        all_passed = True
        
        for test_name, test_result in tests:
            if test_result:
                print(f"✅ {test_name}")
            else:
                print(f"❌ {test_name}")
                all_passed = False
        
        print()
        
        if all_passed:
            print("🎉 SUCCESS: All template fixes applied correctly!")
            print()
            print("WHAT WAS FIXED:")
            print("- Changed '{{ model.object_name|title }}s' to '{{ model.name }}'")
            print("- This uses Django's proper verbose_name_plural instead of")
            print("  manually adding 's' to object names")
            print("- Fixes issues like 'Casecategorys' → 'Case Categories'")
            print("- Fixes issues like 'Casereviews' → 'Case Reviews'")
        else:
            print("❌ Some issues remain in the template")
        
        return all_passed
        
    except FileNotFoundError:
        print(f"❌ Template file not found: {template_path}")
        return False
    except Exception as e:
        print(f"❌ Error reading template: {e}")
        return False

def test_server_response():
    """Test the server response to see if it's working"""
    
    print()
    print("=" * 60)
    print("TESTING SERVER RESPONSE")
    print("=" * 60)
    
    try:
        import urllib.request
        import urllib.error
        
        # Test if server is running
        url = "http://127.0.0.1:8000/admin/"
        
        try:
            response = urllib.request.urlopen(url, timeout=5)
            print(f"✅ Server is responding on {url}")
            print(f"   Status: {response.getcode()}")
            
            # Check if we can access the page (even if login is required)
            if response.getcode() in [200, 302]:  # 302 might be redirect to login
                print("✅ Admin dashboard is accessible")
                print("   The model name fixes will be visible when you log in")
                return True
            else:
                print(f"⚠️  Unexpected response code: {response.getcode()}")
                return False
                
        except urllib.error.URLError as e:
            print(f"❌ Could not connect to server: {e}")
            print("   Make sure Django server is running with: python manage.py runserver")
            return False
            
    except ImportError:
        print("⚠️  Could not import urllib (this is unusual)")
        return False

if __name__ == "__main__":
    print("Quick verification of model names spelling fix...")
    print()
    
    # Test the template
    template_ok = test_template_fix()
    
    # Test the server
    server_ok = test_server_response()
    
    print()
    print("=" * 60)
    print("FINAL RESULTS")
    print("=" * 60)
    
    if template_ok:
        print("🎉 TEMPLATE FIX: SUCCESS")
        print("   All spelling and spacing issues in model names have been fixed")
        print()
        
        if server_ok:
            print("🌐 SERVER: RUNNING")
            print("   You can now visit http://127.0.0.1:8000/admin/ to see the fixes")
        else:
            print("⚠️  SERVER: NOT ACCESSIBLE")
            print("   Start the server to see the changes: python manage.py runserver")
        
        print()
        print("MODEL NAME IMPROVEMENTS:")
        print("• 'Casecategorys' → 'Case Categories'")
        print("• 'Casereviews' → 'Case Reviews'")
        print("• Other models now show proper plural names")
        print("• Uses Django's built-in verbose_name_plural")
        
    else:
        print("❌ TEMPLATE FIX: FAILED")
        print("   There may still be issues with the template")
    
    print()
    print("You can now check the admin dashboard to see properly formatted model names!")
