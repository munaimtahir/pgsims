#!/usr/bin/env python3
"""
SIMS Migration Fix Script
Fixes Django migration files for production deployment
Addresses CheckConstraint syntax issues for newer Django versions
"""

import os
import re
import glob
from pathlib import Path

def fix_migration_files():
    """Fix CheckConstraint syntax in migration files"""
    print("🔧 Fixing Django Migration Files...")
    
    # Find all migration files
    migration_files = glob.glob('**/migrations/*.py', recursive=True)
    
    fixed_count = 0
    
    for file_path in migration_files:
        if os.path.basename(file_path) == '__init__.py':
            continue
            
        try:
            # Read the file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if it contains the old syntax
            if 'CheckConstraint(condition=' in content:
                print(f"   🔍 Found outdated syntax in: {file_path}")
                
                # Replace condition= with check=
                new_content = content.replace(
                    'CheckConstraint(condition=',
                    'CheckConstraint(check='
                )
                
                # Write the fixed content back
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f"   ✅ Fixed: {file_path}")
                fixed_count += 1
                
        except Exception as e:
            print(f"   ❌ Error processing {file_path}: {e}")
    
    if fixed_count == 0:
        print("   ✅ All migration files are already up to date!")
    else:
        print(f"   ✅ Fixed {fixed_count} migration files")

def create_static_directory():
    """Ensure static directory exists"""
    print("\n📁 Setting up static files directory...")
    
    static_dir = Path('static')
    if not static_dir.exists():
        static_dir.mkdir(exist_ok=True)
        print("   ✅ Created static/ directory")
        
        # Create a placeholder file
        placeholder = static_dir / '.gitkeep'
        placeholder.write_text('# Placeholder for static files directory\n')
        print("   ✅ Added .gitkeep placeholder")
    else:
        print("   ✅ static/ directory already exists")

def create_media_directory():
    """Ensure media directory exists"""
    print("\n📁 Setting up media files directory...")
    
    media_dir = Path('media')
    if not media_dir.exists():
        media_dir.mkdir(exist_ok=True)
        print("   ✅ Created media/ directory")
        
        # Create a placeholder file
        placeholder = media_dir / '.gitkeep'
        placeholder.write_text('# Placeholder for media files directory\n')
        print("   ✅ Added .gitkeep placeholder")
    else:
        print("   ✅ media/ directory already exists")

