#!/usr/bin/env python3
"""
Simple script to run the import using Django's shell mechanism.
"""
import os
import sys

# Set environment variable to skip logging configuration
os.environ['DJANGO_SETTINGS_MODULE'] = 'sims_project.settings'

# Temporarily disable file logging
import logging
logging.config = lambda *args, **kwargs: None

# Now import Django
import django
django.setup()

# Import and run
from django.core.management import call_command

file_path = '/home/munaim/Downloads/Trainee_Data_Department_of_Urology.xlsx'

print("="*70)
print("IMPORTING TRAINEE DATA")
print("="*70)

# First, run migration
print("\n1. Running migrations...")
try:
    call_command('migrate', 'users', verbosity=0, interactive=False)
    print("   ✓ Migrations complete")
except Exception as e:
    print(f"   ⚠ Migration error: {e}")

# Then import
print(f"\n2. Importing data from: {file_path}")
try:
    call_command('import_trainees', file_path, dry_run=False, allow_partial=True)
    print("\n✓ Import completed!")
except Exception as e:
    print(f"\n✗ Import error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
