#!/usr/bin/env python3
"""
SIMS System Comprehensive Verification Script
Checks all URLs, templates, and functionality across all apps
"""

import os
import sys
import django
import requests
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

def check_urls():
    """Check if all main URLs are accessible"""
    base_url = "http://127.0.0.1:8000"
    
    # URLs to check
    urls_to_check = [
        # Main pages
        ('/', 'Homepage'),
        ('/users/login/', 'Login Page'),
        
        # App main pages (these should redirect to login if not authenticated)
        ('/users/', 'Users Dashboard'),
        ('/certificates/', 'Certificates List'),
        ('/logbook/', 'Logbook List'),
        ('/rotations/', 'Rotations List'),
        ('/cases/', 'Cases List'),
        
        # Dashboard pages
        ('/certificates/dashboard/', 'Certificates Dashboard'),
        ('/logbook/dashboard/', 'Logbook Dashboard'),
        ('/rotations/dashboard/', 'Rotations Dashboard'),
        
        # Analytics pages
        ('/logbook/analytics/', 'Logbook Analytics'),
    ]
    
    print("🔍 Checking URL accessibility...")
    print("=" * 50)
    
    results = []
    for url, description in urls_to_check:
        try:
            response = requests.get(f"{base_url}{url}", timeout=5)
            status = "✅ OK" if response.status_code in [200, 302] else f"❌ {response.status_code}"
            results.append((url, description, status, response.status_code))
            print(f"{status:<10} {url:<30} - {description}")
        except requests.exceptions.RequestException as e:
            results.append((url, description, f"❌ ERROR", str(e)))
            print(f"❌ ERROR   {url:<30} - {description} ({e})")
    
    return results

def check_templates():
    """Check if all expected templates exist"""
    template_dir = Path("templates")
    
    expected_templates = {
        'base': ['base.html'],
        'home': ['index.html'],
        'registration': ['login.html', 'password_change_form.html', 'password_change_done.html', 
                        'password_reset_form.html', 'password_reset_done.html', 
                        'password_reset_confirm.html', 'password_reset_complete.html'],
        'users': ['admin_dashboard.html', 'pg_dashboard.html', 'supervisor_dashboard.html',
                 'profile.html', 'user_detail.html', 'user_list.html', 'user_create.html',
                 'user_edit.html', 'pg_list.html', 'supervisor_list.html',
                 'admin_analytics.html', 'pg_analytics.html', 'supervisor_analytics.html',
                 'user_reports.html'],
        'certificates': ['dashboard.html', 'certificate_list.html', 'certificate_form.html', 
                        'certificate_detail.html'],
        'logbook': ['dashboard.html', 'analytics.html', 'logbook_list.html', 
                   'logbook_form.html', 'logbook_detail.html'],
        'rotations': ['dashboard.html', 'rotation_list.html', 'rotation_form.html', 
                     'rotation_detail.html'],
        'cases': ['case_list.html', 'case_form.html', 'case_detail.html', 
                 'case_review_form.html', 'case_statistics.html']
    }
    
    print("\n📄 Checking template files...")
    print("=" * 50)
    
    missing_templates = []
    existing_templates = []
    
    for app, templates in expected_templates.items():
        app_dir = template_dir / app
        print(f"\n{app.upper()} App Templates:")
        
        for template in templates:
            template_path = app_dir / template
            if template_path.exists():
                existing_templates.append(f"{app}/{template}")
                print(f"  ✅ {template}")
            else:
                missing_templates.append(f"{app}/{template}")
                print(f"  ❌ {template} (MISSING)")
    
    return existing_templates, missing_templates

def check_static_files():
    """Check static files and CSS/JS includes"""
    static_files = [
        'Bootstrap CSS (CDN)',
        'Font Awesome (CDN)',
        'jQuery (CDN)',
        'Select2 (CDN)',
        'Chart.js (CDN)'
    ]
    
    print("\n🎨 Static Files & CDN Resources:")
    print("=" * 50)
    
    # Check if base template includes all necessary CDNs
    base_template = Path("templates/base/base.html")
    if base_template.exists():
        content = base_template.read_text()
        
        cdn_checks = [
            ('Bootstrap CSS', 'bootstrap@5.1.3/dist/css/bootstrap.min.css'),
            ('Font Awesome', 'font-awesome/6.0.0/css/all.min.css'),
            ('Select2 CSS', 'select2@4.1.0-rc.0/dist/css/select2.min.css'),
            ('Bootstrap JS', 'bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js'),
            ('jQuery', 'jquery-3.6.0.min.js'),
            ('Select2 JS', 'select2@4.1.0-rc.0/dist/js/select2.min.js'),
            ('Chart.js', 'chart.js'),
        ]
        
        for name, cdn_part in cdn_checks:
            if cdn_part in content:
                print(f"  ✅ {name}")
            else:
                print(f"  ❌ {name} (NOT FOUND)")
    else:
        print("  ❌ Base template not found")

