# ✅ VPS Deployment Checklist

## Configuration Status: ✅ COMPLETE

All configuration files have been updated for VPS deployments:
- **Primary VPS:** `http://139.162.9.224:81/`
- **Secondary VPS:** `http://172.237.95.120:81/`

---

# Primary VPS Deployment Checklist - 139.162.9.224:81

## 📋 Pre-Deployment Verification

### ✅ Configuration Files Updated
- [x] `sims_project/settings.py` - ALLOWED_HOSTS, CORS, INTERNAL_IPS
- [x] `docker-compose.yml` - Port 81 mapping, environment variables
- [x] `deployment/nginx.conf` - Server name updated
- [x] `deployment/nginx_sims.conf` - Server name and port updated
- [x] `.env.example` - IP address configuration
- [x] `deployment/server_config.env` - Server IP updated
- [x] `frontend/lib/api/client.ts` - Auto-detection for VPS IP

### ✅ Documentation Created
- [x] `VPS_DEPLOYMENT_GUIDE_139.162.9.224.md` - Complete deployment guide
- [x] `VPS_CONFIG_139.162.9.224.md` - Quick reference guide
- [x] `DEPLOYMENT_CHECKLIST.md` - This checklist

## 🚀 Deployment Steps

### Step 1: Prepare VPS
```bash
# SSH into VPS
ssh user@139.162.9.224

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker (if not installed)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose (if not installed)
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### Step 2: Upload Project
```bash
# From local machine
scp -r . user@139.162.9.224:/opt/sims_project/

# Or use git
ssh user@139.162.9.224
cd /opt
git clone <your-repo-url> sims_project
cd sims_project
```

### Step 3: Configure Environment
```bash
cd /opt/sims_project

# Copy environment template
cp .env.example .env

# Edit environment file
nano .env
```

**Required .env settings:**
```bash
DEBUG=False
SECRET_KEY=<generate-strong-secret-key>
ALLOWED_HOSTS=139.162.9.224,localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://139.162.9.224:81

# Database (Docker will handle this)
DB_NAME=sims_db
DB_USER=sims_user
DB_PASSWORD=<secure-password>

# Redis (Docker will handle this)
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/1
CELERY_RESULT_BACKEND=redis://redis:6379/1
```

**Generate Secret Key:**
```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 4: Configure Firewall
```bash
# Allow port 81
sudo ufw allow 81/tcp
sudo ufw reload

# Or for firewalld
sudo firewall-cmd --permanent --add-port=81/tcp
sudo firewall-cmd --reload
```

### Step 5: Deploy with Docker Compose
```bash
cd /opt/sims_project

# Build and start containers
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### Step 6: Initialize Database
```bash
# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput
```

### Step 7: Verify Deployment
```bash
# Test health endpoint
curl http://139.162.9.224:81/healthz/

# Test homepage
curl http://139.162.9.224:81/

# Check container logs
docker-compose logs web
docker-compose logs nginx
```

## 🌐 Access URLs

After successful deployment, access:

- **Homepage:** http://139.162.9.224:81/
- **Login:** http://139.162.9.224:81/users/login/
- **Admin:** http://139.162.9.224:81/admin/
- **API:** http://139.162.9.224:81/api/
- **Health:** http://139.162.9.224:81/healthz/

## 🔍 Troubleshooting

### Check Container Status
```bash
docker-compose ps
docker-compose logs -f web
docker-compose logs -f nginx
```

### Verify Configuration
```bash
# Check Django settings
docker-compose exec web python manage.py shell
>>> from django.conf import settings
>>> print(settings.ALLOWED_HOSTS)
>>> print(settings.CORS_ALLOWED_ORIGINS)
```

### Test Database Connection
```bash
docker-compose exec web python manage.py dbshell
```

### Check Port Accessibility
```bash
# From VPS
sudo netstat -tlnp | grep 81

# From external machine
curl -v http://139.162.9.224:81/healthz/
```

## 📊 Post-Deployment Monitoring

### View Logs
```bash
# Application logs
docker-compose logs -f web

# Nginx logs
docker-compose logs -f nginx

# Database logs
docker-compose logs -f db
```

### Monitor Resources
```bash
# Container stats
docker stats

# Disk usage
df -h
docker system df
```

## 🔄 Maintenance Commands

### Update Application
```bash
cd /opt/sims_project
git pull
docker-compose down
docker-compose build
docker-compose up -d
docker-compose exec web python manage.py migrate
```

### Backup Database
```bash
docker-compose exec db pg_dump -U sims_user sims_db > backup_$(date +%Y%m%d_%H%M%S).sql
```

### Restart Services
```bash
docker-compose restart
# Or restart specific service
docker-compose restart web
docker-compose restart nginx
```

## ✅ Final Verification Checklist

- [ ] All containers running (`docker-compose ps`)
- [ ] Health endpoint responding (`curl http://139.162.9.224:81/healthz/`)
- [ ] Homepage accessible (`curl http://139.162.9.224:81/`)
- [ ] Login page loads correctly
- [ ] Admin panel accessible
- [ ] Static files loading
- [ ] No errors in logs
- [ ] Database migrations applied
- [ ] Superuser created
- [ ] Firewall configured correctly

## 🎉 Deployment Complete!

Once all checks pass, your SIMS application is successfully deployed at:
**http://139.162.9.224:81/**

---

**Need Help?** Refer to `VPS_DEPLOYMENT_GUIDE_139.162.9.224.md` for detailed instructions.

---

# Secondary VPS Deployment Checklist - 172.237.95.120:81

