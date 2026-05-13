# Daily Backup Verification Procedure

**Frequency**: Every morning during pilot (after health check)
**Time**: 08:30 UTC (or immediately after health check)
**Owner**: Support Person
**Created**: 2025-05-13

---

## Purpose

Verify that:
1. Automated backup process completed successfully
2. Database backup is accessible and readable
3. No data corruption since last backup
4. Rollback is possible if needed

---

## Daily Backup Check Steps (10 min)

### Step 1: Confirm Backup File Exists

Run:
```bash
ls -lah docs/_implementation/20260513_0912_pilot_deployment_readiness/backups/pgsims_pilot_readiness_backup.sql
```

Expected Output:
```
-rw-rw-r-- 1 munaim munaim 552K May 13 09:00 pgsims_pilot_readiness_backup.sql
```

**Action if NOT FOUND**:
- Create backup immediately:
  ```bash
  docker compose exec db pg_dump -U pgsims_user pgsims > docs/_implementation/20260513_0912_pilot_deployment_readiness/backups/pgsims_pilot_readiness_backup_$(date +%s).sql
  ```
- Escalate to Technical Lead
- Log as backup failure issue

---

### Step 2: Verify Backup File Size

Run:
```bash
du -h docs/_implementation/20260513_0912_pilot_deployment_readiness/backups/pgsims_pilot_readiness_backup.sql
```

Expected: ≥100 KB (if pilot has data loaded)

**Action if SMALL** (<100 KB):
- File may be corrupted or incomplete
- Verify database has data:
  ```bash
  docker compose exec db psql -U pgsims_user -d pgsims -c "SELECT count(*) FROM auth_user;"
  ```
- If database has data but backup is small, recreate backup
- Log as backup quality issue

---

### Step 3: Verify Backup File Integrity

Run:
```bash
head -20 docs/_implementation/20260513_0912_pilot_deployment_readiness/backups/pgsims_pilot_readiness_backup.sql
```

Expected (first 20 lines should show):
```
--
-- PostgreSQL database dump
--
-- Dumped from database version X.X.X
-- Dump started on YYYY-MM-DD HH:MM:SS

SET statement_timeout = 0;
SET lock_timeout = 0;
...
```

**Action if CORRUPT** (binary data, truncated, or error):
- Backup file is corrupted
- Recreate backup immediately:
  ```bash
  docker compose exec db pg_dump -U pgsims_user pgsims > docs/_implementation/20260513_0912_pilot_deployment_readiness/backups/pgsims_pilot_readiness_backup_$(date +%s).sql
  ```
- Escalate to Technical Lead
- Log as critical issue

---

### Step 4: Verify Backup Completeness

Run:
```bash
tail -20 docs/_implementation/20260513_0912_pilot_deployment_readiness/backups/pgsims_pilot_readiness_backup.sql
```

Expected (last 20 lines should show):
```
...
COMMIT;

--
-- PostgreSQL database dump complete
--
```

**Action if INCOMPLETE** (missing footer or truncated):
- Backup was not completed fully
- Recreate backup:
  ```bash
  docker compose exec db pg_dump -U pgsims_user pgsims > docs/_implementation/20260513_0912_pilot_deployment_readiness/backups/pgsims_pilot_readiness_backup_$(date +%s).sql
  ```
- Escalate to Technical Lead
- Log as backup failure issue

---

### Step 5: Count Key Tables in Backup

Run:
```bash
grep -c "CREATE TABLE" docs/_implementation/20260513_0912_pilot_deployment_readiness/backups/pgsims_pilot_readiness_backup.sql
```

Expected: ≥20 (at least 20 tables created)

**Action if TOO FEW** (<10 tables):
- Backup may not have captured schema
- Recreate backup:
  ```bash
  docker compose exec db pg_dump -U pgsims_user pgsims > docs/_implementation/20260513_0912_pilot_deployment_readiness/backups/pgsims_pilot_readiness_backup_$(date +%s).sql
  ```
