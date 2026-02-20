#!/usr/bin/env python
import os
import sys
import django
from django.conf import settings

# Add the project directory to the path
sys.path.append('d:/PMC/sims_project-2')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')

django.setup()

try:
    from sims.logbook.forms import PGLogbookEntryForm
    from sims.logbook.models import LogbookEntry
    
    print("=== LOGBOOK FORM TEST ===\n")
    
    # Test form initialization
    print("1. Testing form initialization...")
    form = PGLogbookEntryForm()
    print("✅ Form initialized successfully")
    
    # Test form fields
    print("\n2. Form fields available:")
    model_fields = []
    custom_fields = []
    
    for field_name, field in form.fields.items():
        if field_name in form._meta.fields:
            model_fields.append(field_name)
        else:
            custom_fields.append(field_name)
    
    print(f"Model fields ({len(model_fields)}):")
    for field in model_fields:
        print(f"  - {field}")
    
    print(f"\nCustom fields ({len(custom_fields)}):")
    for field in custom_fields:
        print(f"  - {field}")
    
    # Test form validation
    print("\n3. Testing basic form validation...")
    test_data = {
        'case_title': 'Test Case',
        'date': '2025-06-24',
        'location_of_activity': 'Ward A',
        'patient_history_summary': 'Test history',
        'management_action': 'Test management',
    }
    
    form = PGLogbookEntryForm(data=test_data)
    if form.is_valid():
        print("✅ Form validation passed with minimal required fields")
    else:
        print("❌ Form validation failed:")
        for field, errors in form.errors.items():
            print(f"  {field}: {errors}")
    
    print("\n4. Form rendering test...")
    form = PGLogbookEntryForm()
    form_html = str(form)
    if len(form_html) > 100:
        print("✅ Form renders properly")
        print(f"Form HTML length: {len(form_html)} characters")
    else:
        print("❌ Form rendering issue")
        print(f"Form HTML: {form_html[:200]}...")
    
    print("\n=== TEST COMPLETED ===")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
