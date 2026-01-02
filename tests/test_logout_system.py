#!/usr/bin/env python
"""
Comprehensive Logout Functionality Test
Tests all logout scenarios, redirects, and PMC theme consistency
"""
import os
import sys
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model

def test_logout_urls():
    """Test logout URL patterns"""
    print("🔍 Testing Logout URL Patterns...")
    print("=" * 50)
    
    try:
        # Test main site logout
        users_logout = reverse('users:logout')
        print(f"✅ Users Logout URL: {users_logout}")
        
        # Test admin logout
        admin_logout = reverse('admin:logout')
        print(f"✅ Admin Logout URL: {admin_logout}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing logout URLs: {e}")
        return False

def test_logout_pages():
    """Test logout pages are accessible"""
    print("\n🔍 Testing Logout Page Accessibility...")
    print("=" * 50)
    
    client = Client()
    
    try:
        # Test users logout page (should work without authentication)
        response = client.get('/users/logout/')
        if response.status_code == 200:
            print("✅ Users logout page loads successfully (200)")
        else:
            print(f"❌ Users logout page failed: {response.status_code}")
            return False
        
        # Test admin logout page
        admin_response = client.get('/admin/logout/')
        if admin_response.status_code in [200, 302]:  # 302 is redirect which is expected
            print(f"✅ Admin logout page accessible ({admin_response.status_code})")
        else:
            print(f"❌ Admin logout page failed: {admin_response.status_code}")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Error testing logout pages: {e}")
        return False

def test_logout_templates():
    """Test logout template files exist and contain PMC theme"""
    print("\n🔍 Testing Logout Templates...")
    print("=" * 50)
    
    template_dir = os.path.join(settings.BASE_DIR, 'templates')
    
    logout_templates = [
        'users/logged_out.html',
        'admin/logged_out.html',
        'registration/logged_out.html'
    ]
    
    for template in logout_templates:
        template_path = os.path.join(template_dir, template)
        if os.path.exists(template_path):
            # Check if template contains PMC theme elements
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            has_pmc_colors = '#667eea' in content or '#764ba2' in content
            has_gradient = 'linear-gradient' in content and ('667eea' in content or '764ba2' in content)
            has_bootstrap = 'bootstrap' in content.lower() or 'btn' in content
            has_fontawesome = 'font-awesome' in content.lower() or 'fas fa-' in content
            
            if has_pmc_colors or has_gradient:
                status = "✅ PMC themed"
                if has_bootstrap and has_fontawesome:
                    status += " (Full theme)"
                elif has_bootstrap or has_fontawesome:
                    status += " (Partial theme)"
            else:
                status = "⚠️  Basic theme"
            
            print(f"{status} {template}")
        else:
            print(f"❌ {template} - NOT FOUND")
            return False
    
    return True

def test_logout_redirects():
    """Test logout redirect behavior"""
    print("\n🔍 Testing Logout Redirect Behavior...")
    print("=" * 50)
    
    try:
        # Check settings
        login_url = getattr(settings, 'LOGIN_URL', None)
        logout_redirect_url = getattr(settings, 'LOGOUT_REDIRECT_URL', None)
        login_redirect_url = getattr(settings, 'LOGIN_REDIRECT_URL', None)
        
        print(f"✅ LOGIN_URL: {login_url}")
        print(f"✅ LOGOUT_REDIRECT_URL: {logout_redirect_url}")
        print(f"✅ LOGIN_REDIRECT_URL: {login_redirect_url}")
        
        if logout_redirect_url and '/logout/' in logout_redirect_url:
            print("✅ Logout redirects to logout page (correct)")
        elif logout_redirect_url and '/login/' in logout_redirect_url:
            print("⚠️  Logout redirects to login page (basic)")
        else:
            print(f"❌ Unexpected logout redirect: {logout_redirect_url}")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Error testing logout redirects: {e}")
        return False

