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

SIMS (Surgical Information Management System) is a comprehensive web-based management system designed specifically for postgraduate medical training programs. It provides a complete solution for tracking trainee progress, managing rotations, maintaining digital logbooks, and handling clinical case submissions.

**Current Status**: ✅ **Production-Ready for Pilot Deployment**

**Deployment**: Now supports **Coolify/Traefik** for easy single-VPS deployment with automatic HTTPS! See [docs/DEPLOY_COOLIFY_TRAEFIK.md](docs/DEPLOY_COOLIFY_TRAEFIK.md) for the recommended production deployment method.

## ✨ Features

### Core Features (Ready to Use)

- **👥 User Management**: Role-based access control for admins, supervisors, and postgraduate students
- **📊 Dashboard System**: Customized dashboards for each user role with analytics
- **🔄 Rotation Management**: Track and manage training rotations across different departments
- **📜 Certificate Management**: Manage and track certifications and achievements
- **📚 Digital Logbook**: Record training activities, procedures, and evaluations
- **🏥 Clinical Cases**: Submit, review, and manage clinical cases with detailed documentation
- **📈 Analytics & Reporting**: Comprehensive statistics and data visualization
- **🔍 Advanced Filtering**: Search and filter capabilities across all modules
- **📤 Data Export**: Export data to CSV format for all major modules
- **🔐 Security**: Role-based permissions, secure authentication, and session management
- **🌐 Global Search**: Cross-module search with suggestions, highlights, and per-user history
- **🛡️ Audit Trail**: Historical tracking for key models plus Activity Log APIs and CSV export
- **✅ Business Rules Engine**: Centralised validators, sanitisation and consistent error handling

### Additional Features

- **Admin Interface**: Comprehensive Django admin with custom branding
- **RESTful APIs**: JSON endpoints for statistics and data retrieval
- **File Management**: Upload and manage documents and images
- **Responsive Design**: Mobile-friendly Bootstrap 5 interface
- **PMC Theme**: Professional medical college branding throughout

For a detailed breakdown of all features by development status, see [FEATURES_STATUS.md](docs/FEATURES_STATUS.md).

## 📊 Development Status

The SIMS application has completed its initial development phase with the following status:

- **✅ Ready to Use**: ~90 features (60%) - Fully functional and production-ready
- **⚠️ Needs Work**: ~25 features (17%) - Implemented but requires debugging or completion
- **🔜 Planned**: ~35 features (23%) - Yet to be built

### Module Status Summary

| Module | Completion | Status |
|--------|------------|--------|
| Authentication | 100% | ✅ Complete |
| User Management | 95% | ✅ Nearly Complete |
| Dashboards | 100% | ✅ Complete |
| Clinical Cases | 90% | ✅ Functional |
| Digital Logbook | 95% | ✅ Nearly Complete |
| Certificates | 95% | ✅ Nearly Complete |
| Rotations | 90% | ✅ Functional |
| Admin Interface | 100% | ✅ Complete |
| UI/UX | 95% | ✅ Nearly Complete |

See [docs/FEATURES_STATUS.md](docs/FEATURES_STATUS.md) for complete feature categorization.

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

## 🖥️ Deployment Options

SIMS supports deployment on both **localhost** (for development and local demonstrations) and **VPS** (for production).

### Localhost Deployment

For local development and demonstrations:

**Quick Start:**
```bash
# Automated setup (Windows)
.\scripts\setup_localhost_windows.ps1

# Or manual deployment
python manage.py migrate
python manage.py runserver
```

**Access:** http://localhost:8000/

### VPS Deployment

For production deployment on a VPS:

**Quick Start:**
```bash
# Deploy with Docker
docker compose up -d --build
docker compose exec web python manage.py migrate
```

See [docs/DEPLOY_COOLIFY_TRAEFIK.md](docs/DEPLOY_COOLIFY_TRAEFIK.md) for the recommended production deployment method.

### Environment Configuration Files

- **Localhost:** `.env.localhost` → copy to `.env`
- **VPS:** `.env.vps` → copy to `.env`
- **Template:** `.env.example` (reference only)

**Frontend Configuration:**
- **Localhost:** `frontend/.env.localhost` → copy to `frontend/.env.local`
- **VPS:** `frontend/.env.vps` → copy to `frontend/.env.local`

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
├── deploy/                 # 🚀 Deployment Scripts & Configs
│   ├── Caddyfile.pgsims    # Caddy reverse proxy config
│   └── deploy*.sh          # VPS deployment utilities
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
- **web**: Django application (Gunicorn)
- **worker**: Celery worker for background tasks
- **beat**: Celery beat scheduler
- **nginx**: Reverse proxy and static file server

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

- `81`: Nginx (HTTP)
- `443`: Nginx (HTTPS)
- `8000`: Django (internal, proxied through nginx)

