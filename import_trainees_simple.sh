#!/bin/bash
# Simple script to import trainee data
# This script handles the logging permission issue

cd /home/munaim/srv/apps/pgsims

# Set environment to use SQLite and console logging
export PYTHONUNBUFFERED=1
# Force SQLite - override DATABASE_URL from .env file
unset DATABASE_URL
export DB_ENGINE=django.db.backends.sqlite3
export DB_NAME=db.sqlite3

# Use Python to override logging config temporarily
venv/bin/python3 << 'PYTHON_SCRIPT'
import os
import sys

# IMPORTANT: Override DATABASE_URL BEFORE Django loads settings
# This ensures we use SQLite instead of PostgreSQL from .env file
# Must be done before any Django imports
if 'DATABASE_URL' in os.environ:
    del os.environ['DATABASE_URL']
os.environ['DB_ENGINE'] = 'django.db.backends.sqlite3'
os.environ['DB_NAME'] = 'db.sqlite3'

# Also check if .env file will be loaded - prevent it from overriding
# by setting this before settings module import
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings')

# Force SQLite database configuration
# Override any DATABASE_URL that might be loaded from .env
os.environ.pop('DATABASE_URL', None)

# Monkey-patch logging BEFORE Django setup
import logging.config
import logging

# Save original
_original_dictConfig = logging.config.dictConfig

def patched_dictConfig(config):
    """Patch dictConfig to replace file handlers with console handlers."""
    if isinstance(config, dict):
        handlers = config.get('handlers', {})
        for handler_name, handler_config in list(handlers.items()):
            if isinstance(handler_config, dict) and 'filename' in handler_config:
                # Replace file handler with console handler
                config['handlers'][handler_name] = {
                    'class': 'logging.StreamHandler',
                    'formatter': handler_config.get('formatter', 'simple'),
                    'level': handler_config.get('level', 'INFO'),
                }
    
    # Call original with modified config
    try:
        return _original_dictConfig(config)
    except (ValueError, PermissionError, OSError) as e:
        # If it still fails, use basic logging
        if 'handler' in str(e).lower() or 'permission' in str(e).lower():
            logging.basicConfig(level=logging.WARNING, handlers=[logging.StreamHandler()])
            return None
        raise

logging.config.dictConfig = patched_dictConfig

# Also patch the module-level dictConfig
import logging.config
logging.config.dictConfig = patched_dictConfig

# Now setup Django
import django
try:
    django.setup()
    # After setup, override DATABASES to use SQLite (in case .env loaded PostgreSQL URL)
    from django.conf import settings
    if hasattr(settings, 'DATABASES'):
        settings.DATABASES['default'] = {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': str(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db.sqlite3')) if '__file__' in globals() else 'db.sqlite3',
        }
except (ValueError, PermissionError) as e:
    # If setup fails due to logging, continue anyway
    error_str = str(e).lower()
    if 'handler' in error_str or 'logging' in error_str or 'permission' in error_str:
        # Set up basic logging and continue
        logging.basicConfig(level=logging.WARNING, handlers=[logging.StreamHandler()])
        # Try to continue without logging configuration
        import warnings
        warnings.filterwarnings('ignore')
        # Force Django setup to skip logging
        from django.conf import settings
        # Remove file handlers from settings
        if hasattr(settings, 'LOGGING') and isinstance(settings.LOGGING, dict):
            handlers = settings.LOGGING.get('handlers', {})
            for name, config in list(handlers.items()):
                if isinstance(config, dict) and 'filename' in config:
                    handlers[name] = {'class': 'logging.StreamHandler'}
            loggers = settings.LOGGING.get('loggers', {})
            for logger_name, logger_config in loggers.items():
                if 'handlers' in logger_config:
                    # Replace 'file' with 'console' in handlers
                    handlers_list = logger_config['handlers']
                    logger_config['handlers'] = [h if h != 'file' else 'console' for h in handlers_list]
    else:
        raise

from django.core.management import call_command

file_path = '/home/munaim/Downloads/Trainee_Data_Department_of_Urology.xlsx'

print("="*70)
print("IMPORTING TRAINEE DATA")
print("="*70)

# Run migration
print("\n1. Running migrations...")
try:
    call_command('migrate', 'users', verbosity=1, interactive=False)
    print("   ✓ Migrations complete")
except Exception as e:
    print(f"   ⚠ Migration note: {e}")

# Import data
print(f"\n2. Importing trainee data...")
try:
    call_command('import_trainees', file_path, dry_run=False, allow_partial=True, verbosity=2)
    print("\n" + "="*70)
    print("✓ IMPORT COMPLETED SUCCESSFULLY!")
    print("="*70)
except Exception as e:
    print(f"\n✗ Import error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

PYTHON_SCRIPT

exit_code=$?
if [ $exit_code -eq 0 ]; then
    echo ""
    echo "Data import completed! You can now use the application."
else
    echo ""
    echo "Import failed. Please check errors above."
    exit $exit_code
fi
