# User Support Script - Troubleshooting Guide

**For**: Support Person and Pilot Team
**Created**: 2025-05-13
**Version**: 1.0

---

## Quick Support Checklist

When a user reports an issue:

1. ✅ **Acknowledge immediately** - "I'm here to help. Let me investigate."
2. ✅ **Gather details** - Use templates below
3. ✅ **Check health** - Run `./scripts/pgsims_health.sh`
4. ✅ **Try workaround** - Use troubleshooting guide
5. ✅ **Log issue** - See 06_ISSUE_LOG_TEMPLATE.md
6. ✅ **Escalate if needed** - Notify Technical Lead
7. ✅ **Follow up** - Keep user informed of progress

---

## Common Issues & Resolutions

### Issue 1: Login Failures

**User reports**: Cannot log in / "Invalid credentials" / "Account locked"

**Troubleshooting**:
1. Verify user account exists:
   ```bash
   docker compose exec db psql -U pgsims_user -d pgsims -c "SELECT id, email, is_active FROM auth_user WHERE email='user@hospital.local';"
   ```
   
   If not found → Account not created yet
   - [ ] Escalate to IT for account provisioning
   - [ ] Provide username/email to IT
   - [ ] Wait for account creation
   - [ ] User tries login again after IT confirmation

2. Verify account is active:
   ```bash
   docker compose exec db psql -U pgsims_user -d pgsims -c "SELECT id, is_active, date_joined FROM auth_user WHERE email='user@hospital.local';"
   ```
   
   If `is_active = false` → Account disabled
   - [ ] Ask user to reset password: "Click 'Forgot Password' on login page"
   - [ ] If still fails → Contact IT to enable account
   - [ ] Provide user email to IT

3. Browser cache issue:
   - [ ] User clears browser cache (Ctrl+Shift+Delete or Cmd+Shift+Delete)
   - [ ] User closes and reopens browser
   - [ ] User tries different browser
   - [ ] If works → Cache issue confirmed

4. Password reset:
   - [ ] User clicks "Forgot Password" on login page
   - [ ] User checks email (including spam folder)
   - [ ] User clicks reset link within 1 hour
   - [ ] User enters new password
   - [ ] User tries login with new password

**If still not working** → Escalate to Technical Lead with:
- [ ] User email
- [ ] Screenshot of error
- [ ] Browser type/version
- [ ] Time of attempt
- [ ] DB query results above

---

### Issue 2: Wrong Role / Missing Permissions

**User reports**: "I can't see my residents" / "I can't access this page" / "403 Forbidden"

**Troubleshooting**:
1. Verify user role:
   ```bash
   docker compose exec db psql -U pgsims_user -d pgsims -c "SELECT id, email, groups FROM auth_user WHERE email='user@hospital.local';"
   ```
   
   Expected: User should be in correct group:
   - `utrmc_admin` for UTRMC admins
   - `supervisor` for supervisors
   - `resident` or `pg` for residents

2. If role is wrong:
   - [ ] Update user group via Django admin (if available)
   - [ ] Or via API: `PATCH /api/users/[id]/ { "groups": ["supervisor"] }`
   - [ ] Restart session: User logs out and logs back in

3. If role is correct but permissions denied:
   - [ ] Check supervisor-resident mapping (see 03_SUPERVISOR_RESIDENT_MAPPING_TEMPLATE.md)
   - [ ] Run: `docker compose exec db psql -U pgsims_user -d pgsims -c "SELECT * FROM rotations_rotation WHERE supervisor_id='[id]';"`
   - [ ] If no results → User not assigned to residents
   - [ ] Escalate to UTRMC Lead to manually assign residents

**If still not working** → Escalate to Technical Lead with:
- [ ] User email
- [ ] Expected role
- [ ] Actual role (from DB query)
- [ ] Expected access
- [ ] Actual error/screenshot

---

### Issue 3: Missing Resident / Supervisor

**User reports**: "I don't see my resident in the list" / "My supervisor is not showing up"

**Troubleshooting**:
1. Verify data import completed:
   ```bash
   docker compose exec db psql -U pgsims_user -d pgsims -c "SELECT count(*) FROM academics_resident;"
   ```
   
   If 0 → Data not imported yet
   - [ ] Contact data owner to run import
   - [ ] See 02_PILOT_DATA_COLLECTION_TEMPLATE.md for import procedure
   - [ ] Verify mapping after import

