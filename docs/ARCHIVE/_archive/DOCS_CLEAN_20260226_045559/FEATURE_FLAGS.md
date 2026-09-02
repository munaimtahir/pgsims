# Feature Flags & Environment Configuration - SIMS v1.0.0

This document describes all environment variables and feature flags available in SIMS.

## Core Settings

### SECRET_KEY
**Type:** String (required)  
**Default:** `django-insecure-your-secret-key-change-in-production`  
**Production:** Must be set to a secure random value  
**Example:** `SECRET_KEY=your-super-secret-key-here`

### DEBUG
**Type:** Boolean  
**Default:** `True`  
**Production:** Must be `False`  
**Values:** `true`, `false`, `1`, `0`, `yes`, `no` (case-insensitive)  
**Example:** `DEBUG=False`

### ALLOWED_HOSTS
**Type:** Comma-separated string  
**Default:** `localhost,127.0.0.1,0.0.0.0,testserver,139.162.9.224`  
**Production:** Set to your actual domains  
**Example:** `ALLOWED_HOSTS=example.com,www.example.com`

## Database Configuration

### DATABASE_URL
**Type:** Database URL string  
**Default:** SQLite (file-based)  
**Production:** PostgreSQL recommended  
**Format:** `postgresql://user:password@host:port/database`  
**Example:** `DATABASE_URL=postgresql://sims_user:password@localhost:5432/sims_db`

## Cache & Performance

### REDIS_URL
**Type:** Redis connection string  
**Default:** `redis://localhost:6379/0`  
**Optional:** Yes (falls back to local memory cache)  
**Example:** `REDIS_URL=redis://localhost:6379/0`

### CACHE_BACKEND
**Type:** String  
**Default:** `django.core.cache.backends.locmem.LocMemCache`  
**Options:**
- `django_redis.cache.RedisCache` (requires REDIS_URL)
- `django.core.cache.backends.locmem.LocMemCache`
- `django.core.cache.backends.dummy.DummyCache` (testing)  
**Example:** `CACHE_BACKEND=django_redis.cache.RedisCache`

### CACHE_TIMEOUT
**Type:** Integer (seconds)  
**Default:** `300`  
**Example:** `CACHE_TIMEOUT=600`

## Search Configuration

### SEARCH_MAX_RESULTS
**Type:** Integer  
**Default:** `100`  
**Description:** Maximum number of search results to return  
**Example:** `SEARCH_MAX_RESULTS=50`

## Email Configuration

### EMAIL_BACKEND
**Type:** String  
**Default:** `django.core.mail.backends.console.EmailBackend` (DEBUG=True)  
**Production:** `django.core.mail.backends.smtp.EmailBackend`  
**Example:** `EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend`

### EMAIL_HOST
**Type:** String  
**Default:** `localhost`  
**Example:** `EMAIL_HOST=smtp.gmail.com`

### EMAIL_PORT
**Type:** Integer  
**Default:** `587`  
**Common values:** 25, 465 (SSL), 587 (TLS)  
**Example:** `EMAIL_PORT=587`

### EMAIL_USE_TLS
**Type:** Boolean  
**Default:** `True`  
**Example:** `EMAIL_USE_TLS=True`

### EMAIL_USE_SSL
**Type:** Boolean  
**Default:** `False`  
**Example:** `EMAIL_USE_SSL=False`

### EMAIL_HOST_USER
**Type:** String  
**Default:** Empty  
**Example:** `EMAIL_HOST_USER=your-email@gmail.com`

### EMAIL_HOST_PASSWORD
**Type:** String  
**Default:** Empty  
**Example:** `EMAIL_HOST_PASSWORD=your-app-password`

### DEFAULT_FROM_EMAIL
**Type:** String  
**Default:** `SIMS System <noreply@sims.medical.edu>`  
**Example:** `DEFAULT_FROM_EMAIL=noreply@yourdomain.com`

## Celery Configuration

### CELERY_BROKER_URL
**Type:** String  
**Default:** `redis://localhost:6379/1`  
**Required for:** Scheduled reports, async tasks  
**Example:** `CELERY_BROKER_URL=redis://localhost:6379/1`

