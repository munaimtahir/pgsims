# Environment Variables Documentation

Complete reference for all environment variables used in SIMS.

## Core Django Settings

### SECRET_KEY
- **Required**: Yes (production)
- **Default**: Insecure key for development
- **Description**: Django secret key for cryptographic signing
- **Example**: `SECRET_KEY=your-secret-key-min-50-chars-random-string`
- **Generation**: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`

### DEBUG
- **Required**: No
- **Default**: `True` in development, `False` in production
- **Values**: `True`, `False`, `1`, `0`, `yes`, `no`
- **Description**: Enable/disable debug mode
- **Example**: `DEBUG=False`
- **⚠️ WARNING**: Never set to `True` in production

### ALLOWED_HOSTS
- **Required**: Yes (production)
- **Default**: `localhost,127.0.0.1,0.0.0.0,testserver`
- **Format**: Comma-separated list
- **Description**: Allowed hostnames for the application
- **Example**: `ALLOWED_HOSTS=example.com,www.example.com,api.example.com`

## Database Configuration

### DATABASE_URL (Recommended)
- **Required**: No
- **Default**: SQLite database
- **Format**: Database URL
- **Description**: Complete database connection string
- **Examples**:
  - PostgreSQL: `postgresql://user:password@localhost:5432/sims_db`
  - SQLite: `sqlite:///db.sqlite3`
  - MySQL: `mysql://user:password@localhost:3306/sims_db`

### Individual Database Settings (Alternative to DATABASE_URL)

#### DB_ENGINE
- **Default**: `django.db.backends.sqlite3`
- **Options**: 
  - `django.db.backends.postgresql`
  - `django.db.backends.mysql`
  - `django.db.backends.sqlite3`

#### DB_NAME
- **Default**: `db.sqlite3`
- **Example**: `sims_db`

#### DB_USER
- **Default**: Empty
- **Example**: `sims_user`

#### DB_PASSWORD
- **Default**: Empty
- **Example**: `secure_password_here`

#### DB_HOST
- **Default**: Empty (localhost)
- **Example**: `localhost`, `db`, `postgres.example.com`

#### DB_PORT
- **Default**: Empty
- **Example**: `5432` (PostgreSQL), `3306` (MySQL)

## Redis & Caching

### REDIS_URL
- **Required**: No
- **Default**: `redis://localhost:6379/0`
- **Description**: Redis connection URL for caching
- **Example**: `redis://redis:6379/0`

### CACHE_BACKEND
- **Default**: `django.core.cache.backends.locmem.LocMemCache`
- **For Redis**: `django_redis.cache.RedisCache`
- **Description**: Django cache backend class

### SESSION_ENGINE
- **Default**: File-based sessions
- **For cache**: `django.contrib.sessions.backends.cache`
- **Description**: Session storage backend

## Celery Configuration

### CELERY_BROKER_URL
- **Required**: For async tasks
- **Default**: `redis://localhost:6379/1`
- **Description**: Message broker URL for Celery
- **Example**: `redis://redis:6379/1`

### CELERY_RESULT_BACKEND
- **Required**: For task results
- **Default**: `redis://localhost:6379/1`
- **Description**: Results storage for Celery tasks
- **Example**: `redis://redis:6379/1`

## Email Configuration

### EMAIL_BACKEND
- **Default**: `console` in dev, `smtp` in production
- **Options**:
  - `django.core.mail.backends.smtp.EmailBackend` (production)
  - `django.core.mail.backends.console.EmailBackend` (development)
  - `django.core.mail.backends.locmem.EmailBackend` (testing)

### EMAIL_HOST
- **Required**: For SMTP
- **Example**: `smtp.gmail.com`, `smtp.sendgrid.net`

### EMAIL_PORT
- **Default**: `587`
- **Common values**: `587` (TLS), `465` (SSL), `25` (plain)

### EMAIL_USE_TLS
- **Default**: `True`
- **Values**: `True`, `False`
- **Description**: Use TLS encryption

### EMAIL_USE_SSL
- **Default**: `False`
- **Values**: `True`, `False`
- **Description**: Use SSL encryption (mutually exclusive with TLS)

