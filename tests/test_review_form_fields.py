#!/usr/bin/env python3
"""
Test script to verify LogbookReviewForm fields and crispy forms compatibility.
This checks if the form fields exist and can be properly rendered.

Created: 2025-01-27
Author: GitHub Copilot
"""

import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from sims.logbook.models import LogbookEntry, LogbookReview
from sims.logbook.forms import LogbookReviewForm

User = get_user_model()

def test_review_form_fields():
    """Test LogbookReviewForm field definitions and rendering"""
    print("=== Testing LogbookReviewForm Fields ===")
    
    # Create a basic form instance
    form = LogbookReviewForm()
    
    # Check if all expected fields exist
    expected_fields = [
        'status', 'review_date', 'feedback', 'strengths_identified',
        'areas_for_improvement', 'recommendations', 'follow_up_required',
        'clinical_knowledge_score', 'clinical_skills_score', 
        'professionalism_score', 'overall_score'
    ]
    
    print("Checking form fields:")
    for field_name in expected_fields:
        if field_name in form.fields:
            field = form.fields[field_name]
            print(f"  ✓ {field_name}: {type(field).__name__} - Label: '{field.label}'")
        else:
            print(f"  ✗ {field_name}: MISSING")
    
    print(f"\nForm has {len(form.fields)} total fields")
    print("All form fields:", list(form.fields.keys()))
    
    # Test form validation
    print("\n=== Testing Form Validation ===")
    test_data = {
        'status': 'approved',
        'review_date': '2025-01-27',
        'feedback': 'Test feedback',
        'clinical_knowledge_score': 8,
        'clinical_skills_score': 7,
        'professionalism_score': 9,
        'overall_score': 8
    }
    
    form_with_data = LogbookReviewForm(data=test_data)
    print(f"Form is valid: {form_with_data.is_valid()}")
    if not form_with_data.is_valid():
        print("Form errors:", form_with_data.errors)
    
    # Test with entry and user context
    print("\n=== Testing Form with Context ===")
    try:
        # Try to get a sample user and entry
        user = User.objects.filter(role='supervisor').first()
        entry = LogbookEntry.objects.first()
        
        if user and entry:
            print(f"Testing with user: {user.username} (role: {user.role})")
            print(f"Testing with entry: {entry.id}")
            
            context_form = LogbookReviewForm(user=user, entry=entry, data=test_data)
            print(f"Context form is valid: {context_form.is_valid()}")
            if not context_form.is_valid():
                print("Context form errors:", context_form.errors)
        else:
            print("No suitable user or entry found for context testing")
            
    except Exception as e:
        print(f"Error testing with context: {e}")

if __name__ == "__main__":
    test_review_form_fields()
