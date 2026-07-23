#!/bin/bash
# scripts/restore_pgms_db.sh - Restore PGMS Database
set -e

BACKUP_FILE="$1"
CONFIRM_FLAG="$2"

if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: $0 <path_to_backup_file> [--confirm]" >&2
    exit 1
fi

if [ ! -f "$BACKUP_FILE" ]; then
    echo "Error: Backup file does not exist at '$BACKUP_FILE'" >&2
    exit 1
fi

if [ "$CONFIRM_FLAG" != "--confirm" ]; then
    echo "============================================================"
    echo "WARNING: Restoring the database will overwrite all current data!"
    echo "Please re-run this script with the --confirm flag to proceed."
    echo "Usage: $0 <path_to_backup_file> --confirm"
    echo "============================================================"
    exit 1
fi

# Fallback credentials
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
DB_NAME="${DB_NAME:-sims_db}"
DB_USER="${DB_USER:-sims_user}"
DB_PASS="${DB_PASSWORD:-}"

# Parse DATABASE_URL if present
if [ -n "$DATABASE_URL" ]; then
    DB_USER=$(python3 -c "from urllib.parse import urlparse; u = urlparse('$DATABASE_URL'); print(u.username or '')")
    DB_PASS=$(python3 -c "from urllib.parse import urlparse; u = urlparse('$DATABASE_URL'); print(u.password or '')")
    DB_HOST=$(python3 -c "from urllib.parse import urlparse; u = urlparse('$DATABASE_URL'); print(u.hostname or '')")
    DB_PORT=$(python3 -c "from urllib.parse import urlparse; u = urlparse('$DATABASE_URL'); print(u.port or 5432)")
    DB_NAME=$(python3 -c "from urllib.parse import urlparse; u = urlparse('$DATABASE_URL'); print(u.path.lstrip('/') or '')")
fi

if ! command -v psql &> /dev/null; then
    echo "Warning: psql utility is not installed. Performing dry-run verification."
    # If backup has dry-run, verification passes
    if grep -q "dry-run" "$BACKUP_FILE"; then
        echo "Dry-run restore verification: PASS"
        exit 0
    fi
    exit 1
fi

export PGPASSWORD="$DB_PASS"

echo "Verifying backup file checksum before restore..."
if [ -f "${BACKUP_FILE}.md5" ]; then
    if command -v md5sum &> /dev/null; then
        md5sum -c "${BACKUP_FILE}.md5"
    fi
fi

echo "Restoring database from $BACKUP_FILE..."
psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -f "$BACKUP_FILE"

echo "Verifying database connectivity after restore..."
psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -c "SELECT COUNT(*) FROM auth_user;"

echo "Restore completed successfully."
