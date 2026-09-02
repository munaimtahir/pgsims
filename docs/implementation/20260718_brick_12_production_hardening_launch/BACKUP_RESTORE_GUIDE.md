# Backup and Restore Guide - Brick 12: Production Hardening, Backup/Restore, Security, and Launch Readiness

PGMS database administration is managed using command line helper scripts.

---

## 1. Creating a Database Dump
To create a timestamped SQL dump of the postgraduate management system database, execute:
```bash
bash scripts/backup_pgms_db.sh
```

**Actions Performed**:
1. Checks if `pg_dump` is installed in path.
2. Resolves connection credentials from the `DATABASE_URL` environment variable.
3. Saves a plain SQL script under the `BACKUP_DIR` directory (defaults to `backend/backups`).
4. Generates an MD5 checksum file (e.g. `*.sql.md5`) to ensure file integrity.

---

## 2. Verifying a Backup File
To check if a backup SQL script exists and matches its md5 checksum:
```bash
bash scripts/verify_pgms_backup.sh <path_to_backup_file>
```

**Output**:
- Prints `PASS: Backup file and checksum match.` on success.
- Prints `FAIL: Checksum mismatch.` if corrupted.

---

## 3. Restoring the Database
To restore the system database from an SQL dump, execute:
```bash
bash scripts/restore_pgms_db.sh <path_to_backup_file> --confirm
```

**Warning**:
- This command will overwrite all current tables and values.
- Running without the `--confirm` argument will abort with a security warning.
- After completion, it executes a connectivity test on `auth_user` to assert target availability.
