# SIMS Nginx Server Deployment Guide - 172.236.152.35

## 📋 Pre-Deployment Checklist

### Server Requirements
- ✅ Ubuntu/Debian Linux Server
- ✅ Python 3.8+ installed
- ✅ Nginx web server
- ✅ Git (for code deployment)
- ✅ SQLite3 (or PostgreSQL for production)

### IP Address Configuration
**Server IP**: `172.236.152.35`
**Web Server**: Nginx with Gunicorn
**ALLOWED_HOSTS**: Updated to include server IP

## 🚀 Step-by-Step Deployment

### 1. Server Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3 python3-pip python3-venv nginx git supervisor

# Start and enable Nginx
sudo systemctl start nginx
sudo systemctl enable nginx
```

### 2. Deploy SIMS Code
```bash
# Create project directory
sudo mkdir -p /var/www/sims_project
cd /var/www/sims_project

# Clone or copy your SIMS project files here
# (Upload your project files to this directory)

# Set up virtual environment
sudo python3 -m venv venv
sudo chown -R www-data:www-data /var/www/sims_project
```

### 3. Configure Environment
```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn  # WSGI server for Nginx

# Set environment variables
export SECRET_KEY="$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')"
export DEBUG="False"
export ALLOWED_HOSTS="172.236.152.35,localhost,127.0.0.1"
```

### 4. Database Setup
```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

### 5. Configure Nginx and Gunicorn
```bash
# Copy Nginx configuration
sudo cp nginx_sims.conf /etc/nginx/sites-available/sims

# Enable the site
sudo ln -s /etc/nginx/sites-available/sims /etc/nginx/sites-enabled/

# Remove default Nginx site (optional)
sudo rm /etc/nginx/sites-enabled/default

# Copy systemd service file for Gunicorn
sudo cp sims.service /etc/systemd/system/

# Reload systemd and enable the service
sudo systemctl daemon-reload
sudo systemctl enable sims

# Test Nginx configuration
sudo nginx -t

# Start services
sudo systemctl start sims
sudo systemctl restart nginx
```

### 6. Set File Permissions
```bash
# Set ownership
sudo chown -R www-data:www-data /var/www/sims_project

# Set permissions
sudo chmod -R 755 /var/www/sims_project
sudo chmod -R 775 /var/www/sims_project/media
sudo chmod -R 775 /var/www/sims_project/logs
sudo chmod 664 /var/www/sims_project/db.sqlite3
```

## 🌐 Access Points

After successful deployment, access your SIMS system at:

| Service | URL | Description |
|---------|-----|-------------|
| **Homepage** | `http://172.236.152.35/` | Main landing page |
| **Login** | `http://172.236.152.35/users/login/` | User authentication |
| **Admin Panel** | `http://172.236.152.35/admin/` | Administrative interface |
| **Password Reset** | `http://172.236.152.35/users/password-reset/` | Password recovery |

## 🔧 Configuration Details

### Settings Updated for Server
- ✅ **ALLOWED_HOSTS**: Added `172.236.152.35`
- ✅ **Static Files**: Configured for production
- ✅ **Security**: Basic security headers enabled
- ✅ **Database**: SQLite for initial deployment
- ✅ **Environment Variables**: Support for production settings

### Security Considerations
```bash
# Firewall configuration
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS (when SSL is configured)
sudo ufw enable

# SSL Certificate (recommended for production)
# sudo apt install certbot python3-certbot-apache
# sudo certbot --apache -d 172.236.152.35
```

## 🧪 Testing Deployment

### 1. Check Django Configuration
```bash
cd /var/www/sims_project
source venv/bin/activate
python manage.py check --deploy
```

### 2. Test Web Server
```bash
# Test Apache status
sudo systemctl status apache2

# Check Apache logs
sudo tail -f /var/log/apache2/sims_error.log
sudo tail -f /var/log/apache2/sims_access.log
```

### 3. Verify URLs
- Visit: `http://172.236.152.35/`
- Login: `http://172.236.152.35/users/login/`
- Admin: `http://172.236.152.35/admin/`

## 🔍 Troubleshooting

### Common Issues

**1. Internal Server Error (500)**
```bash
# Check Apache error logs
sudo tail -f /var/log/apache2/sims_error.log

# Check Django logs
tail -f /var/www/sims_project/logs/sims.log
```

**2. Static Files Not Loading**
```bash
# Ensure static files are collected
python manage.py collectstatic --noinput

# Check Apache configuration for /static alias
```

**3. Database Permissions**
```bash
# Fix database permissions
sudo chown www-data:www-data /var/www/sims_project/db.sqlite3
sudo chmod 664 /var/www/sims_project/db.sqlite3
```

**4. Python Path Issues**
```bash
# Verify virtual environment in Apache config
# Check WSGIDaemonProcess python-path and python-home
```

## 📊 Performance Optimization

### 1. Enable Gzip Compression
Already configured in Apache virtual host.

### 2. Browser Caching
Already configured for static files.

### 3. Database Optimization (for high traffic)
```bash
# Consider PostgreSQL for production
sudo apt install postgresql postgresql-contrib
sudo -u postgres createuser sims_user
sudo -u postgres createdb sims_db
```

## 🔄 Maintenance

### Daily Tasks
- Monitor Apache logs
- Check disk space
- Verify system functionality

### Weekly Tasks
- Update system packages
- Backup database
- Review security logs

### Monthly Tasks
- Update Django dependencies
- Review user accounts
- Analyze system performance

## 📞 Support

### Log Files
- Apache Error: `/var/log/apache2/sims_error.log`
- Apache Access: `/var/log/apache2/sims_access.log`
- Django Logs: `/var/www/sims_project/logs/sims.log`

### Key Commands
```bash
# Restart Apache
sudo systemctl restart apache2

# Restart Django (if using development server)
python manage.py runserver 172.236.152.35:8000

# Check system status
sudo systemctl status apache2
python manage.py check
```

---

## ✅ Deployment Verification

Once deployed, verify these features work:

- [ ] Homepage loads with PMC theme
- [ ] User registration and login
- [ ] Admin panel accessible
- [ ] Password reset functionality
- [ ] Static files loading correctly
- [ ] Media file uploads working
- [ ] Database operations functional
- [ ] All authentication flows working

**🎉 SIMS is now deployed and accessible at http://172.236.152.35/**
