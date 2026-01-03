# SIMS Deployment Environments Guide

This guide explains the differences between localhost and VPS deployment configurations and how to switch between them.

## Overview

SIMS supports multiple deployment environments:

1. **Localhost** - For local development and demonstrations on your Windows machine
2. **VPS (Primary)** - For production deployment on VPS server (139.162.9.224:81)
3. **VPS (Secondary)** - For production deployment on VPS server (172.237.95.120:81)

All configurations can coexist in the same codebase, allowing you to easily switch between them.

## Environment Comparison

| Feature | Localhost | VPS (Primary) | VPS (Secondary) |
|---------|-----------|---------------|-----------------|
| **Purpose** | Development, testing, demonstrations | Production deployment | Production deployment |
| **URL** | http://localhost:8000 | http://139.162.9.224:81 | http://172.237.95.120:81 |
| **Port** | 8000 | 81 | 81 |
| **DEBUG Mode** | True | False | False |
| **ALLOWED_HOSTS** | localhost,127.0.0.1 | 139.162.9.224,localhost,127.0.0.1 | 172.237.95.120,localhost,127.0.0.1 |
| **Database** | SQLite (default) or local PostgreSQL | PostgreSQL in Docker | PostgreSQL in Docker |
| **Redis** | Optional (can use Docker) | Required (Docker container) | Required (Docker container) |
| **Nginx** | Optional | Required | Required |
| **SSL/HTTPS** | Not required | Recommended for production | Recommended for production |
| **Celery** | Optional | Required for production | Required for production |
| **Static Files** | Development server | Nginx served | Nginx served |
| **Email Backend** | Console (prints to terminal) | SMTP server | SMTP server |

## Configuration Files

### Localhost Configuration

- **Backend:** `.env.localhost` → copy to `.env`
- **Frontend:** `frontend/.env.localhost` → copy to `frontend/.env.local`
- **Docker:** `docker-compose.localhost.yml`
- **Nginx:** `deployment/nginx.localhost.conf`

### VPS Configuration (Primary - 139.162.9.224)

- **Backend:** `.env.vps` → copy to `.env` (or use server-specific config)
- **Frontend:** `frontend/.env.vps` → copy to `frontend/.env.local`
- **Docker:** `docker-compose.yml` (default)
- **Nginx:** `deployment/nginx.conf`
- **Deployment Script:** `deployment/deploy_docker_compose.sh`

### VPS Configuration (Secondary - 172.237.95.120)

- **Backend:** `deployment/server_config_172.237.95.120.env` → copy to `.env`
- **Frontend:** `frontend/.env.vps` → copy to `frontend/.env.local` (update API URL)
- **Docker:** `docker-compose.yml` (default)
- **Nginx:** `deployment/nginx.conf`
- **Deployment Script:** `deployment/deploy_server_172.237.95.120.sh`

## When to Use Each Environment

### Use Localhost When:

- Developing new features
- Testing changes locally
- Running demonstrations on your local machine
- Debugging issues
- Learning the codebase
- Working offline

### Use VPS When:

- Deploying to production
- Sharing with remote users
- Running production workloads
- Need stable, accessible deployment
- Testing production-like environment

**VPS Server Selection:**
- **139.162.9.224** - Primary production server
- **172.237.95.120** - Secondary production server (backup, load balancing, or separate environment)

## Switching Between Environments

### Quick Switch

**Switch to Localhost:**
```powershell
# Windows PowerShell
.\deployment\switch_to_localhost.ps1

# Linux/Mac
./deployment/switch_to_localhost.sh
```

**Switch to VPS:**
```powershell
# Windows PowerShell (if script available)
.\deployment\switch_to_vps.sh

# Linux/Mac
./deployment/switch_to_vps.sh
```

### Manual Switch

**1. Switch Backend Configuration:**

```powershell
# To localhost
Copy-Item .env.localhost .env

# To VPS
Copy-Item .env.vps .env
```

**2. Switch Frontend Configuration:**

```powershell
# To localhost
Copy-Item frontend\.env.localhost frontend\.env.local

# To VPS
Copy-Item frontend\.env.vps frontend\.env.local
```

**3. Use Appropriate Docker Compose:**

```powershell
# Localhost
docker compose -f docker-compose.localhost.yml up -d

# VPS
docker compose up -d
```

## Environment-Specific Settings

### Localhost Settings

