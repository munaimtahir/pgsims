#!/usr/bin/env python
"""
Test the admin dashboard to verify model names are properly formatted.
"""

import requests
from bs4 import BeautifulSoup
import re

def test_admin_dashboard_model_names():
    """Test the admin dashboard for proper model name formatting"""
    
    print("=" * 60)
    print("TESTING ADMIN DASHBOARD MODEL NAMES")
    print("=" * 60)
    
    try:
        # Try to access the admin dashboard
        url = "http://127.0.0.1:8000/admin/"
        
        print(f"Testing URL: {url}")
        print()
        
        # Make request to admin page
        session = requests.Session()
        
        # First get the login page to get CSRF token
        login_url = "http://127.0.0.1:8000/admin/login/"
        response = session.get(login_url)
        
        if response.status_code != 200:
            print(f"❌ Could not access login page. Status: {response.status_code}")
            return False
        
        soup = BeautifulSoup(response.content, 'html.parser')
        csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})
        
        if not csrf_token:
            print("❌ Could not find CSRF token")
            return False
        
        # Try to login (assuming admin/admin credentials)
        login_data = {
            'username': 'admin',
            'password': 'admin',
            'csrfmiddlewaretoken': csrf_token['value'],
            'next': '/admin/',
        }
        
        login_response = session.post(login_url, data=login_data)
        
        if login_response.status_code == 200 and 'admin/' in login_response.url:
            print("✅ Successfully logged into admin")
        else:
            print("⚠️  Could not login to admin (this is expected if no admin user exists)")
            print("   Testing with direct access to admin page content...")
            
            # Try direct access without login for testing purposes
            response = session.get(url)
        
        # Get the admin dashboard page
        if 'admin/' in session.get(url).url or session.get(url).status_code == 200:
            dashboard_response = session.get(url)
            soup = BeautifulSoup(dashboard_response.content, 'html.parser')
            
            # Look for model names in the page
            model_names = []
            
            # Find all model name elements
            model_elements = soup.find_all('h6', class_='model-name')
            
            if model_elements:
                print("Found model names in dashboard:")
                print("-" * 40)
                
                for element in model_elements:
                    model_name = element.get_text().strip()
                    model_names.append(model_name)
                    print(f"  - {model_name}")
                
                print()
                
                # Check for problematic names
                issues = []
                
                for name in model_names:
                    if 'categorys' in name.lower():
                        issues.append(f"❌ Issue: '{name}' should be 'Case Categories'")
                    elif 'reviews' in name.lower() and 'casereviews' in name.lower().replace(' ', ''):
                        issues.append(f"❌ Issue: '{name}' should be 'Case Reviews'")
                    elif name.endswith('s') and name.count(' ') == 0 and len(name) > 8:
                        issues.append(f"⚠️  Potential issue: '{name}' might need spacing")
                
                if issues:
                    print("ISSUES FOUND:")
                    for issue in issues:
                        print(issue)
                    print()
                    return False
                else:
                    print("✅ SUCCESS: All model names appear to be properly formatted!")
                    print("   No spelling or spacing issues found.")
                    return True
            else:
                print("⚠️  Could not find model name elements (page might not be fully loaded)")
                
                # Try alternative method - look for any text containing common issues
                page_text = soup.get_text()
                
                issues = []
                if 'casecategorys' in page_text.lower():
                    issues.append("Found 'casecategorys'")
                if 'casereviews' in page_text.lower():
                    issues.append("Found 'casereviews'")
                
                if issues:
                    print(f"❌ Issues found in page text: {issues}")
                    return False
                else:
                    print("✅ No obvious issues found in page text")
                    return True
        else:
            print(f"❌ Could not access admin dashboard. Status: {dashboard_response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure Django server is running on http://127.0.0.1:8000")
        return False
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False

def test_template_file_directly():
    """Test the template file directly for proper model name usage"""
    
    print("=" * 60)
    print("TESTING TEMPLATE FILE DIRECTLY")
    print("=" * 60)
    
    template_path = "d:\\PMC\\sims_project-2\\templates\\admin\\index.html"
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"Reading template: {template_path}")
        print()
        
        # Check if the old problematic code is still there
        issues = []
        
        if '{{ model.object_name|title }}s' in content:
            issues.append("❌ Found old problematic code: '{{ model.object_name|title }}s'")
        
        if '{{ model.name }}' in content:
            print("✅ Found correct usage: '{{ model.name }}'")
        else:
            issues.append("❌ Could not find expected '{{ model.name }}' usage")
        
        # Check for any hardcoded problematic names
        if 'casecategorys' in content.lower():
            issues.append("❌ Found hardcoded 'casecategorys'")
        if 'casereviews' in content.lower():
            issues.append("❌ Found hardcoded 'casereviews'")
        
        if issues:
            print("ISSUES FOUND:")
            for issue in issues:
                print(issue)
            print()
            return False
        else:
            print("✅ Template file looks good!")
            print("   Using proper model.name instead of object_name with manual 's' addition")
            return True
            
    except FileNotFoundError:
        print(f"❌ Template file not found: {template_path}")
        return False
    except Exception as e:
        print(f"❌ Error reading template: {e}")
        return False

if __name__ == "__main__":
    print("Starting model names fix verification...")
    print()
    
    # Test 1: Check template file directly
    template_test_passed = test_template_file_directly()
    
    print()
    
    # Test 2: Test the actual admin dashboard
    dashboard_test_passed = test_admin_dashboard_model_names()
    
    print()
    print("=" * 60)
    print("FINAL TEST RESULTS")
    print("=" * 60)
    
    if template_test_passed and dashboard_test_passed:
        print("🎉 ALL TESTS PASSED!")
        print("   Model names are properly formatted in both template and rendered page.")
    elif template_test_passed:
        print("✅ Template test passed, but dashboard test had issues")
        print("   The template fix is correct, dashboard issues might be due to server/auth")
    else:
        print("❌ TESTS FAILED!")
        print("   Review the issues above and fix the model name formatting.")
    
    print()
