# Local Development Guide

This guide explains how to set up SIMS for local development on your laptop or development machine.

## Prerequisites

- Docker Desktop (Windows/Mac) or Docker + Docker Compose (Linux)
- Git
- 8GB+ RAM recommended
- 10GB+ free disk space

## Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/munaimtahir/sims.git
cd sims
```

### 2. Create Environment File
```bash
cp .env.example .env
```

Edit `.env` and set:
```bash
DEBUG=True
SECRET_KEY=any-random-string-for-development
DB_PASSWORD=dev_password
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 3. Build and Start Services
```bash
docker-compose -f docker-compose.local.yml up -d
```

This will start:
- PostgreSQL database (port 5432)
- Redis cache (port 6379)
- Django web application (port 8000)
- Celery worker (optional)
- Celery beat (optional)

### 4. Create Superuser
```bash
docker-compose -f docker-compose.local.yml exec web python manage.py createsuperuser
```

### 5. Access Application
- Application: http://localhost:8000
- Admin Panel: http://localhost:8000/admin/
- Health Check: http://localhost:8000/healthz/

## Development Workflow

### Running Without Docker

For faster development, you can run Django directly:

1. **Install Python dependencies:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Start database and redis:**
```bash
docker-compose -f docker-compose.local.yml up -d db redis
```

3. **Run migrations:**
```bash
python manage.py migrate
```

4. **Collect static files:**
```bash
python manage.py collectstatic --noinput
```

5. **Run development server:**
```bash
python manage.py runserver
```

### Working with Docker

#### View Logs
```bash
# All services
docker-compose -f docker-compose.local.yml logs -f

# Specific service
docker-compose -f docker-compose.local.yml logs -f web
```

#### Execute Commands
```bash
# Django shell
docker-compose -f docker-compose.local.yml exec web python manage.py shell

# Create migrations
docker-compose -f docker-compose.local.yml exec web python manage.py makemigrations

# Run tests
docker-compose -f docker-compose.local.yml exec web pytest
```

#### Restart Services
```bash
# Restart specific service
docker-compose -f docker-compose.local.yml restart web

# Restart all services
docker-compose -f docker-compose.local.yml restart
```

#### Stop Services
```bash
docker-compose -f docker-compose.local.yml down
```

#### Rebuild After Code Changes
```bash
docker-compose -f docker-compose.local.yml up -d --build
```

## Optional Services

The local compose file uses profiles for optional services:

### With Celery Workers
```bash
docker-compose -f docker-compose.local.yml --profile with-celery up -d
```

### With PostgreSQL (instead of SQLite)
```bash
docker-compose -f docker-compose.local.yml --profile with-postgres up -d
```

### With Redis
```bash
docker-compose -f docker-compose.local.yml --profile with-redis up -d
```

### With Nginx (for testing reverse proxy)
```bash
docker-compose -f docker-compose.local.yml --profile with-nginx up -d
```

## Configuration

### Environment Variables

For local development, you can use these default values in `.env`:

```bash
# Debug Mode
DEBUG=True

# Security (use simple values for development)
SECRET_KEY=django-insecure-local-dev-key-change-for-production
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (optional - uses SQLite by default)
DATABASE_URL=postgresql://sims_user:dev_password@localhost:5432/sims_db
DB_NAME=sims_db
DB_USER=sims_user
DB_PASSWORD=dev_password
DB_HOST=localhost
DB_PORT=5432

# Redis (optional)
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/1

# Email (console backend for development)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# CORS (for frontend development)
CORS_ALLOWED_ORIGINS=http://localhost:8000,http://localhost:3000
```

### Using SQLite (Simplest)

For simple local development without PostgreSQL:

1. Don't set `DATABASE_URL` in `.env`
2. Django will automatically use SQLite
3. No need to start PostgreSQL container

### Using PostgreSQL (Recommended)

For production-like local setup:

1. Set `DATABASE_URL` in `.env`
2. Start PostgreSQL:
```bash
docker-compose -f docker-compose.local.yml --profile with-postgres up -d
```

## Testing

### Run All Tests
```bash
docker-compose -f docker-compose.local.yml exec web pytest
```

### Run Specific Tests
```bash
docker-compose -f docker-compose.local.yml exec web pytest tests/test_users.py
```

### Run with Coverage
```bash
docker-compose -f docker-compose.local.yml exec web pytest --cov=sims --cov-report=html
```

