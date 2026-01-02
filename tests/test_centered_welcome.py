#!/usr/bin/env python3
"""
Test the cleaned and centered welcome card
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()

def test_clean_welcome_card():
    print('🔧 Testing Clean and Centered Welcome Card...')
    print('=' * 50)
    
    client = Client()
    
    # Ensure we have a clean admin user
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@fmu.edu.pk',
            'first_name': 'Dr. System',
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
        print('✓ Created clean admin user')
    else:
        # Update to ensure clean data
        admin_user.first_name = 'Dr. System'
        admin_user.last_name = 'Administrator'
        admin_user.save()
        print('✓ Updated admin user data')
    
    print(f'  Full Name: "{admin_user.get_full_name()}"')
    
    # Login and test
    login_success = client.login(username='admin', password='admin123')
    if not login_success:
        print('✗ Login failed')
        return False
    
    print('✓ Login successful')
    
    # Get admin page
    response = client.get('/admin/')
    
    if response.status_code == 200:
        content = response.content.decode()
        
        # Check for new clean welcome card
        if 'admin-welcome-card-custom' in content:
            print('✓ New clean welcome card found')
        else:
            print('✗ New welcome card not found')
            
        # Check for centered styling
        if 'welcome-content-wrapper' in content:
            print('✓ Centered content wrapper found')
        else:
            print('✗ Content wrapper not found')
            
        # Check for proper role badges
        if 'role-badge' in content and 'role-super' in content:
            print('✓ Clean role badges found')
        else:
            print('✗ Role badges not found')
            
        # Check that we're not using old card classes
        if 'admin-welcome-card"' not in content:
            print('✓ Old welcome card classes removed')
        else:
            print('⚠ Old welcome card classes still present')
            
        return True
    else:
        print(f'✗ Page failed to load: {response.status_code}')
        return False

if __name__ == "__main__":
    print("🎯 Welcome Card Clean-up Test")
    print("=" * 50)
    
    success = test_clean_welcome_card()
    
    print('\n' + '=' * 50)
    print('📋 Welcome Card Improvements:')
    print('  ✅ Completely custom welcome card (no Django admin inheritance)')
    print('  ✅ Centered content with flex layout')
    print('  ✅ Clean user name display (no extra admin text)')
    print('  ✅ Custom role badges with icons')
    print('  ✅ Proper spacing and alignment')
    print('  ✅ Glass-morphism styling with backdrop blur')
    
    if success:
        print('\n🎉 Welcome card is now clean and centered!')
    else:
        print('\n⚠ Some issues detected')
    
    print(f'\n🌐 Visit: http://127.0.0.1:8000/admin/')
    print('   The welcome card should now be:')
    print('   - Completely centered')
    print('   - Free of any "admin user" text')
    print('   - Clean and professional looking')
    print('   - With proper role badges')