2. Verify mapping exists:
   ```bash
   docker compose exec db psql -U pgsims_user -d pgsims -c "SELECT * FROM rotations_rotation WHERE resident_id='[id]' AND supervisor_id='[id]';"
   ```
   
   If no results → Mapping not created
   - [ ] Contact UTRMC Lead
   - [ ] See 03_SUPERVISOR_RESIDENT_MAPPING_TEMPLATE.md
   - [ ] Update mapping and restart session

3. Browser cache issue:
   - [ ] User clears browser cache
   - [ ] User closes and reopens browser
   - [ ] User refreshes page (F5 or Cmd+R)

**If still not working** → Escalate to Technical Lead with:
- [ ] User email
- [ ] Missing resident/supervisor name
- [ ] DB query results above

---

### Issue 4: Logbook Submission Error

**User reports**: "Cannot submit logbook entry" / "Submit button does nothing" / "Error: [X]"

**Troubleshooting**:
1. Check browser console for errors:
   - [ ] Open browser Developer Tools (F12)
   - [ ] Go to Console tab
   - [ ] Try submitting again
   - [ ] Screenshot any red error messages
   - [ ] Send screenshot to Support Person

2. Verify backend is responding:
   ```bash
   curl -X POST http://localhost:3000/api/logbook/entries/ \
     -H "Authorization: Bearer [TEST_TOKEN]" \
     -H "Content-Type: application/json" \
     -d '{"date":"2025-05-13","note":"test"}'
   ```
   
   If error → Backend issue
   - [ ] Check logs: `./scripts/pgsims_logs.sh backend`
   - [ ] Look for validation errors or DB errors
   - [ ] Escalate to Technical Lead

3. Check user permissions for this workflow:
   - [ ] Verify user role is "resident"
   - [ ] Verify supervisor is assigned (see Issue 3)
   - [ ] Verify logbook entry status is "draft" or "returned"
   - [ ] User cannot edit "submitted" or "approved" entries

4. Try clearing cache and retry:
   - [ ] Clear browser cache (Ctrl+Shift+Delete)
   - [ ] Close browser
   - [ ] Open browser again
   - [ ] Try submitting again

5. Try different browser:
   - [ ] Use Chrome, Firefox, Safari, or Edge
   - [ ] Try private/incognito window
   - [ ] If works in different browser → Browser cache/extension issue

**If still not working** → Escalate to Technical Lead with:
- [ ] User email
- [ ] Exact error message/screenshot
- [ ] Browser console errors (screenshot)
- [ ] Time of attempt
- [ ] Logbook entry details (date, content)

---

### Issue 5: Leave Approval Workflow

**User reports**: "Cannot approve leave" / "Leave request not showing" / "Cannot submit leave request"

**Troubleshooting**:
1. For submitting leave request (Resident):
   - [ ] Verify resident role: `SELECT groups FROM auth_user WHERE email='...'`
   - [ ] Verify resident is active: `SELECT is_active FROM auth_user WHERE email='...'`
   - [ ] Try different browser/cache clear
   - [ ] Check backend logs for validation errors

2. For approving leave request (Supervisor):
   - [ ] Verify supervisor role: `SELECT groups FROM auth_user WHERE email='...'`
   - [ ] Verify supervisor is assigned to resident: See Issue 3
   - [ ] Check if request exists: `SELECT * FROM leave_request WHERE resident_id='[id]';`
   - [ ] If not found → Resident may not have submitted yet

3. Check request status:
   ```bash
   docker compose exec db psql -U pgsims_user -d pgsims -c "SELECT id, resident_id, status, created_at FROM leave_request WHERE resident_id='[id]' ORDER BY created_at DESC;"
   ```
   
   Supervisor can only approve requests with status `pending`

**If still not working** → Escalate to Technical Lead with:
- [ ] User email, role, assigned residents
- [ ] Leave request ID (from DB query)
- [ ] Expected vs actual status
- [ ] Error message/screenshot

---

### Issue 6: Performance / Slow Loading

**User reports**: "Page is very slow" / "Keeps timing out" / "Freezes for 30 seconds"

