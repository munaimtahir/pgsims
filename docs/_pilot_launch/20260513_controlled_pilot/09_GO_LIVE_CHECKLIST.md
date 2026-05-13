# GO-LIVE Checklist

**Pilot Start Date**: TBD
**Launch Lead**: TBD (UTRMC Lead)
**Created**: 2025-05-13

---

## Pre-Flight Verification (24 hours before GO-LIVE)

### Code & Infrastructure ✅

- [ ] Latest code pulled from main branch
  ```bash
  cd /home/munaim/srv/apps/pgsims
  git status
  # Should be: "On branch main" and "nothing to commit"
  ```

- [ ] Helper scripts present and executable
  ```bash
  ls -la scripts/pgsims_*.sh
  # Should show 7 scripts, all with -rwxr-xr-x permissions
  ```

- [ ] `.env` file exists with all required vars
  ```bash
  ls -la .env
  grep -E "SECRET_KEY|DATABASE_URL|REDIS_URL" .env | wc -l
  # Should show at least 3 lines
  ```

- [ ] Docker images built and ready
  ```bash
  docker images | grep pgsims
  # Should show backend, frontend, db images
  ```

- [ ] All containers start and stay healthy
  ```bash
  ./scripts/pgsims_down.sh
  ./scripts/pgsims_up.sh
  sleep 60
  ./scripts/pgsims_health.sh
  # All should show 200 ✅
  ```

---

### Data Verification ✅

- [ ] Database backup created and verified
  ```bash
  ls -lah docs/_implementation/20260513_0912_pilot_deployment_readiness/backups/pgsims_pilot_readiness_backup.sql
  # Should be ≥100 KB
  ```

- [ ] Backup integrity checked (see 05_DAILY_BACKUP_CHECK.md)
  ```bash
  head -10 docs/_implementation/20260513_0912_pilot_deployment_readiness/backups/pgsims_pilot_readiness_backup.sql
  # Should show PostgreSQL dump header
  ```

- [ ] Database empty (ready for pilot data)
  ```bash
  docker compose exec db psql -U pgsims_user -d pgsims -c "SELECT count(*) FROM auth_user;"
  # Should show: count=1 (just superuser, or 0)
  ```

---

### User Provisioning ✅

- [ ] All pilot users created in system
  - [ ] 1 UTRMC admin
  - [ ] 2–3 supervisors
  - [ ] 5–10 residents
  
  ```bash
  docker compose exec db psql -U pgsims_user -d pgsims -c "SELECT count(*) FROM auth_user;"
  # Should match total user count (10–14)
  ```

- [ ] All user accounts tested and verified
  - [ ] Test UTRMC admin login: can see /dashboard/utrmc
  - [ ] Test supervisor login: can see /dashboard/supervisor
  - [ ] Test resident login: can see /dashboard/resident

- [ ] All passwords distributed securely
  - [ ] No passwords in email body
  - [ ] No passwords in Slack/Teams
  - [ ] Only secure password reset links sent
  - [ ] All users confirmed receipt

- [ ] User roles assigned correctly
  ```bash
  docker compose exec db psql -U pgsims_user -d pgsims -c "SELECT email, groups FROM auth_user;"
  # Verify each user has correct group
  ```

---

### Data Import ✅

- [ ] Pilot data collected and cleaned (see 02_PILOT_DATA_COLLECTION_TEMPLATE.md)
  - [ ] CSV file prepared
  - [ ] All required columns present
  - [ ] No blank required fields
  - [ ] All emails valid format
  - [ ] All supervisors assigned

- [ ] Dry-run import completed successfully
  ```bash
  # Use /api/bulk/preview endpoint
  # Upload pilot CSV
  # Verify: 0 errors, all warnings noted
  ```

- [ ] Supervisor-resident mappings verified (see 03_SUPERVISOR_RESIDENT_MAPPING_TEMPLATE.md)
  - [ ] Each resident has exactly 1 primary supervisor
  - [ ] Each supervisor has 3–5 residents
  - [ ] No orphaned residents
  - [ ] All mappings verified by department head

