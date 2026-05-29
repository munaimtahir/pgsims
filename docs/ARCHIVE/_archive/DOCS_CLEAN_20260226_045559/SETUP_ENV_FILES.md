# Setting Up Environment Files

## Important Note

The `.env` files are in `.gitignore` for security reasons, so you need to create them manually from the templates.

## Required Files to Create

### Backend Environment Files

1. **Create `.env.localhost`** (for localhost deployment):
   ```powershell
   # Copy the template content from LOCALHOST_DEPLOYMENT_GUIDE.md
   # Or use deployment/server_config.localhost.env as reference
   ```

   **Minimum content for .env.localhost:**
   ```env
   SECRET_KEY=django-insecure-localhost-dev-key-change-this-min-50-chars
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   CORS_ALLOWED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000,http://localhost:3000,http://127.0.0.1:3000
   REDIS_URL=redis://localhost:6379/0
   CELERY_BROKER_URL=redis://localhost:6379/1
   CELERY_RESULT_BACKEND=redis://localhost:6379/1
   EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
   LOG_LEVEL=DEBUG
   ```

2. **Create `.env.vps`** (for VPS deployment):
   ```env
   SECRET_KEY=your-production-secret-key-here-make-it-random-and-secure-min-50-chars
   DEBUG=False
   ALLOWED_HOSTS=139.162.9.224,localhost,127.0.0.1
   CORS_ALLOWED_ORIGINS=http://139.162.9.224:81
   DB_NAME=sims_db
   DB_USER=sims_user
   DB_PASSWORD=your-secure-db-password-change-this
   DB_HOST=db
   DB_PORT=5432
   DATABASE_URL=postgresql://sims_user:your-secure-db-password-change-this@db:5432/sims_db
   REDIS_URL=redis://redis:6379/0
   CELERY_BROKER_URL=redis://redis:6379/1
   CELERY_RESULT_BACKEND=redis://redis:6379/1
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   CACHE_BACKEND=django_redis.cache.RedisCache
   CACHE_TIMEOUT=300
   LOG_LEVEL=INFO
   ```

### Frontend Environment Files

1. **Create `frontend/.env.localhost`:**
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

2. **Create `frontend/.env.vps`:**
   ```env
   NEXT_PUBLIC_API_URL=http://139.162.9.224:81
   ```

## Quick Setup

### For Localhost

```powershell
# Create backend .env.localhost
@"
SECRET_KEY=django-insecure-localhost-dev-key-change-this-min-50-chars
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000,http://localhost:3000,http://127.0.0.1:3000
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/1
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
LOG_LEVEL=DEBUG
"@ | Out-File -FilePath ".env.localhost" -Encoding utf8

# Create frontend .env.localhost
New-Item -Path "frontend\.env.localhost" -ItemType File -Force
"NEXT_PUBLIC_API_URL=http://localhost:8000" | Out-File -FilePath "frontend\.env.localhost" -Encoding utf8

# Copy to active .env
Copy-Item .env.localhost .env
Copy-Item frontend\.env.localhost frontend\.env.local
```

### For VPS

Similar process, but use the VPS values from above.

## Using the Setup Scripts

The setup scripts (`setup_localhost_windows.ps1` and `setup_localhost_windows.bat`) will automatically create `.env.localhost` if it doesn't exist, so you may not need to create it manually.

However, you should still review and customize the values after the script creates it.

## Security Note

- **NEVER commit `.env` files to git**
- **NEVER commit `.env.local` files to git**
- Use strong `SECRET_KEY` values in production
- Use strong database passwords in production
- Keep `.env.localhost` and `.env.vps` templates safe (these CAN be in git as templates)