def check_models_and_apps():
    """Check if all Django apps are properly configured"""
    from django.apps import apps
    from django.conf import settings
    
    print("\n🏗️  Django Apps Configuration:")
    print("=" * 50)
    
    expected_apps = [
        'sims.users',
        'sims.certificates', 
        'sims.logbook',
        'sims.rotations',
        'sims.cases'
    ]
    
    installed_apps = settings.INSTALLED_APPS
    
    for app in expected_apps:
        if app in installed_apps:
            print(f"  ✅ {app}")
            try:
                # Try to get models from the app
                app_config = apps.get_app_config(app.split('.')[-1])
                models = app_config.get_models()
                print(f"     📊 {len(models)} model(s) found")
            except Exception as e:
                print(f"     ⚠️  Error getting models: {e}")
        else:
            print(f"  ❌ {app} (NOT INSTALLED)")

def check_database():
    """Check database connectivity and basic data"""
    print("\n🗄️  Database Connectivity:")
    print("=" * 50)
    
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        user_count = User.objects.count()
        print(f"  ✅ Database connected")
        print(f"  👥 {user_count} user(s) in system")
        
        # Check if superuser exists
        admin_users = User.objects.filter(is_superuser=True).count()
        print(f"  🔑 {admin_users} admin user(s)")
        
        # Check each model
        model_checks = []
        try:
            from sims.users.models import User
            from sims.certificates.models import Certificate
            from sims.logbook.models import LogbookEntry
            from sims.rotations.models import Rotation
            from sims.cases.models import Case
            
            models_to_check = [
                (User, 'Users'),
                (Certificate, 'Certificates'),
                (LogbookEntry, 'Logbook Entries'),
                (Rotation, 'Rotations'),
                (Case, 'Cases')
            ]
            
            for model, name in models_to_check:
                try:
                    count = model.objects.count()
                    print(f"  📊 {count} {name}")
                    model_checks.append((name, count, True))
                except Exception as e:
                    print(f"  ❌ Error querying {name}: {e}")
                    model_checks.append((name, 0, False))
                    
        except ImportError as e:
            print(f"  ⚠️  Could not import models: {e}")
            
    except Exception as e:
        print(f"  ❌ Database error: {e}")

def main():
    """Run comprehensive system check"""
    print("🏥 SIMS - Comprehensive System Verification")
    print("=" * 60)
    print("Checking all components of the SIMS system...\n")
    
    # Check if Django server is running
    try:
        response = requests.get("http://127.0.0.1:8000/health/", timeout=5)
        if response.status_code == 200:
            print("✅ Django server is running")
        else:
            print("⚠️  Django server responded but with unexpected status")
    except requests.exceptions.RequestException:
        print("❌ Django server is not running or not accessible")
        print("   Please start the server with: py manage.py runserver")
        return
    
    # Run all checks
    url_results = check_urls()
    existing_templates, missing_templates = check_templates()
    check_static_files()
    check_models_and_apps()
    check_database()
    
    # Summary
    print("\n📋 SUMMARY")
    print("=" * 60)
    
    total_urls = len(url_results)
    working_urls = len([r for r in url_results if r[3] in [200, 302]])
    print(f"URLs: {working_urls}/{total_urls} working")
    
    total_expected_templates = sum(len(templates) for templates in {
        'base': ['base.html'],
        'home': ['index.html'],
        'registration': ['login.html', 'password_change_form.html', 'password_change_done.html', 
                        'password_reset_form.html', 'password_reset_done.html', 
                        'password_reset_confirm.html', 'password_reset_complete.html'],
        'users': ['admin_dashboard.html', 'pg_dashboard.html', 'supervisor_dashboard.html',
                 'profile.html', 'user_detail.html', 'user_list.html', 'user_create.html',
                 'user_edit.html', 'pg_list.html', 'supervisor_list.html',
                 'admin_analytics.html', 'pg_analytics.html', 'supervisor_analytics.html',
                 'user_reports.html'],
        'certificates': ['dashboard.html', 'certificate_list.html', 'certificate_form.html', 
                        'certificate_detail.html'],
        'logbook': ['dashboard.html', 'analytics.html', 'logbook_list.html', 
                   'logbook_form.html', 'logbook_detail.html'],
        'rotations': ['dashboard.html', 'rotation_list.html', 'rotation_form.html', 
                     'rotation_detail.html'],
        'cases': ['case_list.html', 'case_form.html', 'case_detail.html', 
                 'case_review_form.html', 'case_statistics.html']
    }.values())
    
    existing_count = len(existing_templates)
    print(f"Templates: {existing_count}/{total_expected_templates} exist")
    
    if missing_templates:
        print(f"\n⚠️  Missing Templates ({len(missing_templates)}):")
        for template in missing_templates:
            print(f"   - {template}")
    
    # Overall health score
    url_health = (working_urls / total_urls) * 100
    template_health = (existing_count / total_expected_templates) * 100
    overall_health = (url_health + template_health) / 2
    
    print(f"\n🏥 Overall System Health: {overall_health:.1f}%")
    
    if overall_health >= 90:
        print("🟢 Excellent - System is fully functional")
    elif overall_health >= 75:
        print("🟡 Good - Minor issues detected")
    elif overall_health >= 50:
        print("🟠 Fair - Several issues need attention")
    else:
        print("🔴 Poor - Major issues require immediate attention")

if __name__ == "__main__":
    main()
