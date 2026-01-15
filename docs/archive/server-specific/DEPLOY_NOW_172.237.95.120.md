# Deploy to 172.237.95.120 - Execution Instructions

## Quick Deployment

All configuration files have been updated. To deploy to server 172.237.95.120, follow these steps:

### Option 1: Automated Deployment (Recommended)

1. **SSH into the server:**
   ```bash
   ssh user@172.237.95.120
   # Replace 'user' with your actual username
   ```

2. **Clone or upload the repository:**
   ```bash
   cd /opt
   sudo git clone https://github.com/munaimtahir/sims.git sims_project
   sudo chown -R $USER:$USER sims_project
   cd sims_project
   ```

3. **Run the automated deployment script:**
   ```bash
   chmod +x deployment/deploy_server_172.237.95.120.sh
   ./deployment/deploy_server_172.237.95.120.sh
   ```

The script will handle:
- Docker and Docker Compose installation (if needed)
- Environment variable setup
- Firewall configuration
- Container building and startup
- Database migrations
- Static file collection
- Deployment verification

### Option 2: Manual Deployment

If you prefer manual deployment, follow the detailed guide:
- See: `deployment/DEPLOYMENT_INSTRUCTIONS_172.237.95.120.md`

## What Has Been Configured

✅ **Django Settings** - Updated to include `172.237.95.120` in ALLOWED_HOSTS
✅ **Docker Compose** - Updated environment variables
✅ **Nginx Configuration** - Updated to accept both server IPs
✅ **Frontend API Client** - Auto-detects new server IP
✅ **Deployment Script** - Created and ready to use
✅ **Documentation** - Complete guides available

## Verification After Deployment

Once deployed, verify the application is accessible:

```bash
# Test health endpoint
curl http://172.237.95.120:81/healthz/

# Test homepage
curl http://172.237.95.120:81/

# Check containers
docker compose ps
```

## Access URLs

After successful deployment:
- **Homepage:** http://172.237.95.120:81/
- **Login:** http://172.237.95.120:81/users/login/
- **Admin:** http://172.237.95.120:81/admin/
- **API:** http://172.237.95.120:81/api/
- **Health:** http://172.237.95.120:81/healthz/

## Troubleshooting

If you encounter issues:
1. Check the deployment logs: `docker compose logs -f`
2. Verify firewall: `sudo ufw status`
3. Check container status: `docker compose ps`
4. Review the detailed guide: `deployment/DEPLOYMENT_INSTRUCTIONS_172.237.95.120.md`