**Troubleshooting**:
1. Check system health:
   ```bash
   ./scripts/pgsims_health.sh
   ```
   
   Look for slow services (>500ms response time)
   - [ ] If backend slow → May need restart
   - [ ] If frontend slow → May be browser issue
   - [ ] If database slow → May be query optimization issue

2. Check server load:
   ```bash
   top
   # Or: htop
   # Look for % CPU and memory usage
   ```
   
   If very high (>80%) → Server is overloaded
   - [ ] Check which process is consuming resources
   - [ ] May need to restart services or scale up

3. Check database connections:
   ```bash
   docker compose exec db psql -U pgsims_user -d pgsims -c "SELECT count(*) FROM pg_stat_activity WHERE state='active';"
   ```
   
   If very high (>20) → Database may be bottleneck
   - [ ] Check for long-running queries
   - [ ] Escalate to Technical Lead for query optimization

4. Try from different device/network:
   - [ ] Use different computer
   - [ ] Use mobile phone
   - [ ] If fast elsewhere → User's device/network issue

**If persistent** → Escalate to Technical Lead with:
- [ ] Health check results
- [ ] Server load (top output)
- [ ] DB connection count
- [ ] Which page/workflow is slow
- [ ] User's browser/device/network

---

### Issue 7: Browser / Cache Issues

**General troubleshooting for any "weird" behavior**:

1. **Clear browser cache**
   - Chrome: Settings → Privacy → Clear browsing data
   - Firefox: Preferences → Privacy → Clear Data
   - Safari: Develop → Empty Web Storage
   - Edge: Settings → Privacy → Clear Browsing Data

2. **Use incognito/private window**
   - Chrome: Ctrl+Shift+N
   - Firefox: Ctrl+Shift+P
   - Safari: Cmd+Shift+N
   - Edge: Ctrl+Shift+P

3. **Disable browser extensions**
   - [ ] Turn off ad blockers
   - [ ] Turn off password managers
   - [ ] Turn off VPNs/proxies
   - [ ] Try again

4. **Try different browser**
   - [ ] Chrome (if not already)
   - [ ] Firefox (if not already)
   - [ ] Safari (if not already)
   - [ ] Edge (if not already)

---

## Support Escalation Contacts

| Issue Type | First Contact | Second Contact | Emergency |
|---|---|---|---|
| Login/Auth | Support Person | Technical Lead | UTRMC Lead |
| Permissions | Support Person | UTRMC Lead | Technical Lead |
| Data | Technical Lead | UTRMC Lead | CTO |
| Performance | Technical Lead | CTO | Infrastructure Team |
| System Down | Technical Lead | Infrastructure Team | CTO |

---

## When to Escalate

**Escalate to Technical Lead immediately if**:
- [ ] System down (backend, frontend, or database)
- [ ] Data loss or corruption
- [ ] Unauthorized access
- [ ] User's browser history shows hacking
- [ ] Same error from multiple users
- [ ] Performance degradation affecting >50% workflows
- [ ] Backup/restore issue
- [ ] Cannot reproduce issue after 15 min troubleshooting

**Escalate to UTRMC Lead if**:
- [ ] Multiple critical issues in same day
- [ ] Data integrity concerns
- [ ] Need to pause/rollback pilot
- [ ] Policy or compliance issue
- [ ] Cannot resolve within 2 hours

---

## Support Log Template

```
=== SUPPORT TICKET ===
Ticket #: [Auto-assign]
Date: YYYY-MM-DD HH:MM UTC
Reported By: [Name/Email]
User Role: [resident/supervisor/admin]
Support Person: [Your name]

ISSUE SUMMARY:
[One line describing the problem]

TROUBLESHOOTING STEPS TAKEN:
- [ ] Reproduced issue
- [ ] Checked health: ./scripts/pgsims_health.sh
- [ ] Cleared cache and retried
- [ ] Tried different browser
- [ ] Checked logs: [which logs]
- [ ] DB query results: [results]

ROOT CAUSE:
[What was the root cause, if identified]

RESOLUTION:
[What was done to fix it]

RESOLUTION TIME:
[From report to resolution: X minutes]

FOLLOW UP NEEDED:
Yes/No - [If yes, describe]
```

---

**Created**: 2025-05-13
**Version**: 1.0
**Last Updated**: 2025-05-13
