# 🚀 SIMS Quick Access Information

## 🌐 Public URLs

### Primary Server
**http://139.162.9.224:81/**

- Login: http://139.162.9.224:81/users/login/
- Admin: http://139.162.9.224:81/admin/
- Health: http://139.162.9.224:81/healthz/

### Secondary Server
**http://172.237.95.120:81/**

- Login: http://172.237.95.120:81/users/login/
- Admin: http://172.237.95.120:81/admin/
- Health: http://172.237.95.120:81/healthz/

### PHC Production Server (Primary)
**https://phc.alshifalab.pk/**

- Login: https://phc.alshifalab.pk/users/login/
- Admin: https://phc.alshifalab.pk/admin/
- Health: https://phc.alshifalab.pk/healthz/
- Server IP: 34.124.150.231
- Backend Port: 8014 (internal, proxied by Caddy)

---

## 🔐 Demo Credentials

### Admin
- **Username:** `admin`
- **Password:** `admin123`

### Supervisors
- **Username:** `dr_smith` | **Password:** `supervisor123`
- **Username:** `dr_jones` | **Password:** `supervisor123`

### Students
- **Username:** `pg_ahmed` | **Password:** `student123`
- **Username:** `pg_fatima` | **Password:** `student123`

---

## ✅ Quick Verification

### Test from Command Line
```bash
# Test Primary Server
curl http://139.162.9.224:81/healthz/

# Test Secondary Server
curl http://172.237.95.120:81/healthz/

# Test PHC Production Server
curl https://phc.alshifalab.pk/healthz/
```

### Test in Browser
1. Open: http://139.162.9.224:81/
2. Click "Login" or go to: http://139.162.9.224:81/users/login/
3. Login with: `admin` / `admin123`
4. Verify dashboard loads

---

## 📊 Demo Data

Demo data includes:
- ✅ 1 Admin user
- ✅ 2 Supervisor users  
- ✅ 2 PG Student users
- ✅ 2 Hospitals with 8 Departments
- ✅ 4 Rotations (completed & ongoing)
- ✅ 4 Certificates
- ✅ Multiple Logbook entries
- ✅ 4 Clinical Cases

**To seed demo data on server:**
```bash
ssh user@139.162.9.224
cd /opt/sims_project
docker compose exec web python scripts/preload_demo_data.py
```

---

## 🔧 Server Commands

### Check Status
```bash
docker compose ps
```

### View Logs
```bash
docker compose logs -f web
```

### Restart
```bash
docker compose restart
```

---

**For detailed information, see:** 
- `DEPLOYMENT_STATUS.md` - Complete deployment status
- `PHC_DEPLOYMENT_SUMMARY.md` - PHC deployment configuration
- `deployment/DEPLOY_PHC.md` - PHC deployment guide
