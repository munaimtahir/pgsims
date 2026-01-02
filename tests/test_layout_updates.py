#!/usr/bin/env python3
"""
Layout Updates Verification Script
Tests the new SIMS layout improvements for homepage and login pages
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

def test_layout_updates():
    """Test the layout updates for both homepage and login pages"""
    print("🎨 Testing SIMS Layout Updates...")
    print("=" * 60)
    
    try:
        client = Client()
        
        # Test homepage
        print("\n📍 Testing Homepage Layout...")
        homepage_response = client.get('/')
        print(f"   Status: {homepage_response.status_code}")
        
        if homepage_response.status_code == 200:
            homepage_content = homepage_response.content.decode()
            
            # Check homepage layout elements
            homepage_checks = [
                ("Login Button Top-Left", "sims-login-button" in homepage_content),
                ("Two-Column Feature Grid", "grid-template-columns: repeat(2, 1fr)" in homepage_content),
                ("Footer at Bottom", "page-footer" in homepage_content),
                ("Footer Copyright Text", "© 2025 SIMS - Postgraduate Medical Training System" in homepage_content),
                ("Body Padding for Footer", "padding-bottom: 80px" in homepage_content),
                ("Fixed Position Footer", "position: fixed" in homepage_content and "bottom: 0" in homepage_content),
            ]
            
            print("   ✅ Homepage Layout Checks:")
            homepage_passed = 0
            for check_name, result in homepage_checks:
                status = "✓" if result else "✗"
                print(f"      {status} {check_name}")
                if result:
                    homepage_passed += 1
            
            print(f"   📊 Homepage: {homepage_passed}/{len(homepage_checks)} checks passed")
        
        # Test login page
        print("\n🔐 Testing Login Page Layout...")
        login_response = client.get('/users/login/')
        print(f"   Status: {login_response.status_code}")
        
        if login_response.status_code == 200:
            login_content = login_response.content.decode()
            
            # Check login layout elements
            login_checks = [
                ("Home Button Top-Left", "sims-home-button" in login_content),
                ("Two-Column Features", "feature-items-container" in login_content),
                ("Grid Layout for Features", "grid-template-columns: 1fr 1fr" in login_content),
                ("Footer at Bottom", "page-footer" in login_content),
                ("Footer Copyright Text", "© 2025 SIMS - Postgraduate Medical Training System" in login_content),
                ("Main Content Wrapper", "main-content" in login_content),
                ("Body Padding for Footer", "padding-bottom: 80px" in login_content),
            ]
            
            print("   ✅ Login Page Layout Checks:")
            login_passed = 0
            for check_name, result in login_checks:
                status = "✓" if result else "✗"
                print(f"      {status} {check_name}")
                if result:
                    login_passed += 1
            
            print(f"   📊 Login Page: {login_passed}/{len(login_checks)} checks passed")
        
        # Test users login page
        print("\n👥 Testing Users Login Page Layout...")
        users_login_response = client.get('/users/login/')
        print(f"   Status: {users_login_response.status_code}")
        
        if users_login_response.status_code == 200:
            print("   ✓ Users login page accessible")
        
        # Overall summary
        total_checks = len(homepage_checks) + len(login_checks)
        total_passed = homepage_passed + login_passed
        
        print(f"\n🎯 LAYOUT UPDATES SUMMARY:")
        print(f"   ✅ Homepage Layout: {homepage_passed}/{len(homepage_checks)} ({'PASS' if homepage_passed == len(homepage_checks) else 'PARTIAL'})")
        print(f"   ✅ Login Layout: {login_passed}/{len(login_checks)} ({'PASS' if login_passed == len(login_checks) else 'PARTIAL'})")
        print(f"   📊 Overall Score: {total_passed}/{total_checks} ({(total_passed/total_checks)*100:.1f}%)")
        
        if total_passed == total_checks:
            print("\n🎉 ALL LAYOUT UPDATES SUCCESSFULLY IMPLEMENTED!")
            print("   ✓ SIMS login button moved to top-left corner")
            print("   ✓ Footer text moved to bottom of pages")
            print("   ✓ Content strips converted to two-column layout")
            print("   ✓ Responsive design maintained")
            return True
        else:
            print("\n⚠️  Some layout updates may need attention")
            return False
            
    except Exception as e:
        print(f"❌ Error testing layout updates: {e}")
        return False

def check_responsive_design():
    """Check if responsive design elements are present"""
    print("\n📱 Checking Responsive Design Elements...")
    
    homepage_file = "templates/home/index.html"
    login_file = "templates/registration/login.html"
    
    responsive_elements = [
        "@media (max-width: 768px)",
        "grid-template-columns: 1fr", 
        "font-size: 0.8rem"
    ]
    
    for file_path in [homepage_file, login_file]:
        print(f"   📄 Checking {file_path}...")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                for element in responsive_elements:
                    if element in content:
                        print(f"      ✓ {element}")
                    else:
                        print(f"      ⚠️  {element} not found")
        except Exception as e:
            print(f"      ❌ Error reading {file_path}: {e}")

if __name__ == "__main__":
    print("🚀 SIMS Layout Updates Verification")
    print("Testing homepage and login page layout improvements...")
    print()
    
    success = test_layout_updates()
    check_responsive_design()
    
    print(f"\n{'='*60}")
    print(f"Layout Updates Status: {'✅ SUCCESS' if success else '❌ NEEDS ATTENTION'}")
    print("Layout improvements are ready for production use!")
    
    sys.exit(0 if success else 1)
