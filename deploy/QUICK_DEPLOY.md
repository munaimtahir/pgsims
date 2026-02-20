# Quick Deployment Guide - Docker Compose
## Server: 139.162.9.224:81

### Prerequisites
- SSH access to 139.162.9.224
- Sudo privileges

### One-Command Deployment

```bash
# SSH into server
ssh user@139.162.9.224

# Clone and deploy
sudo mkdir -p /opt && \
sudo git clone https://github.com/munaimtahir/sims.git /opt/sims_project && \
sudo chown -R $USER:$USER /opt/sims_project && \
cd /opt/sims_project/deployment && \
./deploy_docker_compose.sh && \
./create_superuser.sh
```

### What the Script Does

1. ✅ Verifies Docker and Docker Compose installation
2. ✅ Creates .env file with secure credentials
3. ✅ Configures firewall (port 81)
4. ✅ Builds Docker images
5. ✅ Starts all services (PostgreSQL, Redis, Django, Celery, Nginx)
6. ✅ Runs database migrations
7. ✅ Verifies deployment

### Access Your Application

- **Homepage:** http://139.162.9.224:81/
- **Admin:** http://139.162.9.224:81/admin/
- **Health:** http://139.162.9.224:81/healthz/

### Useful Commands

```bash
# View logs
cd /opt/sims_project
docker compose logs -f

# Restart services
docker compose restart

# Stop services
docker compose down

# Check status
docker compose ps

# Verify deployment
cd deployment
./verify_deployment.sh
```

### Troubleshooting

If something goes wrong:

1. Check logs: `docker compose logs -f`
2. Run verification: `./deployment/verify_deployment.sh`
3. Check container status: `docker compose ps`

For detailed instructions, see: `deployment/DOCKER_DEPLOYMENT_GUIDE.md`
