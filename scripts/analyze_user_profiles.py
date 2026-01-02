#!/usr/bin/env python

import os
import sys

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')

try:
    import django
    django.setup()
    
    print("=== USER PROFILE PAGE ANALYSIS ===\n")
    
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    # Check if users exist
    users = User.objects.all()
    print(f"Total users in database: {users.count()}")
    
    if users.exists():
        print("\n👥 AVAILABLE USERS:")
        for user in users[:5]:  # Show first 5 users
            print(f"  ID: {user.pk} | Username: {user.username} | Name: {user.get_full_name()} | Role: {user.role}")
        
        # Test profile access for first user
        first_user = users.first()
        print(f"\n🔍 TESTING PROFILE ACCESS FOR USER ID {first_user.pk}:")
        
        # Check if user has profile attributes
        profile_fields = [
            'first_name', 'last_name', 'email', 'role', 'is_active', 
            'date_joined', 'specialty', 'year', 'department'
        ]
        
        for field in profile_fields:
            try:
                value = getattr(first_user, field, 'N/A')
                print(f"  ✅ {field}: {value}")
            except Exception as e:
                print(f"  ❌ {field}: Error - {e}")
        
        # Check related data
        print(f"\n📊 ACTIVITY COUNTS:")
        try:
            print(f"  Logbook entries: {first_user.logbook_entries.count()}")
        except:
            print(f"  Logbook entries: Error accessing")
        
        try:
            print(f"  Cases: {first_user.cases.count()}")
        except:
            print(f"  Cases: Error accessing")
            
        try:
            print(f"  Certificates: {first_user.certificates.count()}")
        except:
            print(f"  Certificates: Error accessing")
            
        try:
            print(f"  Rotations: {first_user.rotations.count()}")
        except:
            print(f"  Rotations: Error accessing")
    
    else:
        print("❌ No users found in database")
        print("💡 Create users using: py manage.py createsuperuser")
    
    print("\n=== ANALYSIS COMPLETE ===")
    
except ImportError as e:
    print(f"❌ Import Error: {e}")
except Exception as e:
    print(f"❌ Unexpected Error: {e}")
    import traceback
    traceback.print_exc()
