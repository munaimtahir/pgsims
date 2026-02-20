import os
import django
import sys

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

from django.urls import reverse

print("=== Testing URL Resolution ===")

try:
    print(f"home: {reverse('home')}")
except Exception as e:
    print(f"home ERROR: {e}")

try:
    print(f"users:login: {reverse('users:login')}")
except Exception as e:
    print(f"users:login ERROR: {e}")

try:
    print(f"users:password_reset: {reverse('users:password_reset')}")
except Exception as e:
    print(f"users:password_reset ERROR: {e}")

try:
    print(f"admin:index: {reverse('admin:index')}")
except Exception as e:
    print(f"admin:index ERROR: {e}")

print("=== URL Test Complete ===")
