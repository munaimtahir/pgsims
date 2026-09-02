# Coolify/Traefik Deployment Guide

This guide explains how to deploy SIMS on a VPS using Coolify with Traefik as the reverse proxy. This is the **recommended production deployment method** for single-VPS deployments.

## Overview

This deployment architecture:
- ✅ Uses **Traefik** for reverse proxy and automatic SSL/TLS termination
- ✅ Uses **Coolify** for container orchestration and deployment
- ✅ Uses **WhiteNoise** for efficient static file serving (no nginx needed)
- ✅ Exposes only port 8000 internally (Traefik handles external access)
- ✅ No port 80/443 bindings from the application (handled by Traefik)
- ✅ Automatic HTTPS with Let's Encrypt
- ✅ Health checks and automatic container restart

## Prerequisites

### 1. VPS Requirements
- Ubuntu 20.04/22.04 or Debian 11/12
- Minimum 2GB RAM, 2 CPU cores
- 20GB+ disk space
- Public IP address
- Domain name pointing to your VPS

### 2. Install Coolify
Follow the official installation guide at https://coolify.io/docs/installation

Quick install:
```bash
curl -fsSL https://get.coolify.io | bash
```

Access Coolify at: `http://your-vps-ip:8000`

### 3. Domain Configuration
Point your domain's A record to your VPS IP:
```
Type: A
Name: @ (or subdomain like 'sims')
Value: YOUR_VPS_IP
TTL: 3600
```

## Deployment Steps

### Step 1: Create New Resource in Coolify

1. Log into Coolify dashboard
2. Click "New Resource"
3. Select "Public Repository"
4. Enter repository URL: `https://github.com/munaimtahir/sims.git`
5. Select branch: `main` (or your desired branch)
6. Click "Continue"

### Step 2: Configure Build Settings

In the "Build" tab:

| Setting | Value |
|---------|-------|
| **Build Pack** | Dockerfile |
| **Dockerfile Location** | `Dockerfile` |
| **Docker Compose File** | `docker-compose.coolify.yml` (if using compose) |
| **Port** | `8000` |
| **Health Check Path** | `/healthz/` |
| **Health Check Interval** | `30s` |

### Step 3: Configure Environment Variables

In the "Environment Variables" tab, add the following **REQUIRED** variables:

#### Required Variables
```bash
# Django Secret Key (REQUIRED - generate a strong one)
SECRET_KEY=your-strong-random-secret-key-minimum-50-characters-long

# Database Password (REQUIRED)
DB_PASSWORD=your-strong-database-password

# Allowed Hosts (REQUIRED - use your domain)
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Debug Mode (MUST be False in production)
DEBUG=False
```

#### Security Variables (Recommended)
```bash
# SSL/Security Settings
# Note: SECURE_SSL_REDIRECT should match your Traefik configuration
# Set to True if Traefik is NOT handling HTTP->HTTPS redirects
# Set to False if Traefik IS handling redirects (recommended)
SECURE_SSL_REDIRECT=False

# Cookie security - Set to True in production behind HTTPS
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS=https://yourdomain.com

# Reverse proxy headers - Keep True when behind Traefik
USE_PROXY_HEADERS=True

# HSTS (enable after SSL is working)
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
```

#### Optional Variables
```bash
# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-app-password

# Database (optional - defaults are fine)
DB_NAME=sims_db
DB_USER=sims_user

# CORS (if using separate frontend)
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://app.yourdomain.com
```

### Step 4: Configure Domain & SSL

In the "Domains" tab:

