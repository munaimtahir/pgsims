#!/bin/bash
# Import trainee data using SQLite temporarily

cd /home/munaim/srv/apps/pgsims

echo "="*70
echo "IMPORTING TRAINEE DATA (Using SQLite)"
echo "="*70

# Backup and modify .env to use SQLite
if [ -f .env ]; then
    cp .env .env.backup.$(date +%Y%m%d_%H%M%S)
    echo "\n📝 Temporarily modifying .env to use SQLite..."
    
    # Comment out DATABASE_URL
    sed -i 's/^DATABASE_URL=/#DATABASE_URL=/' .env
    
    # Add SQLite config (if not present)
    if ! grep -q "^DB_ENGINE=" .env; then
        echo "DB_ENGINE=django.db.backends.sqlite3" >> .env
    else
        sed -i 's/^DB_ENGINE=.*/DB_ENGINE=django.db.backends.sqlite3/' .env
    fi
    
    if ! grep -q "^DB_NAME=" .env; then
        echo "DB_NAME=db.sqlite3" >> .env
    else
        sed -i 's|^DB_NAME=.*|DB_NAME=db.sqlite3|' .env
    fi
fi

# Run the import
bash import_trainees_simple.sh

# Restore .env
if [ -f .env.backup.* ]; then
    BACKUP_FILE=$(ls -t .env.backup.* | head -1)
    if [ -f "$BACKUP_FILE" ]; then
        echo "\n📝 Restoring original .env file..."
        mv "$BACKUP_FILE" .env
    fi
fi

echo "\n✅ Done!"