- [ ] Final import dry-run passed
  - [ ] All validations green
  - [ ] Sample data spot-checked
  - [ ] Department head sign-off received

---

### Documentation & Support ✅

- [ ] All operational documents ready
  - [ ] 00_PILOT_SCOPE.md (scope locked)
  - [ ] 01_PILOT_USER_LIST_TEMPLATE.md (users finalized)
  - [ ] 02_PILOT_DATA_COLLECTION_TEMPLATE.md (data cleaned)
  - [ ] 03_SUPERVISOR_RESIDENT_MAPPING_TEMPLATE.md (mappings verified)
  - [ ] 04_DAILY_HEALTH_CHECK.md (procedure understood)
  - [ ] 05_DAILY_BACKUP_CHECK.md (backup tested)
  - [ ] 06_ISSUE_LOG_TEMPLATE.md (issue template ready)
  - [ ] 07_USER_SUPPORT_SCRIPT.md (troubleshooting ready)
  - [ ] 08_DEMO_WALKTHROUGH.md (demo completed, feedback received)
  - [ ] 10_ROLLBACK_QUICK_GUIDE.md (procedure memorized)

- [ ] Support person assigned and trained
  - [ ] Name: [TBD]
  - [ ] Email: [TBD]
  - [ ] Phone: [TBD]
  - [ ] Backup support: [TBD]
  - [ ] Training completed: [ ] Yes
  - [ ] Familiar with troubleshooting guide: [ ] Yes

- [ ] Escalation contacts finalized
  - [ ] Technical Lead: [TBD]
  - [ ] UTRMC Lead: [TBD]
  - [ ] CTO (for critical escalations): [TBD]
  - [ ] All contact info distributed to pilot team

---

### Demo & Stakeholder Sign-Off ✅

- [ ] Demo walkthrough completed (see 08_DEMO_WALKTHROUGH.md)
  - [ ] All stakeholders attended
  - [ ] All workflows demonstrated
  - [ ] Q&A addressed
  - [ ] Concerns documented

- [ ] Feedback reviewed and addressed
  - [ ] Any blockers: [list if any]
  - [ ] Any missing features: [list]
  - [ ] Any scope changes needed: [ ] No changes / [ ] Approved changes [list]

- [ ] UTRMC Lead sign-off received
  - [ ] Signoff Date: [TBD]
  - [ ] Signoff Name: [TBD]
  - [ ] Any conditions: [TBD]

---

## GO-LIVE Day (Execution)

### 1. System Verification (08:00 UTC) ✅

```bash
./scripts/pgsims_ps.sh          # All containers running
./scripts/pgsims_health.sh      # All endpoints 200
git status                      # Working tree clean
./scripts/pgsims_backup.sh      # Final backup created (if available)
```

- [ ] All services running
- [ ] All endpoints healthy
- [ ] No uncommitted changes
- [ ] Final backup created

**Approval**: [ ] Technical Lead sign-off

---

### 2. Data Import (09:00 UTC) ✅

```bash
# Run final dry-run
curl -X POST http://localhost:3000/api/bulk/preview \
  -H "Content-Type: multipart/form-data" \
  -F "file=@pilot_resident_data.csv" \
  -H "Authorization: Bearer [ADMIN_TOKEN]"

# Verify: 0 errors, all warnings noted

# Commit import
curl -X POST http://localhost:3000/api/bulk/import \
  -H "Content-Type: multipart/form-data" \
  -F "file=@pilot_resident_data.csv" \
  -H "Authorization: Bearer [ADMIN_TOKEN]"

# Verify import success
docker compose exec db psql -U pgsims_user -d pgsims \
  -c "SELECT count(*) FROM academics_resident;"
# Should show: count >= 5
```

- [ ] Dry-run passed (0 errors)
- [ ] Import completed successfully
- [ ] Resident count matches expected
- [ ] Supervisor mappings verified

**Approval**: [ ] Data Owner sign-off

---

### 3. Smoke Test (09:30 UTC) ✅

