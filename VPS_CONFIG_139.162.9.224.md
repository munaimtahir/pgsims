# 🚀 Quick Reference: VPS Configuration for 139.162.9.224:81

## IP Address Configuration Summary

**Target IP:** `139.162.9.224`  
**Port:** `81`  
**Full URL:** `http://139.162.9.224:81/`

## ✅ Configuration Files Updated

### 1. Django Settings (`sims_project/settings.py`)
- ✅ `ALLOWED_HOSTS` includes `139.162.9.224`
- ✅ `CORS_ALLOWED_ORIGINS` includes `http://139.162.9.224:81`
- ✅ `INTERNAL_IPS` includes `139.162.9.224`

### 2. Docker Compose (`docker-compose.yml`)
- ✅ Nginx port mapping: `81:80`
- ✅ `ALLOWED_HOSTS` environment variable includes `139.162.9.224`

### 3. Nginx Configuration
- ✅ `deployment/nginx.conf` - Server name updated
- ✅ `deployment/nginx_sims.conf` - Server name and port updated

### 4. Environment Files
- ✅ `.env.example` - Updated with new IP
- ✅ `deployment/server_config.env` - Updated with new IP

### 5. Frontend Configuration
- ✅ `frontend/lib/api/client.ts` - Auto-detects VPS IP

## 🔧 Quick Setup Commands

### Docker Compose Deployment
```bash
# 1. Copy environment file
cp .env.example .env

# 2. Edit .env and set:
ALLOWED_HOSTS=139.162.9.224,localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://139.162.9.224:81

# 3. Start services
docker-compose up -d

# 4. Run migrations
docker-compose exec web python manage.py migrate

# 5. Create superuser
docker-compose exec web python manage.py createsuperuser

# 6. Collect static files
docker-compose exec web python manage.py collectstatic --noinput
```

### Traditional Deployment
```bash
# 1. Set environment variables
export ALLOWED_HOSTS="139.162.9.224,localhost,127.0.0.1"
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
| Homepage | `http://139.162.9.224:81/` |
| Login | `http://139.162.9.224:81/users/login/` |
| Admin | `http://139.162.9.224:81/admin/` |
| API | `http://139.162.9.224:81/api/` |
| Health | `http://139.162.9.224:81/healthz/` |

## 🔍 Verification

```bash
# Test health endpoint
curl http://139.162.9.224:81/healthz/

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
2. **ALLOWED_HOSTS**: Must include `139.162.9.224`
3. **CORS**: Frontend must use `http://139.162.9.224:81` for API calls
4. **Static Files**: Run `collectstatic` after deployment
5. **Database**: Ensure database is accessible and migrations are applied

## 🐛 Common Issues

### Issue: "DisallowedHost" error
**Solution:** Verify `ALLOWED_HOSTS` includes `139.162.9.224`

### Issue: Port 81 not accessible
**Solution:** Check firewall rules and ensure port is open

### Issue: Static files not loading
**Solution:** Run `python manage.py collectstatic --noinput`

### Issue: CORS errors
**Solution:** Verify `CORS_ALLOWED_ORIGINS` includes `http://139.162.9.224:81`

---

For detailed deployment instructions, see `VPS_DEPLOYMENT_GUIDE_139.162.9.224.md`