### CELERY_RESULT_BACKEND
**Type:** String  
**Default:** `redis://localhost:6379/1`  
**Example:** `CELERY_RESULT_BACKEND=redis://localhost:6379/1`

## Security Settings

### SECURE_SSL_REDIRECT
**Type:** Boolean  
**Default:** `False`  
**Production:** `True` if using HTTPS  
**Example:** `SECURE_SSL_REDIRECT=True`

### SESSION_COOKIE_SECURE
**Type:** Boolean  
**Default:** `True` when DEBUG=False  
**Example:** `SESSION_COOKIE_SECURE=True`

### CSRF_COOKIE_SECURE
**Type:** Boolean  
**Default:** `True` when DEBUG=False  
**Example:** `CSRF_COOKIE_SECURE=True`

### SECURE_HSTS_SECONDS
**Type:** Integer  
**Default:** `0` (DEBUG=True), `31536000` (DEBUG=False)  
**Production:** `31536000` (1 year)  
**Example:** `SECURE_HSTS_SECONDS=31536000`

## API Throttling

### THROTTLE_ANON_RATE
**Type:** String (rate/period)  
**Default:** `100/hour`  
**Example:** `THROTTLE_ANON_RATE=50/hour`

### THROTTLE_USER_RATE
**Type:** String (rate/period)  
**Default:** `1000/hour`  
**Example:** `THROTTLE_USER_RATE=2000/hour`

### THROTTLE_SEARCH_RATE
**Type:** String (rate/period)  
**Default:** `30/min`  
**Example:** `THROTTLE_SEARCH_RATE=60/min`

### DRF_PAGE_SIZE
**Type:** Integer  
**Default:** `25`  
**Description:** Default pagination size for API endpoints  
**Example:** `DRF_PAGE_SIZE=50`

## Feature Flags (SIMS_SETTINGS)

These are configured in `settings.py` and can be overridden via environment:

### ENABLE_ANALYTICS
**Type:** Boolean  
**Default:** `True`  
**Description:** Enable analytics features  

### ENABLE_TWO_FACTOR_AUTH
**Type:** Boolean  
**Default:** `False`  
**Description:** Enable 2FA for users (future feature)  

### AUTO_APPROVE_CERTIFICATES
**Type:** Boolean  
**Default:** `False`  
**Description:** Automatically approve certificates  

### SEND_EMAIL_NOTIFICATIONS
**Type:** Boolean  
**Default:** `True`  
**Description:** Enable email notifications  

### SEND_SMS_NOTIFICATIONS
**Type:** Boolean  
**Default:** `False`  
**Description:** Enable SMS notifications (future feature)  

## Example Production .env File

```bash
# Core
SECRET_KEY=your-super-secret-key-here-change-this
DEBUG=False
ALLOWED_HOSTS=sims.example.com,www.sims.example.com

# Database
DATABASE_URL=postgresql://sims_user:secure_password@localhost:5432/sims_production

# Cache
REDIS_URL=redis://localhost:6379/0
CACHE_BACKEND=django_redis.cache.RedisCache
CACHE_TIMEOUT=600

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=noreply@example.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=SIMS System <noreply@example.com>

# Celery
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/1

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000

# Search
SEARCH_MAX_RESULTS=100

# API
THROTTLE_USER_RATE=2000/hour
THROTTLE_SEARCH_RATE=60/min
DRF_PAGE_SIZE=25
```

## Environment-Specific Notes

### Development
- DEBUG=True
- SQLite database is fine
- Console email backend
- No Redis required (optional)

### Staging
- DEBUG=False
- PostgreSQL recommended
- SMTP email backend
- Redis recommended

### Production
- DEBUG=False (mandatory)
- PostgreSQL (mandatory)
- SMTP email backend (mandatory)
- Redis (highly recommended)
- HTTPS/SSL enabled
- All security settings enabled

## Validation

Check your configuration:
```bash
python manage.py check --deploy
```

This will warn you about any production security issues.
