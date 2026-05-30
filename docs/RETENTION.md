# Backup Retention and Scheduling Policy

## Retention Policy
To ensure data safety while managing disk space, the following retention policy is recommended:

- **Daily Backups**: Keep the last 7 daily routine backups.
- **Weekly Backups**: Keep the last 4 weekly routine backups.
- **Monthly Backups**: Keep the last 3 monthly backups.
- **Disaster Recovery**: Create a new disaster recovery bundle weekly and after every major system change or migration.

### Auto-Cleanup
The current version of PGSIMS does not automatically delete old backups. Administrators should periodically review the Backup Center and delete obsolete backups manually.

## Scheduling Foundation
Automated backups can be configured using system `cron` jobs calling the management command.

### Example Cron Job (Daily at 2 AM)
```bash
0 2 * * * cd /path/to/pgsims/backend && /path/to/venv/bin/python manage.py create_system_backup --routine --notes "Automated daily backup"
```

### Example Disaster Recovery (Weekly on Sunday)
```bash
0 3 * * 0 cd /path/to/pgsims/backend && /path/to/venv/bin/python manage.py create_system_backup --disaster --notes "Automated weekly disaster recovery"
```

## Off-Server Storage
It is **CRITICAL** to store copies of backups off-server.
- **Recommended**: Sync the `backend/backups/` directory to a secure cloud storage bucket or a secondary server using `rsync` or `s3cmd`.
- **Encryption**: If storing on public clouds, ensure the transfer is encrypted (HTTPS/SSH) and the destination bucket is private.
