import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sims_project.settings")
django.setup()

from sims.users.admin import CustomUserCreationForm
form = CustomUserCreationForm()
print("Form initialized successfully.", form.fields.keys())
