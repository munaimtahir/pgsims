# 🚀 SIMS VPS Deployment Guide - 139.162.9.224:81

## Overview
This guide provides step-by-step instructions for deploying the SIMS application on a VPS using IP address `139.162.9.224` on port `81`.

## ✅ Pre-Deployment Checklist

### Configuration Updates Completed
- ✅ Django `ALLOWED_HOSTS` updated with `139.162.9.224`
- ✅ Docker Compose configured for port 81
- ✅ Nginx configuration updated for port 81
- ✅ CORS settings updated for the new IP
- ✅ Environment variables configured
- ✅ Frontend API client configured

## 📋 Deployment Options

### Option 1: Docker Compose Deployment (Recommended)

#### Prerequisites
- Docker and Docker Compose installed on VPS
- Port 81 available and accessible
- Firewall configured to allow port 81

#### Steps

1. **Clone/Upload Project to VPS**
   ```bash
   # On your local machine
   scp -r . user@139.162.9.224:/opt/sims_project/
   
   # Or use git
   ssh user@139.162.9.224
   cd /opt
   git clone <your-repo-url> sims_project
   ```

2. **Create Environment File**
   ```bash
   ssh user@139.162.9.224
   cd /opt/sims_project
   cp .env.example .env
   nano .env
   ```

3. **Configure Environment Variables**
   ```bash
   # Required settings for .env file
   DEBUG=False
   SECRET_KEY=your-production-secret-key-min-50-chars
   ALLOWED_HOSTS=139.162.9.224,localhost,127.0.0.1
   CORS_ALLOWED_ORIGINS=http://139.162.9.224:81
   
   # Database (using Docker PostgreSQL)
   DB_NAME=sims_db
   DB_USER=sims_user
   DB_PASSWORD=your-secure-db-password
   
   # Redis (using Docker Redis)
   REDIS_URL=redis://redis:6379/0
   CELERY_BROKER_URL=redis://redis:6379/1
   CELERY_RESULT_BACKEND=redis://redis:6379/1
   ```

4. **Start Services with Docker Compose**
   ```bash
   cd /opt/sims_project
   docker-compose up -d
   ```

5. **Run Migrations**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

6. **Create Superuser (if needed)**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

7. **Collect Static Files**
   ```bash
   docker-compose exec web python manage.py collectstatic --noinput
   ```

8. **Verify Deployment**
   ```bash
   # Check container status
   docker-compose ps
   
   # Check logs
   docker-compose logs -f web
   
   # Test health endpoint
   curl http://139.162.9.224:81/healthz/
   ```

### Option 2: Traditional Nginx + Gunicorn Deployment

#### Prerequisites
- Python 3.11+ installed
- PostgreSQL installed and running
- Redis installed and running
- Nginx installed
- Virtual environment (optional but recommended)

#### Steps

1. **Upload Project to VPS**
   ```bash
   scp -r . user@139.162.9.224:/var/www/sims_project/
   ```

2. **Set Up Python Environment**
   ```bash
   ssh user@139.162.9.224
   cd /var/www/sims_project
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**
   ```bash
   cp .env.example .env
   nano .env
   # Set the same variables as in Option 1
   ```

4. **Run Migrations**
   ```bash
   python manage.py migrate
   python manage.py collectstatic --noinput
   python manage.py createsuperuser
   ```

5. **Configure Gunicorn**
   ```bash
   # Use the provided gunicorn.conf.py
   cp deployment/gunicorn.conf.py /var/www/sims_project/gunicorn.conf.py
   ```

6. **Create Systemd Service**
   ```bash
   sudo cp deployment/sims.service /etc/systemd/system/sims.service
   sudo nano /etc/systemd/system/sims.service
   # Update paths and user as needed
   sudo systemctl daemon-reload
   sudo systemctl enable sims
   sudo systemctl start sims
   ```

7. **Configure Nginx**
   ```bash
   # Copy nginx configuration
   sudo cp deployment/nginx_sims.conf /etc/nginx/sites-available/sims
   
   # Update the configuration for port 81
   sudo nano /etc/nginx/sites-available/sims
   # Change listen 80 to listen 81
   
   # Enable site
   sudo ln -s /etc/nginx/sites-available/sims /etc/nginx/sites-enabled/
   
   # Test and reload
   sudo nginx -t
   sudo systemctl reload nginx
   ```

8. **Configure Firewall**
   ```bash
   # For UFW
   sudo ufw allow 81/tcp
   sudo ufw reload
   
   # For firewalld
   sudo firewall-cmd --permanent --add-port=81/tcp
   sudo firewall-cmd --reload
   ```

## 🔧 Nginx Configuration for Port 81

If deploying without Docker, update `/etc/nginx/sites-available/sims`:

```nginx
server {
    listen 81;
    server_name 139.162.9.224;
    
    # ... rest of configuration from nginx_sims.conf
}
```

## 🌐 Access URLs

After successful deployment:

| Service | URL | Status |
|---------|-----|--------|
| **Homepage** | `http://139.162.9.224:81/` | ✅ Ready |
| **Login** | `http://139.162.9.224:81/users/login/` | ✅ Ready |
| **Admin Panel** | `http://139.162.9.224:81/admin/` | ✅ Ready |
| **API** | `http://139.162.9.224:81/api/` | ✅ Ready |
| **Health Check** | `http://139.162.9.224:81/healthz/` | ✅ Ready |

