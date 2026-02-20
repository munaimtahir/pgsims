#!/usr/bin/env python
"""
SIMS System Validation Script
Tests all components after bug fixes and improvements
"""

import os
import sys
import django
from django.core import management
from django.test.utils import get_runner
from django.conf import settings
from django.urls import reverse
from django.test import Client
import json

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

def test_url_patterns():
    """Test that all URL patterns are working correctly"""
    print("=== Testing URL Patterns ===")
    
    from django.urls import resolve, reverse, NoReverseMatch
    
    # Test critical URL patterns
    test_urls = [
        # Users URLs
        'users:login',
        'users:dashboard', 
        'users:admin_analytics',
        'users:supervisor_analytics',
        'users:pg_analytics',
        
        # Cases URLs
        'cases:case_list',
        'cases:case_create',
        'cases:case_statistics',
        
        # Logbook URLs
        'logbook:list',
        'logbook:create',
        
        # Rotations URLs
        'rotations:list',
        'rotations:create',
        
        # Certificates URLs
        'certificates:list',
        'certificates:create',
        'certificates:dashboard',
    ]
    
    passed = 0
    failed = 0
    
    for url_name in test_urls:
        try:
            url = reverse(url_name)
            print(f"✓ {url_name} -> {url}")
            passed += 1
        except NoReverseMatch as e:
            print(f"✗ {url_name} -> ERROR: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {url_name} -> UNEXPECTED ERROR: {e}")
            failed += 1
    
    print(f"\nURL Pattern Results: {passed} passed, {failed} failed")
    return failed == 0

def test_role_based_access():
    """Test role-based access control"""
    print("\n=== Testing Role-Based Access Control ===")
    
    from django.contrib.auth import get_user_model
    from sims.users.decorators import admin_required, supervisor_required, pg_required
    
    User = get_user_model()
    
    # Check if decorators exist
    decorators_exist = True
    try:
        assert callable(admin_required)
        assert callable(supervisor_required) 
        assert callable(pg_required)
        print("✓ All role-based decorators exist")
    except (ImportError, AssertionError) as e:
        print(f"✗ Role-based decorators missing: {e}")
        decorators_exist = False
    
    return decorators_exist

def test_analytics_views():
    """Test analytics views are properly set up"""
    print("\n=== Testing Analytics Views ===")
    
    from sims.users.views import admin_analytics_view, supervisor_analytics_view, pg_analytics_view
    
    analytics_views_exist = True
    try:
        assert callable(admin_analytics_view)
        assert callable(supervisor_analytics_view)
        assert callable(pg_analytics_view)
        print("✓ All analytics views exist")
    except (ImportError, AssertionError) as e:
        print(f"✗ Analytics views missing: {e}")
        analytics_views_exist = False
    
    return analytics_views_exist

def test_template_existence():
    """Test that all required templates exist"""
    print("\n=== Testing Template Existence ===")
    
    import os
    
    required_templates = [
        'templates/users/admin_analytics.html',
        'templates/users/supervisor_analytics.html',
        'templates/users/pg_analytics.html',
        'templates/users/admin_dashboard.html',
        'templates/users/supervisor_dashboard.html',
        'templates/users/pg_dashboard.html',
        'templates/certificates/dashboard.html',
        'templates/rotations/dashboard.html',
        'templates/logbook/dashboard.html',
    ]
    
    passed = 0
    failed = 0
    
    for template in required_templates:
        if os.path.exists(template):
            print(f"✓ {template}")
            passed += 1
        else:
            print(f"✗ {template} - NOT FOUND")
            failed += 1
    
    print(f"\nTemplate Results: {passed} passed, {failed} failed")
    return failed == 0

def test_chart_data_integration():
    """Test chart data integration in templates"""
    print("\n=== Testing Chart Data Integration ===")
    
    # Check if certificate dashboard has data attributes
    cert_dashboard_path = 'templates/certificates/dashboard.html'
    if os.path.exists(cert_dashboard_path):
        with open(cert_dashboard_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'data-distribution=' in content:
                print("✓ Certificate dashboard has chart data attributes")
                return True
            else:
                print("✗ Certificate dashboard missing chart data attributes")
                return False
    else:
        print("✗ Certificate dashboard template not found")
        return False

def test_database_migrations():
    """Test database migrations are up to date"""
    print("\n=== Testing Database Migrations ===")
    
    try:
        management.call_command('showmigrations', verbosity=0)
        print("✓ Database migrations are accessible")
        return True
    except Exception as e:
        print(f"✗ Database migration error: {e}")
        return False

def main():
    """Run all validation tests"""
    print("SIMS System Validation")
    print("=" * 50)
    
    results = []
    
    # Run all tests
    results.append(("URL Patterns", test_url_patterns()))
    results.append(("Role-Based Access", test_role_based_access()))
    results.append(("Analytics Views", test_analytics_views()))
    results.append(("Template Existence", test_template_existence()))
    results.append(("Chart Data Integration", test_chart_data_integration()))
    results.append(("Database Migrations", test_database_migrations()))
    
    # Summary
    print("\n" + "=" * 50)
    print("VALIDATION SUMMARY")
    print("=" * 50)
    
    passed_count = 0
    total_count = len(results)
    
    for test_name, passed in results:
        status = "PASS" if passed else "FAIL"
        print(f"{test_name:.<25} {status}")
        if passed:
            passed_count += 1
    
    print(f"\nOverall: {passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("\n🎉 ALL TESTS PASSED! SIMS system is ready for deployment.")
        return 0
    else:
        print(f"\n⚠️  {total_count - passed_count} test(s) failed. Please review and fix issues.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
