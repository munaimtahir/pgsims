# SIMS Deployment Instructions for VPS (172.237.95.120:81)

## Overview
This guide provides step-by-step instructions to deploy the SIMS application on your VPS at `172.237.95.120` on port `81`.

## Prerequisites
- SSH access to the VPS server (172.237.95.120)
- Sudo/root access on the VPS
- Git installed on the VPS (or ability to transfer files via SCP)
- Docker and Docker Compose installed (recommended) OR Python 3.x with virtual environment

## Quick Deployment (Docker Compose - Recommended)

The easiest way to deploy is using the automated Docker Compose script:

```bash
# 1. SSH into your VPS
ssh user@172.237.95.120

# 2. Clone the repository
cd /opt
sudo git clone https://github.com/munaimtahir/sims.git sims_project
sudo chown -R $USER:$USER sims_project
cd sims_project

# 3. Run the automated deployment script
chmod +x deployment/deploy_server_172.237.95.120.sh
./deployment/deploy_server_172.237.95.120.sh
```

The script will:
- Verify Docker and Docker Compose installation
- Set up environment variables
- Configure firewall
- Build and start all containers
- Run database migrations
- Verify deployment

## Manual Deployment Steps

### Step 1: Prepare the Server

1. **SSH into your VPS:**
   ```bash
   ssh user@172.237.95.120
   ```

2. **Update system packages:**
   ```bash
   sudo apt update
   sudo apt upgrade -y
   ```

3. **Install required packages:**
   ```bash
   sudo apt install -y python3 python3-pip python3-dev build-essential nginx git
   ```

### Step 2: Transfer Project Files

**Option A: Using Git (Recommended)**
```bash
cd /opt
sudo git clone https://github.com/munaimtahir/sims.git sims_project
cd sims_project
sudo chown -R $USER:$USER sims_project
```

**Option B: Using SCP (from your local machine)**
```bash
# From your local machine:
scp -r /path/to/sims user@172.237.95.120:/opt/sims_project
```

### Step 3: Set Up Project Directory

```bash
cd /opt/sims_project
sudo mkdir -p static staticfiles media logs backups
sudo chown -R $USER:$USER /opt/sims_project
```

### Step 4: Configure Environment Variables

Create a `.env` file or set environment variables:

```bash
cd /opt/sims_project
cat > .env << EOF
SECRET_KEY=$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
DEBUG=False
ALLOWED_HOSTS=172.237.95.120,localhost,127.0.0.1
DJANGO_SETTINGS_MODULE=sims_project.settings
EOF
```

Or export them directly:
```bash
export SECRET_KEY="your-secret-key-here"
export DEBUG="False"
export ALLOWED_HOSTS="172.237.95.120,localhost,127.0.0.1"
```

### Step 5: Install Python Dependencies

**Option A: Using Virtual Environment (Recommended)**
```bash
cd /opt/sims_project
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn
deactivate
```

**Option B: System-wide Installation**
```bash
cd /opt/sims_project
sudo pip3 install --break-system-packages -r requirements.txt
sudo pip3 install --break-system-packages gunicorn
```

### Step 6: Run Database Migrations

```bash
cd /opt/sims_project
source venv/bin/activate  # If using venv
python manage.py migrate
python manage.py collectstatic --noinput
deactivate  # If using venv
```

### Step 7: Configure Nginx

1. **Copy nginx configuration:**
   ```bash
   sudo cp /opt/sims_project/deployment/nginx_sims.conf /etc/nginx/sites-available/sims
   sudo ln -sf /etc/nginx/sites-available/sims /etc/nginx/sites-enabled/
   sudo rm -f /etc/nginx/sites-enabled/default
   ```

2. **Update nginx config paths if needed:**
   - Ensure paths in `nginx_sims.conf` match your setup
   - Default paths assume `/opt/sims_project/`

3. **Test nginx configuration:**
   ```bash
   sudo nginx -t
   ```

4. **Ensure port 81 is open:**
   ```bash
   sudo ufw allow 81/tcp
   sudo ufw reload
   ```

### Step 8: Configure Systemd Service

1. **Copy service file:**
   ```bash
   sudo cp /opt/sims_project/deployment/sims_no_venv.service /etc/systemd/system/sims.service
   # OR if using venv:
   sudo cp /opt/sims_project/deployment/sims.service /etc/systemd/system/sims.service
   ```

