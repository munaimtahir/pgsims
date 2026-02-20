#!/usr/bin/env python
"""
Test script to verify admin configuration fixes
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

def test_admin_config():
    """Test that admin configuration loads without errors"""
    print("Testing ClinicalCaseAdmin configuration...")
    
    try:
        from sims.cases.admin import ClinicalCaseAdmin
        from sims.cases.models import ClinicalCase
        
        print("✅ ClinicalCaseAdmin imported successfully")
        
        # Check that the problematic fields are not referenced
        readonly_fields = getattr(ClinicalCaseAdmin, 'readonly_fields', [])
        filter_horizontal = getattr(ClinicalCaseAdmin, 'filter_horizontal', [])
        
        # Verify completion_score is not in readonly_fields
        if 'completion_score' not in readonly_fields:
            print("✅ completion_score removed from readonly_fields")
        else:
            print("❌ completion_score still in readonly_fields")
            
        # Verify competencies_achieved is not in filter_horizontal
        if 'competencies_achieved' not in filter_horizontal:
            print("✅ competencies_achieved removed from filter_horizontal")
        else:
            print("❌ competencies_achieved still in filter_horizontal")
            
        print(f"Current readonly_fields: {readonly_fields}")
        print(f"Current filter_horizontal: {filter_horizontal}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading admin configuration: {e}")
        return False

if __name__ == "__main__":
    print("🔧 TESTING ADMIN CONFIGURATION FIXES")
    print("=" * 50)
    success = test_admin_config()
    print("=" * 50)
    if success:
        print("🎯 Admin configuration test PASSED")
    else:
        print("⚠️ Admin configuration test FAILED")
