#!/usr/bin/env python3
"""
Nginx Deployment Verification for SIMS on 139.162.9.224
Verifies all configuration files are ready for Nginx deployment
"""

import os
import django
from pathlib import Path

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
django.setup()

def test_nginx_files():
    """Test that all Nginx deployment files exist"""
    print("📁 Testing Nginx Deployment Files...")
    
    required_files = [
        ('nginx_sims.conf', 'Nginx virtual host configuration'),
        ('gunicorn.conf.py', 'Gunicorn WSGI server settings'),
        ('sims.service', 'Systemd service file'),
        ('deploy_server.sh', 'Automated deployment script'),
        ('requirements.txt', 'Python dependencies with Gunicorn'),
    ]
    
    all_good = True
    for filename, description in required_files:
        file_path = Path(filename)
        if file_path.exists():
            print(f"   ✅ {description}: {filename}")
        else:
            print(f"   ❌ {description}: MISSING - {filename}")
            all_good = False
    
    return all_good

def test_nginx_config_content():
    """Test that Nginx config contains required settings"""
    print("\n⚙️ Testing Nginx Configuration Content...")
    
    nginx_conf = Path('nginx_sims.conf')
    if not nginx_conf.exists():
        print("   ❌ nginx_sims.conf not found")
        return False
    
    content = nginx_conf.read_text()
    
    checks = [
        ('server_name 139.162.9.224', 'Server IP configured'),
        ('location /static/', 'Static files location configured'),
        ('location /media/', 'Media files location configured'),
        ('proxy_pass http://sims_app', 'Gunicorn upstream configured'),
        ('unix:/opt/sims_project/sims.sock', 'Unix socket configured'),
    ]
    
    all_good = True
    for check_string, description in checks:
        if check_string in content:
            print(f"   ✅ {description}")
        else:
            print(f"   ❌ {description}: NOT FOUND")
            all_good = False
    
    return all_good

def test_gunicorn_config():
    """Test Gunicorn configuration"""
    print("\n🦄 Testing Gunicorn Configuration...")
    
    gunicorn_conf = Path('gunicorn.conf.py')
    if not gunicorn_conf.exists():
        print("   ❌ gunicorn.conf.py not found")
        return False
    
    content = gunicorn_conf.read_text()
    
    checks = [
        ('bind = "unix:', 'Unix socket binding'),
        ('workers =', 'Worker process configuration'),
        ('errorlog =', 'Error logging configured'),
        ('accesslog =', 'Access logging configured'),
        ('user = "www-data"', 'User configuration'),
    ]
    
    all_good = True
    for check_string, description in checks:
        if check_string in content:
            print(f"   ✅ {description}")
        else:
            print(f"   ❌ {description}: NOT FOUND")
            all_good = False
    
    return all_good

def test_systemd_service():
    """Test systemd service configuration"""
    print("\n🔧 Testing Systemd Service Configuration...")
    
    service_file = Path('sims.service')
    if not service_file.exists():
        print("   ❌ sims.service not found")
        return False
    
    content = service_file.read_text()
    
    checks = [
        ('ExecStart=', 'Gunicorn execution command'),
        ('WorkingDirectory=/var/www/sims_project', 'Working directory'),
        ('User=www-data', 'Service user'),
        ('WantedBy=multi-user.target', 'Auto-start configuration'),
        ('ALLOWED_HOSTS=139.162.9.224', 'Server IP in environment'),
    ]
    
    all_good = True
    for check_string, description in checks:
        if check_string in content:
            print(f"   ✅ {description}")
        else:
            print(f"   ❌ {description}: NOT FOUND")
            all_good = False
    
    return all_good

def test_requirements():
    """Test that requirements.txt includes Gunicorn"""
    print("\n📦 Testing Python Requirements...")
    
    req_file = Path('requirements.txt')
    if not req_file.exists():
        print("   ❌ requirements.txt not found")
        return False
    
    content = req_file.read_text()
    
    if 'gunicorn' in content.lower():
        print("   ✅ Gunicorn included in requirements")
        return True
    else:
        print("   ❌ Gunicorn NOT found in requirements.txt")
        return False

def test_django_settings():
    """Test Django settings for production"""
    print("\n⚙️ Testing Django Settings...")
    
    from django.conf import settings
    
    checks = [
        ('139.162.9.224' in settings.ALLOWED_HOSTS, 'Server IP in ALLOWED_HOSTS'),
        (hasattr(settings, 'STATIC_ROOT'), 'STATIC_ROOT configured'),
        (hasattr(settings, 'MEDIA_ROOT'), 'MEDIA_ROOT configured'),
        (settings.STATIC_URL == '/static/', 'STATIC_URL configured'),
        (settings.MEDIA_URL == '/media/', 'MEDIA_URL configured'),
    ]
    
    all_good = True
    for check_result, description in checks:
        if check_result:
            print(f"   ✅ {description}")
        else:
            print(f"   ❌ {description}")
            all_good = False
    
    return all_good

def generate_deployment_summary():
    """Generate deployment command summary"""
    print("\n📋 Nginx Deployment Commands for 139.162.9.224:")
    print("=" * 55)
    
    commands = [
        "# 1. Upload files to server",
        "sudo mkdir -p /opt",
        "sudo git clone https://github.com/munaimtahir/sims.git /opt/sims_project",
        "sudo chown -R $USER:$USER /opt/sims_project",
        "",
        "# 2. SSH to server",
        "ssh user@139.162.9.224",
        "cd /opt/sims_project",
        "",
        "# 3. Run automated deployment",
        "chmod +x deploy_server.sh",
        "./deploy_server.sh",
        "",
        "# 4. Verify services are running",
        "sudo systemctl status sims",
        "sudo systemctl status nginx",
        "",
        "# 5. Test the website",
        "curl http://139.162.9.224:81/",
        "",
        "# 6. Check logs if needed",
        "sudo tail -f /var/log/nginx/sims_error.log",
        "sudo journalctl -u sims -f",
    ]
    
    for cmd in commands:
        print(cmd)

def main():
    """Run all Nginx deployment verification tests"""
    print("🌐 SIMS Nginx Deployment Verification")
    print("🖥️  Target Server: 139.162.9.224")
    print("=" * 50)
    
    tests = [
        test_nginx_files,
        test_nginx_config_content,
        test_gunicorn_config,
        test_systemd_service,
        test_requirements,
        test_django_settings,
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
    print("📊 NGINX DEPLOYMENT VERIFICATION RESULTS")
    
    if all(results):
        print("🎉 ALL TESTS PASSED!")
        print("✅ SIMS is ready for Nginx deployment on 172.236.152.35")
        
        generate_deployment_summary()
        
        print("\n🌐 After deployment, access at:")
        print("   Homepage: http://172.236.152.35/")
        print("   Login:    http://172.236.152.35/users/login/")
        print("   Admin:    http://172.236.152.35/admin/")
        
        print("\n📄 Documentation:")
        print("   - NGINX_DEPLOYMENT_139.162.9.224.md")
        print("   - nginx_sims.conf")
        print("   - gunicorn.conf.py")
        print("   - sims.service")
        
    else:
        print("⚠️ Some tests failed. Please review the issues above.")
        failed_count = len([r for r in results if not r])
        print(f"   {failed_count} out of {len(results)} tests failed.")

if __name__ == '__main__':
    main()
