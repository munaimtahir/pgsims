# SIMS Quick Start Guide

**Status:** ✅ Ready for Deployment

---

## 🚀 Quick Deploy (Docker - Recommended)

The fastest way to deploy SIMS is using Docker Compose:

```bash
# Option 1: Use the deployment script
./DEPLOY_NOW.sh

# Option 2: Manual deployment
docker compose build
docker compose up -d
```

That's it! The application will be available at:
- **Frontend**: http://localhost:81/
- **Backend API**: http://localhost:81/api/
- **Admin Panel**: http://localhost:81/admin/

---

## 📋 What's Already Done

✅ **Environment Files**: Created with secure SECRET_KEY  
✅ **Code Changes**: All security fixes applied  
✅ **Configuration**: Docker Compose ready  
✅ **Documentation**: Complete guides available  

---

## 🔧 Manual Setup (If Not Using Docker)

### 1. Install Python Dependencies

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Set Environment Variables

The `.env` file is already created. Verify it has:
- `SECRET_KEY` (already set)
- `DEBUG=False`
- `ALLOWED_HOSTS=localhost,127.0.0.1`
- Database configuration

### 3. Run Migrations

```bash
export $(grep -v '^#' .env | grep -v '^$' | xargs)
python manage.py migrate
python manage.py migrate django_celery_beat
python manage.py collectstatic --noinput
```

### 4. Start Services

```bash
# Terminal 1: Django
python manage.py runserver

# Terminal 2: Celery Worker
celery -A sims_project worker -l info

# Terminal 3: Celery Beat
celery -A sims_project beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

---

## 🐳 Docker Services

The Docker Compose setup includes:

- **db**: PostgreSQL database
- **redis**: Redis cache and message broker
- **web**: Django application (Gunicorn)
- **worker**: Celery worker for background tasks
- **beat**: Celery beat scheduler
- **nginx**: Reverse proxy and static file server

### Docker Commands

```bash
# Start all services
docker compose up -d

# View logs
docker compose logs -f

# View specific service logs
docker compose logs -f web
docker compose logs -f worker
docker compose logs -f beat

# Stop all services
docker compose down

# Restart services
docker compose restart

# Check status
docker compose ps
```

---

## 🔐 First Time Setup

### Create Admin User

```bash
# Using Docker
docker compose exec web python manage.py createsuperuser

# Or locally
python manage.py createsuperuser
```

**⚠️ Note**: For local development, you can use demo credentials:
- Username: `admin`
- Password: `admin123`

**🚨 SECURITY WARNING**: These are for local development only. Always change passwords in production!

---

## 📚 Documentation

- **Full Setup Guide**: `README.md`
- **Deployment Guide**: `DEPLOYMENT_READY.md`
- **Repair Plan**: `SIMS_REPAIR_PLAN.md`
- **Verification**: `VERIFICATION_SUMMARY.md`

---

## ✅ Verification

After deployment, verify:

1. **Health Check**: http://localhost:81/healthz/ (or http://localhost:8000/healthz/)
2. **Admin Panel**: http://localhost:81/admin/ (or http://localhost:8000/admin/)
3. **API**: http://localhost:81/api/ (or http://localhost:8000/api/)

---

## 🆘 Troubleshooting

### Docker Issues

```bash
# Check if services are running
docker compose ps

# View logs for errors
docker compose logs

# Rebuild if needed
docker compose build --no-cache
docker compose up -d
```

### Database Issues

```bash
# Reset database (WARNING: Deletes all data)
docker compose down -v
docker compose up -d
```

### Port Conflicts

If port 81 is in use, edit `docker-compose.yml` and change:
```yaml
ports:
  - "81:81"  # Change 81 to another port
```

---

## 🎯 Next Steps

1. **Deploy**: Run `./DEPLOY_NOW.sh` or `docker compose up -d`
2. **Create Admin**: Run `docker compose exec web python manage.py createsuperuser`
3. **Access**: Open http://localhost:81/ in your browser
4. **Configure**: Update `.env` with production values when ready

---

**Status:** ✅ **READY TO DEPLOY**

Just run `./DEPLOY_NOW.sh` or `docker compose up -d` to get started!