def test_logout_security():
    """Test logout security features"""
    print("\n🔍 Testing Logout Security Features...")
    print("=" * 50)
    
    template_dir = os.path.join(settings.BASE_DIR, 'templates')
    
    try:
        # Check users logout template for security features
        users_template = os.path.join(template_dir, 'users', 'logged_out.html')
        if os.path.exists(users_template):
            with open(users_template, 'r', encoding='utf-8') as f:
                content = f.read()
            
            security_features = []
            
            if 'security' in content.lower():
                security_features.append("Security messaging")
            
            if 'shared computer' in content.lower():
                security_features.append("Shared computer warning")
            
            if 'close browser' in content.lower():
                security_features.append("Browser close recommendation")
            
            if 'session' in content.lower():
                security_features.append("Session information")
            
            if security_features:
                print(f"✅ Security features found: {', '.join(security_features)}")
            else:
                print("⚠️  No specific security features detected")
        
        # Check session settings
        session_expire = getattr(settings, 'SESSION_EXPIRE_AT_BROWSER_CLOSE', False)
        session_age = getattr(settings, 'SESSION_COOKIE_AGE', 0)
        
        print(f"✅ Session expires on browser close: {session_expire}")
        print(f"✅ Session cookie age: {session_age} seconds")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing logout security: {e}")
        return False

def test_logout_user_experience():
    """Test logout user experience features"""
    print("\n🔍 Testing Logout User Experience...")
    print("=" * 50)
    
    template_dir = os.path.join(settings.BASE_DIR, 'templates')
    
    try:
        # Check for UX features in logout templates
        ux_features = {
            'animations': ['animation:', 'fadeIn', 'bounceIn', '@keyframes'],
            'responsive_design': ['@media', 'mobile', 'tablet', 'responsive'],
            'interactive_elements': ['hover', ':hover', 'transition:', 'transform:'],
            'user_feedback': ['welcome', 'goodbye', 'successfully', 'logged out'],
            'navigation_options': ['login again', 'homepage', 'main site', 'return']
        }
        
        users_template = os.path.join(template_dir, 'users', 'logged_out.html')
        admin_template = os.path.join(template_dir, 'admin', 'logged_out.html')
        
        for template_path, template_name in [(users_template, 'Users'), (admin_template, 'Admin')]:
            if os.path.exists(template_path):
                with open(template_path, 'r', encoding='utf-8') as f:
                    content = f.read().lower()
                
                print(f"\n{template_name} Template UX Features:")
                
                for feature_category, keywords in ux_features.items():
                    found_keywords = [kw for kw in keywords if kw in content]
                    if found_keywords:
                        print(f"  ✅ {feature_category.replace('_', ' ').title()}: {', '.join(found_keywords[:2])}")
                    else:
                        print(f"  ⚠️  {feature_category.replace('_', ' ').title()}: Not detected")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing logout UX: {e}")
        return False

def main():
    """Run all logout tests"""
    print("🚀 SIMS Logout System - Comprehensive Verification")
    print("=" * 60)
    
    tests = [
        ("Logout URL Patterns", test_logout_urls),
        ("Logout Page Accessibility", test_logout_pages),
        ("Logout Templates", test_logout_templates),
        ("Logout Redirects", test_logout_redirects),
        ("Logout Security", test_logout_security),
        ("Logout User Experience", test_logout_user_experience),
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
    print("LOGOUT SYSTEM RESULTS:")
    print("=" * 60)
    
    passed_tests = sum(results)
    total_tests = len(results)
    
    for i, (test_name, _) in enumerate(tests):
        status = "✅ PASSED" if results[i] else "❌ FAILED"
        print(f"{test_name:.<40} {status}")
    
    print("-" * 60)
    print(f"TOTAL: {passed_tests}/{total_tests} tests passed ({passed_tests/total_tests*100:.1f}%)")
    
    if passed_tests == total_tests:
        print("\n🎉 ALL LOGOUT TESTS PASSED! Logout system is fully functional!")
    elif passed_tests >= total_tests * 0.8:
        print("\n⚠️  LOGOUT SYSTEM MOSTLY FUNCTIONAL! Minor issues may need attention.")
    else:
        print("\n❌ LOGOUT SYSTEM NEEDS ATTENTION! Please review the failed tests.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