Run full E2E smoke test:
```bash
cd frontend && npm run test:e2e:smoke:local 2>&1 | tee /tmp/smoke_test.log
```

Expected: All 17 smoke tests pass

- [ ] All smoke tests pass (17/17)
- [ ] No critical errors
- [ ] Response times acceptable (<2 sec per page)

**Approval**: [ ] Technical Lead sign-off

---

### 4. User Access Verification (10:00 UTC) ✅

Verify each user type can log in and see expected dashboard:

- [ ] UTRMC admin can log in → sees /dashboard/utrmc
- [ ] Supervisor 1 can log in → sees /dashboard/supervisor → sees assigned residents
- [ ] Supervisor 2 can log in → sees different residents (correct mappings)
- [ ] Resident 1 can log in → sees /dashboard/resident → sees schedule and logbook

**Approval**: [ ] Support Person sign-off

---

### 5. Pilot Team Notification (10:30 UTC) ✅

Send email to all pilot users:

```
Subject: PGSIMS Pilot System Live - Welcome!

Dear Pilot Participants,

The PGSIMS system is now live for our controlled pilot phase. 
You can log in at: [URL]

Your username: [provided earlier]
First-time login: Use "Forgot Password" link

What's included:
- Resident schedule view
- Logbook submission and review
- Leave request and approval
- RBAC-enforced access

Support contact: [Support Person] - [Email] - [Phone]
Troubleshooting guide: [Shared document link]

Thank you for participating!
[UTRMC Lead]
```

- [ ] Email sent to all pilot users
- [ ] Support contact confirmed
- [ ] Issue log ready

---

### 6. Daily Operations Start (Next Day, 08:00 UTC) ✅

Begin regular operations:

- [ ] Run daily health check (see 04_DAILY_HEALTH_CHECK.md)
- [ ] Run daily backup check (see 05_DAILY_BACKUP_CHECK.md)
- [ ] Monitor for issues reported by users
- [ ] Respond to support requests
- [ ] Log all issues (see 06_ISSUE_LOG_TEMPLATE.md)

---

## Post-GO-LIVE (First Week)

### Daily Checks

- [ ] 04_DAILY_HEALTH_CHECK.md every morning (08:00 UTC)
- [ ] 05_DAILY_BACKUP_CHECK.md every morning (08:30 UTC)
- [ ] Issue log reviewed daily (16:00 UTC)

### Weekly Review

- [ ] Friday 17:00 UTC: Issue log review meeting
- [ ] Document all issues and resolutions
- [ ] Discuss any patterns or systemic issues
- [ ] Plan fixes for next week

### Success Criteria (First 2 Weeks)

- [ ] Zero unplanned downtime (>1 min per day)
- [ ] All health checks pass
- [ ] All backups complete and verified
- [ ] Issue response time <1 hour
- [ ] Issue resolution within 24 hours
- [ ] User feedback positive
- [ ] No data loss incidents
- [ ] All stakeholders report satisfaction

---

## If GO-LIVE Blocked

If any go-live verification fails:

**STOP** - Do not proceed

1. Document exact failure
2. Contact Technical Lead
3. Investigate root cause
4. Fix the issue
5. Re-run verification
6. Get re-approval
7. Retry GO-LIVE (next available time slot)

**Possible block scenarios**:
- Docker containers not starting
- Health check failing
- Smoke tests failing
- Data import failing
- Users cannot log in
- Database backup missing/corrupt

---

## GO-LIVE Sign-Off

| Role | Name | Date | Time | Approval |
|---|---|---|---|---|
| UTRMC Lead | [TBD] | [TBD] | [TBD] | ✅/❌ |
| Technical Lead | [TBD] | [TBD] | [TBD] | ✅/❌ |
| Data Owner | [TBD] | [TBD] | [TBD] | ✅/❌ |
| Support Person | [TBD] | [TBD] | [TBD] | ✅/❌ |

**Verdict**: [APPROVED / BLOCKED]

---

**Created**: 2025-05-13
**Version**: 1.0
**Ready for Activation**: TBD