### EMAIL_HOST_USER
- **Required**: For authenticated SMTP
- **Example**: `noreply@example.com`

### EMAIL_HOST_PASSWORD
- **Required**: For authenticated SMTP
- **Example**: `your-email-app-password`

### DEFAULT_FROM_EMAIL
- **Default**: `SIMS System <noreply@sims.medical.edu>`
- **Example**: `SIMS <noreply@yourdomain.com>`

## Security Settings

### SECURE_SSL_REDIRECT
- **Default**: `False` in dev, `True` in production
- **Values**: `True`, `False`
- **Description**: Redirect HTTP to HTTPS

### SESSION_COOKIE_SECURE
- **Default**: Same as `DEBUG` inverse
- **Values**: `True`, `False`
- **Description**: Only send session cookies over HTTPS

### CSRF_COOKIE_SECURE
- **Default**: Same as `DEBUG` inverse
- **Values**: `True`, `False`
- **Description**: Only send CSRF cookies over HTTPS

### SECURE_HSTS_SECONDS
- **Default**: `0` in dev, `31536000` (1 year) in production
- **Description**: HTTP Strict Transport Security duration
- **Example**: `31536000`

### SECURE_HSTS_INCLUDE_SUBDOMAINS
- **Default**: `False` in dev, `True` in production
- **Values**: `True`, `False`

### SECURE_HSTS_PRELOAD
- **Default**: `False`
- **Values**: `True`, `False`
- **Description**: Enable HSTS preloading (for hsts preload list)

## API & Throttling

### DRF_PAGE_SIZE
- **Default**: `25`
- **Description**: Default page size for API pagination

### THROTTLE_ANON_RATE
- **Default**: `100/hour`
- **Format**: `number/period` (min, hour, day)
- **Description**: Anonymous user throttle rate

### THROTTLE_USER_RATE
- **Default**: `1000/hour`
- **Description**: Authenticated user throttle rate

### THROTTLE_SEARCH_RATE
- **Default**: `30/min`
- **Description**: Search API throttle rate

## Storage Configuration

### STORAGE_BACKEND
- **Default**: `local`
- **Options**: `local`, `s3`
- **Description**: File storage backend

### AWS_ACCESS_KEY_ID
- **Required**: For S3 storage
- **Description**: AWS access key

### AWS_SECRET_ACCESS_KEY
- **Required**: For S3 storage
- **Description**: AWS secret key

### AWS_STORAGE_BUCKET_NAME
- **Required**: For S3 storage
- **Example**: `sims-media-files`

### AWS_S3_REGION_NAME
- **Default**: `us-east-1`
- **Example**: `eu-west-1`

## Application-Specific

### ATTENDANCE_THRESHOLD
- **Default**: `75.0`
- **Range**: `0.0` to `100.0`
- **Description**: Minimum attendance percentage for eligibility

### LOG_LEVEL
- **Default**: `INFO`
- **Options**: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
- **Description**: Logging verbosity level

## CORS Configuration (Optional)

### CORS_ALLOWED_ORIGINS
- **Default**: None
- **Format**: Comma-separated URLs
- **Example**: `https://app.example.com,https://admin.example.com`

### CORS_ALLOW_CREDENTIALS
- **Default**: `True`
- **Values**: `True`, `False`

## Monitoring (Optional)

### SENTRY_DSN
- **Required**: For Sentry error tracking
- **Example**: `https://xxx@sentry.io/xxx`

## Example .env File for Production

```env
# Core
SECRET_KEY=your-50-char-random-secret-key-here
DEBUG=False
ALLOWED_HOSTS=example.com,www.example.com

# Database
DATABASE_URL=postgresql://sims_user:secure_password@db:5432/sims_db

# Redis & Celery
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/1
CELERY_RESULT_BACKEND=redis://redis:6379/1

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=SG.xxx
DEFAULT_FROM_EMAIL=SIMS <noreply@example.com>

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True

# Throttling
THROTTLE_ANON_RATE=100/hour
THROTTLE_USER_RATE=1000/hour

# Application
ATTENDANCE_THRESHOLD=75.0
LOG_LEVEL=INFO
```
