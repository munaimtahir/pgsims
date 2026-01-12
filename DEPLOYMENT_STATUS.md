# 🚀 SIMS Deployment Status & Public Access Information

## 📍 Public Deployment URLs

### Primary Server (139.162.9.224)
- **Homepage:** http://139.162.9.224:81/
- **Login Page:** http://139.162.9.224:81/users/login/
- **Admin Panel:** http://139.162.9.224:81/admin/
- **API Endpoint:** http://139.162.9.224:81/api/
- **Health Check:** http://139.162.9.224:81/healthz/

### Secondary Server (172.237.95.120)
- **Homepage:** http://172.237.95.120:81/
- **Login Page:** http://172.237.95.120:81/users/login/
- **Admin Panel:** http://172.237.95.120:81/admin/
- **API Endpoint:** http://172.237.95.120:81/api/
- **Health Check:** http://172.237.95.120:81/healthz/

### PGSIMS Production Server (pgsims.alshifalab.pk)
- **Homepage:** https://pgsims.alshifalab.pk/
- **Login Page:** https://pgsims.alshifalab.pk/users/login/
- **Admin Panel:** https://pgsims.alshifalab.pk/admin/
- **API Endpoint:** https://pgsims.alshifalab.pk/api/
- **Health Check:** https://pgsims.alshifalab.pk/healthz/
- **Server IP:** 34.124.150.231
- **Backend Port:** 8014 (internal, proxied by Caddy)
- **Reverse Proxy:** Caddy (automatic SSL/TLS)

---

## 🔐 Demo Credentials

**⚠️ SECURITY WARNING:** These credentials are for **DEMO/TESTING ONLY**. Change all passwords immediately in production environments.

### Admin Account
- **Username:** `admin`
- **Password:** `admin123`
- **Access:** Full system administration, user management, analytics

### Supervisor Accounts
- **Username:** `dr_smith`
- **Password:** `supervisor123`
- **Specialty:** Surgery
- **Access:** Review logbooks, evaluate cases, manage assigned students

- **Username:** `dr_jones`
- **Password:** `supervisor123`
- **Specialty:** Medicine
- **Access:** Review logbooks, evaluate cases, manage assigned students

### PG Student Accounts
- **Username:** `pg_ahmed`
- **Password:** `student123`
- **Specialty:** Surgery
- **Year:** 1
- **Registration:** PG2024001
- **Access:** Submit logbooks, create clinical cases, view progress

- **Username:** `pg_fatima`
- **Password:** `student123`
- **Specialty:** Medicine
- **Year:** 2
- **Registration:** PG2024002
- **Access:** Submit logbooks, create clinical cases, view progress

---

## ✅ Deployment Verification Checklist

### 1. Check Server Accessibility

Test from your local machine:
```bash
# Test Primary Server
curl -I http://139.162.9.224:81/healthz/

# Test Secondary Server
curl -I http://172.237.95.120:81/healthz/
```

Expected response: HTTP 200 OK

### 2. Verify Docker Containers (On Server)

SSH into the server and run:
```bash
# On Primary Server (139.162.9.224)
ssh user@139.162.9.224
cd /opt/sims_project
docker compose ps

# On Secondary Server (172.237.95.120)
ssh user@172.237.95.120
cd /opt/sims_project
docker compose ps
```

All containers should show as "Up":
- ✅ sims_db (PostgreSQL)
- ✅ sims_redis (Redis)
- ✅ sims_web (Django/Gunicorn)
- ✅ sims_worker (Celery Worker)
- ✅ sims_beat (Celery Beat)
- ✅ sims_nginx (Nginx)

### 3. Run Deployment Verification Script

On each server:
```bash
cd /opt/sims_project/deployment
./verify_deployment.sh
```

### 4. Test Login with Demo Credentials

1. Navigate to: http://139.162.9.224:81/users/login/ (or secondary server)
2. Try logging in with each demo account
3. Verify dashboard loads correctly

---

## 📊 Demo Data Status

### Seeded Demo Data Includes:

1. **Users:**
   - 1 Admin user
   - 2 Supervisor users
   - 2 PG Student users

2. **Organizational Structure:**
   - 2 Hospitals (FMU Teaching Hospital, Allied Hospital)
   - 8 Departments (Surgery, Medicine, Cardiology, etc.)

3. **Training Records:**
   - 4 Rotations (2 per student: 1 completed, 1 ongoing)
   - 4 Certificates (2 per student: BLS, ACLS)
   - Multiple Logbook entries
   - 4 Clinical Cases (2 per student)

