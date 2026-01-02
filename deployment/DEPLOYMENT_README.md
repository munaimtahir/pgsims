# SIMS Docker Compose Deployment

This directory contains all scripts and configuration files needed to deploy the SIMS application on server **139.162.9.224** using Docker Compose.

## Quick Start

1. **SSH into the server:**
   ```bash
   ssh user@139.162.9.224
   ```

2. **Clone the repository:**
   ```bash
   sudo mkdir -p /opt
   sudo git clone https://github.com/munaimtahir/sims.git /opt/sims_project
   sudo chown -R $USER:$USER /opt/sims_project
   cd /opt/sims_project
   ```

3. **Run the automated deployment:**
   ```bash
   cd deployment
   ./deploy_docker_compose.sh
   ```

4. **Create superuser:**
   ```bash
   ./create_superuser.sh
   ```

5. **Verify deployment:**
   ```bash
   ./verify_deployment.sh
   ```

## Files in This Directory

### Deployment Scripts

- **`deploy_docker_compose.sh`** - Main automated deployment script
  - Verifies Docker installation
  - Creates .env file with secure credentials
  - Configures firewall
  - Builds and starts all containers
  - Runs migrations
  - Verifies deployment

- **`create_superuser.sh`** - Helper script to create Django admin user
  - Interactive script to create superuser in Docker container

- **`verify_deployment.sh`** - Comprehensive deployment verification
  - Checks all containers
  - Tests endpoints
  - Verifies database and Redis connections
  - Displays status summary

### Configuration Files

- **`nginx.conf`** - Nginx reverse proxy configuration
  - Configured for port 81
  - Server name: 139.162.9.224
  - Static and media file serving
  - Health check endpoints

- **`nginx_sims.conf`** - Alternative nginx config for traditional deployment
  - Used with systemd service (non-Docker deployment)

- **`gunicorn.conf.py`** - Gunicorn configuration
  - Used for traditional deployment

- **`server_config.env`** - Example server configuration
  - Template for environment variables

### Service Files

- **`sims.service`** - Systemd service file (traditional deployment)
- **`sims_no_venv.service`** - Systemd service without virtual environment

### Documentation

- **`DOCKER_DEPLOYMENT_GUIDE.md`** - Complete Docker Compose deployment guide
- **`QUICK_DEPLOY.md`** - Quick reference for deployment
- **`DEPLOYMENT_INSTRUCTIONS_139.162.9.224.md`** - Traditional deployment guide
- **`DEPLOYMENT_SUMMARY.md`** - Configuration summary

## Deployment Methods

### Method 1: Docker Compose (Recommended)

**Use:** `deploy_docker_compose.sh`

**Advantages:**
- Isolated containers
- Easy to manage
- Consistent environment
- Built-in health checks
- Easy scaling

**Services:**
- PostgreSQL database
- Redis cache/broker
- Django web application
- Celery worker
- Celery beat scheduler
- Nginx reverse proxy

### Method 2: Traditional Deployment

**Use:** `deploy_server.sh` or `DEPLOY_NOW.sh`

**Advantages:**
- Direct server installation
- No Docker overhead
- Full server control

**Requirements:**
- Python 3.11+
- PostgreSQL or SQLite
- Nginx
- Systemd

## Access URLs

After deployment:

- **Homepage:** http://139.162.9.224:81/
- **Login:** http://139.162.9.224:81/users/login/
- **Admin Panel:** http://139.162.9.224:81/admin/
- **Health Check:** http://139.162.9.224:81/healthz/

## Common Commands

### Docker Compose

```bash
# View logs
docker compose logs -f [service_name]

# Restart services
docker compose restart

# Stop services
docker compose down

# Start services
docker compose up -d

# Check status
docker compose ps

# Execute command in container
docker compose exec web python manage.py [command]
```

### Database Management

```bash
# Backup
docker compose exec db pg_dump -U sims_user sims_db > backup.sql

# Restore
docker compose exec -T db psql -U sims_user sims_db < backup.sql

# Access database shell
docker compose exec db psql -U sims_user sims_db
```

## Troubleshooting

### Containers Not Starting

```bash
# Check logs
docker compose logs

# Check specific service
docker compose logs web
docker compose logs nginx
docker compose logs db
```

### Port Not Accessible

```bash
# Check if port is listening
sudo ss -tulpn | grep 81

# Check firewall
sudo ufw status
```

### Database Issues

```bash
# Test connection
docker compose exec db pg_isready -U sims_user

# Check database logs
docker compose logs db
```

### Static Files Not Loading

```bash
# Recollect static files
docker compose exec web python manage.py collectstatic --noinput
```

## Security Checklist

- [x] SECRET_KEY is strong and random (auto-generated)
- [x] DEBUG=False in production
- [x] ALLOWED_HOSTS includes server IP
- [x] Strong database password (auto-generated)
- [x] Firewall configured (port 81)
- [ ] SSL/TLS certificates (recommended for production)
- [ ] Regular backups configured
- [ ] Monitoring set up

## Support

For issues:
1. Check logs: `docker compose logs -f`
2. Run verification: `./verify_deployment.sh`
3. Review documentation in parent directory

## Next Steps

After successful deployment:

1. Create superuser account
2. Configure email settings (if needed)
3. Set up SSL certificates (recommended)
4. Configure automated backups
5. Set up monitoring and logging
