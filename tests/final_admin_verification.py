#!/usr/bin/env python
"""
Final Admin System Verification Test
Tests all admin functionality, URLs, templates, and PMC theme consistency
"""
import os
import sys
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

from django.urls import reverse
from django.test import Client
from django.contrib.auth import get_user_model

def test_admin_accessibility():
    """Test admin pages are accessible"""
    print("🔍 Testing Admin Page Accessibility...")
    print("=" * 50)
    
    client = Client()
    
    # Test admin login page
    response = client.get('/admin/')
    if response.status_code == 302:  # Redirect to login
        print("✅ Admin index redirects to login (as expected)")
        
        login_response = client.get('/admin/login/')
        if login_response.status_code == 200:
            print("✅ Admin login page loads successfully")
        else:
            print(f"❌ Admin login page failed: {login_response.status_code}")
            return False
    else:
        print(f"❌ Admin index unexpected status: {response.status_code}")
        return False
    
    return True

def test_admin_url_patterns():
    """Test all admin URL patterns"""
    print("\n🔍 Testing Admin URL Patterns...")
    print("=" * 50)
    
    urls_to_test = [
        ('admin:index', 'Admin Index'),
        ('admin:login', 'Admin Login'),
        ('admin:logout', 'Admin Logout'),
        ('admin:password_change', 'Password Change'),
        ('admin:users_user_add', 'Add User'),
        ('admin:users_user_changelist', 'User List'),
    ]
    
    for url_name, description in urls_to_test:
        try:
            url = reverse(url_name)
            print(f"✅ {description}: {url}")
        except Exception as e:
            print(f"❌ {description}: Error - {e}")
            return False
    
    return True

def test_admin_templates():
    """Test admin template files exist and contain PMC theme"""
    print("\n🔍 Testing Admin Templates...")
    print("=" * 50)
    
    template_dir = os.path.join(settings.BASE_DIR, 'templates', 'admin')
    
    required_templates = [
        'base.html',
        'base_site.html',
        'index.html', 
        'login.html',
        'logged_out.html',
        'change_form.html',
        'change_list.html',
        'delete_confirmation.html',
        '404.html',
        '500.html'
    ]
    
    for template in required_templates:
        template_path = os.path.join(template_dir, template)
        if os.path.exists(template_path):
            # Check if template contains PMC theme elements
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if '#667eea' in content or '#764ba2' in content or 'pmc' in content.lower():
                    print(f"✅ {template} (PMC themed)")
                else:
                    print(f"⚠️  {template} (no PMC theme detected)")
        else:
            print(f"❌ {template} - NOT FOUND")
            return False
    
    return True

def test_user_model_admin():
    """Test custom User model admin registration"""
    print("\n🔍 Testing User Model Admin...")
    print("=" * 50)
    
    User = get_user_model()
    
    # Check model details
    print(f"✅ User model: {User._meta.label}")
    print(f"✅ User model app: {User._meta.app_label}")
    print(f"✅ User model name: {User._meta.model_name}")
    
    # Check admin registration
    from django.contrib.admin.sites import site
    if User in site._registry:
        admin_class = site._registry[User]
        print(f"✅ User admin class: {admin_class.__class__.__name__}")
        
        # Check if it has import/export
        if hasattr(admin_class, 'resource_class'):
            print("✅ Import/Export functionality enabled")
        else:
            print("⚠️  Import/Export functionality not detected")
    else:
        print("❌ User model not registered in admin")
        return False
    
    return True

def test_pmc_theme_consistency():
    """Test PMC theme consistency across templates"""
    print("\n🔍 Testing PMC Theme Consistency...")
    print("=" * 50)
    
    theme_colors = ['#667eea', '#764ba2']
    template_dir = os.path.join(settings.BASE_DIR, 'templates', 'admin')
    
    themed_templates = 0
    total_templates = 0
    
    for root, dirs, files in os.walk(template_dir):
        for file in files:
            if file.endswith('.html'):
                total_templates += 1
                template_path = os.path.join(root, file)
                
                try:
                    with open(template_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    has_pmc_colors = any(color in content for color in theme_colors)
                    has_gradient = 'linear-gradient' in content and ('667eea' in content or '764ba2' in content)
                    has_bootstrap = 'bootstrap' in content.lower()
                    has_fontawesome = 'font-awesome' in content.lower() or 'fas fa-' in content
                    
                    if has_pmc_colors or has_gradient:
                        themed_templates += 1
                        status = "✅"
                        if has_bootstrap and has_fontawesome:
                            status += " (Full PMC theme)"
                        elif has_bootstrap or has_fontawesome:
                            status += " (Partial PMC theme)"
                        else:
                            status += " (PMC colors only)"
                    else:
                        status = "⚠️  (No PMC theme)"
                    
                    rel_path = os.path.relpath(template_path, template_dir)
                    print(f"{status} {rel_path}")
                    
                except Exception as e:
                    print(f"❌ {file} - Error reading: {e}")
    
    theme_percentage = (themed_templates / total_templates * 100) if total_templates > 0 else 0
    print(f"\n📊 PMC Theme Coverage: {themed_templates}/{total_templates} templates ({theme_percentage:.1f}%)")
    
    return theme_percentage >= 80  # At least 80% should be themed

def main():
    """Run all admin tests"""
    print("🚀 SIMS Admin System - Final Verification")
    print("=" * 60)
    
    tests = [
        ("Admin Accessibility", test_admin_accessibility),
        ("URL Patterns", test_admin_url_patterns), 
        ("Template Files", test_admin_templates),
        ("User Model Admin", test_user_model_admin),
        ("PMC Theme Consistency", test_pmc_theme_consistency),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append(result)
            if result:
                print(f"\n✅ {test_name}: PASSED")
            else:
                print(f"\n❌ {test_name}: FAILED")
        except Exception as e:
            print(f"\n❌ {test_name}: ERROR - {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    print("FINAL RESULTS:")
    print("=" * 60)
    
    passed_tests = sum(results)
    total_tests = len(results)
    
    for i, (test_name, _) in enumerate(tests):
        status = "✅ PASSED" if results[i] else "❌ FAILED"
        print(f"{test_name:.<40} {status}")
    
    print("-" * 60)
    print(f"TOTAL: {passed_tests}/{total_tests} tests passed ({passed_tests/total_tests*100:.1f}%)")
    
    if passed_tests == total_tests:
        print("\n🎉 ALL TESTS PASSED! Admin system is fully functional with PMC theme!")
    elif passed_tests >= total_tests * 0.8:
        print("\n⚠️  MOSTLY SUCCESSFUL! Minor issues may need attention.")
    else:
        print("\n❌ SIGNIFICANT ISSUES DETECTED! Please review the failed tests.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