def create_deployment_guide():
    """Create a deployment guide for the server"""
    print("\n📋 Creating deployment guide...")
    
    guide_content = """# SIMS Server Deployment Guide

## Pre-Deployment Checklist

### 1. Environment Setup
```bash
# On your server, ensure Python 3.8+ is installed
python3 --version

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\\Scripts\\activate    # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Variables
Create a `.env` file in your project root:
```bash
SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com,your-server-ip
DATABASE_URL=sqlite:///opt/sims_project/db.sqlite3
```

### 3. Database Migration
```bash
# Run migrations (this script has already fixed compatibility issues)
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

### 4. Fixed Migration Issues
✅ **CheckConstraint Syntax**: Fixed `condition=` → `check=` for Django 4.2+ compatibility
✅ **Static Files**: Created static/ directory and improved settings
✅ **Media Files**: Created media/ directory for uploads

### 5. Production Settings
The settings.py file now supports environment variables:
- `SECRET_KEY`: Set a secure secret key
- `DEBUG`: Set to `False` for production
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts

### 6. Web Server Configuration

#### Apache Configuration (.htaccess or virtual host)
```apache
<VirtualHost *:80>
    ServerName your-domain.com
    DocumentRoot /opt/sims_project
    
    WSGIDaemonProcess sims python-path=/opt/sims_project python-home=/opt/sims_project/venv
    WSGIProcessGroup sims
    WSGIScriptAlias / /opt/sims_project/sims_project/wsgi.py
    
    <Directory /opt/sims_project/sims_project>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>
    
    Alias /static /opt/sims_project/staticfiles
    <Directory /opt/sims_project/staticfiles>
        Require all granted
    </Directory>
    
    Alias /media /opt/sims_project/media
    <Directory /opt/sims_project/media>
        Require all granted
    </Directory>
</VirtualHost>
```

#### Nginx Configuration
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /opt/sims_project;
    }
    
    location /media/ {
        root /opt/sims_project;
    }
    
    location / {
        include proxy_params;
        proxy_pass http://unix:/opt/sims_project/sims_project.sock;
    }
}
```

### 7. Security Checklist
- [ ] Set strong SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Configure proper ALLOWED_HOSTS
- [ ] Set up HTTPS/SSL certificates
- [ ] Configure firewall rules
- [ ] Set proper file permissions
- [ ] Enable database backups

### 8. Testing Deployment
```bash
# Test that the server starts without errors
python manage.py check --deploy

# Run the Django development server for testing
python manage.py runserver 0.0.0.0:8000

# Access these URLs to verify:
# - http://your-server:8000/ (Homepage)
# - http://your-server:8000/users/login/ (Login)
# - http://your-server:8000/admin/ (Admin)
```

## Troubleshooting

### Common Issues:
1. **Static files not loading**: Run `python manage.py collectstatic`
2. **Permission errors**: Check file/directory permissions
3. **Database errors**: Ensure database file is writable
4. **Import errors**: Verify all dependencies are installed

### Getting Help:
- Check Django logs in `logs/` directory
- Verify all environment variables are set
- Ensure virtual environment is activated
- Check server error logs (Apache/Nginx)

## Success Indicators
✅ Homepage loads with PMC theme
✅ Login system works (/users/login/)
✅ Admin panel accessible (/admin/)
✅ Static files load correctly
✅ No migration errors
✅ All authentication flows work

## Contact
For deployment support, check the Django documentation or SIMS project documentation.
"""
    
    with open('DEPLOYMENT_GUIDE.md', 'w', encoding='utf-8') as f:
        f.write(guide_content)
    
    print("   ✅ Created DEPLOYMENT_GUIDE.md")

def verify_settings():
    """Verify that settings are properly configured"""
    print("\n⚙️  Verifying settings configuration...")
    
    try:
        import django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')
        django.setup()
        
        from django.conf import settings
        
        # Check critical settings
        checks = [
            ('SECRET_KEY', hasattr(settings, 'SECRET_KEY') and settings.SECRET_KEY),
            ('STATIC_URL', hasattr(settings, 'STATIC_URL')),
            ('STATIC_ROOT', hasattr(settings, 'STATIC_ROOT')),
            ('ALLOWED_HOSTS', hasattr(settings, 'ALLOWED_HOSTS')),
        ]
        
        for setting_name, is_ok in checks:
            status = "✅" if is_ok else "❌"
            print(f"   {status} {setting_name}")
            
        print("   ✅ Settings verification complete")
        
    except Exception as e:
        print(f"   ⚠️  Could not verify settings: {e}")

def main():
    """Run all migration and deployment fixes"""
    print("🚀 SIMS Deployment Preparation")
    print("=" * 50)
    
    # Fix migration files
    fix_migration_files()
    
    # Setup directories
    create_static_directory()
    create_media_directory()
    
    # Create deployment guide
    create_deployment_guide()
    
    # Verify configuration
    verify_settings()
    
    print("\n🎉 Deployment preparation complete!")
    print("\nNext steps:")
    print("1. Review DEPLOYMENT_GUIDE.md")
    print("2. Set environment variables")
    print("3. Run: python manage.py migrate")
    print("4. Run: python manage.py collectstatic")
    print("5. Run: python manage.py createsuperuser")
    print("6. Deploy to your server")
    
    print("\n🔗 Test URLs after deployment:")
    print("   - Homepage: http://your-server/")
    print("   - Login: http://your-server/users/login/")
    print("   - Admin: http://your-server/admin/")

if __name__ == '__main__':
    main()
