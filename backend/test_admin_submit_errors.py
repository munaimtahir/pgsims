import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sims_project.settings")
django.setup()

from django.test import Client
from sims.users.models import User

# Create superuser
User.objects.filter(username="testadmin").delete()
admin = User.objects.create_superuser("testadmin", "admin@test.com", "password", role="admin")

client = Client(SERVER_NAME="localhost")
client.force_login(admin)

response = client.post('/admin/users/user/add/', {
    'username': 'newpg',
    'email': 'newpg@test.com',
    'first_name': 'New',
    'last_name': 'PG',
    'role': 'pg',
    'specialty': 'medicine',
    'year': '1',
    'password1': 'StrongP@ss123',
    'password2': 'StrongP@ss123',
    'supervisor': admin.id,
})
if response.status_code == 200:
    for message in response.context.get('messages', []):
        print(message)
    if 'form' in response.context:
        print("Form errors:", response.context['form'].errors)