## 🔒 Security Considerations

1. **Firewall Configuration**
   - Ensure only necessary ports are open
   - Consider restricting access by IP if possible

2. **SSL/HTTPS (Recommended)**
   - Set up SSL certificate using Let's Encrypt
   - Update `SECURE_SSL_REDIRECT=True` in settings
   - Configure HTTPS in Nginx

3. **Secret Key**
   - Generate a strong secret key: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
   - Never commit secret keys to version control

4. **Database Security**
   - Use strong database passwords
   - Restrict database access to localhost only
   - Regular backups

## 🐛 Troubleshooting

### Port 81 Not Accessible
```bash
# Check if port is listening
sudo netstat -tlnp | grep 81
sudo ss -tlnp | grep 81

# Check firewall
sudo ufw status
sudo firewall-cmd --list-ports
```

### Django ALLOWED_HOSTS Error
```bash
# Verify environment variable
echo $ALLOWED_HOSTS
# Should include: 139.162.9.224

# Check Django settings
docker-compose exec web python manage.py shell
>>> from django.conf import settings
>>> print(settings.ALLOWED_HOSTS)
```

### Static Files Not Loading
```bash
# Collect static files
docker-compose exec web python manage.py collectstatic --noinput

# Check Nginx static file configuration
sudo nginx -t
```

### Database Connection Issues
```bash
# Test database connection
docker-compose exec web python manage.py dbshell

# Check database logs
docker-compose logs db
```

## 📊 Monitoring

### Check Service Status
```bash
# Docker Compose
docker-compose ps
docker-compose logs -f

# Systemd (traditional deployment)
sudo systemctl status sims
sudo systemctl status nginx
```

### View Logs
```bash
# Application logs
docker-compose logs -f web

# Nginx logs
sudo tail -f /var/log/nginx/sims_access.log
sudo tail -f /var/log/nginx/sims_error.log

# Django logs
tail -f /var/www/sims_project/logs/sims.log
```

## 🔄 Updates and Maintenance

### Update Application
```bash
# Pull latest changes
git pull origin main

# Rebuild Docker containers
docker-compose down
docker-compose build
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate
```

### Backup Database
```bash
# Docker Compose
docker-compose exec db pg_dump -U sims_user sims_db > backup_$(date +%Y%m%d).sql

# Traditional
pg_dump -U sims_user sims_db > backup_$(date +%Y%m%d).sql
```

## 📝 Environment Variables Reference

Key environment variables for deployment:

```bash
# Core Settings
DEBUG=False
SECRET_KEY=<your-secret-key>
ALLOWED_HOSTS=139.162.9.224,localhost,127.0.0.1

# Database
DB_NAME=sims_db
DB_USER=sims_user
DB_PASSWORD=<secure-password>
DB_HOST=localhost  # or db for Docker
DB_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379/0  # or redis:6379/0 for Docker

# CORS
CORS_ALLOWED_ORIGINS=http://139.162.9.224:81

# Email (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=<your-email>
EMAIL_HOST_PASSWORD=<your-password>
```

## ✅ Verification Checklist

- [ ] Application accessible at `http://139.162.9.224:81/`
- [ ] Login page loads correctly
- [ ] Admin panel accessible
- [ ] Static files loading properly
- [ ] Database migrations applied
- [ ] Health check endpoint responding
- [ ] Logs show no critical errors
- [ ] Firewall configured correctly
- [ ] SSL configured (if applicable)

## 🆘 Support

For issues or questions:
1. Check application logs
2. Review Nginx error logs
3. Verify environment variables
4. Test database connectivity
5. Check firewall rules

---

**🎉 Deployment Complete!**

Your SIMS application should now be accessible at `http://139.162.9.224:81/`
