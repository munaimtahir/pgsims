#!/usr/bin/env python3
"""
SIMS System Template and URL Verification
Checks templates and URL configuration without external dependencies
"""

import os
import sys
import django
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

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
    
    print("📄 Checking template files...")
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

def check_urls():
    """Check URL configuration"""
    from django.urls import reverse
    from django.core.exceptions import NoReverseMatch
    
    print("\n🔗 Checking URL patterns...")
    print("=" * 50)
    
    # URLs to test (name, description)
    urls_to_test = [
        ('home', 'Homepage'),
        ('users:login', 'Login'),
        ('users:dashboard', 'User Dashboard'),
        ('certificates:list', 'Certificates List'),
        ('certificates:dashboard', 'Certificates Dashboard'),
        ('logbook:list', 'Logbook List'),
        ('logbook:dashboard', 'Logbook Dashboard'),
        ('logbook:analytics', 'Logbook Analytics'),
        ('rotations:list', 'Rotations List'),
        ('rotations:dashboard', 'Rotations Dashboard'),
        ('cases:case_list', 'Cases List'),
    ]
    
    working_urls = []
    broken_urls = []
    
    for url_name, description in urls_to_test:
        try:
            url = reverse(url_name)
            working_urls.append((url_name, description, url))
            print(f"  ✅ {url_name:<25} -> {url}")
        except NoReverseMatch as e:
            broken_urls.append((url_name, description, str(e)))
            print(f"  ❌ {url_name:<25} -> ERROR: {e}")
    
    return working_urls, broken_urls

def check_models():
    """Check if models can be imported and basic functionality"""
    print("\n🏗️  Model Accessibility:")
    print("=" * 50)
    
    models_to_check = [
        ('sims.users.models', 'User'),
        ('sims.certificates.models', 'Certificate'),
        ('sims.logbook.models', 'LogbookEntry'),
        ('sims.rotations.models', 'Rotation'),
        ('sims.cases.models', 'Case'),
    ]
    
    working_models = []
    broken_models = []
    
    for module_path, model_name in models_to_check:
        try:
            module = __import__(module_path, fromlist=[model_name])
            model = getattr(module, model_name)
            count = model.objects.count()
            working_models.append((model_name, count))
            print(f"  ✅ {model_name:<15} - {count} records")
        except Exception as e:
            broken_models.append((model_name, str(e)))
            print(f"  ❌ {model_name:<15} - ERROR: {e}")
    
    return working_models, broken_models

def check_apps_configuration():
    """Check Django apps configuration"""
    from django.conf import settings
    from django.apps import apps
    
    print("\n⚙️  Apps Configuration:")
    print("=" * 50)
    
    expected_sims_apps = [
        'sims.users',
        'sims.certificates',
        'sims.logbook', 
        'sims.rotations',
        'sims.cases'
    ]
    
    installed_apps = settings.INSTALLED_APPS
    
    for app in expected_sims_apps:
        if app in installed_apps:
            try:
                app_config = apps.get_app_config(app.split('.')[-1])
                models = app_config.get_models()
                print(f"  ✅ {app:<20} - {len(models)} model(s)")
            except Exception as e:
                print(f"  ⚠️  {app:<20} - Installed but error: {e}")
        else:
            print(f"  ❌ {app:<20} - NOT INSTALLED")

def check_base_template():
    """Check base template for required includes"""
    print("\n🎨 Base Template Check:")
    print("=" * 50)
    
    base_template_path = Path("templates/base/base.html")
    
    if not base_template_path.exists():
        print("  ❌ Base template not found")
        return
    
    content = base_template_path.read_text()
    
    required_includes = [
        ('Bootstrap CSS', 'bootstrap'),
        ('Font Awesome', 'font-awesome'),
        ('jQuery', 'jquery'),
        ('CSRF Token', 'csrf_token'),
        ('Block Title', 'block title'),
        ('Block Content', 'block content'),
        ('Navigation', 'navbar'),
    ]
    
    for name, check_string in required_includes:
        if check_string.lower() in content.lower():
            print(f"  ✅ {name}")
        else:
            print(f"  ⚠️  {name} - May be missing")

def main():
    """Run verification"""
    print("🏥 SIMS - Template and Configuration Verification")
    print("=" * 60)
    
    # Check templates
    existing_templates, missing_templates = check_templates()
    
    # Check URLs
    working_urls, broken_urls = check_urls()
    
    # Check models
    working_models, broken_models = check_models()
    
    # Check apps
    check_apps_configuration()
    
    # Check base template
    check_base_template()
    
    # Summary
    print("\n📊 SUMMARY")
    print("=" * 60)
    
    # Calculate totals
    total_expected_templates = 33  # Based on expected_templates count
    existing_count = len(existing_templates)
    missing_count = len(missing_templates)
    
    total_urls = len(working_urls) + len(broken_urls)
    working_urls_count = len(working_urls)
    
    total_models = len(working_models) + len(broken_models)
    working_models_count = len(working_models)
    
    print(f"Templates: {existing_count}/{total_expected_templates} exist ({missing_count} missing)")
    print(f"URLs: {working_urls_count}/{total_urls} working")
    print(f"Models: {working_models_count}/{total_models} accessible")
    
    if missing_templates:
        print(f"\n⚠️  Missing Templates:")
        for template in missing_templates[:10]:  # Show first 10
            print(f"   - {template}")
        if len(missing_templates) > 10:
            print(f"   ... and {len(missing_templates) - 10} more")
    
    if broken_urls:
        print(f"\n⚠️  Broken URLs:")
        for url_name, description, error in broken_urls:
            print(f"   - {url_name}: {error[:50]}...")
    
    # Health calculation
    template_health = (existing_count / total_expected_templates) * 100
    url_health = (working_urls_count / total_urls) * 100 if total_urls > 0 else 100
    model_health = (working_models_count / total_models) * 100 if total_models > 0 else 100
    
    overall_health = (template_health + url_health + model_health) / 3
    
    print(f"\n🏥 System Health Score: {overall_health:.1f}%")
    
    if overall_health >= 90:
        print("🟢 Excellent - System is ready for production")
    elif overall_health >= 80:
        print("🟡 Good - Minor improvements needed")
    elif overall_health >= 60:
        print("🟠 Fair - Several issues need attention")
    else:
        print("🔴 Poor - Major issues require immediate fixes")
    
    print("\n✅ Verification complete!")

if __name__ == "__main__":
    main()
