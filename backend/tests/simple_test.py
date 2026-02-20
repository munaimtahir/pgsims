#!/usr/bin/env python
"""
Simple SIMS system test
"""
import os
import sys

print("Starting SIMS System Test...")
print(f"Python version: {sys.version}")
print(f"Working directory: {os.getcwd()}")

# Test Django import
try:
    import django
    print(f"✅ Django installed: {django.get_version()}")
except ImportError as e:
    print(f"❌ Django import error: {e}")
    sys.exit(1)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')

try:
    django.setup()
    print("✅ Django setup successful")
except Exception as e:
    print(f"❌ Django setup error: {e}")
    sys.exit(1)

# Test basic imports
try:
    from django.contrib.auth.models import User
    from sims.users.models import Profile
    print("✅ Basic models imported successfully")
except Exception as e:
    print(f"❌ Model import error: {e}")

# Test views import
try:
    from sims.users.views import AdminDashboardView
    print("✅ Dashboard views imported successfully")
except Exception as e:
    print(f"❌ Views import error: {e}")

# Test URL configuration
try:
    from django.urls import reverse
    admin_url = reverse('users:admin_dashboard')
    print(f"✅ URL reverse working: {admin_url}")
except Exception as e:
    print(f"❌ URL configuration error: {e}")

print("\n✅ Basic system test completed!")
