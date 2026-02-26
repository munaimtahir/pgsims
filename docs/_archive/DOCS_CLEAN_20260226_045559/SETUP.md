# SIMS Setup Guide

## Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 15+ (or SQLite for development)
- Redis 7+ (optional, for caching and Celery)
- Docker & Docker Compose (optional, for containerized deployment)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/munaimtahir/sims.git
   cd sims
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install --upgrade pip wheel
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # For development tools
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   # For local dev, you can use defaults (SQLite, console email backend)
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files**
   ```bash
   python manage.py collectstatic --noinput
   ```

8. **Run development server**
   ```bash
   python manage.py runserver
   # Or use: make dev
   ```

9. **Access the application**
   - Web interface: http://localhost:8000
   - Admin: http://localhost:8000/admin
   - API docs: http://localhost:8000/api/schema/
   - Health check: http://localhost:8000/healthz/

### Docker Setup (Recommended for Production-like Environment)

1. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with production-like settings
   ```

2. **Build and start services**
   ```bash
   docker-compose up -d --build
   # Or use: make up
   ```

3. **Run migrations**
   ```bash
   docker-compose exec web python manage.py migrate
   # Or use: make migrate
   ```

4. **Create superuser**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

5. **View logs**
   ```bash
   docker-compose logs -f
   # Or use: make logs
   ```

6. **Access the application**
   - Web interface: http://localhost
   - Admin: http://localhost/admin

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=sims --cov-report=html --cov-report=term-missing

# Or use Makefile
make test

# Run specific test file
pytest sims/users/tests.py -v

# Run specific test
pytest sims/users/tests.py::UserModelTests::test_user_creation -v
```

### Seeding Demo Data

```bash
# Local development
python manage.py sims_seed_demo

# Docker
docker-compose exec web python manage.py sims_seed_demo
# Or use: make seed
```

## Project Structure

```
sims/
├── sims/                      # Django apps
│   ├── analytics/            # Analytics and dashboard APIs
│   ├── attendance/           # Attendance tracking and eligibility
│   ├── audit/                # Audit trail
│   ├── bulk/                 # Bulk operations
│   ├── cases/                # Clinical cases
│   ├── certificates/         # Certificate management
│   ├── logbook/              # Logbook entries
│   ├── notifications/        # Notification system
│   ├── reports/              # Report generation
│   ├── rotations/            # Rotation management
│   ├── search/               # Search functionality
│   └── users/                # User management
├── sims_project/             # Project settings
│   ├── settings.py          # Main settings
│   ├── urls.py              # URL configuration
│   ├── celery.py            # Celery configuration
│   └── health.py            # Health check views
├── templates/                # HTML templates
├── static/                   # Static files
├── deployment/               # Deployment configurations
│   └── nginx.conf           # Nginx configuration
├── docs/                     # Documentation
├── tests/                    # Test utilities
├── Dockerfile               # Docker build configuration
├── docker-compose.yml       # Docker Compose setup
├── Makefile                 # Common commands
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variables template
└── manage.py                # Django management script
```

## Common Tasks

### Database Management

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Reset database (WARNING: deletes all data)
python manage.py flush

# Backup database
pg_dump sims_db > backup.sql

# Restore database
psql sims_db < backup.sql
```

### User Management

```bash
# Create superuser
python manage.py createsuperuser

# Change user password
python manage.py changepassword username

# List users
python manage.py shell
>>> from sims.users.models import User
>>> User.objects.all()
```

### Celery Tasks

```bash
# Start Celery worker (development)
celery -A sims_project worker -l info

# Start Celery beat scheduler
celery -A sims_project beat -l info

# Monitor Celery with Flower (optional)
celery -A sims_project flower
```

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>
```

### Database Connection Issues
- Verify PostgreSQL is running
- Check DATABASE_URL in .env
- Ensure database exists: `createdb sims_db`

### Static Files Not Loading
```bash
# Collect static files again
python manage.py collectstatic --clear --noinput

# Check STATIC_ROOT and STATIC_URL in settings
```

### Docker Issues
```bash
# Rebuild containers
docker-compose build --no-cache

# Clean up
docker-compose down -v  # Remove volumes
docker system prune -a  # Clean Docker system

# View container logs
docker-compose logs web
```

## Next Steps

- Read [ENV_VARS.md](ENV_VARS.md) for environment configuration
- Read [SECURITY.md](SECURITY.md) for security best practices
- Read [API.md](API.md) for API documentation
- Read [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
