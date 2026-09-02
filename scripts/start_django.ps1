# PowerShell script to test and start Django
Set-Location "d:\PMC\sims_project"

Write-Host "Testing Django installation..." -ForegroundColor Green
py -c "import django; print('Django version:', django.get_version())"

Write-Host "Running Django system check..." -ForegroundColor Green
py manage.py check

Write-Host "Creating superuser..." -ForegroundColor Green
py -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@sims.com', 'admin123', first_name='Admin', last_name='User', role='admin')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists: admin/admin123')
"

Write-Host "Starting Django development server..." -ForegroundColor Green
Write-Host "Server will be available at: http://127.0.0.1:8000" -ForegroundColor Yellow
Write-Host "Admin interface: http://127.0.0.1:8000/admin" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
py manage.py runserver 127.0.0.1:8000
