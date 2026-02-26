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

import tempfile
import atexit
import shutil

# Use a temporary directory for media files during tests
TEMP_MEDIA_ROOT = tempfile.mkdtemp(prefix='django_tests_media_')
MEDIA_ROOT = TEMP_MEDIA_ROOT

# Clean up the temporary directory on exit
atexit.register(lambda: shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True))
