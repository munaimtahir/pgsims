# Migration Notes

This document tracks all database migrations for the SIMS application, including notes about breaking changes, data migrations, and rollback procedures.

## Overview

- All migrations are designed to be **idempotent** and **backward-compatible** where possible
- Migrations are tested in development and staging before production
- Always backup database before running migrations in production
- Follow the deployment checklist for each release

---

## Current Version: 1.0.0 (In Progress)

### Planned Migrations

#### Analytics Module
- **No schema changes** - Uses existing models
- **Data migrations**: None required
- **Indexes to add**:
  - Add composite index on `logbook_logbookentry(created_at, status, pg_id)` for analytics queries
  - Add index on `cases_clinicalcase(created_at, status, pg_id)` for trend analysis
  - Add index on `certificates_certificate(issue_date, pg_id)` for compliance tracking
  - Add index on `rotations_rotation(start_date, end_date, status, pg_id)` for date range queries

**Performance Impact**: 
- Index creation will lock tables briefly (< 1 second per index on tables < 100k rows)
- Use `CREATE INDEX CONCURRENTLY` in production

**Rollback**: 
```sql
DROP INDEX IF EXISTS idx_logbook_analytics;
DROP INDEX IF EXISTS idx_cases_analytics;
DROP INDEX IF EXISTS idx_certificates_analytics;
DROP INDEX IF EXISTS idx_rotations_dates;
```

---

#### Notifications Module
- **Schema changes**:
  - `notifications_notification` table already exists
  - `notifications_notificationpreference` table already exists
  - No new migrations required

**Data migration**: None

**Rollback**: N/A (no changes)

---

#### Bulk Operations Module
- **Schema changes**:
  - `bulk_bulkoperation` table already exists
  - Add field `error_details` (JSONField) to store detailed error information
  - Add field `retry_count` (IntegerField) to track retry attempts

**Migration script**:
```python
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('bulk', '0001_initial'),
    ]
    
    operations = [
        migrations.AddField(
            model_name='bulkoperation',
            name='error_details',
            field=models.JSONField(blank=True, null=True, help_text='Detailed error information per record'),
        ),
        migrations.AddField(
            model_name='bulkoperation',
            name='retry_count',
            field=models.IntegerField(default=0, help_text='Number of retry attempts'),
        ),
    ]
```

**Rollback**:
```sql
ALTER TABLE bulk_bulkoperation DROP COLUMN IF EXISTS error_details;
ALTER TABLE bulk_bulkoperation DROP COLUMN IF EXISTS retry_count;
```

---

#### Reporting Module
- **Schema changes**:
  - `reports_reportconfig` table already exists
  - `reports_scheduledreport` table already exists
  - Add field `last_run_at` (DateTimeField, nullable)
  - Add field `next_run_at` (DateTimeField, nullable)

**Migration script**:
```python
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('reports', '0001_initial'),
    ]
    
    operations = [
        migrations.AddField(
            model_name='scheduledreport',
            name='last_run_at',
            field=models.DateTimeField(blank=True, null=True, help_text='Last execution time'),
        ),
        migrations.AddField(
            model_name='scheduledreport',
            name='next_run_at',
            field=models.DateTimeField(blank=True, null=True, help_text='Next scheduled execution'),
        ),
    ]
```

**Rollback**:
```sql
ALTER TABLE reports_scheduledreport DROP COLUMN IF EXISTS last_run_at;
ALTER TABLE reports_scheduledreport DROP COLUMN IF EXISTS next_run_at;
```

---

#### Search Module
- **Schema changes**:
  - `search_searchhistory` table already exists
  - Add index on `search_term` for faster lookups
  - Add GIN index for PostgreSQL full-text search

**PostgreSQL-specific migration**:
```python
from django.db import migrations
from django.contrib.postgres.operations import TrigramExtension, UnaccentExtension

class Migration(migrations.Migration):
    dependencies = [
        ('search', '0001_initial'),
    ]
    
    operations = [
        # Enable PostgreSQL extensions for full-text search
        TrigramExtension(),
        UnaccentExtension(),
        
        # Add indexes
        migrations.RunSQL(
            sql="""
            CREATE INDEX IF NOT EXISTS idx_search_history_term_trgm 
            ON search_searchhistory USING gin(search_term gin_trgm_ops);
            """,
            reverse_sql="DROP INDEX IF EXISTS idx_search_history_term_trgm;"
        ),
    ]
```

**Note**: Requires PostgreSQL >= 9.6 with `pg_trgm` extension

**Rollback**:
```sql
DROP INDEX IF EXISTS idx_search_history_term_trgm;
-- Note: Extensions are not dropped automatically to avoid affecting other apps
```

---

#### Audit Module
- **Schema changes**:
  - Historical tables created by `django-simple-history`:
    - `historicaluser`
    - `historicalrotation`
    - `historicallogbookentry`
    - `historicalclinicalcase`
    - `historicalcertificate`
  - `audit_activitylog` table for non-CRUD events

**Migration script**:
```python
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('audit', '0001_initial'),
    ]
    
    operations = [
        # ActivityLog table already exists from 0001_initial
        # Add indexes for common queries
        migrations.RunSQL(
            sql="""
            CREATE INDEX IF NOT EXISTS idx_activity_log_user_action 
            ON audit_activitylog(user_id, action, created_at DESC);
            """,
            reverse_sql="DROP INDEX IF EXISTS idx_activity_log_user_action;"
        ),
    ]
```

