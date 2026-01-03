# 🚀 PHC Deployment Configuration Summary

## Overview

This document summarizes the configuration for deploying SIMS on **phc.alshifalab.pk** with Caddy reverse proxy.

## Configuration Details

### Server Information
- **Domain:** phc.alshifalab.pk
- **Server IP:** 34.124.150.231
- **Backend Port:** 8014 (internal, proxied by Caddy)
- **Reverse Proxy:** Caddy (automatic SSL/TLS on ports 80/443)

### Updated Configuration Files

#### 1. Django Settings (`sims_project/settings.py`)
- ✅ **ALLOWED_HOSTS** updated to include:
  - `34.124.150.231`
  - `phc.alshifalab.pk`
  - `localhost`
  - `127.0.0.1`

#### 2. Docker Compose (`docker-compose.phc.yml`)
- ✅ New PHC-specific compose file created
- ✅ Backend configured to run on port 8014
- ✅ Environment variables configured for Caddy proxy
- ✅ SSL/TLS settings enabled (SECURE_SSL_REDIRECT=True)
- ✅ CSRF and CORS configured for HTTPS domain

#### 3. Frontend API Client (`frontend/lib/api/client.ts`)
- ✅ Auto-detection for `phc.alshifalab.pk` domain
- ✅ Returns `https://phc.alshifalab.pk` for API calls
- ✅ Fallback support for IP address `34.124.150.231`

#### 4. Gunicorn Configuration (`deployment/gunicorn_phc.conf.py`)
- ✅ Updated to bind to `0.0.0.0:8014` (for Docker)
- ✅ Configured for PHC deployment

#### 5. Caddy Configuration (`deployment/Caddyfile.phc`)
- ✅ Complete Caddyfile template created
- ✅ SSL/TLS automatic certificate management
- ✅ Security headers configured
- ✅ Reverse proxy to localhost:8014
- ✅ Static and media file handling
- ✅ Health check endpoint routing

#### 6. Environment Variables (`deployment/.env.phc.example`)
- ✅ PHC-specific environment template
- ✅ Includes all required variables:
  - ALLOWED_HOSTS
  - CORS_ALLOWED_ORIGINS
  - CSRF_TRUSTED_ORIGINS
  - SSL/TLS settings

#### 7. Deployment Script (`deployment/deploy_phc.sh`)
- ✅ Automated deployment script
- ✅ Checks Docker and Caddy configuration
- ✅ Builds and starts containers
- ✅ Runs migrations and collects static files
- ✅ Verifies deployment

#### 8. Deployment Guide (`deployment/DEPLOY_PHC.md`)
- ✅ Complete step-by-step deployment instructions
- ✅ Caddy configuration guide
- ✅ Troubleshooting section
- ✅ Maintenance commands

## Quick Deployment

### 1. Configure Environment
```bash
cd /home/munaim/srv/pgsims
cp deployment/.env.phc.example .env
# Edit .env with your SECRET_KEY, DB_PASSWORD, etc.
```

### 2. Configure Caddy
```bash
# Copy Caddyfile
sudo cp deployment/Caddyfile.phc /etc/caddy/Caddyfile

# Or add to existing Caddyfile
sudo nano /etc/caddy/Caddyfile
# Add configuration from deployment/Caddyfile.phc

# Validate and reload
sudo caddy validate --config /etc/caddy/Caddyfile
sudo systemctl reload caddy
```

### 3. Deploy Application
```bash
# Run deployment script
cd /home/munaim/srv/pgsims
./deployment/deploy_phc.sh

# Or manually:
docker compose -f docker-compose.phc.yml up -d --build
```

### 4. Create Superuser
```bash
docker compose -f docker-compose.phc.yml exec web python manage.py createsuperuser
```

### 5. Seed Demo Data (Optional)
```bash
docker compose -f docker-compose.phc.yml exec web python scripts/preload_demo_data.py
```

## Access URLs

- **Homepage:** https://phc.alshifalab.pk/
- **Login:** https://phc.alshifalab.pk/users/login/
- **Admin:** https://phc.alshifalab.pk/admin/
- **API:** https://phc.alshifalab.pk/api/
- **Health:** https://phc.alshifalab.pk/healthz/

