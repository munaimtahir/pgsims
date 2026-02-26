import re
import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sims_project.settings")
django.setup()

from django.test import Client
from sims.users.models import User

# Cleanup
User.objects.filter(username="testadmin").delete()
User.objects.filter(username="newpg").delete()
User.objects.filter(email="newpg@test.com").delete()

admin = User.objects.create_superuser("testadmin", "admin@test.com", "password", role="admin")

User.objects.filter(username="sup").delete()
admin_supervisor = User.objects.create_user(username="sup", password="password", role="supervisor", specialty="medicine", email="sup@sup.com", is_active=True)

client = Client(SERVER_NAME="localhost")
client.force_login(admin)

response = client.post('/users/create/', {
    'username': 'newpg',
    'email': 'newpg@test.com',
    'first_name': 'New',
    'last_name': 'PG',
    'role': 'pg',
    'specialty': 'medicine',
    'year': '1',
    'password1': 'StrongP@ss123',
    'password2': 'StrongP@ss123',
    'supervisor_choice': admin_supervisor.id,
})

print("Status:", response.status_code)
if response.status_code == 200:
    html = response.content.decode('utf-8')
    alerts = re.findall(r'<div class="alert[^>]*>(.*?)</div>', html, re.DOTALL)
    for a in alerts:
        print("ALERT:", a.strip())
elif response.status_code == 302:
    print("Redirected to:", response.url)
