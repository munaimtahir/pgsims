# Rollback Quick Guide (Emergency Procedure)

**Purpose**: Emergency rollback if pilot encounters critical issues
**Use Case**: Data loss, security breach, critical data corruption, unrecoverable system failure
**Created**: 2025-05-13
**Version**: 1.0

---

## When to Trigger Rollback

**Rollback is authorized by UTRMC Lead ONLY when**:

- [ ] Data loss or corruption detected
- [ ] Security breach or unauthorized access
- [ ] System down for >30 minutes (cannot be recovered)
- [ ] Core workflows completely non-functional
- [ ] Database constraints violated (orphaned records)
- [ ] Multiple critical issues cannot be fixed quickly

**Do NOT rollback for**:
- ❌ Single user cannot log in (user support issue)
- ❌ Performance degradation (restart/optimize)
- ❌ Minor workflow bugs (apply fix)
- ❌ User error/data misentry (manual correction)

---

## Pre-Rollback Decision

1. **Technical Lead assesses situation** (5–10 min)
   - Identify root cause
   - Estimate time to fix vs rollback
   - Risk assessment: fix vs rollback

2. **UTRMC Lead makes decision** (3–5 min)
   - Is rollback justified?
   - Any data that should be saved?
   - Pilot participants to notify?

3. **If YES → Execute rollback immediately**
   - See steps below

4. **If NO → Apply targeted fix instead**
   - Do not use rollback for minor issues

---

## Rollback Procedure (Step-by-Step)

### Phase 1: Preparation (2 min)

**Stop accepting new data**:
```bash
# Notify all users immediately
# Email / Slack / Call:
# "PGSIMS pilot paused for emergency maintenance. 
#  Do not submit any new entries. 
#  We will restore from backup and resume shortly."
```

**Log into server** (or ensure you have access):
```bash
cd /home/munaim/srv/apps/pgsims
git branch --show-current     # Should be: main
git status                    # Should show clean or minimal changes
```

---

### Phase 2: Stop Services (2 min)

**Stop all running services**:
```bash
./scripts/pgsims_down.sh
# Output should show: Stopping pgsims_backend ... done, etc.

# Verify all stopped
docker ps | grep pgsims
# Should return: (empty)
```

---

### Phase 3: Restore Database (10 min)

**Step 1: Delete current database volume** (⚠️ DESTRUCTIVE):
```bash
docker volume rm pgsims_db_data 2>/dev/null || echo "Volume not found (okay)"
```

**Step 2: Restart database only**:
```bash
docker compose up -d db
# Wait for database to initialize
sleep 30
docker compose ps db
# Should show: db ... Up (healthy)
```

**Step 3: Restore from backup**:
```bash
# Restore the pilot-readiness backup
docker exec -i pgsims_db psql -U pgsims_user < \
  docs/_implementation/20260513_0912_pilot_deployment_readiness/backups/pgsims_pilot_readiness_backup.sql

# This takes 1–2 minutes depending on backup size
echo "✅ Database restore completed"
```

**Step 4: Verify restoration**:
```bash
# Check a few key tables exist
docker compose exec db psql -U pgsims_user -d pgsims -c \
  "SELECT count(*) as table_count FROM information_schema.tables WHERE table_schema='public';"

# Should return: table_count=35+ (or similar)

# Check user count
docker compose exec db psql -U pgsims_user -d pgsims -c \
  "SELECT count(*) FROM auth_user;"

# Should match pre-rollback count
```

---

### Phase 4: Restart All Services (5 min)

**Restart complete stack**:
```bash
./scripts/pgsims_up.sh
# Output should show: Creating pgsims_backend ... done, etc.

# Wait for startup
sleep 60

# Verify all services healthy
./scripts/pgsims_health.sh
# All endpoints should show: 200 ✅
```

**Verify container health**:
```bash
./scripts/pgsims_ps.sh
# All containers should show: Up (healthy)
```

---

### Phase 5: Smoke Test (5 min)

**Run smoke tests to verify rollback success**:
```bash
cd frontend && npm run test:e2e:smoke:local 2>&1 | head -50
# Look for: "X passed" (should be 17 or close)
# If all pass → rollback successful ✅
```

**Manual spot check**:
```bash
# Test UTRMC admin login (if test account available)
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@test.local","password":"[ADMIN_PASSWORD]"}'

# Should return: {"access": "TOKEN", "refresh": "TOKEN"}
```

---

### Phase 6: Verify Data Integrity (5 min)

**Check critical tables**:
```bash
docker compose exec db psql -U pgsims_user -d pgsims << EOF
SELECT 
  (SELECT count(*) FROM auth_user) as users,
  (SELECT count(*) FROM academics_resident) as residents,
  (SELECT count(*) FROM rotations_rotation) as rotations,
  (SELECT count(*) FROM leave_request) as leave_requests;
EOF

# Compare counts to what they were BEFORE pilot
# If counts match → data integrity verified ✅
```

---

### Phase 7: Notify Stakeholders (5 min)

**Send status update**:
```
Subject: PGSIMS Pilot - Emergency Maintenance Complete

Dear Pilot Participants,

An issue was identified and the system has been restored 
from backup. All data has been preserved to the point of 
the last backup (approximately [TIME]).

PGSIMS is now back online. You may resume normal operations.

Any data entered after the backup point will need to be 
re-entered. We apologize for the inconvenience.

Support contact: [Support Person]

[UTRMC Lead / Technical Lead]
```

---

### Phase 8: Post-Rollback Investigation (Ongoing)