## 🚀 Deployment

### Localhost Deployment (Development)

For local development and demonstrations:

1. **Quick Setup:**
   ```bash
   # For Windows
   .\scripts\setup_localhost_windows.ps1
   
   # For Linux/Mac
   python manage.py migrate
   python manage.py runserver
   ```

2. **Access:** http://localhost:8000/

See [docs/LOCAL_DEV.md](docs/LOCAL_DEV.md) for complete development instructions.

### VPS Deployment (Production)

For production deployment on VPS:

1. **Deploy:**
   ```bash
   docker compose up -d --build
   ```

2. **Access your domain or IP**

See [docs/DEPLOY_COOLIFY_TRAEFIK.md](docs/DEPLOY_COOLIFY_TRAEFIK.md) for complete production deployment instructions.

### Frontend Environment Setup

**For localhost:**
```bash
cp frontend/.env.local.example frontend/.env.local
# Edit frontend/.env.local with your settings
```

**For production:**
```bash
cp frontend/.env.local.example frontend/.env.local
# Update NEXT_PUBLIC_API_URL with your production API URL
```

### Production Deployment Options

SIMS offers multiple deployment methods:

#### 1. Coolify/Traefik Deployment (Recommended)

**Best for:** Single VPS, automatic SSL, easy management

```bash
# Use the Coolify-ready compose file
docker-compose -f docker-compose.coolify.yml up -d
```

**Features:**
- ✅ Automatic HTTPS with Let's Encrypt (via Coolify/Traefik)
- ✅ No nginx configuration needed
- ✅ WhiteNoise serves static files efficiently
- ✅ Zero port 80/443 conflicts
- ✅ Built-in health checks

See **[docs/DEPLOY_COOLIFY_TRAEFIK.md](docs/DEPLOY_COOLIFY_TRAEFIK.md)** for complete guide.

#### 2. Docker Compose (Direct)

**Best for:** Custom VPS setup with your own reverse proxy

```bash
# Standard deployment
docker-compose up -d
```

See [docs/DEPLOY_COOLIFY_TRAEFIK.md](docs/DEPLOY_COOLIFY_TRAEFIK.md) for complete deployment instructions.

#### 3. Local Development

**Best for:** Development and testing

```bash
# Local development with hot reload
docker-compose -f docker-compose.local.yml up -d
```

See **[docs/LOCAL_DEV.md](docs/LOCAL_DEV.md)** for complete development guide.

### Quick Start

#### Local Development (5 minutes)
```bash
# 1. Clone repository
git clone https://github.com/munaimtahir/sims.git
cd sims

# 2. Create environment file
cp .env.example .env
# Edit .env with your settings

# 3. Start services
docker-compose -f docker-compose.local.yml up -d

# 4. Create admin user
docker-compose -f docker-compose.local.yml exec web python manage.py createsuperuser

# 5. Access application
open http://localhost:8000
```

#### Coolify Deployment (10 minutes)
See **[docs/DEPLOY_COOLIFY_TRAEFIK.md](docs/DEPLOY_COOLIFY_TRAEFIK.md)** for step-by-step Coolify deployment.

### Production Deployment Checklist

For production deployment, consider:

1. **Environment Configuration**
   - Set `DEBUG = False` in environment variables
   - Use environment variables for all sensitive data
   - Configure `ALLOWED_HOSTS` with your domain(s)
   - Set `SECRET_KEY` to a secure random value

2. **Database**
   - Use PostgreSQL for production
   - Configure proper database backup strategy
   - Set strong database passwords

3. **Static Files**
   - Collect static files: `python manage.py collectstatic`
   - Serve via nginx or CDN
   - Configure media file storage

4. **Web Server**
   - Use Gunicorn or uWSGI (included in Docker setup)
   - Configure nginx as reverse proxy (included in Docker setup)
   - Set up SSL/TLS certificates for HTTPS

5. **Security Checklist**
   - ✅ `SECRET_KEY` set from environment (REQUIRED)
   - ✅ `DEBUG = False` in production
   - ✅ `ALLOWED_HOSTS` configured with your domain
   - ✅ Strong database passwords
   - ✅ HTTPS/SSL configured
   - ✅ Security headers enabled (`SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, etc.)
   - ✅ CORS origins restricted to your frontend domain
   - ✅ No default credentials in production
   - ✅ Regular security updates
   - ✅ Database backups configured
   - ✅ Logging configured

6. **Celery**
   - Celery worker running for background tasks
   - Celery beat running for scheduled tasks
   - Redis configured as broker and result backend

See [docs/DEPLOY_COOLIFY_TRAEFIK.md](docs/DEPLOY_COOLIFY_TRAEFIK.md) for detailed deployment instructions.

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
