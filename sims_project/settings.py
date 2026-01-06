"""
Django settings for sims_project.

SIMS - Postgraduate Medical Training System
A comprehensive platform for managing postgraduate medical training,
rotations, certificates, workshops, logbooks, and clinical cases.

Created: 2025-05-29 16:07:57 UTC
Author: SMIB2012

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path
from django.contrib.messages import constants as messages

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).resolve().parent.parent / '.env'
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
except ImportError:
    # python-dotenv not installed, environment variables must be set manually
    pass

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY environment variable is required")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", "False").lower() in ("true", "1", "yes")

# ALLOWED_HOSTS - Support both localhost and VPS deployments
# For localhost: localhost,127.0.0.1
# For VPS: 139.162.9.224,172.237.95.120,34.124.150.231,phc.alshifalab.pk,localhost,127.0.0.1
ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get(
        "ALLOWED_HOSTS", "139.162.9.224,172.237.95.120,34.124.150.231,phc.alshifalab.pk,localhost,127.0.0.1"
    ).split(",")
    if host.strip()
]

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",  # For number formatting
    "django.contrib.postgres",
    # Third-party apps
    "corsheaders",  # For CORS support
    "crispy_forms",  # For better form rendering
    "crispy_bootstrap5",  # Bootstrap 5 support for forms
    "import_export",  # For CSV/Excel import/export
    "rest_framework",  # For API endpoints
    "rest_framework_simplejwt",  # For JWT authentication
    "django_filters",  # For Advanced filtering
    "widget_tweaks",  # For form widget customization
    "simple_history",  # For audit history
    "django_celery_beat",  # For Celery beat periodic task scheduling
    # SIMS apps
    "sims.users",
    "sims.academics",
    "sims.rotations",
    "sims.certificates",
    "sims.logbook",
    "sims.cases",
    "sims.search",
    "sims.audit",
    "sims.analytics",
    "sims.bulk",
    "sims.notifications",
    "sims.reports",
    "sims.attendance",
    "sims.results",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Serve static files efficiently
    "sims_project.middleware.HostDebugMiddleware",  # Debug: capture Host header (retain until verification)
    "corsheaders.middleware.CorsMiddleware",  # CORS middleware (should be early)
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
    "sims_project.middleware.PerformanceTimingMiddleware",  # Performance monitoring
]

ROOT_URLCONF = "sims_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",  # Global templates
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "sims.context_processors.admin_stats_context",
            ],
        },
    },
]

WSGI_APPLICATION = "sims_project.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# Support for DATABASE_URL (recommended for production)
DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    # Parse DATABASE_URL if provided
    import dj_database_url
    DATABASES = {
        "default": dj_database_url.config(default=DATABASE_URL, conn_max_age=600)
    }
else:
    # Fall back to individual settings or SQLite
    DATABASES = {
        "default": {
            "ENGINE": os.environ.get("DB_ENGINE", "django.db.backends.sqlite3"),
            "NAME": os.environ.get("DB_NAME", str(BASE_DIR / "db.sqlite3")),
            "USER": os.environ.get("DB_USER", ""),
            "PASSWORD": os.environ.get("DB_PASSWORD", ""),
            "HOST": os.environ.get("DB_HOST", ""),
            "PORT": os.environ.get("DB_PORT", ""),
        }
    }

# Custom User Model
AUTH_USER_MODEL = "users.User"

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 8,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# WhiteNoise configuration for efficient static file serving
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = DEBUG  # Only refresh in debug mode
WHITENOISE_MAX_AGE = 31536000 if not DEBUG else 0  # 1 year cache for production

# Only include static directory if it exists and has content
STATICFILES_DIRS = []
static_dir = BASE_DIR / "static"
if static_dir.exists():
    STATICFILES_DIRS.append(static_dir)

# Media files (User uploads)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Login/Logout URLs
LOGIN_URL = "/users/login/"
LOGIN_REDIRECT_URL = "/users/dashboard/"
LOGOUT_REDIRECT_URL = "/users/login/"

# Session settings
SESSION_COOKIE_AGE = 28800  # 8 hours
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True

# Security settings - hardened for production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SECURE_REFERRER_POLICY = "same-origin"

# Reverse Proxy SSL Header (for Traefik/Nginx/Cloudflare)
# This allows Django to detect HTTPS when behind a reverse proxy
# IMPORTANT: Only enable this when behind a TRUSTED reverse proxy
# Set USE_PROXY_HEADERS=False if not using a reverse proxy
USE_PROXY_HEADERS = os.environ.get("USE_PROXY_HEADERS", "True").lower() in ("true", "1", "yes")
if USE_PROXY_HEADERS:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
else:
    SECURE_PROXY_SSL_HEADER = None

# SSL/HTTPS Settings (from environment)
SECURE_SSL_REDIRECT = os.environ.get("SECURE_SSL_REDIRECT", "False").lower() in ("true", "1", "yes")
SESSION_COOKIE_SECURE = os.environ.get("SESSION_COOKIE_SECURE", str(not DEBUG)).lower() in ("true", "1", "yes")
CSRF_COOKIE_SECURE = os.environ.get("CSRF_COOKIE_SECURE", str(not DEBUG)).lower() in ("true", "1", "yes")

# CSRF Trusted Origins (for API requests from frontend)
# Expected format: comma-separated list like "https://example.com,https://app.example.com"
csrf_origins_str = os.environ.get("CSRF_TRUSTED_ORIGINS", "")
if csrf_origins_str:
    CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in csrf_origins_str.split(",") if origin.strip()]
else:
    CSRF_TRUSTED_ORIGINS = []

# HSTS Settings (from environment)
SECURE_HSTS_SECONDS = int(os.environ.get("SECURE_HSTS_SECONDS", "0" if DEBUG else "31536000"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = os.environ.get("SECURE_HSTS_INCLUDE_SUBDOMAINS", str(not DEBUG)).lower() in ("true", "1", "yes")
SECURE_HSTS_PRELOAD = os.environ.get("SECURE_HSTS_PRELOAD", "False").lower() in ("true", "1", "yes")

# Django Messages Framework
MESSAGE_TAGS = {
    messages.DEBUG: "alert-info",
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-success",
    messages.WARNING: "alert-warning",
    messages.ERROR: "alert-danger",
}

# Crispy Forms Configuration
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Django REST Framework Settings
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": int(os.environ.get("DRF_PAGE_SIZE", "25")),
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": os.environ.get("THROTTLE_ANON_RATE", "100/hour"),
        "user": os.environ.get("THROTTLE_USER_RATE", "1000/hour"),
        "search": os.environ.get("THROTTLE_SEARCH_RATE", "30/min"),
    },
}

# Email Configuration
EMAIL_BACKEND = os.environ.get(
    "EMAIL_BACKEND",
    "django.core.mail.backends.console.EmailBackend" if DEBUG else "django.core.mail.backends.smtp.EmailBackend"
)
EMAIL_HOST = os.environ.get("EMAIL_HOST", "localhost")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "True").lower() in ("true", "1", "yes")
EMAIL_USE_SSL = os.environ.get("EMAIL_USE_SSL", "False").lower() in ("true", "1", "yes")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "SIMS System <noreply@sims.medical.edu>")
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@sims.medical.edu")

# Cache Configuration (Redis)
REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
CACHES = {
    "default": {
        "BACKEND": os.environ.get("CACHE_BACKEND", "django.core.cache.backends.locmem.LocMemCache"),
        "LOCATION": REDIS_URL if "redis" in os.environ.get("CACHE_BACKEND", "") else "unique-snowflake",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        } if "redis" in os.environ.get("CACHE_BACKEND", "") else {},
    }
}

# Session Configuration
if os.environ.get("SESSION_ENGINE") == "django.contrib.sessions.backends.cache":
    SESSION_ENGINE = "django.contrib.sessions.backends.cache"
    SESSION_CACHE_ALIAS = "default"

# Celery Configuration
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/1")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/1")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 minutes

# File Upload Settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
FILE_UPLOAD_PERMISSIONS = 0o644

# Allowed file extensions for uploads
ALLOWED_UPLOAD_EXTENSIONS = [
    ".pdf",
    ".doc",
    ".docx",
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".xlsx",
    ".xls",
    ".csv",
]

# Maximum file size for uploads (in bytes)
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB

# SIMS Specific Settings
SIMS_SETTINGS = {
    # System Information
    "SYSTEM_NAME": "SIMS - Postgraduate Medical Training System",
    "SYSTEM_VERSION": "1.0.0",
    "INSTITUTION_NAME": "Medical College",
    "INSTITUTION_ADDRESS": "Medical College Address",
    "CONTACT_EMAIL": "contact@sims.medical.edu",
    "CONTACT_PHONE": "+1-234-567-8900",
    # Training Settings
    "DEFAULT_ROTATION_DURATION_MONTHS": 6,
    "MIN_LOGBOOK_ENTRIES_PER_ROTATION": 10,
    "MIN_CASES_PER_YEAR": 50,
    "REQUIRED_WORKSHOP_HOURS_PER_YEAR": 40,
    # Document Review Settings
    "AUTO_APPROVE_CERTIFICATES": False,
    "REVIEW_DEADLINE_DAYS": 7,
    "REMINDER_DAYS_BEFORE_DEADLINE": 2,
    # Notification Settings
    "SEND_EMAIL_NOTIFICATIONS": True,
    "SEND_SMS_NOTIFICATIONS": False,
    "NOTIFICATION_BATCH_SIZE": 50,
    # Analytics Settings
    "ENABLE_ANALYTICS": True,
    "ANALYTICS_RETENTION_MONTHS": 24,
    "GENERATE_MONTHLY_REPORTS": True,
    # Security Settings
    "ENABLE_TWO_FACTOR_AUTH": False,
    "PASSWORD_EXPIRY_DAYS": 90,
    "MAX_LOGIN_ATTEMPTS": 5,
    "LOCKOUT_DURATION_MINUTES": 30,
    # Backup Settings
    "AUTO_BACKUP_ENABLED": True,
    "BACKUP_RETENTION_DAYS": 30,
    "BACKUP_LOCATION": BASE_DIR / "backups",
}

GLOBAL_SEARCH_CONFIG = {
    "MAX_RESULTS": int(os.environ.get("SEARCH_MAX_RESULTS", "100")),
    "RECENT_HISTORY_LIMIT": 10,
    "SUGGESTION_LIMIT": 8,
    "DEBOUNCE_MS": 250,
}

# Logging Configuration
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logs" / "sims.log",
            "formatter": "verbose",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["file", "console"],
            "level": "INFO",
            "propagate": False,
        },
        "sims": {
            "handlers": ["file", "console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

# Create logs directory if it doesn't exist
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# Cache Configuration (Redis preferred)
REDIS_URL = os.environ.get("REDIS_URL")
if REDIS_URL:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": REDIS_URL,
            "TIMEOUT": int(os.environ.get("CACHE_TIMEOUT", "300")),
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            },
        }
    }
else:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "unique-snowflake",
            "TIMEOUT": 300,  # 5 minutes
            "OPTIONS": {
                "MAX_ENTRIES": 1000,
            },
        }
    }

# Celery Configuration (for background tasks)
# CELERY_BROKER_URL = 'redis://localhost:6379/0'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'
# CELERY_TIMEZONE = TIME_ZONE

# Import/Export Settings
IMPORT_EXPORT_USE_TRANSACTIONS = True
IMPORT_EXPORT_SKIP_ADMIN_LOG = False
IMPORT_EXPORT_TMP_STORAGE_CLASS = "import_export.tmp_storages.TempFolderStorage"

# Django Extensions (if using)
# INSTALLED_APPS += ['django_extensions']

# Environment-specific settings
if DEBUG:
    # Development settings
    INTERNAL_IPS = ["127.0.0.1", "localhost"]

    # Debug toolbar (if installed)
    try:
        import debug_toolbar

        INSTALLED_APPS.append("debug_toolbar")
        MIDDLEWARE.insert(1, "debug_toolbar.middleware.DebugToolbarMiddleware")
        DEBUG_TOOLBAR_CONFIG = {
            "SHOW_TOOLBAR_CALLBACK": lambda request: DEBUG,
        }
    except ImportError:
        pass

else:
    # Production settings
    SECURE_SSL_REDIRECT = False  # Set to True when SSL is configured
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SESSION_COOKIE_SECURE = False  # Set to True when SSL is configured
    CSRF_COOKIE_SECURE = False  # Set to True when SSL is configured

    # Use environment variables for sensitive data
    SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", SECRET_KEY)
    # ALLOWED_HOSTS is already set at the top of the file from ALLOWED_HOSTS env var
    # Only override if DJANGO_ALLOWED_HOSTS is explicitly set
    django_allowed_hosts = os.environ.get("DJANGO_ALLOWED_HOSTS")
    if django_allowed_hosts:
        ALLOWED_HOSTS = [host.strip() for host in django_allowed_hosts.split(",") if host.strip()]

    # Database from environment (SQLite for now, PostgreSQL for full production)
    if os.environ.get("DB_NAME"):
        DATABASES["default"].update(
            {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": os.environ.get("DB_NAME"),
                "USER": os.environ.get("DB_USER"),
                "PASSWORD": os.environ.get("DB_PASSWORD"),
                "HOST": os.environ.get("DB_HOST", "localhost"),
                "PORT": os.environ.get("DB_PORT", "5432"),
            }
        )

    # Email settings from environment
    if os.environ.get("EMAIL_HOST"):
        EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
        EMAIL_HOST = os.environ.get("EMAIL_HOST")
        EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 587))
        EMAIL_USE_TLS = True
        EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
        EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")

# Logging Configuration
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{levelname}] {asctime} {name} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "handlers": {
        "console": {
            "level": LOG_LEVEL,
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "file": {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": BASE_DIR / "logs" / "sims_error.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "django.request": {
            "handlers": ["console", "file"],
            "level": "ERROR",
            "propagate": False,
        },
        "sims": {
            "handlers": ["console", "file"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
    },
}

# JWT Settings for REST Framework SimpleJWT
from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=int(os.environ.get("JWT_ACCESS_TOKEN_MINUTES", "60"))),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=int(os.environ.get("JWT_REFRESH_TOKEN_DAYS", "7"))),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
}

# Attendance eligibility threshold
ATTENDANCE_THRESHOLD = float(os.environ.get("ATTENDANCE_THRESHOLD", "75.0"))

# CORS Configuration for frontend - explicit origins only
# Supports both localhost and VPS deployments
cors_origins_env = os.environ.get("CORS_ALLOWED_ORIGINS", "")
if cors_origins_env:
    CORS_ALLOWED_ORIGINS = [origin.strip() for origin in cors_origins_env.split(",") if origin.strip()]
else:
    # Default origins based on DEBUG mode
    if DEBUG:
        # Localhost development defaults
        CORS_ALLOWED_ORIGINS = [
            "http://localhost:8000",
            "http://127.0.0.1:8000",
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ]
    else:
        # Production/VPS - must be explicitly set
        CORS_ALLOWED_ORIGINS = []

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# Login rate limiting (cache-based)
LOGIN_RATE_LIMIT = os.environ.get("LOGIN_RATE_LIMIT", "5/min")
LOGIN_RATE_LIMIT_BLOCK_DURATION = int(os.environ.get("LOGIN_RATE_LIMIT_BLOCK_DURATION", "300"))  # 5 minutes

# Load local settings if available
try:
    from .local_settings import *
except ImportError:
    pass
