import re
import uuid
import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sims_project.settings")
django.setup()

from django.test import Client
from sims.users.models import User

# Create superuser
User.objects.filter(username="testadmin").delete()
admin = User.objects.create_superuser("testadmin", "admin@test.com", "password", role="admin")

client = Client(SERVER_NAME="localhost")
client.force_login(admin)

username = str(uuid.uuid4())[:8]
response = client.post('/admin/users/user/add/', {
    'username': username,
    'email': f'{username}@test.com',
    'first_name': 'New',
    'last_name': 'PG',
    'role': 'pg',
    'specialty': 'medicine',
    'year': '1',
    'password1': 'StrongP@ss123',
    'password2': 'StrongP@ss123',
})

print("Status:", response.status_code)
if response.status_code == 200:
    html = response.content.decode('utf-8')
    errornotes = re.findall(r'<p class="errornote">(.*?)</p>', html, re.DOTALL)
    for note in errornotes: print("ErrorNote:", note.strip())
    
    errorlists = re.findall(r'<ul class="errorlist">(.*?)</ul>', html, re.DOTALL)
    for err in errorlists:
        items = re.findall(r'<li>(.*?)</li>', err, re.DOTALL)
        for item in items: print("FieldError:", item.strip())
