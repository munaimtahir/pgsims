# 🚀 Quick Reference: VPS Configuration for 172.237.95.120:81

## IP Address Configuration Summary

**Target IP:** `172.237.95.120`  
**Port:** `81`  
**Full URL:** `http://172.237.95.120:81/`

## ✅ Configuration Files Updated

### 1. Django Settings (`sims_project/settings.py`)
- ✅ `ALLOWED_HOSTS` includes `172.237.95.120`
- ✅ `CORS_ALLOWED_ORIGINS` includes `http://172.237.95.120:81`
- ✅ `INTERNAL_IPS` includes `172.237.95.120`

### 2. Docker Compose (`docker-compose.yml`)
- ✅ Nginx port mapping: `81:81`
- ✅ `ALLOWED_HOSTS` environment variable includes `172.237.95.120`

### 3. Nginx Configuration
- ✅ `deployment/nginx.conf` - Server name updated
- ✅ `deployment/nginx_sims.conf` - Server name and port updated

### 4. Environment Files
- ✅ `.env.example` - Updated with new IP
- ✅ `deployment/server_config_172.237.95.120.env` - Server-specific config

### 5. Frontend Configuration
- ✅ `frontend/lib/api/client.ts` - Auto-detects VPS IP

## 🔧 Quick Setup Commands

### Docker Compose Deployment
```bash
# 1. Copy environment file
cp .env.example .env

# 2. Edit .env and set:
ALLOWED_HOSTS=172.237.95.120,localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://172.237.95.120:81

# 3. Start services
docker-compose up -d

# 4. Run migrations
docker-compose exec web python manage.py migrate

# 5. Create superuser
docker-compose exec web python manage.py createsuperuser

# 6. Collect static files
docker-compose exec web python manage.py collectstatic --noinput
```

### Automated Deployment Script
```bash
# Use the automated deployment script
cd /opt/sims_project
./deployment/deploy_server_172.237.95.120.sh
```

### Traditional Deployment
```bash
# 1. Set environment variables
export ALLOWED_HOSTS="172.237.95.120,localhost,127.0.0.1"
export DEBUG="False"

# 2. Run migrations
python manage.py migrate
python manage.py collectstatic --noinput

# 3. Configure Nginx for port 81
sudo cp deployment/nginx_sims.conf /etc/nginx/sites-available/sims
sudo nano /etc/nginx/sites-available/sims  # Change listen to 81
sudo ln -s /etc/nginx/sites-available/sims /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

# 4. Configure firewall
sudo ufw allow 81/tcp
```

## 🌐 Access Points

| Service | URL |
|---------|-----|
| Homepage | `http://172.237.95.120:81/` |
| Login | `http://172.237.95.120:81/users/login/` |
| Admin | `http://172.237.95.120:81/admin/` |
| API | `http://172.237.95.120:81/api/` |
| Health | `http://172.237.95.120:81/healthz/` |

## 🔍 Verification

```bash
# Test health endpoint
curl http://172.237.95.120:81/healthz/

# Check if port is listening
sudo netstat -tlnp | grep 81

# Check Docker containers
docker-compose ps

# Check Nginx status
sudo systemctl status nginx

# View logs
docker-compose logs -f web
```

## 📝 Important Notes

1. **Port 81**: Ensure firewall allows port 81
2. **ALLOWED_HOSTS**: Must include `172.237.95.120`
3. **CORS**: Frontend must use `http://172.237.95.120:81` for API calls
4. **Static Files**: Run `collectstatic` after deployment
5. **Database**: Ensure database is accessible and migrations are applied

## 🐛 Common Issues

### Issue: "DisallowedHost" error
**Solution:** Verify `ALLOWED_HOSTS` includes `172.237.95.120`

### Issue: Port 81 not accessible
**Solution:** Check firewall rules and ensure port is open

### Issue: Static files not loading
**Solution:** Run `python manage.py collectstatic --noinput`

### Issue: CORS errors
**Solution:** Verify `CORS_ALLOWED_ORIGINS` includes `http://172.237.95.120:81`

---

For detailed deployment instructions, see `deployment/DEPLOYMENT_INSTRUCTIONS_172.237.95.120.md`

