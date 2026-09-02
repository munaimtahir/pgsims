"""
Test settings for local/CI test runs.

Uses base settings but switches staticfiles storage to non-manifest storage and
relaxes a few expensive production settings to make tests deterministic.
"""

from .settings import *  # noqa: F401,F403

DEBUG = True

# Avoid manifest/staticfiles lookup failures in tests without collectstatic.
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# Faster hashing for tests.
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# Keep tests local and deterministic.
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Disable file-based logging during tests to avoid missing logs/ directory errors.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
}

# Disable all throttling during tests.
REST_FRAMEWORK = {
    **globals().get("REST_FRAMEWORK", {}),
    "DEFAULT_THROTTLE_CLASSES": [],
    "DEFAULT_THROTTLE_RATES": {},
}

# Use in-memory cache so throttle counters don't bleed from production Redis.
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

# Set a very high login rate limit so throttling never triggers in tests.
LOGIN_RATE_LIMIT = "10000/min"
LOGIN_RATE_LIMIT_BLOCK_DURATION = 1

import tempfile
import atexit
import shutil

# Use a temporary directory for media files during tests
TEMP_MEDIA_ROOT = tempfile.mkdtemp(prefix='django_tests_media_')
MEDIA_ROOT = TEMP_MEDIA_ROOT

# Clean up the temporary directory on exit
atexit.register(lambda: shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True))
