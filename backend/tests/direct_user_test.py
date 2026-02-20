#!/usr/bin/env python
"""
Simple user creation test
"""
import os
import sys

# Setup Django
sys.path.append('d:/PMC/sims_project-2')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')

import django
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def create_test_user():
    # Create a simple test user directly
    import time
    timestamp = int(time.time())
    username = f'directtest_{timestamp}'
    
    try:
        user = User(
            username=username,
            email=f'{username}@example.com',
            first_name='Direct',
            last_name='Test',
            role='admin',
            is_active=True
        )
        user.set_password('testpass123')
        user.save()
        
        print(f"✅ Successfully created user: {user.username} ({user.role})")
        print(f"   ID: {user.id}")
        print(f"   Email: {user.email}")
        print(f"   Active: {user.is_active}")
        
    except Exception as e:
        print(f"❌ Error creating user: {e}")

if __name__ == '__main__':
    create_test_user()
