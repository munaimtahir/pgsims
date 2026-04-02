# SIMS - Student (Postgrduate) Information Management System

A comprehensive Django web application for managing postgraduate medical residents' academic and training records.

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Django Version](https://img.shields.io/badge/django-4.2+-green.svg)](https://www.djangoproject.com/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Linter: flake8](https://img.shields.io/badge/linter-flake8-blue.svg)](https://flake8.pycqa.org/)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Development Status](#development-status)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [User Roles](#user-roles)
- [Development Guidelines](#development-guidelines)
- [Testing](#testing)
- [Deployment](#deployment)
- [Documentation](#documentation)
- [Contributing](#contributing)

## 🎯 Overview

SIMS is the postgraduate training operations system for UTRMC. The current engineering priority is truth alignment and workflow stabilization, not broad feature expansion.

**Current Status**: ⚠️ **Active surface stabilized; legacy workflow boundary still constrained**

Authoritative current-state docs:
- `docs/_recovery/20260402T122809Z/00-executive-recovery-summary.md`
- `docs/_recovery/20260402T122809Z/01-active-surface-map.md`
- `docs/_recovery/20260402T122809Z/04-core-workflow-closure-report.md`
- `docs/contracts/`

**Deployment**: Production deployment is standardized on Docker Compose (`docker/docker-compose.prod.yml`) + Caddy reverse proxy. See [docs/deploy/CADDY_ROUTINE.md](docs/deploy/CADDY_ROUTINE.md).

## ✨ Features

### Active Surface

- **👥 User Management**: Role-based access control for admins, supervisors, and postgraduate students
- **📊 Dashboard System**: Customized dashboards for resident, supervisor, and UTRMC roles
- **🔄 Rotation Management**: Track and manage training rotations across different departments
- **🗓️ Leave Workflow**: Resident leave draft/submission and supervisor approval on active resident/supervisor surfaces
- **📜 Certificate Management**: Manage and track certifications and achievements
- **🎓 Academic Core**: Research, thesis, workshops, eligibility, postings
- **📈 Analytics & Reporting**: Active for training and eligibility dashboards; legacy analytics modules remain deferred
- **🔍 Advanced Filtering**: Search and filter capabilities across all modules
- **📤 Data Export**: Export data to CSV format for all major modules
- **🔐 Security**: Role-based permissions, secure authentication, and session management
- **🌐 Global Search**: Cross-module search with suggestions, highlights, and per-user history
- **🛡️ Audit Trail**: Historical tracking for key models plus Activity Log APIs and CSV export
- **✅ Business Rules Engine**: Centralised validators, sanitisation and consistent error handling

### Deferred or Legacy Surface

- **📚 Digital Logbook**: Not part of the active frontend or active backend URL include set in the current runtime
- **🏥 Clinical Cases**: Not part of the active frontend or active backend URL include set in the current runtime
- **📈 Legacy Analytics Modules**: Historical docs and code remain, but are not the authoritative active surface

### Additional Features

- **Admin Interface**: Comprehensive Django admin with custom branding
- **RESTful APIs**: JSON endpoints for statistics and data retrieval
- **File Management**: Upload and manage documents and images
- **Responsive Design**: Mobile-friendly Bootstrap 5 interface
- **PMC Theme**: Professional medical college branding throughout

Historical status snapshots such as [FEATURES_STATUS.md](docs/FEATURES_STATUS.md) are not authoritative for current delivery truth. Use `docs/_recovery/20260402T122809Z/` and `docs/contracts/` instead.

## 📊 Development Status

Recovery baseline after the 2026-04-02 stabilization pass:

- **Active and verified**: authentication, userbase administration, resident dashboard, supervisor dashboard, resident leave workflow, active rotation lifecycle, active postings lifecycle, research workflow, thesis/workshops baseline, eligibility monitor
- **Active but partial**: some resident/supervisor/UTRMC happy paths outside the promoted workflow gate, broader program administration depth beyond the active workflow surface
- **Deferred**: logbook, cases, legacy analytics

See `docs/_recovery/20260402T122809Z/STATUS_AFTER_RECOVERY_SCORECARD.md` for the current scored baseline.

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/munaimtahir/sims.git
cd sims
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Configure Environment Variables

Create a `.env` file in the project root (copy from `.env.example` if available):

```bash
# Required settings
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (use DATABASE_URL or individual settings)
DATABASE_URL=postgresql://user:password@localhost:5432/sims_db
# OR
DB_NAME=sims_db
DB_USER=sims_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379/0

# Celery
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/1

# JWT Settings
JWT_ACCESS_TOKEN_MINUTES=60
JWT_REFRESH_TOKEN_DAYS=7

# CORS (comma-separated)
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

**Note:** See `.env.example` for a complete list of available environment variables.

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run Database Migrations

```bash
python manage.py migrate
```

### 6. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

**⚠️ LOCAL DEVELOPMENT ONLY:** For local testing, you can use these demo credentials:
- Username: `admin`
- Password: `admin123`

**🚨 SECURITY WARNING:** These credentials are for local development only. NEVER use default credentials in production. Always create a strong password for production deployments.

### 7. Start Development Server

```bash
python manage.py runserver
```

### 8. Access the Application

- **Main Application**: http://127.0.0.1:8000
- **Admin Interface**: http://127.0.0.1:8000/admin
- **Login**: Use admin credentials

## 🖥️ Deployment

### Production (Canonical Path)

PGSIMS supports one production deployment path only:

1. Start stack with Docker Compose:

```bash
cd /srv/apps/pgsims
docker compose -f docker/docker-compose.prod.yml up -d --build
```

2. Sync and reload Caddy:

```bash
cd /srv/apps/pgsims
./ops/caddy_sync_reload.sh
```

3. Follow full verification routine in [docs/deploy/CADDY_ROUTINE.md](docs/deploy/CADDY_ROUTINE.md).

### Local Development

Use local scripts and compose variants under `scripts/local_dev/` and `docker/docker-compose.local.yml` for developer workflows.

## 📁 Project Structure

SIMS is organized as a clean monorepo with separate concern domains:

```
sims/
├── backend/                # 🐍 Django Backend Application
│   ├── sims/               # CORE application modules (Users, Rotations, etc.)
│   ├── sims_project/       # Project configuration (settings, urls, wsgi)
│   ├── templates/          # Global Django templates
│   ├── static/             # Backend static assets
│   ├── tests/              # Backend test suites
│   ├── manage.py           # Django management script
│   └── requirements.txt    # Python dependencies
├── frontend/               # ⚛️ Next.js Frontend Application
│   ├── app/                # Next.js App router
│   ├── components/         # React components
│   └── public/             # Static assets
├── docker/                 # 🐳 Docker Configuration
│   ├── docker-compose.yml  # Main production compose file
│   └── docker-compose.*.yml # Environment-specific compose files
├── deploy/                 # 🚀 Deployment Config
│   └── Caddyfile.pgsims    # Canonical Caddy reverse proxy config
├── scripts/                # 🛠️ Maintenance & Local Dev Utilities
│   ├── local_dev/          # Desktop dev helper scripts
│   └── sandbox/            # Demo data seeders & test scripts
├── docs/                   # 📖 Consolidated Documentation
├── Makefile                # Unified entry point for development commands
└── .env                    # Environment secrets (Root & Backend)
```

## 👥 User Roles

The system supports three primary user roles:

### 1. **Admin** 
- Full system access
- User management and creation
- System configuration
- View all data and analytics
- Manage all modules

### 2. **Supervisor**
- Manage assigned postgraduate students
- Review and approve logbook entries
- Review clinical cases
- Evaluate rotations
- View trainee progress and analytics

### 3. **Postgraduate (PG)**
- Maintain personal digital logbook
- Submit clinical cases for review
- Track certifications and achievements
- View rotation schedule
- Access personal analytics and progress

## 🛠️ Development Guidelines

### Code Style

This project follows Python and Django best practices:

- **Code Formatting**: [Black](https://github.com/psf/black) with 100 character line length
- **Linting**: [Flake8](https://flake8.pycqa.org/) for code quality checks
- **Style Guide**: [PEP 8](https://www.python.org/dev/peps/pep-0008/)

### Running Code Quality Checks

```bash
# Format code with Black
black sims/ --line-length 100

# Run Flake8 linter
flake8 sims/ --count --statistics

# Run both
black sims/ --line-length 100 && flake8 sims/ --count --statistics
```

### Git Workflow

1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Make your changes and commit: `git commit -m "Description of changes"`
3. Push to the branch: `git push origin feature/your-feature-name`
4. Create a Pull Request

### Commit Messages

Follow conventional commit format:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python manage.py test

# Run tests for a specific app
python manage.py test sims.users

# Run with pytest (if configured)
pytest
```

### Writing Tests

- Place tests in `tests.py` within each app
- Follow Django testing best practices
- Aim for good test coverage of critical functionality
- Test both success and error cases

## 🔄 Celery Worker & Beat Setup

SIMS uses Celery for background task processing and scheduled tasks.

### Prerequisites

- Redis server running (required for Celery broker)
- Django migrations run (including `django_celery_beat` migrations)

### Running Celery Worker

```bash
# Start Celery worker
celery -A sims_project worker -l info

# With concurrency control
celery -A sims_project worker -l info --concurrency=2
```

### Running Celery Beat (Scheduler)

```bash
# Start Celery beat with DatabaseScheduler
celery -A sims_project beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

### Running Both (Development)

For development, you can run both in separate terminals, or use a process manager like `supervisord`.

### Database Migrations for Celery Beat

```bash
# Run migrations to create django_celery_beat tables
python manage.py migrate django_celery_beat
```

### Configuration

Celery configuration is in `sims_project/celery.py` and uses settings from `sims_project/settings.py`:

- `CELERY_BROKER_URL`: Redis broker URL (default: `redis://localhost:6379/1`)
- `CELERY_RESULT_BACKEND`: Result backend URL (default: `redis://localhost:6379/1`)

Periodic tasks are configured in `sims_project/celery.py` and can be managed via Django admin after running migrations.

## 🐳 Docker Deployment

SIMS includes a complete Docker Compose setup for production-ready deployment.

### Prerequisites

- Docker and Docker Compose installed
- `.env` file configured with all required environment variables

### Quick Start

```bash
# Build all services
docker compose build

# Start all services
docker compose up -d

# View logs
docker compose logs -f

# Stop all services
docker compose down
```

### Services

The Docker Compose setup includes:

- **db**: PostgreSQL database
- **redis**: Redis cache and message broker
- **backend**: Django application (Gunicorn)
- **worker**: Celery worker for background tasks
- **beat**: Celery beat scheduler
- **caddy**: External reverse proxy (host service)

### Environment Variables

**⚠️ SECURITY WARNING:** Before running in production, ensure you have set:

- `SECRET_KEY`: A secure Django secret key (REQUIRED)
- `DB_PASSWORD`: Strong database password (REQUIRED)
- `ALLOWED_HOSTS`: Comma-separated list of allowed hostnames
- Other production settings as needed

Create a `.env` file in the project root with these values. See `.env.example` for reference.

### Health Checks

All services include health checks. Check service status:

```bash
docker compose ps
```

### Volumes

- `postgres_data`: PostgreSQL data persistence
- `redis_data`: Redis data persistence
- `static_volume`: Collected static files
- `media_volume`: User-uploaded media files

### Ports

- `127.0.0.1:8014`: Django backend target for Caddy
- `127.0.0.1:8082`: Next.js frontend target for Caddy

## 🚀 Deployment Routine

Use the canonical routine only:

- Compose file: `docker/docker-compose.prod.yml`
- Caddy source: `deploy/Caddyfile.pgsims`
- Active Caddy path: `/etc/caddy/Caddyfile`
- Step-by-step runbook: [docs/deploy/CADDY_ROUTINE.md](docs/deploy/CADDY_ROUTINE.md)

Quick commands:

```bash
cd /srv/apps/pgsims
docker compose -f docker/docker-compose.prod.yml up -d --build
./ops/caddy_sync_reload.sh
```

## 📖 Documentation

All documentation has been consolidated under `docs/` for consistency. Start with the [documentation index](docs/README.md) to see every guide, report, and checklist that previously lived in the project root.

Key references:

- [PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md) – Up-to-date directory layout.
- [PROJECT_ORGANIZATION_GUIDE.md](docs/PROJECT_ORGANIZATION_GUIDE.md) & [COMPLETE_ORGANIZATION_GUIDE.md](docs/COMPLETE_ORGANIZATION_GUIDE.md) – Detailed notes that were relocated from the root without content changes.
- [PROJECT_SUMMARY.md](docs/PROJECT_SUMMARY.md) – Overall platform overview and readiness summary.
- [FEATURES_STATUS.md](docs/FEATURES_STATUS.md) & [SYSTEM_STATUS.md](docs/SYSTEM_STATUS.md) – Feature completeness and system health tracking.
- [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) – Common issues and remediation steps.

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork the repository** and create your branch from `main`
2. **Write clear commit messages** following the commit message format
3. **Follow the code style** guidelines (Black + Flake8)
4. **Add tests** for new features
5. **Update documentation** as needed
6. **Submit a pull request** with a clear description of changes

### Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt

# Install pre-commit hooks (optional)
pip install pre-commit
pre-commit install

# Run code quality checks before committing
black sims/ --check
flake8 sims/
python manage.py test
```

## 📄 License

This project is proprietary software developed for medical training management.

## 📞 Support

For support, issues, or questions:
- **Issues**: Open an issue on GitHub
- **Documentation**: Check the docs/ directory
- **Email**: admin@sims.com

## 🙏 Acknowledgments

- Built with [Django](https://www.djangoproject.com/)
- UI framework: [Bootstrap 5](https://getbootstrap.com/)
- Icons: [Font Awesome](https://fontawesome.com/)

---

**SIMS - Surgical Information Management System**  
*Version 1.0 - January 2025*  
*Production-Ready for Pilot Deployment*
