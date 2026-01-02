#!/usr/bin/env python3
"""
Quick script to set up admin user and test welcome display
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def setup_admin_user():
    print('🔧 Setting up Admin User for Welcome Test...')
    print('=' * 50)
    
    # Create/update admin user
    admin, created = User.objects.get_or_create(
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
    
    if not created:
        # Update existing user
        admin.first_name = 'Dr. System'
        admin.last_name = 'Administrator'
        admin.email = 'admin@fmu.edu.pk'
        admin.role = 'admin'
        admin.is_staff = True
        admin.is_superuser = True
        admin.is_active = True
        admin.save()
        print('✓ Updated existing admin user')
    else:
        admin.set_password('admin123')
        admin.save()
        print('✓ Created new admin user')
    
    print(f'  Username: "{admin.username}"')
    print(f'  Full Name: "{admin.get_full_name()}"')
    print(f'  First Name: "{admin.first_name}"')
    print(f'  Last Name: "{admin.last_name}"')
    print(f'  Email: {admin.email}')
    print(f'  Role: {admin.role}')
    print(f'  Is Superuser: {admin.is_superuser}')
    print(f'  Is Staff: {admin.is_staff}')
    
    return admin

def create_sample_staff():
    print('\n👥 Creating Sample Staff Users...')
    print('=' * 40)
    
    # Create a regular staff member
    staff, created = User.objects.get_or_create(
        username='staff',
        defaults={
            'email': 'staff@fmu.edu.pk',
            'first_name': 'Staff',
            'last_name': 'Member',
            'role': 'admin',
            'is_staff': True,
            'is_superuser': False,
            'is_active': True
        }
    )
    
    if created:
        staff.set_password('staff123')
        staff.save()
        print('✓ Created staff user')
    
    # Create a supervisor
    supervisor, created = User.objects.get_or_create(
        username='supervisor',
        defaults={
            'email': 'supervisor@fmu.edu.pk',
            'first_name': 'Dr. John',
            'last_name': 'Smith',
            'role': 'supervisor',
            'specialty': 'Internal Medicine',
            'is_staff': False,
            'is_superuser': False,
            'is_active': True
        }
    )
    
    if created:
        supervisor.set_password('super123')
        supervisor.save()
        print('✓ Created supervisor user')
    
    print(f'  Staff: "{staff.get_full_name()}" ({staff.username})')
    print(f'  Supervisor: "{supervisor.get_full_name()}" ({supervisor.username})')

if __name__ == "__main__":
    print("🔧 Admin Welcome Section Setup")
    print("=" * 50)
    
    # Setup admin user
    admin = setup_admin_user()
    
    # Create sample users
    create_sample_staff()
    
    print('\n' + '=' * 50)
    print('🎉 Setup Complete!')
    print('\n📋 Test the welcome section with these users:')
    print('  👑 Super Admin: username="admin", password="admin123"')
    print('  🛠️  Staff Admin: username="staff", password="staff123"')
    print('  👨‍⚕️ Supervisor: username="supervisor", password="super123"')
    
    print('\n🌐 Visit: http://127.0.0.1:8000/admin/')
    print('   The welcome section should now show:')
    print('   - Proper full names instead of "Admin User"')
    print('   - Role-specific badges with icons')
    print('   - Better styling and contrast')
    
    print('\n📝 Welcome Section Improvements:')
    print('  ✓ Dynamic name display (First + Last or fallback to username)')
    print('  ✓ Role-specific badges (Super Admin = red, Admin = green)')
    print('  ✓ Icons for different user types')
    print('  ✓ Better text contrast and styling')
    print('  ✓ Fallback handling for missing names')
