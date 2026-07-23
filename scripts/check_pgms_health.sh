#!/bin/bash
# scripts/check_pgms_health.sh - Overall PGMS Health check
set -e

echo "Checking PGMS System Health..."

# 1. Backend python syntax and integrity check
echo "Running Django check..."
python3 backend/manage.py check

# 2. Database Connectivity
echo "Checking database connection..."
python3 -c "
import os, sys
sys.path.append('backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sims_project.settings_test')
import django
django.setup()
from django.db import connection
try:
    connection.ensure_connection()
    print('Database connection: OK')
except Exception as e:
    print(f'Database connection: FAILED - {e}')
    sys.exit(1)
"

# 3. Check for frontend production build folder (if built)
if [ -d "frontend/.next" ]; then
    echo "Frontend build artifacts: Present"
else
    echo "Frontend build artifacts: Missing (Run npm run build inside frontend first)"
fi

echo "PGMS System Health: PASS"
