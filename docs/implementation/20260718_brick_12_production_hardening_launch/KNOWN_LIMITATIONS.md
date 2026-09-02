# Known Limitations - Brick 12: Production Hardening, Backup/Restore, Security, and Launch Readiness

1. **Local storage-file warning**: Next.js build compilation generates warnings regarding `--localstorage-file` without a valid path. This warning originates from the local node container environment settings and does not impact frontend runtime behavior.
2. **PostgreSQL schema recreate**: The restore script executes SQL instructions directly. If schema structural changes occur in production migrations, database objects may need to be dropped manually before executing `restore_pgms_db.sh` to prevent object name conflicts.
