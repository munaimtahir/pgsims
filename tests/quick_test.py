import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

print("Django setup complete!")

from django.contrib.auth import get_user_model

User = get_user_model()
print(f"User model: {User}")

# Check if superuser exists
if User.objects.filter(username='admin').exists():
    print("Superuser 'admin' already exists!")
else:
    # Create superuser
    user = User.objects.create_superuser(
        username='admin',
        email='admin@sims.com',
        password='admin123',
        first_name='Admin',
        last_name='User',
        role='admin'
    )
    print("Superuser 'admin' created successfully!")
    print("Username: admin")
    print("Password: admin123")

print("Test complete!")