2. **Update service file paths if needed:**
   - Edit `/etc/systemd/system/sims.service` to match your paths
   - Update WorkingDirectory, User, and paths as needed

3. **Reload systemd:**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable sims
   ```

### Step 9: Set File Permissions

```bash
sudo chown -R www-data:www-data /opt/sims_project
sudo chmod -R 755 /opt/sims_project
sudo chmod -R 775 /opt/sims_project/media
sudo chmod -R 775 /opt/sims_project/logs
sudo chmod 664 /opt/sims_project/db.sqlite3  # If using SQLite
```

### Step 10: Start Services

1. **Start SIMS service:**
   ```bash
   sudo systemctl start sims
   sudo systemctl status sims
   ```

2. **Start/restart Nginx:**
   ```bash
   sudo systemctl restart nginx
   sudo systemctl status nginx
   ```

### Step 11: Verify Deployment

1. **Check service status:**
   ```bash
   sudo systemctl status sims
   sudo systemctl status nginx
   ```

2. **Check if socket file exists:**
   ```bash
   ls -la /opt/sims_project/sims.sock
   ```

3. **Test from server:**
   ```bash
   curl http://172.237.95.120:81/
   curl http://localhost:81/
   curl http://172.237.95.120:81/healthz/
   ```

4. **Check logs if issues:**
   ```bash
   sudo journalctl -u sims -f
   sudo tail -f /var/log/nginx/sims_error.log
   ```

### Step 12: Create Admin User

```bash
cd /opt/sims_project
source venv/bin/activate  # If using venv
python manage.py createsuperuser
deactivate  # If using venv
```

## Docker Compose Deployment (Recommended)

For Docker Compose deployment, use the automated script:

```bash
cd /opt/sims_project
chmod +x deployment/deploy_server_172.237.95.120.sh
./deployment/deploy_server_172.237.95.120.sh
```

Or manually:

```bash
cd /opt/sims_project
cp .env.example .env
# Edit .env and set ALLOWED_HOSTS=172.237.95.120,localhost,127.0.0.1
docker compose up -d
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py collectstatic --noinput
```

## Access URLs

After successful deployment, access your application at:

- **Homepage:** http://172.237.95.120:81/
- **Login:** http://172.237.95.120:81/users/login/
- **Admin Panel:** http://172.237.95.120:81/admin/
- **API:** http://172.237.95.120:81/api/
- **Health Check:** http://172.237.95.120:81/healthz/

## Troubleshooting

### Service won't start
```bash
sudo journalctl -u sims -n 50
sudo systemctl status sims
```

### Nginx 502 Bad Gateway
- Check if sims.sock file exists and has correct permissions
- Verify gunicorn is running: `ps aux | grep gunicorn`
- Check nginx error logs: `sudo tail -f /var/log/nginx/sims_error.log`

### Port 81 not accessible
- Check firewall: `sudo ufw status`
- Verify nginx is listening: `sudo ss -tulpn | grep :81`
- Check nginx config: `sudo nginx -t`

### Permission issues
```bash
sudo chown -R www-data:www-data /opt/sims_project
sudo chmod -R 755 /opt/sims_project
```

### Docker containers not starting
```bash
docker compose logs
docker compose ps
docker compose restart
```

## Maintenance Commands

```bash
# Restart services
sudo systemctl restart sims
sudo systemctl restart nginx

# Or for Docker:
docker compose restart

# View logs
sudo journalctl -u sims -f
sudo tail -f /var/log/nginx/sims_access.log

# Or for Docker:
docker compose logs -f web

# Update code (if using git)
cd /opt/sims_project
git pull
source venv/bin/activate  # If using venv
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart sims

# Or for Docker:
docker compose exec web python manage.py migrate
docker compose exec web python manage.py collectstatic --noinput
docker compose restart web
```

## Security Notes

1. **Change SECRET_KEY** - Use a strong, random secret key in production
2. **Set DEBUG=False** - Already configured in deployment scripts
3. **Configure SSL** - Consider setting up SSL/TLS certificates for HTTPS
4. **Firewall** - Ensure only necessary ports are open
5. **Regular Updates** - Keep system and dependencies updated

## Next Steps

1. Set up SSL certificate (Let's Encrypt recommended)
2. Configure automated backups
3. Set up monitoring and logging
4. Configure email settings for password resets
5. Review and harden security settings