- Escalate to Technical Lead

---

## Weekly Full Backup (Friday)

**Every Friday at 18:00 UTC**:

Run:
```bash
docker compose exec db pg_dump -U pgsims_user pgsims > docs/_implementation/20260513_0912_pilot_deployment_readiness/backups/pgsims_full_backup_$(date +%Y%m%d_%H%M%S).sql

# Archive to external storage (example, adjust path)
cp docs/_implementation/20260513_0912_pilot_deployment_readiness/backups/pgsims_full_backup_*.sql /mnt/backups/pgsims/ 2>/dev/null || echo "External backup not configured, local backup created"
```

Log:
- Time backup created
- File size
- Location (local + external)
- Signed by support person

---

## Backup Test Procedure (Monthly)

**First Monday of each month at 10:00 UTC**:

Run a full restore test (on test environment only):

```bash
# Create test environment
docker run -d --name pgsims_test_db -e POSTGRES_PASSWORD=testpass postgres:15

# Wait for startup
sleep 10

# Restore backup
docker exec -i pgsims_test_db psql -U postgres < docs/_implementation/20260513_0912_pilot_deployment_readiness/backups/pgsims_pilot_readiness_backup.sql

# Verify restore success
docker exec pgsims_test_db psql -U postgres -d pgsims -c "SELECT count(*) FROM auth_user;"

# Clean up
docker stop pgsims_test_db
docker rm pgsims_test_db
```

Document:
- [ ] Restore completed successfully
- [ ] Row counts match expected
- [ ] No errors during restore
- [ ] Test environment cleaned up
- [ ] Results logged in backup verification tracker

---

## Backup Verification Log

| Date | Time | File Size | Tables | Integrity | Complete? | Issues? | Support Person | Signed Off |
|------|------|-----------|--------|-----------|-----------|---------|---|---|
| YYYY-MM-DD | HH:MM UTC | XXX KB | ≥20 | ✅/⚠️/❌ | Yes/No | Yes/No | Name | Time |
| 2025-05-13 | 08:30 | 552 | 35 | ✅ | Yes | No | Support | 08:40 |

---

## If Backup is Stale or Missing

**Action immediately**:

1. Create emergency backup:
   ```bash
   docker compose exec db pg_dump -U pgsims_user pgsims > docs/_implementation/20260513_0912_pilot_deployment_readiness/backups/pgsims_backup_$(date +%Y%m%d_%H%M%S)_EMERGENCY.sql
   ```

2. Verify backup integrity:
   ```bash
   ls -lah docs/_implementation/20260513_0912_pilot_deployment_readiness/backups/pgsims_backup_*_EMERGENCY.sql
   ```

3. Notify Technical Lead:
   - Email with backup file location
   - Timestamp created
   - Database row counts

4. Log issue (see 06_ISSUE_LOG_TEMPLATE.md):
   - Severity: HIGH
   - Category: Data Protection
   - Issue: Stale/missing backup
   - Resolution: Emergency backup created

---

## Backup Storage Policy

| Backup Type | Frequency | Retention | Location | Retention Period |
|---|---|---|---|---|
| Daily check | Every morning | Verify only | Local | N/A |
| Weekly full | Every Friday | Keep all | Local + External | 4 weeks |
| Monthly test | 1st Monday | Logged only | Test env | N/A |
| Emergency | As needed | Keep all | Local + External | 12 weeks |

---

## Escalation Contacts

| Scenario | Contact | Action |
|---|---|---|
| Backup fails | Support Person | Recreate backup, notify Tech Lead |
| File corrupted | Technical Lead | Emergency backup, investigate root cause |
| Restore fails | Technical Lead + UTRMC Lead | May trigger rollback procedure |
| Multiple failures | UTRMC Lead + Technical Lead | May pause pilot |

---

**Created**: 2025-05-13
**Version**: 1.0
**Review Schedule**: Daily during pilot