### Run Linting
```bash
docker-compose -f docker-compose.local.yml exec web flake8
```

## Database Management

### Apply Migrations
```bash
docker-compose -f docker-compose.local.yml exec web python manage.py migrate
```

### Create Migrations
```bash
docker-compose -f docker-compose.local.yml exec web python manage.py makemigrations
```

### Database Shell
```bash
docker-compose -f docker-compose.local.yml exec web python manage.py dbshell
```

### Reset Database
```bash
docker-compose -f docker-compose.local.yml down -v
docker-compose -f docker-compose.local.yml up -d
docker-compose -f docker-compose.local.yml exec web python manage.py migrate
docker-compose -f docker-compose.local.yml exec web python manage.py createsuperuser
```

## Debugging

### Enable Debug Toolbar

1. Install debug toolbar:
```bash
pip install django-debug-toolbar
```

2. It's already configured in settings when `DEBUG=True`

3. Access any page and you'll see the debug toolbar on the right

### View Django Logs
```bash
docker-compose -f docker-compose.local.yml exec web tail -f /app/logs/django.log
```

### Access Django Shell
```bash
docker-compose -f docker-compose.local.yml exec web python manage.py shell
```

### Connect to PostgreSQL
```bash
docker-compose -f docker-compose.local.yml exec db psql -U sims_user -d sims_db
```

### Connect to Redis
```bash
docker-compose -f docker-compose.local.yml exec redis redis-cli
```

## Hot Reload

The local compose file mounts your source code as a volume:
```yaml
volumes:
  - .:/app  # Your code changes are reflected immediately
```

Changes to Python files will automatically reload the Django development server.

For template/static changes:
- Templates: Reload automatically
- Static files: May need to refresh browser cache (Ctrl+F5)

## IDE Configuration

### VS Code

1. Install Docker extension
2. Install Python extension
3. Create `.vscode/settings.json`:
```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true
}
```

### PyCharm

1. Configure Python interpreter to use Docker container
2. Enable Django support in settings
3. Set Django project root to repository root
4. Set Django settings to `sims_project.settings`

## Common Issues

### Port Already in Use
```bash
# Find process using port 8000
sudo lsof -i :8000  # Mac/Linux
netstat -ano | findstr :8000  # Windows

# Kill the process or change port in docker-compose.local.yml
```

### Permission Issues (Linux)
```bash
# Fix file ownership
sudo chown -R $USER:$USER .

# Or run with proper user in container
docker-compose -f docker-compose.local.yml exec -u $(id -u):$(id -g) web bash
```

### Database Connection Failed
```bash
# Check if PostgreSQL is running
docker-compose -f docker-compose.local.yml ps

# Check PostgreSQL logs
docker-compose -f docker-compose.local.yml logs db

# Restart database
docker-compose -f docker-compose.local.yml restart db
```

### Static Files Not Loading
```bash
# Collect static files
docker-compose -f docker-compose.local.yml exec web python manage.py collectstatic --noinput

# Clear browser cache (Ctrl+Shift+R)
```

## Performance Tips

1. **Use SQLite for development** unless you need PostgreSQL-specific features
2. **Limit Docker resource usage** in Docker Desktop settings
3. **Use volumes for node_modules** if you have frontend
4. **Disable Celery** if not needed for your work
5. **Use `--profile` flags** to only start services you need

## Best Practices

1. ✅ Always work in a git branch, never in `main`
2. ✅ Write tests for new features
3. ✅ Run linting before committing
4. ✅ Use meaningful commit messages
5. ✅ Keep dependencies updated
6. ✅ Document new environment variables in `.env.example`
7. ✅ Never commit `.env` file
8. ✅ Use migrations for database changes
9. ✅ Test in Docker before pushing
10. ✅ Review your own code before creating PR

## Next Steps

- Read the main [README.md](../README.md) for project overview
- Check [DEPLOY_COOLIFY_TRAEFIK.md](DEPLOY_COOLIFY_TRAEFIK.md) for production deployment
- Review [SMOKE_TEST.md](SMOKE_TEST.md) for testing procedures
- See Django docs: https://docs.djangoproject.com/

## Getting Help

- Project issues: GitHub Issues
- Django questions: Django documentation
- Docker questions: Docker documentation
- Community: Stack Overflow with tags `django`, `docker`, `docker-compose`
