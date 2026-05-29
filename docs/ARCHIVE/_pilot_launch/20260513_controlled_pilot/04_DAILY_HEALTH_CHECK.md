# Daily Health Check Procedure

**Frequency**: Every morning during pilot
**Time**: 08:00 UTC (or as assigned)
**Owner**: Support Person (rotate as needed)
**Created**: 2025-05-13

---

## Pre-Flight Steps (5 min)

1. **Open terminal and SSH to pilot server** (or local if running)
   ```bash
   cd /home/munaim/srv/apps/pgsims
   ```

2. **Confirm you are in correct directory**
   ```bash
   pwd
   git branch --show-current
   ```
   Expected: `/home/munaim/srv/apps/pgsims` and `main`

---

## Health Check Steps (15 min)

### Step 1: Container Status Check (2 min)

Run:
```bash
./scripts/pgsims_ps.sh
```

Expected Output:
```
CONTAINER ID   STATUS              NAMES
abc123...      Up 2 hours (healthy) pgsims_backend
def456...      Up 2 hours (healthy) pgsims_frontend
ghi789...      Up 2 hours (healthy) pgsims_db
jkl012...      Up 2 hours (healthy) pgsims_redis
mno345...      Up 2 hours (healthy) pgsims_worker
pqr678...      Up 2 hours (healthy) pgsims_beat
```

**Action if RED**:
- Note which container(s) are not running or unhealthy
- Run: `./scripts/pgsims_logs.sh [service]` (e.g., `pgsims_logs.sh backend`)
- Check for error messages
- If critical error, escalate to Technical Lead immediately

---

### Step 2: API Health Endpoints (5 min)

Run:
```bash
./scripts/pgsims_health.sh
```

Expected Output:
```
Backend API:     200 ✅ (response time <200ms)
Frontend:        200 ✅ (response time <500ms)
Database:        200 ✅ (connected)
Redis Cache:     200 ✅ (connected)
```

**Action if YELLOW (>500ms)**:
- Note which service is slow
- Check server load: `top` or `htop`
- Check database activity: `docker compose exec db psql -U pgsims_user -d pgsims -c "SELECT count(*) FROM pg_stat_activity;"`
- If persistent, log as performance issue (see 06_ISSUE_LOG_TEMPLATE.md)

**Action if RED (error or timeout)**:
- Immediately escalate to Technical Lead
- Do not attempt automatic restart without approval
- Document exact error message
- Check logs: `./scripts/pgsims_logs.sh backend`

---

### Step 3: Database Connectivity (3 min)

Run:
```bash
docker compose exec db psql -U pgsims_user -d pgsims -c "SELECT count(*) FROM auth_user;"
```

Expected: Number ≥ 1 (showing users exist)

**Action if ERROR**:
- Database connection failed
- Escalate to Technical Lead immediately
- Do not restart without approval

---

### Step 4: Sample Service Calls (5 min)

**As UTRMC Admin** (if test account available):
```bash
curl -X GET http://localhost:3000/api/dashboard/utrmc/residents \
  -H "Authorization: Bearer [TEST_TOKEN]"
```

Expected: 200 response with resident list (empty okay if no data)

**As Supervisor** (if test account available):
```bash
curl -X GET http://localhost:3000/api/dashboard/supervisor/residents \
  -H "Authorization: Bearer [TEST_TOKEN]"
```

Expected: 200 response with assigned residents

**As Resident** (if test account available):
```bash
curl -X GET http://localhost:3000/api/dashboard/resident/profile \
  -H "Authorization: Bearer [TEST_TOKEN]"
```

Expected: 200 response with user profile

**Action if ERROR (401, 403, 500)**:
- Note exact endpoint and error
- Check backend logs: `./scripts/pgsims_logs.sh backend`
- If authentication issue, check token validity
- If permission issue, check RBAC configuration
- Log as issue (see 06_ISSUE_LOG_TEMPLATE.md)

---

## Post-Check Reporting (5 min)

### Fill in Daily Health Check Log

| Date | Time | Backend | Frontend | Database | Redis | All Endpoints | Issues? | Support Person | Signed Off |
|------|------|---------|----------|----------|-------|---|---|---|---|
| YYYY-MM-DD | HH:MM UTC | ✅/⚠️/❌ | ✅/⚠️/❌ | ✅/⚠️/❌ | ✅/⚠️/❌ | ✅/⚠️/❌ | Yes/No | Name | Time |
| 2025-05-13 | 08:00 | ✅ | ✅ | ✅ | ✅ | ✅ | No | Support Person | 08:15 |

---

### If Any Issues Found

1. **Document issue with timestamp**
   - Time discovered
   - Service affected
   - Error message or symptom
   - Impact (blocking? degraded? informational?)

2. **Notify on-call**
   - Email or Slack to Technical Lead
   - Include error message and screenshot
   - Include this health check log

3. **Create Issue Log Entry** (see 06_ISSUE_LOG_TEMPLATE.md)
   - Date, time, service, severity
   - Add to central issue tracker

4. **Do NOT attempt fix without approval**
   - Exception: Restart containers if explicitly authorized
   - All changes must be logged

---

## If Reboot Required (Emergency Only)

**Authorization required before restart**

If approved by Technical Lead:
```bash
./scripts/pgsims_restart.sh
```

Then:
1. Wait 60 seconds for startup
2. Run health check again: `./scripts/pgsims_health.sh`
3. Verify all services back to green
4. Document restart reason and timestamp
5. Notify UTRMC lead

---

## Daily Log Template

```
=== DAILY HEALTH CHECK LOG ===
Date: YYYY-MM-DD
Time: HH:MM UTC
Support Person: [Name]

CONTAINER STATUS:
[Paste output from pgsims_ps.sh]

HEALTH ENDPOINTS:
[Paste output from pgsims_health.sh]

ISSUES: [Yes/No]
[If yes, list each issue with timestamp and description]

ACTIONS TAKEN:
[List any restarts, escalations, or fixes]

SIGNED OFF: [Name] at [HH:MM UTC]
```

---

## Escalation Contacts

| Level | Role | Contact | Availability |
|-------|------|---------|---|
| Tier 1 | Support Person | See 01_PILOT_USER_LIST_TEMPLATE.md | Daily |
| Tier 2 | Technical Lead | See 01_PILOT_USER_LIST_TEMPLATE.md | Business hours + on-call |
| Tier 3 | UTRMC Lead | See 01_PILOT_USER_LIST_TEMPLATE.md | Business hours |

---

**Created**: 2025-05-13
**Version**: 1.0
**Review Schedule**: Daily during pilot
