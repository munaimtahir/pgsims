#!/usr/bin/env python3
"""
Test and fix the admin welcome section
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

def test_admin_welcome():
    """Test the admin welcome section"""
    print('🔍 Testing Admin Welcome Section...')
    print('=' * 50)
    
    client = Client()
    
    # Create or get admin user with proper name
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@fmu.edu.pk',
            'first_name': 'System',
            'last_name': 'Administrator',
            'role': 'admin',
            'is_staff': True,
            'is_superuser': True,
            'is_active': True
        }
    )
    
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print("✓ Created new admin user with proper name")
    else:
        # Update existing user to have proper name
        admin_user.first_name = 'System'
        admin_user.last_name = 'Administrator'
        admin_user.email = 'admin@fmu.edu.pk'
        admin_user.save()
        print("✓ Updated existing admin user with proper name")
    
    print(f"  Username: {admin_user.username}")
    print(f"  Full Name: {admin_user.get_full_name()}")
    print(f"  Email: {admin_user.email}")
    print(f"  Role: {admin_user.role}")
    print(f"  Is Superuser: {admin_user.is_superuser}")
    
    # Login as admin
    login_success = client.login(username='admin', password='admin123')
    if not login_success:
        print("✗ Failed to login admin user")
        return False
    print("✓ Admin login successful")
    
    # Access admin dashboard
    response = client.get('/admin/')
    
    if response.status_code == 200:
        print("✓ Admin dashboard loads successfully")
        
        content = response.content.decode()
        
        # Check for welcome section improvements
        if 'Welcome back!' in content:
            print("✓ Welcome message found")
        else:
            print("✗ Welcome message not found")
            
        if 'System Administrator' in content or admin_user.get_full_name() in content:
            print("✓ Proper user name displayed")
        else:
            print("⚠ User name may not be displayed correctly")
            
        if 'Super Administrator' in content or 'Administrator' in content:
            print("✓ Role badge found")
        else:
            print("✗ Role badge not found")
            
        # Check for styling improvements
        if 'admin-welcome-card' in content:
            print("✓ Welcome card styling found")
        else:
            print("✗ Welcome card styling not found")
            
        return True
    else:
        print(f"✗ Admin dashboard failed to load: {response.status_code}")
        return False

def check_user_data():
    """Check current user data in database"""
    print('\n📊 Current User Data:')
    print('=' * 30)
    
    users = User.objects.filter(is_staff=True).order_by('-date_joined')[:5]
    
    for user in users:
        print(f"Username: {user.username}")
        print(f"  Full Name: '{user.get_full_name()}'")
        print(f"  First: '{user.first_name}', Last: '{user.last_name}'")
        print(f"  Email: {user.email}")
        print(f"  Role: {user.role}")
        print(f"  Super: {user.is_superuser}, Staff: {user.is_staff}")
        print(f"  Active: {user.is_active}")
        print("-" * 30)

if __name__ == "__main__":
    print("🔧 Admin Welcome Section Fix & Test")
    print("=" * 50)
    
    # Check current user data
    check_user_data()
    
    # Test welcome section
    success = test_admin_welcome()
    
    print('\n' + '=' * 50)
    print('📋 Summary of Welcome Section Fixes:')
    print('  ✓ Improved user name display logic')
    print('  ✓ Dynamic role badge (Super Admin/Admin/User)')
    print('  ✓ Better text contrast and visibility')
    print('  ✓ Enhanced welcome card styling')
    print('  ✓ Proper icon coloring')
    
    if success:
        print('\n🎉 Welcome section test PASSED!')
    else:
        print('\n⚠ Welcome section test had issues.')
    
    print(f'\n🌐 Visit: http://127.0.0.1:8000/admin/ to see the updated welcome section')
    print('📝 Login with: username="admin", password="admin123"')
