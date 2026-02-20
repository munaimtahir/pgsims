#!/usr/bin/env python
import os
import django
import requests
import json

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

# Test the analytics API
def test_analytics_api():
    try:
        # Test internal Django function
        from sims.users.views import admin_stats_api
        from django.test import RequestFactory
        from sims.users.models import User
        
        # Check if we have users
        users = User.objects.all()
        print(f"Total users in database: {users.count()}")
        
        for user in users[:5]:
            print(f"User: {user.username}, Role: {user.role}, Specialty: {user.specialty}")
        
        # Create a mock request
        factory = RequestFactory()
        request = factory.get('/users/api/admin/stats/')
        
        # Create a superuser for the request (admin_required decorator)
        admin_user = User.objects.filter(role='admin', is_staff=True).first()
        if not admin_user:
            print("No admin user found. Creating one...")
            admin_user = User.objects.create_user(
                username='test_admin',
                password='admin123',
                role='admin',
                is_staff=True,
                is_superuser=True
            )
        
        request.user = admin_user
        
        # Call the API function
        response = admin_stats_api(request)
        
        if hasattr(response, 'content'):
            data = json.loads(response.content.decode())
            print("\nAPI Response:")
            print(json.dumps(data, indent=2))
        else:
            print("Error: Response has no content")
            
    except Exception as e:
        print(f"Error testing API: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_analytics_api()
