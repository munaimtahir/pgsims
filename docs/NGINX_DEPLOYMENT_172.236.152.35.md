# 🌐 SIMS Nginx Server Configuration - 172.236.152.35

## ✅ Nginx Configuration Complete

### Architecture Updated for Nginx
- **Web Server**: Nginx (instead of Apache)
- **WSGI Server**: Gunicorn
- **Process Management**: Systemd service
- **Server IP**: 172.236.152.35 ✅

## 📦 Files Created for Nginx Deployment

| File | Purpose | Description |
|------|---------|-------------|
| `nginx_sims.conf` | Nginx virtual host | Server configuration for 172.236.152.35 |
| `gunicorn.conf.py` | Gunicorn settings | WSGI server configuration |
| `sims.service` | Systemd service | Process management and auto-start |
| `deploy_server.sh` | Deployment script | Automated Nginx setup |
| `requirements.txt` | Dependencies | Added Gunicorn for Nginx |

## 🚀 Nginx Deployment Commands

### 1. Upload Files to Server
```bash
scp -r . user@172.236.152.35:/var/www/sims_project/
```

### 2. SSH and Run Automated Deployment
```bash
ssh user@172.236.152.35
cd /var/www/sims_project
chmod +x deploy_server.sh
./deploy_server.sh
```

### 3. Manual Configuration (if needed)
```bash
# Install Nginx and dependencies
sudo apt update
sudo apt install -y nginx python3-venv

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure Nginx
sudo cp nginx_sims.conf /etc/nginx/sites-available/sims
sudo ln -s /etc/nginx/sites-available/sims /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Set up systemd service
sudo cp sims.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable sims
sudo systemctl start sims

# Test and restart Nginx
sudo nginx -t
sudo systemctl restart nginx
```

## 🌐 Access Points

After deployment on Nginx server 172.236.152.35:

| Service | URL | Status |
|---------|-----|--------|
| **Homepage** | `http://172.236.152.35/` | ✅ Ready |
| **Login** | `http://172.236.152.35/users/login/` | ✅ Ready |
| **Admin Panel** | `http://172.236.152.35/admin/` | ✅ Ready |
| **Password Reset** | `http://172.236.152.35/users/password-reset/` | ✅ Ready |

## ⚙️ Nginx Configuration Features

### Performance Optimizations
- ✅ **Gzip Compression**: Enabled for static files
- ✅ **Caching Headers**: 30-day cache for static files, 7-day for media
- ✅ **Gunicorn Workers**: Auto-scaled based on CPU cores
- ✅ **Unix Socket**: Efficient communication between Nginx and Gunicorn

### Security Features
- ✅ **Security Headers**: X-Frame-Options, X-Content-Type-Options, X-XSS-Protection
- ✅ **File Upload Limits**: 10MB max file size
- ✅ **Process Isolation**: Separate user for web processes
- ✅ **SSL Ready**: Configuration prepared for HTTPS

### Monitoring & Logging
- ✅ **Access Logs**: `/var/log/nginx/sims_access.log`
- ✅ **Error Logs**: `/var/log/nginx/sims_error.log`
- ✅ **Gunicorn Logs**: `/var/www/sims_project/logs/`
- ✅ **Django Logs**: `/var/www/sims_project/logs/sims.log`

## 🔧 Service Management

### Start/Stop Services
```bash
# SIMS Application
sudo systemctl start sims
sudo systemctl stop sims
sudo systemctl restart sims
sudo systemctl status sims

# Nginx Web Server
sudo systemctl start nginx
sudo systemctl stop nginx
sudo systemctl restart nginx
sudo systemctl status nginx
```

### View Logs
```bash
# Application logs
sudo journalctl -u sims -f

# Nginx logs
sudo tail -f /var/log/nginx/sims_access.log
sudo tail -f /var/log/nginx/sims_error.log

# Gunicorn logs
tail -f /var/www/sims_project/logs/gunicorn_error.log
```

## 🔐 Security Recommendations

### Immediate Setup
- [ ] Set strong SECRET_KEY in production
- [ ] Configure firewall (UFW)
- [ ] Set proper file permissions
- [ ] Create non-root user for deployment

### Firewall Configuration
```bash
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS (future)
sudo ufw enable
```

### SSL Certificate (Recommended)
```bash
# Install Certbot for Let's Encrypt
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d 172.236.152.35

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

## 🧪 Testing Your Deployment

### 1. Service Status Check
```bash
sudo systemctl status sims
sudo systemctl status nginx
```

### 2. Web Access Test
- Visit: `http://172.236.152.35/`
- Check: Static files loading correctly
- Test: Login/logout functionality
- Verify: Admin panel access

### 3. Performance Test
```bash
# Test Nginx configuration
sudo nginx -t

# Check process status
ps aux | grep gunicorn
ps aux | grep nginx
```

## 📊 Performance Monitoring

### Key Metrics to Monitor
- Response times
- Memory usage
- Disk space
- Log file sizes
- Database performance

### Monitoring Commands
```bash
# System resources
htop
df -h
free -h

# Network connections
sudo netstat -tulpn | grep :80
sudo ss -tulpn | grep :80
```

## 🔄 Maintenance Tasks

### Daily
- Check service status
- Monitor disk space
- Review error logs

### Weekly
- Update system packages
- Backup database
- Review security logs

### Monthly
- Update Django dependencies
- Analyze performance metrics
- Review user accounts

## 📞 Troubleshooting

### Common Issues

**502 Bad Gateway**
```bash
sudo systemctl status sims
sudo journalctl -u sims -f
```

**Static Files Not Loading**
```bash
python manage.py collectstatic --noinput
sudo systemctl restart sims
```

**Permission Denied**
```bash
sudo chown -R www-data:www-data /var/www/sims_project
sudo chmod -R 755 /var/www/sims_project
```

---

## 🎯 Deployment Status

**✅ NGINX CONFIGURATION COMPLETE**
**🌐 READY FOR DEPLOYMENT ON 172.236.152.35**
**⚡ OPTIMIZED FOR PERFORMANCE**
**🔒 SECURITY HEADERS CONFIGURED**

Your SIMS project is now configured for **Nginx server deployment** on **172.236.152.35** with:
- High-performance Gunicorn WSGI server
- Optimized Nginx configuration
- Systemd service management
- Production-ready security settings

**Next Step**: Run the deployment script on your server!