**Storage Impact**: 
- Historical tables will grow over time (approximately 1.5-2x size of main tables)
- Plan for regular archival of old history records (>2 years)

**Rollback**: Not recommended after deployment, as historical data will be lost

---

#### Validation Module
- **No schema changes** - Pure logic changes
- Uses existing model validators and clean methods

---

#### Performance Module
- **No schema changes** - Optimization only
- **Indexes to add** (consolidated list from all modules):

```sql
-- Analytics indexes
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_logbook_analytics 
ON logbook_logbookentry(created_at DESC, status, pg_id);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_cases_analytics 
ON cases_clinicalcase(created_at DESC, status, pg_id);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_certificates_analytics 
ON certificates_certificate(issue_date DESC, pg_id);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_rotations_dates 
ON rotations_rotation(start_date, end_date, status, pg_id);

-- Search indexes
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_logbook_title_text 
ON logbook_logbookentry USING gin(to_tsvector('english', title));

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_cases_diagnosis_text 
ON cases_clinicalcase USING gin(to_tsvector('english', diagnosis));

-- Performance indexes
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_supervisor 
ON users_user(supervisor_id) WHERE supervisor_id IS NOT NULL;

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_notifications_unread 
ON notifications_notification(recipient_id, is_read, created_at DESC) WHERE is_read = FALSE;
```

**Note**: Use `CONCURRENTLY` to avoid locking tables during index creation

**Rollback**:
```sql
DROP INDEX IF EXISTS idx_logbook_analytics;
DROP INDEX IF EXISTS idx_cases_analytics;
DROP INDEX IF EXISTS idx_certificates_analytics;
DROP INDEX IF EXISTS idx_rotations_dates;
DROP INDEX IF EXISTS idx_logbook_title_text;
DROP INDEX IF EXISTS idx_cases_diagnosis_text;
DROP INDEX IF EXISTS idx_users_supervisor;
DROP INDEX IF EXISTS idx_notifications_unread;
```

---

## Migration Checklist

Before deploying migrations:

- [ ] **Backup database** (pg_dump or equivalent)
- [ ] **Review migration SQL** (run `python manage.py sqlmigrate <app> <migration>`)
- [ ] **Test in development** (run `python manage.py migrate`)
- [ ] **Test in staging** (run migrations on staging copy of production data)
- [ ] **Check disk space** (ensure enough space for indexes and historical tables)
- [ ] **Schedule maintenance window** (if downtime required)
- [ ] **Prepare rollback plan** (document reverse migrations)
- [ ] **Monitor performance** (check query times before and after)

---

## Deployment Steps

### 1. Pre-Deployment

```bash
# Backup database
pg_dump sims_db > sims_backup_$(date +%Y%m%d_%H%M%S).sql

# Check pending migrations
python manage.py showmigrations | grep '\[ \]'

# Generate migration SQL for review
python manage.py sqlmigrate app_name migration_number > migration_review.sql
```

### 2. Deployment

```bash
# Deploy code
git pull origin main

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate --no-input

# Create indexes (if not in migrations)
python manage.py shell < scripts/create_indexes.py

# Collect static files
python manage.py collectstatic --no-input

# Restart services
sudo systemctl restart gunicorn
sudo systemctl restart celery
sudo systemctl restart celerybeat
```

### 3. Post-Deployment

```bash
# Verify migrations
python manage.py showmigrations | grep '\[X\]'

# Check for errors
tail -f logs/django.log

# Test critical paths
# - Login
# - Create logbook entry
# - Create rotation
# - Run report

# Monitor performance
# - Check database query times
# - Monitor cache hit rates
# - Check Celery task queue
```

---

## Rollback Procedure

If migrations cause issues:

### Quick Rollback (Code Only)

```bash
# Revert to previous version
git revert HEAD

# Restart services
sudo systemctl restart gunicorn
sudo systemctl restart celery
```

### Full Rollback (With Database)

```bash
# Stop services
sudo systemctl stop gunicorn
sudo systemctl stop celery
sudo systemctl stop celerybeat

# Restore database from backup
psql sims_db < sims_backup_YYYYMMDD_HHMMSS.sql

# Revert code
git revert HEAD

# Restart services
sudo systemctl start gunicorn
sudo systemctl start celery
sudo systemctl start celerybeat
```

---

## Known Issues

### Issue: Long-running index creation
**Symptom**: Index creation takes > 5 minutes  
**Solution**: Use `CREATE INDEX CONCURRENTLY` or schedule during low-traffic period  
**Impact**: Read queries may be slower until index is complete

### Issue: Disk space shortage
**Symptom**: Migration fails with "disk full" error  
**Solution**: Clear old logs, vacuum database, or add more disk space  
**Prevention**: Monitor disk usage before migrations

### Issue: Lock timeout
**Symptom**: Migration times out waiting for table lock  
**Solution**: Retry during low-traffic period or increase `statement_timeout`  
**Prevention**: Use `CONCURRENTLY` for index operations

---

## Version History

| Version | Date | Migrations | Notes |
|---------|------|------------|-------|
| 1.0.0 | 2025-01-XX | Multiple | Initial production-ready release with all 8 modules |

---

## See Also

- [FEATURE_FLAGS.md](FEATURE_FLAGS.md) - Feature flag configuration
- [CHANGELOG.md](CHANGELOG.md) - Version history
- [README.md](README.md) - Setup and deployment guide
