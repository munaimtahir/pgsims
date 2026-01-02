#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
    try:
        from django.core.management import execute_from_command_line
        print("Django management imported successfully!")
        # Test the system
        execute_from_command_line(['manage.py', 'check'])
        print("Django system check passed!")
        
        # Create superuser if it doesn't exist
        from django.contrib.auth import get_user_model
        User = get_user_model()
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@sims.com',
                password='admin123',
                first_name='Admin',
                last_name='User',
                role='admin'
            )
            print("Superuser created: admin/admin123")
        else:
            print("Superuser already exists: admin/admin123")
            
    except ImportError as exc:
        print(f"Import error: {exc}")
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc


if __name__ == '__main__':
    main()