## Configuration Status: ✅ COMPLETE

All configuration files have been updated for VPS deployment at `http://172.237.95.120:81/`

## 📋 Pre-Deployment Verification

### ✅ Configuration Files Updated
- [x] `sims_project/settings.py` - ALLOWED_HOSTS includes `172.237.95.120`
- [x] `docker-compose.yml` - Port 81 mapping, environment variables
- [x] `deployment/nginx.conf` - Server name updated to include `172.237.95.120`
- [x] `deployment/nginx_sims.conf` - Server name and port updated
- [x] `deployment/server_config_172.237.95.120.env` - Server-specific config created
- [x] `frontend/lib/api/client.ts` - Auto-detection for VPS IP `172.237.95.120`

### ✅ Documentation Created
- [x] `deployment/DEPLOYMENT_INSTRUCTIONS_172.237.95.120.md` - Complete deployment guide
- [x] `VPS_CONFIG_172.237.95.120.md` - Quick reference guide
- [x] `deployment/deploy_server_172.237.95.120.sh` - Automated deployment script

## 🚀 Deployment Steps

### Step 1: Prepare VPS
```bash
# SSH into VPS
ssh user@172.237.95.120

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker (if not installed)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose (if not installed)
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### Step 2: Upload Project
```bash
# From local machine
scp -r . user@172.237.95.120:/opt/sims_project/

# Or use git
ssh user@172.237.95.120
cd /opt
git clone <your-repo-url> sims_project
cd sims_project
```

### Step 3: Configure Environment
```bash
cd /opt/sims_project

# Copy environment template
cp .env.example .env

# Edit environment file
nano .env
```

**Required .env settings:**
```bash
DEBUG=False
SECRET_KEY=<generate-strong-secret-key>
ALLOWED_HOSTS=172.237.95.120,localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://172.237.95.120:81

# Database (Docker will handle this)
DB_NAME=sims_db
DB_USER=sims_user
DB_PASSWORD=<secure-password>

# Redis (Docker will handle this)
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/1
CELERY_RESULT_BACKEND=redis://redis:6379/1
```

**Generate Secret Key:**
```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 4: Configure Firewall
```bash
# Allow port 81
sudo ufw allow 81/tcp
sudo ufw reload

# Or for firewalld
sudo firewall-cmd --permanent --add-port=81/tcp
sudo firewall-cmd --reload
```

### Step 5: Deploy with Docker Compose (Automated)
```bash
cd /opt/sims_project

# Use automated deployment script
chmod +x deployment/deploy_server_172.237.95.120.sh
./deployment/deploy_server_172.237.95.120.sh
```

### Step 5 (Alternative): Manual Deployment
```bash
cd /opt/sims_project

# Build and start containers
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### Step 6: Initialize Database
```bash
# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput
```

### Step 7: Verify Deployment
```bash
# Test health endpoint
curl http://172.237.95.120:81/healthz/

# Test homepage
curl http://172.237.95.120:81/

# Check container logs
docker-compose logs web
docker-compose logs nginx
```

## 🌐 Access URLs

After successful deployment, access:

- **Homepage:** http://172.237.95.120:81/
- **Login:** http://172.237.95.120:81/users/login/
- **Admin:** http://172.237.95.120:81/admin/
- **API:** http://172.237.95.120:81/api/
- **Health:** http://172.237.95.120:81/healthz/

## 🔍 Troubleshooting

### Check Container Status
```bash
docker-compose ps
docker-compose logs -f web
docker-compose logs -f nginx
```

### Verify Configuration
```bash
# Check Django settings
docker-compose exec web python manage.py shell
>>> from django.conf import settings
>>> print(settings.ALLOWED_HOSTS)
>>> print(settings.CORS_ALLOWED_ORIGINS)
```

### Test Database Connection
```bash
docker-compose exec web python manage.py dbshell
```

### Check Port Accessibility
```bash
# From VPS
sudo netstat -tlnp | grep 81

# From external machine
curl -v http://172.237.95.120:81/healthz/
```

## 📊 Post-Deployment Monitoring

### View Logs
```bash
# Application logs
docker-compose logs -f web

# Nginx logs
docker-compose logs -f nginx

# Database logs
docker-compose logs -f db
```

### Monitor Resources
```bash
# Container stats
docker stats

# Disk usage
df -h
docker system df
```

## 🔄 Maintenance Commands

### Update Application
```bash
cd /opt/sims_project
git pull
docker-compose down
docker-compose build
docker-compose up -d
docker-compose exec web python manage.py migrate
```

### Backup Database
```bash
docker-compose exec db pg_dump -U sims_user sims_db > backup_$(date +%Y%m%d_%H%M%S).sql
```

### Restart Services
```bash
docker-compose restart
# Or restart specific service
docker-compose restart web
docker-compose restart nginx
```

## ✅ Final Verification Checklist

- [ ] All containers running (`docker-compose ps`)
- [ ] Health endpoint responding (`curl http://172.237.95.120:81/healthz/`)
- [ ] Homepage accessible (`curl http://172.237.95.120:81/`)
- [ ] Login page loads correctly
- [ ] Admin panel accessible
- [ ] Static files loading
- [ ] No errors in logs
- [ ] Database migrations applied
- [ ] Superuser created
- [ ] Firewall configured correctly

## 🎉 Deployment Complete!

Once all checks pass, your SIMS application is successfully deployed at:
**http://172.237.95.120:81/**

---

**Need Help?** Refer to `deployment/DEPLOYMENT_INSTRUCTIONS_172.237.95.120.md` for detailed instructions.
