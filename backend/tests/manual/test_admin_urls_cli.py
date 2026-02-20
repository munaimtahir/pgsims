#!/usr/bin/env python
"""
Test admin URLs to ensure they're all valid
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

from django.urls import reverse
from django.urls.exceptions import NoReverseMatch

def test_admin_urls():
    """Test all admin URLs used in the template"""
    print("🔍 Testing Admin URLs")
    print("-" * 40)
    
    urls_to_test = [
        ('admin:index', 'Django Admin Index'),
        ('admin:users_user_add', 'Add User'),
        ('admin:users_user_changelist', 'User List'),
        ('admin:cases_clinicalcase_changelist', 'Clinical Cases'),
        ('admin:logbook_logbookentry_changelist', 'Logbook Entries'),
        ('admin:rotations_rotation_changelist', 'Rotations'),
        ('users:pg_bulk_upload', 'Bulk Upload PGs'),
        ('users:user_reports', 'User Reports'),
        ('users:activity_log', 'Activity Log'),
        ('users:admin_analytics', 'Admin Analytics'),
        ('users:admin_stats_api', 'Admin Stats API'),
        ('home', 'Homepage'),
    ]
    
    failed_urls = []
    
    for url_name, description in urls_to_test:
        try:
            url = reverse(url_name)
            print(f"✅ {description}: {url}")
        except NoReverseMatch as e:
            print(f"❌ {description}: {url_name} - {e}")
            failed_urls.append((url_name, description))
        except Exception as e:
            print(f"⚠️  {description}: {url_name} - Unexpected error: {e}")
            failed_urls.append((url_name, description))
    
    if failed_urls:
        print(f"\n❌ {len(failed_urls)} URL(s) failed:")
        for url_name, desc in failed_urls:
            print(f"  - {desc} ({url_name})")
        return False
    else:
        print(f"\n✅ All {len(urls_to_test)} URLs are valid!")
        return True

if __name__ == "__main__":
    test_admin_urls()