**Typical .env.localhost:**
```env
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:8000,http://localhost:3000
# SQLite by default (no DB config needed)
REDIS_URL=redis://localhost:6379/0  # Optional
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

**Typical frontend/.env.localhost:**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### VPS Settings (Primary - 139.162.9.224)

**Typical .env.vps:**
```env
DEBUG=False
ALLOWED_HOSTS=139.162.9.224,localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://139.162.9.224:81
DB_NAME=sims_db
DB_USER=sims_user
DB_PASSWORD=secure-password
DB_HOST=db
DATABASE_URL=postgresql://sims_user:password@db:5432/sims_db
REDIS_URL=redis://redis:6379/0
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
```

**Typical frontend/.env.vps:**
```env
NEXT_PUBLIC_API_URL=http://139.162.9.224:81
```

### VPS Settings (Secondary - 172.237.95.120)

**Typical .env for 172.237.95.120:**
```env
DEBUG=False
ALLOWED_HOSTS=172.237.95.120,localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://172.237.95.120:81
DB_NAME=sims_db
DB_USER=sims_user
DB_PASSWORD=secure-password
DB_HOST=db
DATABASE_URL=postgresql://sims_user:password@db:5432/sims_db
REDIS_URL=redis://redis:6379/0
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
```

**Typical frontend/.env.local for 172.237.95.120:**
```env
NEXT_PUBLIC_API_URL=http://172.237.95.120:81
```

## Deployment Workflows

### Localhost Deployment Workflow

1. **Development:**
   ```powershell
   # Activate venv
   venv\Scripts\activate
   
   # Run migrations
   python manage.py migrate
   
   # Start server
   python manage.py runserver
   ```

2. **Docker (optional):**
   ```powershell
   .\deployment\deploy_localhost.ps1
   ```

### VPS Deployment Workflow (Primary - 139.162.9.224)

1. **SSH to VPS:**
   ```bash
   ssh user@139.162.9.224
   ```

2. **Switch to VPS config:**
   ```bash
   ./deployment/switch_to_vps.sh
   ```

3. **Deploy:**
   ```bash
   docker compose up -d --build
   docker compose exec web python manage.py migrate
   ```

### VPS Deployment Workflow (Secondary - 172.237.95.120)

1. **SSH to VPS:**
   ```bash
   ssh user@172.237.95.120
   ```

2. **Use automated deployment script:**
   ```bash
   cd /opt/sims_project
   ./deployment/deploy_server_172.237.95.120.sh
   ```

3. **Or manual deployment:**
   ```bash
   # Set environment variables
   export ALLOWED_HOSTS="172.237.95.120,localhost,127.0.0.1"
   docker compose up -d --build
   docker compose exec web python manage.py migrate
   ```

## Key Differences Explained

### 1. Port Configuration

- **Localhost:** Uses standard port 8000 for Django development server
- **VPS:** Uses port 81 through Nginx reverse proxy (avoids conflicts with other services)

### 2. Database

- **Localhost:** SQLite by default (no setup needed) or local PostgreSQL
- **VPS:** PostgreSQL in Docker container (production-ready, better performance)

### 3. Static Files

- **Localhost:** Served by Django development server (`DEBUG=True`)
- **VPS:** Served by Nginx (better performance, required for production)

### 4. Security

- **Localhost:** DEBUG mode enabled (detailed error pages, helpful for development)
- **VPS:** DEBUG mode disabled, security headers enabled, SSL recommended

### 5. Email

- **Localhost:** Console backend (emails printed to terminal)
- **VPS:** SMTP backend (real email delivery)

## Best Practices

### Development

1. Always develop on localhost first
2. Test changes locally before deploying to VPS
3. Use localhost for demonstrations when possible
4. Keep localhost .env files in version control (template only, no secrets)

### Production (VPS)

1. Never commit production .env files
2. Use strong SECRET_KEY and passwords
3. Enable SSL/HTTPS for production
4. Set DEBUG=False
5. Use proper SMTP configuration
6. Set up backups
7. Monitor logs regularly

### Switching Safely

1. Always backup current .env before switching
2. Review configuration after switching
3. Test after switching environments
4. Keep both configurations up to date

## Troubleshooting

### Configuration Not Switching

- Ensure you're copying the correct file
- Check that .env file exists and has correct content
- Restart services after switching

### Port Conflicts

- Localhost: Change port in .env or runserver command
- VPS: Check if port 81 is available, adjust nginx config if needed

### Database Connection Issues

- Localhost: Check SQLite file permissions or PostgreSQL connection
- VPS: Verify Docker database container is running

### CORS Errors

- Ensure CORS_ALLOWED_ORIGINS includes your frontend URL
- Check both backend and frontend .env files
- Restart services after changes

## File Structure

```
sims/
├── .env.localhost          # Localhost backend config template
├── .env.vps                # VPS backend config template
├── .env                    # Active backend config (not in git)
├── docker-compose.yml      # VPS Docker Compose
├── docker-compose.localhost.yml  # Localhost Docker Compose
├── deployment/
│   ├── nginx.conf          # VPS Nginx config
│   ├── nginx.localhost.conf # Localhost Nginx config
│   ├── switch_to_localhost.sh
│   └── switch_to_vps.sh
├── frontend/
│   ├── .env.localhost      # Localhost frontend config
│   ├── .env.vps            # VPS frontend config
│   └── .env.local          # Active frontend config (not in git)
└── scripts/
    └── setup_localhost_windows.ps1
```

## Summary

- **Localhost** = Development, easy setup, SQLite, port 8000
- **VPS** = Production, PostgreSQL, port 81, full Docker stack
- **Switching** = Copy appropriate .env files and restart services
- **Best Practice** = Develop on localhost, deploy to VPS

For detailed setup instructions:
- Localhost: See [LOCALHOST_DEPLOYMENT_GUIDE.md](LOCALHOST_DEPLOYMENT_GUIDE.md)
- VPS (Primary): See [VPS_DEPLOYMENT_GUIDE_139.162.9.224.md](VPS_DEPLOYMENT_GUIDE_139.162.9.224.md)
- VPS (Secondary): See [deployment/DEPLOYMENT_INSTRUCTIONS_172.237.95.120.md](deployment/DEPLOYMENT_INSTRUCTIONS_172.237.95.120.md)

