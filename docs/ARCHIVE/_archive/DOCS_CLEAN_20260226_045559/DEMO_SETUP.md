# SIMS Demo Setup Guide

This guide provides step-by-step instructions for setting up and running a live demonstration of the SIMS (Student Information Management System) application.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Detailed Setup](#detailed-setup)
- [Loading Demo Data](#loading-demo-data)
- [Demo Walkthrough](#demo-walkthrough)
- [Troubleshooting](#troubleshooting)

## Prerequisites

Before starting, ensure you have:

- Python 3.11 or higher
- pip (Python package manager)
- Git
- PostgreSQL 12+ (optional, SQLite works for demo)
- 4GB RAM minimum
- Modern web browser (Chrome, Firefox, Safari, or Edge)

## Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/munaimtahir/sims.git
cd sims

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env for demo (use default SQLite database)
# Set DEBUG=True for demo
# No need to configure DATABASE_URL for SQLite
```

Minimal `.env` for demo:

```env
DEBUG=True
SECRET_KEY=demo-secret-key-for-testing-only
ALLOWED_HOSTS=localhost,127.0.0.1
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

### 3. Initialize Database

```bash
# Run migrations
python manage.py migrate

# Create media directory
mkdir -p media
```

### 4. Load Demo Data

```bash
# Load comprehensive demo data
python scripts/preload_demo_data.py

# Load attendance data (optional)
python scripts/preload_attendance_data.py
```

This creates:
- 1 Admin user
- 2 Supervisor users
- 2 PG Student users
- 2 Hospitals with departments
- Multiple rotations (completed and ongoing)
- Sample certificates, logbooks, and clinical cases
- Attendance records

### 5. Start Server

```bash
# Start development server
python manage.py runserver

# Or use make command
make dev
```

Access at: **http://127.0.0.1:8000**

## Detailed Setup

### Database Configuration

#### Option 1: SQLite (Recommended for Demo)

No configuration needed! Just run migrations:

```bash
python manage.py migrate
```

#### Option 2: PostgreSQL (Production-like)

```bash
# Create database and user
sudo -u postgres psql
```

```sql
CREATE DATABASE sims_demo;
CREATE USER sims_demo WITH PASSWORD 'demo123';
GRANT ALL PRIVILEGES ON DATABASE sims_demo TO sims_demo;
\q
```

Edit `.env`:

```env
DATABASE_URL=postgresql://sims_demo:demo123@localhost:5432/sims_demo
```

Run migrations:

```bash
python manage.py migrate
```

### Static Files

```bash
# Collect static files (for production-like demo)
python manage.py collectstatic --noinput
```

## Loading Demo Data

### Automated Data Loading

The demo data scripts create realistic test data:

```bash
# Load all demo data
python scripts/preload_demo_data.py
```

This script creates:

1. **Users** (with credentials - **LOCAL DEVELOPMENT ONLY**):
   - Admin: `admin` / `admin123`
   
   **🚨 SECURITY WARNING:** These are demo credentials for local development and testing only. NEVER use these credentials in production. Always change all passwords before deploying to any production environment.
   - Supervisor 1: `dr_smith` / `supervisor123`
   - Supervisor 2: `dr_jones` / `supervisor123`
   - PG Student 1: `pg_ahmed` / `student123`
   - PG Student 2: `pg_fatima` / `student123`

2. **Organizational Structure**:
   - 2 Hospitals (FMU Teaching Hospital, Allied Hospital)
   - 8 Departments (Surgery, Medicine, Cardiology, etc.)

3. **Training Records**:
   - 4 Rotations (2 per student: 1 completed, 1 ongoing)
   - 4 Certificates (2 per student: BLS, ACLS)
   - Multiple Logbooks with entries
   - 4 Clinical Cases (2 per student)

4. **Attendance** (optional):
```bash
python scripts/preload_attendance_data.py
```

### Manual Data Creation

Alternatively, use Django admin or the UI:

1. Login as admin: http://127.0.0.1:8000/admin
2. Create users, departments, rotations manually
3. Login as supervisor/student to create content

## Demo Walkthrough

### Preparation Checklist

Before the demo, verify:

- [ ] Server is running without errors
- [ ] Demo data is loaded
- [ ] All login credentials work
- [ ] Static files are served correctly
- [ ] Media uploads directory exists and is writable

### Demo Script

#### 1. Login as Admin (5 minutes)

**URL**: http://127.0.0.1:8000/users/login/  
**Credentials**: `admin` / `admin123`

**Show**:
- Admin Dashboard with system overview
- User statistics and specialty distribution
- Quick links to manage users, rotations, certificates
- System-wide analytics

**Navigate to**:
- User Management → Show list of all users (admins, supervisors, students)
- Create a new user (demonstrate the process)
- View user details and edit permissions

#### 2. Login as Supervisor (10 minutes)

**Credentials**: `dr_smith` / `supervisor123`

**Show**:
- Supervisor Dashboard with assigned students
- Student progress tracking
- Review pending logbook entries
- Evaluate clinical cases

**Key Features to Demonstrate**:

1. **Dashboard Overview**:
   - Assigned PG students count
   - Pending reviews
   - Recent activities

2. **Logbook Review**:
   - Navigate to: Logbook → Review Entries
   - Show pending entries from students
   - Add supervisor comments
   - Approve or request revisions

3. **Clinical Case Review**:
   - Navigate to: Cases → Pending Cases
   - View case details
   - Provide feedback
   - Approve cases

4. **Student Progress**:
   - Navigate to: Analytics → Assigned Students
   - View individual student progress
   - Check certificates and rotations

#### 3. Login as PG Student (10 minutes)

**Credentials**: `pg_ahmed` / `student123`

**Show**:
- Student Dashboard with personal progress
- Current rotation details
- Create new logbook entry
- Submit clinical case

**Key Features to Demonstrate**:

1. **Dashboard Overview**:
   - Personal statistics (cases, logbooks, certificates)
   - Current rotation information
   - Recent activities

2. **Logbook Management**:
   - Navigate to: Training → Logbook
   - View existing entries
   - Create new entry:
     - Select activity type (procedure, case, seminar)
     - Add description and learning points
     - Submit for review

3. **Clinical Cases**:
   - Navigate to: Clinical Cases → New Case
   - Fill in case details:
     - Patient information
     - History and examination
     - Diagnosis and management
     - Learning points
   - Submit case
   - View existing cases and their review status

4. **Certificates**:
   - Navigate to: Training → Certificates
   - View uploaded certificates
   - Upload new certificate (demonstrate file upload)

5. **Rotations**:
   - Navigate to: Training → Rotations
   - View rotation history
   - Check current rotation details
   - View rotation evaluations

### Demo Tips

1. **Preparation**:
   - Run through the demo beforehand
   - Have multiple browser tabs open (admin, supervisor, student)
   - Prepare talking points for each section
   - Clear browser cache if needed

2. **During Demo**:
   - Start with admin view for context
   - Show workflow: Student submits → Supervisor reviews → Admin monitors
   - Highlight key features: role-based access, approval workflows, analytics
   - Demonstrate real-world scenarios (e.g., "Student submits logbook, supervisor reviews")

3. **Common Questions**:
   - **Data Security**: Explain role-based permissions
   - **Scalability**: Mention database options (PostgreSQL for production)
   - **Customization**: Show department/hospital configuration
   - **Reporting**: Demonstrate export features (CSV exports)

## Troubleshooting

### Server Won't Start

```bash
# Check for port conflicts
lsof -i :8000  # On Linux/Mac
netstat -ano | findstr :8000  # On Windows

# Try different port
python manage.py runserver 8080
```

### Static Files Not Loading

```bash
# Collect static files
python manage.py collectstatic --noinput

# Verify STATIC_ROOT and STATIC_URL in settings
python manage.py shell
>>> from django.conf import settings
>>> print(settings.STATIC_ROOT)
>>> print(settings.STATIC_URL)
```

### Database Errors

```bash
# Reset database (WARNING: Deletes all data)
rm db.sqlite3
python manage.py migrate
python scripts/preload_demo_data.py
```

### Can't Login

```bash
# Reset admin password
python manage.py changepassword admin

# Or create new superuser
python manage.py createsuperuser
```

### Media Upload Errors

```bash
# Ensure media directory exists and is writable
mkdir -p media
chmod 755 media  # On Linux/Mac
```

### Module Import Errors

```bash
# Reinstall dependencies
pip install -r requirements.txt

# Check Python version
python --version  # Should be 3.11+
```

## Post-Demo

### Resetting Demo Environment

To reset the demo environment:

```bash
# Delete database
rm db.sqlite3

# Remove media files
rm -rf media/*

# Run migrations and reload data
python manage.py migrate
python scripts/preload_demo_data.py
python scripts/preload_attendance_data.py
```

### Preparing for Production

After successful demo, for production deployment:

1. Review [POSTGRESQL_SETUP.md](docs/POSTGRESQL_SETUP.md)
2. Configure environment variables in `.env`
3. Set `DEBUG=False`
4. Configure `ALLOWED_HOSTS`
5. Set up proper email backend (SMTP)
6. Configure Gunicorn and Nginx (see `deployment/` directory)
7. Set up SSL/HTTPS certificates
8. Configure backup strategy
9. Set up monitoring and logging

## Additional Resources

- [README.md](README.md) - Project overview
- [docs/POSTGRESQL_SETUP.md](docs/POSTGRESQL_SETUP.md) - Database setup
- [deployment/](deployment/) - Production deployment files
- [docs/](docs/) - Additional documentation

## Support

For issues or questions:
- Check [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
- Open an issue on [GitHub Issues](https://github.com/munaimtahir/sims/issues)

---

**SIMS - Postgraduate Medical Training System**  
*Demo Setup Guide - Version 1.0*