4. **Optional Data:**
   - Attendance records (if attendance script was run)

### How to Seed Demo Data

If demo data is not present, run on the server:

```bash
# SSH into server
ssh user@139.162.9.224  # or 172.237.95.120

# Navigate to project
cd /opt/sims_project

# Run demo data seeding
docker compose exec web python manage.py shell -c "
from scripts.preload_demo_data import main
main()
"

# Or use the seeding script
docker compose exec web python scripts/preload_demo_data.py
```

Or use the automated script:
```bash
cd /opt/sims_project
./scripts/seed_demo_data.sh
```

---

## 🔧 Deployment Commands

### Check Deployment Status
```bash
# View all containers
docker compose ps

# View logs
docker compose logs -f

# View specific service logs
docker compose logs -f web
docker compose logs -f nginx
```

### Restart Services
```bash
# Restart all services
docker compose restart

# Restart specific service
docker compose restart web
```

### Update Deployment
```bash
# Pull latest code
git pull

# Rebuild and restart
docker compose up -d --build

# Run migrations
docker compose exec web python manage.py migrate

# Collect static files
docker compose exec web python manage.py collectstatic --noinput
```

---

## 🌐 Public Access Requirements

### Firewall Configuration

Ensure port 81 is open on both servers:

```bash
# Check if port is open
sudo ufw status
# or
sudo iptables -L -n | grep 81

# Open port 81 if needed
sudo ufw allow 81/tcp
sudo ufw reload
```

### Nginx Configuration

Verify Nginx is configured to listen on port 81:
```bash
# Check nginx config
cat /opt/sims_project/deployment/nginx.conf | grep "listen"
```

Should show: `listen 81;`

### ALLOWED_HOSTS

Verify Django settings allow the server IPs:
- Primary: `139.162.9.224`
- Secondary: `172.237.95.120`

---

## 🚨 Troubleshooting

### Server Not Accessible

1. **Check if containers are running:**
   ```bash
   docker compose ps
   ```

2. **Check Nginx logs:**
   ```bash
   docker compose logs nginx
   ```

3. **Check Django logs:**
   ```bash
   docker compose logs web
   ```

4. **Verify port is open:**
   ```bash
   sudo ss -tulpn | grep 81
   ```

5. **Test from server itself:**
   ```bash
   curl http://localhost:81/healthz/
   ```

### Demo Data Not Present

1. **Check if users exist:**
   ```bash
   docker compose exec web python manage.py shell
   >>> from django.contrib.auth import get_user_model
   >>> User = get_user_model()
   >>> User.objects.count()
   ```

2. **Re-seed demo data:**
   ```bash
   docker compose exec web python scripts/preload_demo_data.py
   ```

### Login Issues

1. **Reset admin password:**
   ```bash
   docker compose exec web python manage.py changepassword admin
   ```

2. **Create new superuser:**
   ```bash
   docker compose exec web python manage.py createsuperuser
   ```

---

## 📝 Quick Reference

### Primary Server (139.162.9.224:81)
- **URL:** http://139.162.9.224:81/
- **Admin:** admin / admin123
- **Status:** Check with `curl http://139.162.9.224:81/healthz/`

### Secondary Server (172.237.95.120:81)
- **URL:** http://172.237.95.120:81/
- **Admin:** admin / admin123
- **Status:** Check with `curl http://172.237.95.120:81/healthz/`

### Demo Users
- Admin: `admin` / `admin123`
- Supervisor: `dr_smith` / `supervisor123`
- Supervisor: `dr_jones` / `supervisor123`
- Student: `pg_ahmed` / `student123`
- Student: `pg_fatima` / `student123`

---

## ✅ Verification Steps Summary

1. ✅ **Test Public URLs** - Verify both servers respond
2. ✅ **Check Containers** - All Docker containers running
3. ✅ **Test Login** - Use demo credentials to login
4. ✅ **Verify Demo Data** - Check users, rotations, cases exist
5. ✅ **Test Functionality** - Create logbook entry, submit case
6. ✅ **Check Health Endpoint** - `/healthz/` returns 200

---

## 📞 Support

If deployment issues persist:
1. Check logs: `docker compose logs -f`
2. Review deployment guide: `deployment/DOCKER_DEPLOYMENT_GUIDE.md`
3. Run verification: `deployment/verify_deployment.sh`
4. Check firewall and port accessibility

---

**Last Updated:** $(date)
**Deployment Status:** Ready for Verification
**Demo Data:** Available via seeding script
