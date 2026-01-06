# 🚀 PHC (PGSIMS) Deployment Guide

## Overview

This guide covers deploying SIMS on **phc.alshifalab.pk** using:
- **Server IP:** 34.124.150.231
- **Domain:** phc.alshifalab.pk
- **Backend Port:** 8014 (internal, proxied by Caddy)
- **Reverse Proxy:** Caddy (handles SSL/TLS automatically)

## Prerequisites

1. Server with Docker and Docker Compose installed
2. Caddy installed and configured
3. Domain `phc.alshifalab.pk` pointing to server IP `34.124.150.231`
4. Port 8014 available (internal, not exposed externally)

## Deployment Steps

### 1. Clone Repository

```bash
cd /home/munaim/srv/pgsims
git pull  # or clone if first time
```

### 2. Configure Environment Variables

```bash
# Copy example environment file
cp deployment/.env.phc.example .env

# Edit .env with your values
nano .env
```

**Required values:**
- `SECRET_KEY` - Generate a strong secret key
- `DB_PASSWORD` - Strong database password
- `ALLOWED_HOSTS` - Should include: `phc.alshifalab.pk,34.124.150.231,localhost,127.0.0.1`
- `CORS_ALLOWED_ORIGINS` - Should include: `https://phc.alshifalab.pk`
- `CSRF_TRUSTED_ORIGINS` - Should include: `https://phc.alshifalab.pk`

### 3. Configure Caddy

```bash
# Copy Caddyfile to Caddy configuration directory
sudo cp deployment/Caddyfile.phc /etc/caddy/Caddyfile.phc

# Or add to existing Caddyfile
sudo nano /etc/caddy/Caddyfile
# Add the contents from deployment/Caddyfile.phc

# Test Caddy configuration
sudo caddy validate --config /etc/caddy/Caddyfile

# Reload Caddy
sudo systemctl reload caddy
# or
sudo caddy reload --config /etc/caddy/Caddyfile
```

### 4. Deploy with Docker Compose

```bash
# Use PHC-specific compose file
docker compose -f docker-compose.phc.yml up -d --build

# Check status
docker compose -f docker-compose.phc.yml ps

# View logs
docker compose -f docker-compose.phc.yml logs -f
```

### 5. Run Database Migrations

```bash
# Migrations should run automatically, but verify:
docker compose -f docker-compose.phc.yml exec web python manage.py migrate

# Collect static files (should run automatically, but verify):
docker compose -f docker-compose.phc.yml exec web python manage.py collectstatic --noinput
```

### 6. Create Superuser

```bash
docker compose -f docker-compose.phc.yml exec web python manage.py createsuperuser
```

### 7. Seed Demo Data (Optional)

```bash
docker compose -f docker-compose.phc.yml exec web python scripts/preload_demo_data.py
```

## Verification

### 1. Check Health Endpoint

```bash
# From server
curl https://phc.alshifalab.pk/healthz/

# Expected response:
# {"status":"healthy","checks":{"database":"ok","cache":"ok"}}
```

### 2. Test Homepage

Open in browser: **https://phc.alshifalab.pk/**

### 3. Test Login

Navigate to: **https://phc.alshifalab.pk/users/login/**

Use demo credentials:
- Admin: `admin` / `admin123`

## Configuration Details

### Port Configuration

- **Backend (Gunicorn):** Port 8014 (internal, localhost only)
- **Caddy:** Ports 80 (HTTP) and 443 (HTTPS) - external
- **Database:** Port 5432 (internal, Docker network)
- **Redis:** Port 6379 (internal, Docker network)

### Network Architecture

```
Internet
    ↓
Caddy (Port 443 - HTTPS)
    ↓
localhost:8014 (Django/Gunicorn)
    ↓
PostgreSQL (Docker network)
Redis (Docker network)
```

### SSL/TLS

Caddy automatically:
- Obtains SSL certificates from Let's Encrypt
- Handles certificate renewal
- Redirects HTTP to HTTPS
- Terminates SSL/TLS

