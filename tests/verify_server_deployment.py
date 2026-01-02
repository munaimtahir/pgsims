#!/usr/bin/env python3
"""
SIMS Server Deployment Verification for 139.162.9.224
Verifies that the SIMS system is properly configured for the target server
"""

import os
import django
import requests
from pathlib import Path

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

def test_server_settings():
    """Test that settings are configured for the server"""
    print("🔧 Testing Server Configuration...")
    
    from django.conf import settings
    
    # Check ALLOWED_HOSTS
    allowed_hosts = settings.ALLOWED_HOSTS
    server_ip = '139.162.9.224'
    
    if server_ip in allowed_hosts:
        print(f"   ✅ Server IP {server_ip} is in ALLOWED_HOSTS")
    else:
        print(f"   ❌ Server IP {server_ip} NOT in ALLOWED_HOSTS: {allowed_hosts}")
        return False
    
    # Check other critical settings
    checks = [
        ('SECRET_KEY configured', bool(settings.SECRET_KEY)),
        ('Static files configured', bool(settings.STATIC_URL and settings.STATIC_ROOT)),
        ('Media files configured', bool(settings.MEDIA_URL and settings.MEDIA_ROOT)),
        ('Database configured', bool(settings.DATABASES['default'])),
    ]
    
    all_good = True
    for check_name, passed in checks:
        status = "✅" if passed else "❌"
        print(f"   {status} {check_name}")
        if not passed:
            all_good = False
    
    return all_good

def test_url_patterns():
    """Test that URL patterns resolve correctly"""
    print("\n🔗 Testing URL Patterns...")
    
    from django.urls import reverse
    
    urls_to_test = [
        ('home', 'Homepage'),
        ('users:login', 'Login Page'),
        ('users:logout', 'Logout'),
        ('users:password_reset', 'Password Reset'),
        ('admin:index', 'Admin Panel'),
    ]
    
    all_good = True
    for url_name, description in urls_to_test:
        try:
            url = reverse(url_name)
            print(f"   ✅ {description}: {url}")
        except Exception as e:
            print(f"   ❌ {description}: ERROR - {e}")
            all_good = False
    
    return all_good

def test_static_directories():
    """Test that required directories exist"""
    print("\n📁 Testing Directory Structure...")
    
    base_dir = Path('.')
    required_dirs = [
        ('static', 'Static files directory'),
        ('staticfiles', 'Collected static files'),
        ('media', 'Media uploads directory'),
        ('logs', 'Log files directory'),
        ('templates', 'Template files directory'),
    ]
    
    all_good = True
    for dir_name, description in required_dirs:
        dir_path = base_dir / dir_name
        if dir_path.exists():
            print(f"   ✅ {description}: {dir_path}")
        else:
            print(f"   ❌ {description}: MISSING - {dir_path}")
            # Create missing directories
            try:
                dir_path.mkdir(exist_ok=True)
                print(f"   ✨ Created: {dir_path}")
            except Exception as e:
                print(f"   ❌ Could not create {dir_path}: {e}")
                all_good = False
    
    return all_good

def test_migration_status():
    """Test migration status"""
    print("\n🗄️ Testing Database Migrations...")
    
    try:
        from django.core.management import call_command
        from io import StringIO
        
        # Check migrations
        out = StringIO()
        call_command('showmigrations', '--verbosity=0', stdout=out)
        
        print("   ✅ All migrations loaded successfully")
        return True
        
    except Exception as e:
        print(f"   ❌ Migration error: {e}")
        return False

def generate_deployment_commands():
    """Generate deployment commands for the server"""
    print("\n📋 Deployment Commands for Server 139.162.9.224:")
    print("=" * 55)
    
    commands = [
        "# 1. Upload project files to server",
        "sudo mkdir -p /opt",
        "sudo git clone https://github.com/munaimtahir/sims.git /opt/sims_project",
        "sudo chown -R $USER:$USER /opt/sims_project",
        "",
        "# 2. SSH to server and set up environment",
        "ssh user@139.162.9.224",
        "cd /opt/sims_project",
        "",
        "# 3. Set environment variables",
        'export SECRET_KEY="$(python3 -c \'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())\')"',
        'export DEBUG="False"',
        'export ALLOWED_HOSTS="139.162.9.224,localhost,127.0.0.1"',
        "",
        "# 4. Set up virtual environment",
        "python3 -m venv venv",
        "source venv/bin/activate",
        "pip install -r requirements.txt",
        "",
        "# 5. Run Django setup",
        "python manage.py migrate",
        "python manage.py collectstatic --noinput",
        "python manage.py createsuperuser",
        "",
        "# 6. Test deployment",
        "python manage.py check --deploy",
        "python manage.py runserver 139.162.9.224:8000",
        "",
        "# 7. Configure Apache (copy apache_sims.conf to /etc/apache2/sites-available/)",
        "sudo cp apache_sims.conf /etc/apache2/sites-available/sims.conf",
        "sudo a2ensite sims.conf",
        "sudo systemctl restart apache2",
    ]
    
    for cmd in commands:
        print(cmd)

def main():
    """Run all verification tests"""
    print("🚀 SIMS Server Deployment Verification")
    print("🌐 Target Server: 139.162.9.224")
    print("=" * 50)
    
    tests = [
        test_server_settings,
        test_url_patterns,
        test_static_directories,
        test_migration_status,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"   ❌ Test failed: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📊 VERIFICATION RESULTS")
    
    if all(results):
        print("🎉 ALL TESTS PASSED!")
        print("✅ SIMS is ready for deployment on 172.236.152.35")
        
        generate_deployment_commands()
        
        print("\n🌐 After deployment, access at:")
        print("   Homepage: http://172.236.152.35/")
        print("   Login:    http://172.236.152.35/users/login/")
        print("   Admin:    http://172.236.152.35/admin/")
        
    else:
        print("⚠️ Some tests failed. Please review the issues above.")
    
    print("\n📄 See SERVER_DEPLOYMENT_GUIDE_139.162.9.224.md for detailed instructions")

if __name__ == '__main__':
    main()
