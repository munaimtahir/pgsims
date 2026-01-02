# SIMS Localhost Deployment Guide

Complete guide for deploying SIMS on your local Windows machine for development and demonstrations.

## Overview

This guide covers deploying SIMS on localhost, allowing you to run the application locally for development, testing, and demonstrations. The localhost deployment is optimized for ease of setup and development workflows.

## Prerequisites

Before starting, ensure you have all prerequisites installed. See [LOCALHOST_PREREQUISITES_WINDOWS.md](LOCALHOST_PREREQUISITES_WINDOWS.md) for detailed installation instructions.

**Quick Checklist:**
- [x] Python 3.11+
- [x] pip (Python package manager)
- [x] Node.js 18+
- [x] npm (comes with Node.js)
- [x] Docker Desktop for Windows
- [x] Git (optional but recommended)

## Quick Start

### Option 1: Automated Setup (Recommended)

1. **Run the setup script:**
   ```powershell
   .\scripts\setup_localhost_windows.ps1
   ```

2. **Deploy with Docker:**
   ```powershell
   .\deployment\deploy_localhost.ps1
   ```

3. **Access the application:**
   - Main App: http://localhost:8000/
   - Admin Panel: http://localhost:8000/admin/

### Option 2: Manual Setup

Follow the detailed steps below for manual setup.

## Detailed Setup Steps

### Step 1: Clone Repository

```powershell
git clone <repository-url>
cd sims
```

### Step 2: Set Up Python Environment

1. **Create virtual environment:**
   ```powershell
   python -m venv venv
   ```

2. **Activate virtual environment:**
   ```powershell
   venv\Scripts\activate
   ```

3. **Upgrade pip:**
   ```powershell
   pip install --upgrade pip wheel
   ```

4. **Install Python dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

### Step 3: Configure Environment Variables

1. **Copy localhost environment template:**
   ```powershell
   Copy-Item .env.localhost .env
   ```

2. **Edit .env file (optional - defaults work for basic setup):**
   ```powershell
   notepad .env
   ```

   **Key settings for localhost:**
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   CORS_ALLOWED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000,http://localhost:3000
   ```

### Step 4: Set Up Database

**Option A: SQLite (Default - Easiest)**

No additional setup needed! SQLite will be used automatically if no PostgreSQL configuration is provided.

**Option B: PostgreSQL in Docker**

1. **Start PostgreSQL in Docker:**
   ```powershell
   docker run -d --name sims_postgres_localhost `
     -e POSTGRES_DB=sims_db `
     -e POSTGRES_USER=sims_user `
     -e POSTGRES_PASSWORD=localhost_dev_password `
     -p 5432:5432 `
     postgres:15-alpine
   ```

2. **Update .env file:**
   ```env
   DB_ENGINE=django.db.backends.postgresql
   DB_NAME=sims_db
   DB_USER=sims_user
   DB_PASSWORD=localhost_dev_password
   DB_HOST=localhost
   DB_PORT=5432
   ```

### Step 5: Run Database Migrations

```powershell
python manage.py migrate
```

### Step 6: Create Superuser

```powershell
python manage.py createsuperuser
```

Follow the prompts to create an admin user.

### Step 7: Collect Static Files

```powershell
python manage.py collectstatic --noinput
```

### Step 8: Start Development Server

```powershell
python manage.py runserver
```

The application will be available at:
- **Main App:** http://localhost:8000/
- **Admin Panel:** http://localhost:8000/admin/
- **Health Check:** http://localhost:8000/healthz/

## Docker Deployment (Alternative)

For a more production-like environment using Docker:

### Step 1: Configure Environment

```powershell
Copy-Item .env.localhost .env
# Edit .env if needed
```

### Step 2: Start Services

```powershell
.\deployment\deploy_localhost.ps1
```

Or manually:
```powershell
docker compose -f docker-compose.localhost.yml up -d --build
```

### Step 3: Run Migrations

```powershell
docker compose -f docker-compose.localhost.yml exec web python manage.py migrate
```

### Step 4: Create Superuser

```powershell
docker compose -f docker-compose.localhost.yml exec web python manage.py createsuperuser
```

### Step 5: Access Application

- **Main App:** http://localhost:8000/
- **Admin Panel:** http://localhost:8000/admin/

## Frontend Setup (Next.js)

### Step 1: Install Dependencies

```powershell
cd frontend
npm install
```

### Step 2: Configure Environment

```powershell
Copy-Item .env.localhost .env.local
```

### Step 3: Start Development Server

```powershell
npm run dev
```

Frontend will be available at: http://localhost:3000/

## Switching Between Localhost and VPS

To switch between localhost and VPS deployments:

**Switch to Localhost:**
```powershell
.\deployment\switch_to_localhost.sh
# Or on Windows PowerShell:
.\deployment\switch_to_localhost.ps1
```

**Switch to VPS:**
```powershell
.\deployment\switch_to_vps.sh
```

## Running Celery (Optional)

For background tasks and scheduled jobs:

### Terminal 1: Celery Worker
```powershell
celery -A sims_project worker -l info
```

### Terminal 2: Celery Beat
```powershell
celery -A sims_project beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

Or use Docker Compose profiles:
```powershell
docker compose -f docker-compose.localhost.yml --profile with-celery up -d
```

## Development Workflow

### Daily Development

1. **Activate virtual environment:**
   ```powershell
   venv\Scripts\activate
   ```

2. **Start Django server:**
   ```powershell
   python manage.py runserver
   ```

3. **In another terminal, start frontend (if needed):**
   ```powershell
   cd frontend
   npm run dev
   ```

### Making Changes

- Code changes: Django will auto-reload (development server)
- Frontend changes: Next.js will hot-reload
- Database changes: Create and run migrations
- Static files: Re-run `collectstatic` after changes

### Creating Migrations

After model changes:
```powershell
python manage.py makemigrations
python manage.py migrate
```

## Troubleshooting

### Port 8000 Already in Use

```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F

# Or use a different port
python manage.py runserver 8001
```

### Docker Issues

**Check Docker status:**
```powershell
docker ps
```

**View logs:**
```powershell
docker compose -f docker-compose.localhost.yml logs -f
```

**Restart services:**
```powershell
docker compose -f docker-compose.localhost.yml restart
```

### Database Connection Issues

**For SQLite:**
- Ensure `db.sqlite3` file has write permissions
- Check disk space

**For PostgreSQL:**
- Ensure PostgreSQL is running
- Check connection credentials in `.env`
- Verify port 5432 is accessible

### Static Files Not Loading

```powershell
python manage.py collectstatic --noinput
```

### Frontend Not Connecting to Backend

1. Check `frontend/.env.local` has correct API URL:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

2. Restart Next.js dev server

3. Clear browser cache

## Environment Variables Reference

Key environment variables for localhost:

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | (required) | Django secret key |
| `DEBUG` | `True` | Enable debug mode |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Allowed hostnames |
| `CORS_ALLOWED_ORIGINS` | `http://localhost:8000,...` | CORS allowed origins |
| `DB_ENGINE` | `sqlite3` | Database backend |
| `REDIS_URL` | `redis://localhost:6379/0` | Redis connection URL |

See `.env.localhost` for complete list.

## Next Steps

- [Read Deployment Environments Guide](DEPLOYMENT_ENVIRONMENTS.md) to understand localhost vs VPS differences
- [Check Prerequisites Guide](LOCALHOST_PREREQUISITES_WINDOWS.md) for detailed installation steps
- [Review Main README](README.md) for project overview

## Support

For issues or questions:
- Check troubleshooting section above
- Review project documentation
- Check GitHub issues

