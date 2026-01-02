# Docker Compose Deployment Guide for SIMS
## Server: 139.162.9.224:81

This guide provides step-by-step instructions for deploying the SIMS application using Docker Compose on server 139.162.9.224.

## Prerequisites

- SSH access to server 139.162.9.224
- Sudo/root access on the server
- Git installed (or ability to transfer files via SCP)

## Quick Start

### Option 1: Automated Deployment (Recommended)

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

3. **Run the deployment script:**
   ```bash
   cd deployment
   ./deploy_docker_compose.sh
   ```

   The script will:
   - Verify Docker and Docker Compose installation
   - Create .env file with secure credentials
   - Configure firewall
   - Build Docker images
   - Start all services
   - Run database migrations
   - Verify deployment

4. **Create a superuser:**
   ```bash
   ./create_superuser.sh
   ```

5. **Verify deployment:**
   ```bash
   ./verify_deployment.sh
   ```

### Option 2: Manual Deployment

If you prefer to deploy manually, follow these steps:

#### Step 1: Prepare Server

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker (if not installed)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose (if not installed)
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Log out and log back in for Docker group to take effect
```

#### Step 2: Clone Repository

```bash
sudo mkdir -p /opt
sudo git clone https://github.com/munaimtahir/sims.git /opt/sims_project
sudo chown -R $USER:$USER /opt/sims_project
cd /opt/sims_project
```

#### Step 3: Create .env File

```bash
# Generate secret key
SECRET_KEY=$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')

# Generate database password
DB_PASSWORD=$(openssl rand -base64 32 | tr -d "=+/" | cut -c1-25)

# Create .env file
cat > .env << EOF
SECRET_KEY=$SECRET_KEY
DEBUG=False
ALLOWED_HOSTS=139.162.9.224,localhost,127.0.0.1

DB_NAME=sims_db
DB_USER=sims_user
DB_PASSWORD=$DB_PASSWORD
DB_HOST=db
DB_PORT=5432

REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/1
CELERY_RESULT_BACKEND=redis://redis:6379/1

EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EOF

echo "DB_PASSWORD: $DB_PASSWORD"  # Save this securely!
```

#### Step 4: Configure Firewall

```bash
# For UFW
sudo ufw allow 81/tcp
sudo ufw reload

# OR for firewalld
sudo firewall-cmd --permanent --add-port=81/tcp
sudo firewall-cmd --reload
```

#### Step 5: Build and Start Services

```bash
# Build images
docker compose build

# Start services
docker compose up -d

# Check status
docker compose ps
```

#### Step 6: Run Migrations

```bash
# Wait for database to be ready (about 10 seconds)
sleep 10

# Run migrations
docker compose exec web python manage.py migrate
```

#### Step 7: Create Superuser

```bash
docker compose exec web python manage.py createsuperuser
```

#### Step 8: Verify Deployment

```bash
# Check health endpoint
curl http://139.162.9.224:81/healthz/

# Check homepage
curl http://139.162.9.224:81/

# Or use the verification script
./deployment/verify_deployment.sh
```

## Access URLs

After successful deployment:

- **Homepage:** http://139.162.9.224:81/
- **Login:** http://139.162.9.224:81/users/login/
- **Admin Panel:** http://139.162.9.224:81/admin/
- **Health Check:** http://139.162.9.224:81/healthz/

## Service Management

### View Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f web
docker compose logs -f nginx
docker compose logs -f db
docker compose logs -f redis
docker compose logs -f worker
docker compose logs -f beat
```

### Restart Services

```bash
# All services
docker compose restart

# Specific service
docker compose restart web
docker compose restart nginx
```

### Stop Services

```bash
docker compose down
```

### Start Services

```bash
docker compose up -d
```

### Check Status

```bash
docker compose ps
```

## Database Management

### Backup Database

```bash
docker compose exec db pg_dump -U sims_user sims_db > backup_$(date +%Y%m%d_%H%M%S).sql
```

### Restore Database

```bash
docker compose exec -T db psql -U sims_user sims_db < backup_file.sql
```

### Access Database Shell

```bash
docker compose exec db psql -U sims_user sims_db
```

## Troubleshooting

### Containers Not Starting

1. Check logs:
   ```bash
   docker compose logs
   ```

2. Verify .env file exists and has required variables:
   ```bash
   cat .env
   ```

3. Check Docker resources:
   ```bash
   docker system df
   docker stats
   ```

### Port 81 Not Accessible

1. Check if port is listening:
   ```bash
   sudo ss -tulpn | grep 81
   ```

2. Check firewall:
   ```bash
   sudo ufw status
   # or
   sudo firewall-cmd --list-ports
   ```

3. Check nginx container:
   ```bash
   docker compose logs nginx
   ```

### Database Connection Issues

1. Check database container:
   ```bash
   docker compose ps db
   docker compose logs db
   ```

2. Test connection:
   ```bash
   docker compose exec db pg_isready -U sims_user
   ```

### Static Files Not Loading

1. Check static files volume:
   ```bash
   docker compose exec web ls -la /app/staticfiles
   ```

2. Recollect static files:
   ```bash
   docker compose exec web python manage.py collectstatic --noinput
   ```

### Health Endpoint Not Responding

1. Check web container:
   ```bash
   docker compose ps web
   docker compose logs web
   ```

2. Test from inside container:
   ```bash
   docker compose exec web curl http://localhost:8000/healthz/
   ```

## Updating the Application

1. **Pull latest code:**
   ```bash
   cd /opt/sims_project
   git pull
   ```

2. **Rebuild and restart:**
   ```bash
   docker compose down
   docker compose build
   docker compose up -d
   docker compose exec web python manage.py migrate
   ```

## Security Checklist

- [x] SECRET_KEY is strong and random
- [x] DEBUG=False in production
- [x] ALLOWED_HOSTS includes server IP
- [x] Strong database password set
- [x] Firewall configured (port 81 open)
- [ ] SSL/TLS certificates configured (recommended for production)
- [ ] Regular backups configured
- [ ] Monitoring and logging set up

## Additional Resources

- Main README: `/opt/sims_project/README.md`
- Deployment Checklist: `/opt/sims_project/DEPLOYMENT_CHECKLIST.md`
- Nginx Configuration: `/opt/sims_project/deployment/nginx.conf`
- Docker Compose File: `/opt/sims_project/docker-compose.yml`

## Support

For issues or questions:
- Check logs: `docker compose logs -f`
- Run verification: `./deployment/verify_deployment.sh`
- Review documentation in `/opt/sims_project/docs/`
