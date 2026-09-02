import sys
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sims_project.settings")
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()
u = User.objects.filter(username="admin").first()
if not u:
    u = User.objects.create_superuser(username="admin", password="admin123", email="a@a.com", first_name="admin", last_name="admin", role="admin")
u.set_password("admin123")
u.is_active = True
u.save()
print("Superuser ready")
