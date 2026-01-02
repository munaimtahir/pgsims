# PostgreSQL Setup for SIMS

This guide provides step-by-step instructions for setting up PostgreSQL as the database backend for SIMS.

## Prerequisites

- PostgreSQL 12 or higher
- Admin access to create databases and users

## Installation

### Ubuntu/Debian

```bash
# Update package list
sudo apt update

# Install PostgreSQL and contrib package
sudo apt install postgresql postgresql-contrib

# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### macOS (via Homebrew)

```bash
# Install PostgreSQL
brew install postgresql

# Start PostgreSQL service
brew services start postgresql
```

### Windows

Download and install PostgreSQL from [postgresql.org](https://www.postgresql.org/download/windows/)

## Database Setup

### 1. Create Database and User

Connect to PostgreSQL as the postgres superuser:

```bash
sudo -u postgres psql
```

Or on macOS/Windows (if postgres user has no password):

```bash
psql -U postgres
```

Then execute the following SQL commands:

```sql
-- Create database
CREATE DATABASE sims_db;

-- Create user with password
CREATE USER sims_user WITH PASSWORD 'your_secure_password_here';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE sims_db TO sims_user;

-- Grant schema privileges (PostgreSQL 15+)
\c sims_db
GRANT ALL ON SCHEMA public TO sims_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO sims_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO sims_user;

-- Exit psql
\q
```

### 2. Verify Connection

Test the connection:

```bash
psql -U sims_user -d sims_db -h localhost
```

Enter the password when prompted. If successful, you'll see the PostgreSQL prompt.

## Configuration for SIMS

### Option 1: Using DATABASE_URL (Recommended)

Create or edit `.env` file in the project root:

```bash
# Copy example environment file
cp .env.example .env
```

Edit `.env` and set:

```env
# Use DATABASE_URL format (recommended)
DATABASE_URL=postgresql://sims_user:your_secure_password_here@localhost:5432/sims_db

# Or for remote database:
DATABASE_URL=postgresql://sims_user:password@db.example.com:5432/sims_db
```

### Option 2: Using Individual Settings

Alternatively, you can use individual database settings:

```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=sims_db
DB_USER=sims_user
DB_PASSWORD=your_secure_password_here
DB_HOST=localhost
DB_PORT=5432
```

### Development vs Production

**Development (.env.local or .env with DEBUG=True):**

```env
DEBUG=True
DATABASE_URL=postgresql://sims_user:dev_password@localhost:5432/sims_dev_db
```

**Production (.env with DEBUG=False):**

```env
DEBUG=False
DATABASE_URL=postgresql://sims_user:strong_prod_password@localhost:5432/sims_db
SECRET_KEY=your-very-long-random-secret-key-min-50-characters
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
```

## Migration and Setup

After configuring the database:

```bash
# Install dependencies (if not already done)
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Load demo data (optional)
python manage.py loaddata demo_data
```

## PostgreSQL Configuration (Optional)

### For Better Performance

Edit PostgreSQL configuration file (location varies by OS):

- Ubuntu/Debian: `/etc/postgresql/[version]/main/postgresql.conf`
- macOS (Homebrew): `/opt/homebrew/var/postgresql@[version]/postgresql.conf`

Suggested settings for a development server:

```conf
# Memory Settings
shared_buffers = 256MB
effective_cache_size = 1GB
work_mem = 10MB
maintenance_work_mem = 64MB

# Connection Settings
max_connections = 100

# Query Planning
random_page_cost = 1.1
effective_io_concurrency = 200
```

Restart PostgreSQL after changes:

```bash
sudo systemctl restart postgresql
```

## Backup and Restore

### Backup Database

```bash
# Full database backup
pg_dump -U sims_user -d sims_db -F c -f sims_backup_$(date +%Y%m%d).dump

# SQL format backup
pg_dump -U sims_user -d sims_db > sims_backup_$(date +%Y%m%d).sql
```

### Restore Database

```bash
# From custom format
pg_restore -U sims_user -d sims_db -c sims_backup_20231201.dump

# From SQL format
psql -U sims_user -d sims_db < sims_backup_20231201.sql
```

## Troubleshooting

### Connection Refused

If you get "connection refused" errors:

1. Check PostgreSQL is running:
   ```bash
   sudo systemctl status postgresql
   ```

2. Check PostgreSQL is listening on the correct port:
   ```bash
   sudo netstat -plunt | grep 5432
   ```

3. Check `pg_hba.conf` allows local connections:
   ```bash
   sudo nano /etc/postgresql/[version]/main/pg_hba.conf
   ```
   
   Ensure this line exists:
   ```
   host    all             all             127.0.0.1/32            md5
   ```

### Authentication Failed

If you get authentication errors:

1. Verify user exists and has password:
   ```sql
   \du  -- List all users
   ```

2. Reset password if needed:
   ```sql
   ALTER USER sims_user WITH PASSWORD 'new_password';
   ```

### Permission Denied

If you get permission errors:

```sql
-- Connect as superuser
sudo -u postgres psql

-- Grant necessary permissions
\c sims_db
GRANT ALL PRIVILEGES ON DATABASE sims_db TO sims_user;
GRANT ALL ON SCHEMA public TO sims_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO sims_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO sims_user;
```

## Using SQLite for Development

If you prefer SQLite for local development, simply don't set `DATABASE_URL`:

```env
# .env for development
DEBUG=True
# DATABASE_URL not set - will default to SQLite
```

The system will automatically use SQLite (`db.sqlite3`) when `DATABASE_URL` is not configured.

## Security Best Practices

1. **Never commit** `.env` file to version control
2. **Use strong passwords** for production databases
3. **Restrict database access** to specific IP addresses in production
4. **Regular backups** - automate daily backups
5. **Update PostgreSQL** regularly for security patches
6. **Use SSL connections** for remote databases:
   ```env
   DATABASE_URL=postgresql://user:pass@host:5432/db?sslmode=require
   ```

## Additional Resources

- [Django PostgreSQL Notes](https://docs.djangoproject.com/en/4.2/ref/databases/#postgresql-notes)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [psycopg2 Documentation](https://www.psycopg.org/docs/)