## Demo Credentials

- **Admin:** `admin` / `admin123`
- **Supervisor:** `dr_smith` / `supervisor123`
- **Supervisor:** `dr_jones` / `supervisor123`
- **Student:** `pg_ahmed` / `student123`
- **Student:** `pg_fatima` / `student123`

## Network Architecture

```
Internet (HTTPS)
    ↓
Caddy (Port 443)
    ↓
localhost:8014 (Django/Gunicorn in Docker)
    ↓
PostgreSQL (Docker network)
Redis (Docker network)
Celery Worker & Beat (Docker network)
```

## Key Configuration Points

### ALLOWED_HOSTS
```
phc.alshifalab.pk,34.124.150.231,localhost,127.0.0.1
```

### CORS_ALLOWED_ORIGINS
```
https://phc.alshifalab.pk
```

### CSRF_TRUSTED_ORIGINS
```
https://phc.alshifalab.pk
```

### Backend Port
- Internal: `8014` (Docker container)
- External: Not exposed (only accessible via Caddy)

### Caddy Ports
- HTTP: `80` (redirects to HTTPS)
- HTTPS: `443` (main access)

## Verification Checklist

- [ ] DNS points `phc.alshifalab.pk` to `34.124.150.231`
- [ ] Caddy is installed and running
- [ ] Caddyfile configured correctly
- [ ] `.env` file created with all required variables
- [ ] Docker containers running (`docker compose -f docker-compose.phc.yml ps`)
- [ ] Backend accessible on localhost:8014
- [ ] HTTPS accessible at https://phc.alshifalab.pk
- [ ] Health check returns 200: `curl https://phc.alshifalab.pk/healthz/`
- [ ] Login page accessible
- [ ] Static files loading correctly
- [ ] Demo data seeded (if needed)

## Troubleshooting

### Backend Not Accessible
```bash
# Check containers
docker compose -f docker-compose.phc.yml ps

# Check logs
docker compose -f docker-compose.phc.yml logs web

# Test backend directly
curl http://localhost:8014/healthz/
```

### Caddy Not Routing
```bash
# Check Caddy status
sudo systemctl status caddy

# Check Caddy logs
sudo journalctl -u caddy -f

# Validate Caddyfile
sudo caddy validate --config /etc/caddy/Caddyfile
```

### SSL Certificate Issues
```bash
# Check certificate status
sudo caddy certmagic --config /etc/caddy/Caddyfile

# Verify DNS
dig phc.alshifalab.pk
```

## Files Created/Updated

### New Files
- `docker-compose.phc.yml` - PHC Docker Compose configuration
- `deployment/Caddyfile.phc` - Caddy configuration template
- `deployment/.env.phc.example` - Environment variables template
- `deployment/deploy_phc.sh` - Automated deployment script
- `deployment/DEPLOY_PHC.md` - Complete deployment guide
- `PHC_DEPLOYMENT_SUMMARY.md` - This file

### Updated Files
- `sims_project/settings.py` - Added new IP and domain to ALLOWED_HOSTS
- `docker-compose.yml` - Added new IP to default ALLOWED_HOSTS
- `frontend/lib/api/client.ts` - Added PHC domain detection
- `deployment/gunicorn_phc.conf.py` - Updated bind address
- `DEPLOYMENT_STATUS.md` - Added PHC server information

## Next Steps

1. **Deploy to Server:**
   - SSH to server (34.124.150.231)
   - Run deployment script or follow manual steps

2. **Configure Caddy:**
   - Copy Caddyfile to `/etc/caddy/Caddyfile`
   - Validate and reload Caddy

3. **Verify Deployment:**
   - Test all URLs
   - Verify SSL certificate
   - Test login functionality
   - Check static files

4. **Production Hardening:**
   - Change demo credentials
   - Review security settings
   - Set up monitoring
   - Configure backups

---

**Last Updated:** $(date)
**Status:** ✅ Configuration Complete - Ready for Deployment
