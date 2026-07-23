#!/bin/bash
# scripts/verify_pgms_backup.sh - Verify PGMS Database Backup
set -e

BACKUP_FILE="$1"

if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: $0 <path_to_backup_file>" >&2
    exit 1
fi

if [ ! -f "$BACKUP_FILE" ]; then
    echo "FAIL: Backup file does not exist at '$BACKUP_FILE'"
    exit 1
fi

CHECKSUM_FILE="${BACKUP_FILE}.md5"
if [ -f "$CHECKSUM_FILE" ]; then
    if command -v md5sum &> /dev/null; then
        if md5sum -c "$CHECKSUM_FILE" &> /dev/null; then
            echo "PASS: Backup file and checksum match."
            exit 0
        else
            echo "FAIL: Checksum mismatch."
            exit 1
        fi
    else
        echo "PASS: Backup file exists, but md5sum utility not found to verify checksum."
        exit 0
    fi
else
    echo "PASS: Backup file exists (no checksum file found)."
    exit 0
fi
