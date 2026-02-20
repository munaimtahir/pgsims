#!/usr/bin/env python3
"""
Test script to verify review submission functionality.

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

def test_review_creation():
    """Test creating a review to ensure no RelatedObjectDoesNotExist error"""
    print("=== Testing Review Creation ===")
    
    # Get or create test data
    supervisor = User.objects.filter(role='supervisor').first()
    entry = LogbookEntry.objects.filter(id=1).first()
    
    if not supervisor:
        print("❌ No supervisor found")
        return False
        
    if not entry:
        print("❌ No entry with ID 1 found")
        return False
        
    print(f"✓ Found supervisor: {supervisor.username}")
    print(f"✓ Found entry: {entry.case_title}")
    print(f"✓ Entry status: {entry.status}")
    print(f"✓ Entry PG: {entry.pg}")
    print(f"✓ Entry supervisor: {entry.supervisor}")
    
    # Test form creation
    form_data = {
        'status': 'approved',
        'review_date': '2025-01-27',
        'feedback': 'Good work on this case presentation.',
        'strengths_identified': 'Clear clinical reasoning',
        'areas_for_improvement': 'Could improve documentation',
        'recommendations': 'Review more complex cases',
        'clinical_knowledge_score': 8,
        'clinical_skills_score': 7,
        'professionalism_score': 9,
        'overall_score': 8,
        'follow_up_required': False
    }
    
    try:
        # Test form validation
        form = LogbookReviewForm(data=form_data, entry=entry, user=supervisor)
        print(f"✓ Form created with data")
        
        if form.is_valid():
            print("✓ Form is valid")
            
            # Test creating the review instance
            review = form.save(commit=False)
            review.logbook_entry = entry
            review.reviewer = supervisor
            
            print("✓ Review instance created")
            
            # Test validation
            try:
                review.clean()
                print("✓ Review validation passed")
                
                # Test saving (commented out to avoid creating duplicate)
                # review.save()
                # print("✓ Review saved successfully")
                
                return True
                
            except Exception as e:
                print(f"❌ Review validation failed: {e}")
                return False
                
        else:
            print("❌ Form validation failed:")
            for field, errors in form.errors.items():
                print(f"  {field}: {errors}")
            return False
            
    except Exception as e:
        print(f"❌ Error creating form or review: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_review_creation()
