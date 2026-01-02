#!/usr/bin/env python3
"""
Test LogbookReviewForm instantiation and crispy forms compatibility.

Created: 2025-01-27
Author: GitHub Copilot
"""

import os
import sys
import django
from django.template import Template, Context
from django.template.loader import get_template

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

from sims.logbook.forms import LogbookReviewForm

def test_form_template_rendering():
    """Test if the form can be rendered with crispy forms"""
    print("=== Testing LogbookReviewForm Template Rendering ===")
    
    try:
        # Create a form instance
        form = LogbookReviewForm()
        print(f"✓ Form created successfully with {len(form.fields)} fields")
        
        # Test if crispy forms can process the form
        template_str = """
        {% load crispy_forms_tags %}
        {{ form.overall_score|as_crispy_field }}
        """
        
        template = Template(template_str)
        context = Context({'form': form})
        
        rendered = template.render(context)
        print("✓ Crispy forms rendering successful")
        print("Rendered HTML length:", len(rendered))
        
        # Test all fields
        all_fields_template = """
        {% load crispy_forms_tags %}
        {% for field in form %}
            {{ field|as_crispy_field }}
        {% endfor %}
        """
        
        template2 = Template(all_fields_template)
        rendered2 = template2.render(context)
        print("✓ All fields rendering successful")
        print("All fields HTML length:", len(rendered2))
        
        return True
        
    except Exception as e:
        print(f"✗ Error during form rendering: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_form_template_rendering()
