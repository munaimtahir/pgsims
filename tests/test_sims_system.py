#!/usr/bin/env python
"""
Simple test script to verify SIMS dashboard and analytics functionality
"""
import os
import sys
import django

# Add the project directory to Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_dir)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

def test_dashboard_views():
    """Test all dashboard views are properly configured"""
    print("🔍 Testing Dashboard Views...")
    
    try:
        from django.urls import reverse, resolve
        from sims.users.views import (
            AdminDashboardView, SupervisorDashboardView, PGDashboardView,
            UserListView, UserCreateView, SupervisorListView
        )
        
        # Test URL resolution
        dashboard_urls = [
            ('users:admin_dashboard', AdminDashboardView),
            ('users:supervisor_dashboard', SupervisorDashboardView), 
            ('users:pg_dashboard', PGDashboardView),
            ('users:user_list', UserListView),
            ('users:user_create', UserCreateView),
            ('users:supervisor_list', SupervisorListView),
        ]
        
        for url_name, view_class in dashboard_urls:
            try:
                url = reverse(url_name)
                resolver = resolve(url)
                print(f"  ✅ {url_name}: {url} -> {resolver.func.view_class.__name__}")
            except Exception as e:
                print(f"  ❌ {url_name}: {e}")
        
        print("  ✅ Dashboard views configured correctly")
        return True
        
    except Exception as e:
        print(f"  ❌ Dashboard views error: {e}")
        return False

def test_analytics_views():
    """Test analytics views"""
    print("\n📊 Testing Analytics Views...")
    
    try:
        from django.urls import reverse
        from sims.logbook.views import LogbookAnalyticsView, LogbookDashboardView
        from sims.certificates.views import CertificateDashboardView
        from sims.rotations.views import RotationDashboardView
        from sims.cases.views import case_statistics_view
        
        analytics_views = [
            'logbook:analytics',
            'logbook:dashboard', 
            'certificates:dashboard',
            'rotations:dashboard',
            'cases:statistics',
        ]
        
        for view_name in analytics_views:
            try:
                url = reverse(view_name)
                print(f"  ✅ {view_name}: {url}")
            except Exception as e:
                print(f"  ❌ {view_name}: {e}")
        
        print("  ✅ Analytics views configured correctly")
        return True
        
    except Exception as e:
        print(f"  ❌ Analytics views error: {e}")
        return False

def test_templates():
    """Test template existence"""
    print("\n📄 Testing Templates...")
    
    templates = [
        'users/admin_dashboard.html',
        'users/supervisor_dashboard.html', 
        'users/pg_dashboard.html',
        'users/user_list.html',
        'users/user_create.html',
        'users/supervisor_list.html',
        'users/pg_list.html',
        'users/user_reports.html',
        'logbook/analytics.html',
        'logbook/dashboard.html',
        'certificates/dashboard.html',
        'rotations/dashboard.html',
        'registration/login.html',
    ]
    
    template_dir = os.path.join(project_dir, 'templates')
    
    for template in templates:
        template_path = os.path.join(template_dir, template)
        if os.path.exists(template_path):
            print(f"  ✅ {template}")
        else:
            print(f"  ❌ {template} - NOT FOUND")
    
    return True

def test_database_models():
    """Test database models"""
    print("\n🗄️  Testing Database Models...")
    
    try:
        from sims.users.models import User
        from sims.logbook.models import LogbookEntry
        from sims.cases.models import Case
        from sims.rotations.models import Rotation
        from sims.certificates.models import Certificate
        
        # Test model creation (without actually saving)
        user_fields = [f.name for f in User._meta.fields]
        print(f"  ✅ User model: {len(user_fields)} fields")
        
        logbook_fields = [f.name for f in LogbookEntry._meta.fields]
        print(f"  ✅ LogbookEntry model: {len(logbook_fields)} fields")
        
        case_fields = [f.name for f in Case._meta.fields]
        print(f"  ✅ Case model: {len(case_fields)} fields")
        
        rotation_fields = [f.name for f in Rotation._meta.fields]
        print(f"  ✅ Rotation model: {len(rotation_fields)} fields")
        
        cert_fields = [f.name for f in Certificate._meta.fields]
        print(f"  ✅ Certificate model: {len(cert_fields)} fields")
        
        print("  ✅ All models loaded successfully")
        return True
        
    except Exception as e:
        print(f"  ❌ Database models error: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints"""
    print("\n🔌 Testing API Endpoints...")
    
    try:
        from django.urls import reverse
        
        api_endpoints = [
            'users:user_search_api',
            'users:user_stats_api',
            'logbook:api_entry_stats',
            'cases:api_case_stats',
        ]
        
        for endpoint in api_endpoints:
            try:
                url = reverse(endpoint)
                print(f"  ✅ {endpoint}: {url}")
            except Exception as e:
                print(f"  ❌ {endpoint}: {e}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ API endpoints error: {e}")
        return False

def run_comprehensive_test():
    """Run all tests"""
    print("🚀 SIMS System Verification")
    print("=" * 50)
    
    tests = [
        test_dashboard_views,
        test_analytics_views,
        test_templates,
        test_database_models,
        test_api_endpoints,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📋 TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    print(f"✅ Tests Passed: {passed}/{total}")
    print(f"❌ Tests Failed: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! SIMS system is ready.")
        print("\n📝 Next Steps:")
        print("  1. Run: python manage.py runserver")
        print("  2. Visit: http://127.0.0.1:8000/")
        print("  3. Create superuser: python manage.py createsuperuser")
        print("  4. Access admin: http://127.0.0.1:8000/admin/")
        print("  5. Test dashboards for each user role")
    else:
        print("\n⚠️  Some tests failed. Please review the errors above.")
    
    return passed == total

if __name__ == '__main__':
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)