Django receives:
- `X-Forwarded-Proto: https` header
- `X-Forwarded-For` header (client IP)
- `X-Forwarded-Host` header

## Frontend Deployment

If deploying a separate frontend:

### Update Frontend Environment

```bash
cd frontend
# Create or update .env.local
echo "NEXT_PUBLIC_API_URL=https://phc.alshifalab.pk" > .env.local
```

### Build and Deploy Frontend

```bash
cd frontend
npm install
npm run build
npm start  # or use PM2/systemd for production
```

## Troubleshooting

### Caddy Not Routing to Backend

1. **Check Caddy is running:**
   ```bash
   sudo systemctl status caddy
   ```

2. **Check Caddy logs:**
   ```bash
   sudo journalctl -u caddy -f
   ```

3. **Verify backend is listening:**
   ```bash
   curl http://localhost:8014/healthz/
   ```

4. **Test Caddy configuration:**
   ```bash
   sudo caddy validate --config /etc/caddy/Caddyfile
   ```

### Backend Not Accessible

1. **Check Docker containers:**
   ```bash
   docker compose -f docker-compose.phc.yml ps
   ```

2. **Check backend logs:**
   ```bash
   docker compose -f docker-compose.phc.yml logs web
   ```

3. **Verify port 8014 is listening:**
   ```bash
   sudo ss -tulpn | grep 8014
   ```

### SSL Certificate Issues

1. **Check Caddy logs for certificate errors:**
   ```bash
   sudo journalctl -u caddy | grep -i cert
   ```

2. **Verify DNS is pointing to server:**
   ```bash
   dig phc.alshifalab.pk
   # Should return: 34.124.150.231
   ```

3. **Manually request certificate:**
   ```bash
   sudo caddy certmagic --config /etc/caddy/Caddyfile
   ```

### CORS Errors

1. **Verify CORS_ALLOWED_ORIGINS in .env:**
   ```bash
   grep CORS_ALLOWED_ORIGINS .env
   # Should include: https://phc.alshifalab.pk
   ```

2. **Restart backend:**
   ```bash
   docker compose -f docker-compose.phc.yml restart web
   ```

## Maintenance

### Update Application

```bash
# Pull latest code
git pull

# Rebuild and restart
docker compose -f docker-compose.phc.yml up -d --build

# Run migrations
docker compose -f docker-compose.phc.yml exec web python manage.py migrate
```

### Backup Database

```bash
docker compose -f docker-compose.phc.yml exec db pg_dump -U sims_user sims_db > backup_$(date +%Y%m%d_%H%M%S).sql
```

### View Logs

```bash
# All services
docker compose -f docker-compose.phc.yml logs -f

# Specific service
docker compose -f docker-compose.phc.yml logs -f web

# Caddy logs
sudo journalctl -u caddy -f
```

## Security Checklist

- [ ] Strong `SECRET_KEY` set in `.env`
- [ ] Strong `DB_PASSWORD` set in `.env`
- [ ] `DEBUG=False` in production
- [ ] `ALLOWED_HOSTS` includes domain and IP
- [ ] `CORS_ALLOWED_ORIGINS` configured correctly
- [ ] `CSRF_TRUSTED_ORIGINS` configured correctly
- [ ] SSL/TLS enabled (automatic with Caddy)
- [ ] Firewall configured (ports 80, 443 open)
- [ ] Regular backups scheduled
- [ ] Demo credentials changed in production

## Access URLs

- **Homepage:** https://phc.alshifalab.pk/
- **Login:** https://phc.alshifalab.pk/users/login/
- **Admin:** https://phc.alshifalab.pk/admin/
- **API:** https://phc.alshifalab.pk/api/
- **Health:** https://phc.alshifalab.pk/healthz/

---

**Last Updated:** $(date)
**Server IP:** 34.124.150.231
**Domain:** phc.alshifalab.pk
**Backend Port:** 8014