**Technical Lead investigates root cause**:

1. **Review logs from before rollback**:
   ```bash
   ./scripts/pgsims_logs.sh backend 2>&1 | tail -100 > /tmp/backend_logs.txt
   # Review error messages
   ```

2. **Document root cause**:
   - What went wrong?
   - When did it happen?
   - Why wasn't it caught earlier?
   - How to prevent in future?

3. **Create action items**:
   - Code fix? → commit and deploy
   - Configuration fix? → update .env
   - Process fix? → update procedures
   - Monitoring gap? → add alerting

4. **Log incident**:
   - Time detected
   - Time resolved
   - Root cause
   - Prevention measures
   - Post-incident actions

---

## Rollback Checklist (Copy & Paste)

```
⏱️ ROLLBACK EXECUTION LOG

Time Started: [HH:MM UTC]
Authorized By: [UTRMC Lead Name]
Technical Lead: [Name]

PREPARATION
- [ ] Users notified of pause
- [ ] Server access confirmed
- [ ] git status verified

STOP SERVICES
- [ ] ./scripts/pgsims_down.sh completed
- [ ] All containers stopped
- [ ] docker ps shows empty

RESTORE DATABASE
- [ ] Old db volume deleted
- [ ] New database started
- [ ] Backup restored
- [ ] Table count verified
- [ ] User count verified

RESTART SERVICES
- [ ] ./scripts/pgsims_up.sh completed
- [ ] All containers healthy
- [ ] ./scripts/pgsims_health.sh shows 200 ✅

SMOKE TEST
- [ ] E2E smoke tests pass (17/17)
- [ ] Manual login test works
- [ ] Dashboard loads

DATA INTEGRITY
- [ ] User count matches expected
- [ ] Resident count matches expected
- [ ] No orphaned records
- [ ] Audit trail consistent

NOTIFY STAKEHOLDERS
- [ ] Status email sent
- [ ] All users notified
- [ ] Support person standing by

INVESTIGATION
- [ ] Root cause documented
- [ ] Action items created
- [ ] Preventive measures identified

Time Completed: [HH:MM UTC]
Total Duration: [minutes]
Result: ✅ SUCCESS / ❌ FAILED

If FAILED:
  - Escalate immediately to CTO
  - Do not attempt second rollback
  - May require manual database intervention
```

---

## Troubleshooting Rollback

### Problem: Database restore hangs or fails

**Solution**:
```bash
# Stop database
docker compose down db

# Remove corrupted volume
docker volume rm pgsims_db_data

# Restart fresh
docker compose up -d db
sleep 30

# Try restore again
docker exec -i pgsims_db psql -U pgsims_user < backup.sql
```

### Problem: Containers fail to start after rollback

**Solution**:
```bash
# Check logs
./scripts/pgsims_logs.sh backend | tail -50

# Likely cause: stale env variables or configuration
# Solution: Ensure .env file is loaded
./scripts/pgsims_down.sh
./scripts/pgsims_up.sh  # This script enforces --env-file .env
```

### Problem: Smoke tests still fail after rollback

**Solution**:
```bash
# This suggests the backup itself was corrupted
# Manual verification needed
docker compose exec db psql -U pgsims_user -d pgsims -c \
  "SELECT count(*) FROM auth_user;"

# If this query fails or returns 0:
# - Backup was corrupted
# - Manual data entry needed
# - Escalate to CTO immediately
```

---

## Rollback Decision Tree

```
CRITICAL ISSUE DETECTED
        ↓
Can it be fixed in <30 minutes?
├─ YES → Apply targeted fix, test, resume
└─ NO → Continue below
        ↓
Is data integrity at risk?
├─ NO → Wait for fix / restart services
└─ YES → Continue below
        ↓
Do we have a valid backup?
├─ NO → Data loss likely, escalate to CTO
└─ YES → Continue below
        ↓
Authorize rollback?
(UTRMC Lead decision only)
├─ NO → Continue troubleshooting, do NOT rollback
└─ YES → Execute rollback procedure above
        ↓
ROLLBACK EXECUTION
        ↓
Did rollback succeed?
├─ YES → Resume operations, investigate cause
└─ NO → Escalate to CTO, do NOT retry rollback
```

---

## Prevention (Avoid Needing Rollback)

To prevent needing an emergency rollback:

1. **Daily backups** (see 05_DAILY_BACKUP_CHECK.md)
   - Verify backup completes every night
   - Test restore monthly

2. **Health checks** (see 04_DAILY_HEALTH_CHECK.md)
   - Run every morning
   - Catch issues early

3. **Issue logging** (see 06_ISSUE_LOG_TEMPLATE.md)
   - Log everything
   - Review weekly

4. **Code quality**
   - E2E tests must pass before deploy
   - Code review required
   - Staging testing before production

5. **Monitoring & Alerting**
   - Set up alerts for:
     - Container crashes
     - High error rates
     - Slow queries
     - Disk space issues
   - Alert Technical Lead immediately

---

## Contacts (Emergency)

| Role | Contact | Phone | Email | Availability |
|---|---|---|---|---|
| UTRMC Lead (Approval) | [TBD] | [TBD] | [TBD] | 24/7 if critical |
| Technical Lead (Execute) | [TBD] | [TBD] | [TBD] | 24/7 if critical |
| CTO (Escalation) | [TBD] | [TBD] | [TBD] | 24/7 if critical |

---

**Created**: 2025-05-13
**Last Review**: 2025-05-13
**Version**: 1.0
**Status**: READY FOR EMERGENCY USE
