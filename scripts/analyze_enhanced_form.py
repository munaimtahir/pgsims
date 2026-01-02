#!/usr/bin/env python

# Simple test script to check form functionality
import os
import sys

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')

try:
    import django
    django.setup()
    
    print("=== ENHANCED LOGBOOK FORM ANALYSIS ===\n")
    
    # Import the form
    from sims.logbook.forms import PGLogbookEntryForm
    
    # Create form instance
    form = PGLogbookEntryForm()
    
    print("✅ Form imported and created successfully")
    print(f"Total fields: {len(form.fields)}")
    
    print("\n📋 ALL FORM FIELDS:")
    for i, (name, field) in enumerate(form.fields.items(), 1):
        field_type = type(field).__name__
        required = "Required" if field.required else "Optional"
        print(f"  {i:2d}. {name:30} ({field_type}) - {required}")
    
    print("\n🔍 CHECKING FIELD TYPES:")
    model_fields = form._meta.fields if hasattr(form._meta, 'fields') else []
    
    for field_name in form.fields:
        if field_name in model_fields:
            print(f"  ✅ {field_name} - Model field")
        else:
            print(f"  🔧 {field_name} - Custom field")
    
    print("\n📝 FORM VALIDATION TEST:")
    
    # Test with minimum required data
    test_data = {
        'case_title': 'Test Enhanced Case',
        'date': '2025-06-24',
        'location_of_activity': 'Test Ward',
        'patient_history_summary': 'Test patient history',
        'management_action': 'Test management action',
        'topic_subtopic': 'Test/Topic',
        'patient_age': 35,
        'patient_gender': 'M',
        'patient_chief_complaint': 'Test complaint',
        'learning_points': 'Test learning points',
        'self_assessment_score': 7,
        'specialty': 'general_medicine',
        'clinical_setting': 'inpatient',
        'competency_level': '3',
        'procedure_performed': 'Test procedure',
        'secondary_diagnosis': 'Test secondary diagnosis',
        'management_plan': 'Test management plan',
        'cme_points': 2.5,
    }
    
    form_with_data = PGLogbookEntryForm(data=test_data)
    
    if form_with_data.is_valid():
        print("  ✅ Form validation PASSED with enhanced data")
    else:
        print("  ❌ Form validation FAILED:")
        for field, errors in form_with_data.errors.items():
            print(f"    - {field}: {', '.join(errors)}")
    
    print("\n=== ANALYSIS COMPLETE ===")
    
except ImportError as e:
    print(f"❌ Import Error: {e}")
except Exception as e:
    print(f"❌ Unexpected Error: {e}")
    import traceback
    traceback.print_exc()
