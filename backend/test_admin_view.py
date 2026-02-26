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
response = client.get('/admin/users/user/add/')
print("GET /admin/users/user/add/ Status Code:", response.status_code)
if response.status_code != 200:
    print(response.content.decode('utf-8')[:1000])