1. Click "Add Domain"
2. Enter your domain: `yourdomain.com`
3. Enable "Generate SSL Certificate" (Let's Encrypt)
4. Enable "Force HTTPS"
5. Save

Coolify will automatically:
- Configure Traefik routing
- Obtain SSL certificate from Let's Encrypt
- Set up automatic certificate renewal
- Configure HTTPS redirect

### Step 5: Deploy

1. Click "Deploy" button
2. Monitor the deployment logs
3. Wait for all services to be healthy (check health status)
4. Access your application at: `https://yourdomain.com`

### Step 6: Create Django Superuser

After deployment, create an admin user:

1. In Coolify, go to your resource
2. Click "Execute Command" or "Terminal"
3. Select the `web` container
4. Run:
```bash
python manage.py createsuperuser
```
5. Follow the prompts to create your admin account

## Architecture Overview

```
Internet
    ↓
Traefik (Port 80/443)
    ↓ (HTTPS termination)
SIMS Web (Port 8000 internal)
    ↓
PostgreSQL (Port 5432 internal)
Redis (Port 6379 internal)
Celery Worker
Celery Beat
```

### Traffic Flow
1. User accesses `https://yourdomain.com`
2. Traefik receives request on port 443
3. Traefik terminates SSL/TLS
4. Traefik forwards to `web:8000` with `X-Forwarded-Proto: https`
5. Django app processes request
6. WhiteNoise serves static files directly
7. Response flows back through Traefik to user

## Important Configuration Notes

### 1. No Port Bindings
The application **does not** bind to ports 80 or 443. Traefik handles all external access.

### 2. SSL/TLS Termination
SSL is terminated at Traefik. The application receives `X-Forwarded-Proto: https` header, which Django uses to detect HTTPS.

### 3. Static Files
Static files are served by **WhiteNoise** middleware, not nginx. This simplifies deployment and reduces memory usage.

### 4. Health Checks
Health checks run at `/healthz/` and verify:
- Database connectivity
- Redis connectivity
- Celery worker status (optional)

### 5. Reverse Proxy Headers
Django is configured to trust these headers from Traefik:
- `X-Forwarded-Proto` - Detects HTTPS
- `X-Forwarded-For` - Client IP address
- `Host` - Request hostname

## Verification

### 1. Check Application Health
```bash
curl https://yourdomain.com/healthz/
```

Expected response:
```json
{
  "status": "healthy",
  "checks": {
    "database": "ok",
    "cache": "ok",
    "celery": "ok"
  }
}
```

### 2. Verify SSL
```bash
curl -I https://yourdomain.com
```

Should see:
- `HTTP/2 200` or `HTTP/1.1 200`
- `Strict-Transport-Security` header
- Valid SSL certificate

### 3. Check Django Admin
Visit `https://yourdomain.com/admin/` and log in with your superuser account.

### 4. Verify Static Files
Check that CSS/JS loads correctly. WhiteNoise should serve all static files with proper caching headers.

## Troubleshooting

### Issue: Application won't start
**Check:**
1. Environment variables are set correctly (especially `SECRET_KEY` and `DB_PASSWORD`)
2. Database service is healthy
3. Check logs in Coolify dashboard

### Issue: SSL certificate not generated
**Solutions:**
1. Verify DNS is pointing to correct IP (wait for propagation)
2. Ensure port 80 and 443 are open on firewall
3. Check Traefik logs in Coolify

### Issue: Static files not loading
**Check:**
1. `collectstatic` ran successfully during deployment
2. WhiteNoise is in `MIDDLEWARE` setting
3. Check browser console for 404 errors

### Issue: "DisallowedHost" error
**Solution:**
Add your domain to `ALLOWED_HOSTS` environment variable:
```bash
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

### Issue: CSRF verification failed
**Solution:**
Add your domain to `CSRF_TRUSTED_ORIGINS`:
```bash
CSRF_TRUSTED_ORIGINS=https://yourdomain.com
```

### Issue: Health check failing
**Check:**
1. Database is running and accessible
2. Redis is running and accessible
3. Check `/healthz/` endpoint in logs

## Maintenance

### Update Application
1. Push code to your Git repository
2. In Coolify, click "Redeploy"
3. Monitor logs for successful deployment

### View Logs
In Coolify dashboard:
1. Select your resource
2. Click "Logs" tab
3. Filter by service (web, worker, db, redis)

### Database Backup
```bash
# From Coolify terminal (db container)
pg_dump -U sims_user sims_db > backup.sql

# Or use Coolify's built-in backup feature
```

### Scale Workers
In `docker-compose.coolify.yml`, adjust `--concurrency` parameter for Celery workers based on load.

## Security Best Practices

1. ✅ **Never use DEBUG=True in production**
2. ✅ **Use strong SECRET_KEY** (50+ characters, random)
3. ✅ **Use strong DB_PASSWORD**
4. ✅ **Enable HSTS** after SSL is working
5. ✅ **Keep dependencies updated** (rebuild regularly)
6. ✅ **Monitor logs** for security issues
7. ✅ **Use environment variables** for all secrets
8. ✅ **Restrict admin access** (firewall rules)
9. ✅ **Regular backups** of database and media files
10. ✅ **Monitor health checks** and set up alerts

## Migration from Nginx Setup

If migrating from an nginx-based setup:

1. Remove nginx service from compose file
2. Remove port 443 bindings
3. Add WhiteNoise to requirements and settings
4. Configure `SECURE_PROXY_SSL_HEADER` in settings
5. Update `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS`
6. Deploy using Coolify with Traefik

## Support

For issues:
1. Check Coolify logs
2. Check application logs at `/app/logs/`
3. Review health check endpoint: `/healthz/`
4. Consult Coolify documentation: https://coolify.io/docs
5. Consult Django documentation: https://docs.djangoproject.com/

## Summary

This deployment method provides:
- ✅ **Simple**: Single compose file, no nginx configuration
- ✅ **Secure**: Automatic HTTPS with Let's Encrypt
- ✅ **Scalable**: Easy to add more workers or services
- ✅ **Maintainable**: GitOps workflow with Coolify
- ✅ **Production-ready**: Health checks, logging, monitoring
- ✅ **Cost-effective**: Single VPS deployment

**Recommended for**: Small to medium deployments, single VPS, < 10k users
