#!/usr/bin/env python
"""
Test script to verify that model names in the admin dashboard are properly formatted.
This checks that we no longer see incorrect names like "Casecategorys" and "Casereviews".
"""

import os
import sys
import django
from datetime import datetime

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims.settings')
django.setup()

def test_model_display_names():
    """Test that model names are displayed correctly in admin interface"""
    from django.contrib.admin import site
    from django.apps import apps
    
    print("=" * 60)
    print("TESTING MODEL DISPLAY NAMES IN ADMIN DASHBOARD")
    print("=" * 60)
    print(f"Test run at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Get all registered models
    app_configs = apps.get_app_configs()
    
    issues_found = []
    correct_names = []
    
    for app_config in app_configs:
        if app_config.label in ['sims', 'users', 'logbook', 'cases', 'certificates', 'rotations']:
            print(f"App: {app_config.verbose_name}")
            print("-" * 40)
            
            for model in app_config.get_models():
                if hasattr(model, '_meta'):
                    model_name = model._meta.verbose_name_plural
                    object_name = model._meta.object_name
                    
                    print(f"  Model: {object_name}")
                    print(f"  Display Name: {model_name}")
                    
                    # Check for common issues
                    if model_name.lower() in ['casecategorys', 'casereviews', 'logbooktrys', 'rotations']:
                        issues_found.append(f"  ❌ Issue: {model_name} (from {object_name})")
                    else:
                        correct_names.append(f"  ✅ Correct: {model_name}")
                    
                    print()
    
    print()
    print("=" * 60)
    print("RESULTS SUMMARY")
    print("=" * 60)
    
    if issues_found:
        print("❌ ISSUES FOUND:")
        for issue in issues_found:
            print(issue)
        print()
    
    if correct_names:
        print("✅ CORRECT NAMES:")
        for name in correct_names:
            print(name)
        print()
    
    if not issues_found:
        print("🎉 SUCCESS: All model names are properly formatted!")
        print("   No spelling or spacing errors found in model display names.")
    else:
        print(f"⚠️  Found {len(issues_found)} issues with model names.")
    
    print()
    return len(issues_found) == 0

def test_template_rendering():
    """Test that the template would render correct model names"""
    from django.apps import apps
    from django.contrib.admin import site
    
    print("=" * 60)
    print("TESTING TEMPLATE MODEL NAME RENDERING")
    print("=" * 60)
    
    # Simulate what the template would receive
    app_list = []
    
    for app_config in apps.get_app_configs():
        if app_config.label in ['users', 'logbook', 'cases', 'certificates', 'rotations']:
            app_dict = {
                'name': app_config.verbose_name,
                'app_label': app_config.label,
                'models': []
            }
            
            for model in app_config.get_models():
                if model in site._registry:
                    model_dict = {
                        'name': model._meta.verbose_name_plural,  # This is what template should use
                        'object_name': model._meta.object_name,
                        'admin_url': f'/admin/{app_config.label}/{model._meta.model_name}/',
                        'add_url': f'/admin/{app_config.label}/{model._meta.model_name}/add/',
                    }
                    app_dict['models'].append(model_dict)
            
            if app_dict['models']:
                app_list.append(app_dict)
    
    print("Template would render these model names:")
    print()
    
    for app in app_list:
        print(f"App: {app['name']}")
        for model in app['models']:
            print(f"  - {model['name']} (from {model['object_name']})")
        print()
    
    # Check for problematic names
    problematic = []
    for app in app_list:
        for model in app['models']:
            name = model['name']
            if any(issue in name.lower() for issue in ['categorys', 'reviews', 'entrys']):
                problematic.append(name)
    
    if problematic:
        print(f"❌ Problematic names found: {problematic}")
        return False
    else:
        print("✅ All model names look good!")
        return True

if __name__ == "__main__":
    try:
        print("Starting model names test...")
        print()
        
        # Test 1: Check Django model verbose names
        test1_passed = test_model_display_names()
        
        print()
        
        # Test 2: Test template rendering simulation
        test2_passed = test_template_rendering()
        
        print()
        print("=" * 60)
        print("FINAL TEST RESULTS")
        print("=" * 60)
        
        if test1_passed and test2_passed:
            print("🎉 ALL TESTS PASSED!")
            print("   Model names are properly formatted and will display correctly.")
        else:
            print("❌ SOME TESTS FAILED!")
            print("   Review the issues above and fix the model name formatting.")
        
        print()
        
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        import traceback
        traceback.print_exc()
