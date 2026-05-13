# PGSIMS Controlled Pilot - Scope Definition

**Pilot Date Range**: TBD (select after handoff)
**Pilot Cohort Size**: 1 department, 2–3 supervisors, 5–10 residents
**Support Contact**: TBD (assign from pilot team)
**Status**: READY FOR ACTIVATION

---

## Included Workflows ✅

### User Access & Authentication
- ✅ User login (email/password or SSO)
- ✅ User logout
- ✅ Session management
- ✅ Role-based access control (RBAC)

### UTRMC Admin Dashboard (/dashboard/utrmc)
- ✅ UTRMC admin login
- ✅ View all residents in pilot cohort
- ✅ View all supervisors in pilot cohort
- ✅ View department details
- ✅ View rotation assignments
- ✅ View leave requests and approvals
- ✅ Export pilot data for reporting

### Supervisor Dashboard (/dashboard/supervisor)
- ✅ Supervisor login
- ✅ View assigned residents
- ✅ Review resident logbook entries
- ✅ Return logbook entries for revision
- ✅ Approve logbook entries
- ✅ Manage resident leave requests
- ✅ Approve/reject leave requests
- ✅ View resident schedule

### Resident Dashboard (/dashboard/resident)
- ✅ Resident login
- ✅ View personal schedule
- ✅ View assigned supervisor(s)
- ✅ Submit logbook entries
- ✅ View logbook entry status (draft/submitted/returned/approved)
- ✅ Revise and resubmit logbook entries
- ✅ Submit leave requests
- ✅ View leave request status
- ✅ View personal profile

### Resident Schedule
- ✅ View daily schedule
- ✅ View rotation details (department, hospital, dates)
- ✅ View shift times and supervisor assignments
- ✅ Export schedule

### Resident Logbook
- ✅ Submit new logbook entry (date, procedures, learning points)
- ✅ Save as draft
- ✅ Submit for supervisor review
- ✅ Receive feedback from supervisor
- ✅ Revise and resubmit after feedback
- ✅ View approval status
- ✅ View entry history

### Supervisor Review/Approval
- ✅ View pending logbook entries
- ✅ Add feedback (optional)
- ✅ Return entry to resident for revision
- ✅ Approve entry
- ✅ Reject entry with reason
- ✅ View audit trail of entries

### Resident Leave Workflow
- ✅ Submit leave request (date range, type, reason)
- ✅ Save as draft
- ✅ Submit for supervisor approval
- ✅ Receive supervisor decision
- ✅ View leave balance
- ✅ View approval history

### Supervisor Leave Approval
- ✅ View pending leave requests
- ✅ Approve leave request
- ✅ Reject leave request with reason
- ✅ View leave calendar for assigned residents
- ✅ Download leave report

### RBAC Enforcement (Role-Specific Access)
- ✅ **utrmc_admin** role: Full access to UTRMC dashboard and reports
- ✅ **supervisor** role: Access only to dashboard/supervisor and assigned residents
- ✅ **resident** role: Access only to dashboard/resident, personal schedule, personal logbook
- ✅ **pg** alias for resident role
- ✅ Unauthorized access returns 403 Forbidden
- ✅ Role verification on every request

### Bulk Setup (Preview/Controlled Only)
- ✅ Dry-run mode: Preview data import without committing
- ✅ CSV upload for bulk resident/supervisor creation
- ✅ Validation report before import
- ✅ No auto-import; manual review required
- ✅ Audit trail of all bulk operations

---

## Excluded Workflows ❌

### Analytics & Reporting
- ❌ Analytics dashboard (/dashboard/analytics)
- ❌ Live performance feed
- ❌ Statistical reporting
- ❌ Trend analysis
- ❌ Reports scheduled delivery

### Research Module (Deferred)
- ❌ Research project creation
- ❌ Research workflow submission
- ❌ Research supervisor assignment
- ❌ Research approval process
- ❌ Any research-related routes

### Admin Portal (Future Phase)
- ❌ /dashboard/admin
- ❌ /dashboard/admin/analytics
- ❌ System-wide configuration
- ❌ User management via admin UI
- ❌ Audit trail viewer
- ❌ System health dashboard

### Advanced Features
- ❌ Multi-department rotation
- ❌ Inter-hospital policy complex cases
- ❌ Integration with external calendars
- ❌ SMS notifications
- ❌ Mobile app
- ❌ Advanced scheduling algorithms

---

## Pilot Rules (Non-Negotiable)

1. **Limited Cohort Only**
   - Exactly 1 department
   - 2–3 supervisors
   - 5–10 residents
   - No additional users without approval

2. **Daily Backup Requirement**
   - Use `./scripts/pgsims_seed_e2e.sh` for backup verification
   - Weekly full database backup to external storage
   - Backup verification log maintained daily (see 05_DAILY_BACKUP_CHECK.md)

3. **Daily Health Checks**
   - Run `./scripts/pgsims_health.sh` every morning
   - Log results (see 04_DAILY_HEALTH_CHECK.md)
   - Alert on-call if any endpoint returns non-200

4. **Issue Logging**
   - All issues must be logged with timestamp, user, role, workflow, severity
   - Screenshot/logs attached for every issue
   - Issue log centralized (see 06_ISSUE_LOG_TEMPLATE.md)
   - NO silent fixes; all corrections logged

5. **No Direct Database Edits**
   - All data changes via UI only
   - Exception: Data corrections require:
     - Documented reason
     - Approval from UTRMC admin
     - Audit trail entry
     - Post-incident review

6. **Support Person Assigned**
   - One named individual available daily
   - Response time: <1 hour for blocking issues
   - Escalation path defined (see 07_USER_SUPPORT_SCRIPT.md)

7. **Pilot User Roster Locked**
   - Users provided and verified before pilot start
   - No additions without 24h advance notice
   - New users added only after testing in staging

8. **Demo Walkthrough Before Go-Live**
   - All stakeholders walk through 08_DEMO_WALKTHROUGH.md (60–90 min)
   - Q&A documented
   - Sign-off from UTRMC lead required

9. **Go-Live Checklist Verified**
   - All items in 09_GO_LIVE_CHECKLIST.md must be ✅
   - No workarounds or exceptions
   - Signed off by pilot lead and UTRMC admin

10. **Rollback Ready**
    - 10_ROLLBACK_QUICK_GUIDE.md is executable from memory
    - Database backup exists and is tested
    - Rollback procedure run in dry-run once before pilot

---

## Success Criteria (Pilot Phase)

### Operational Success
- ✅ Zero unplanned downtime (>1 min) per week
- ✅ All daily health checks pass
- ✅ All backups complete and verified
- ✅ Issue response time <1 hour
- ✅ Issue resolution within 24 hours

### Data Integrity
- ✅ No data loss incidents
- ✅ All transactions logged
- ✅ Audit trail complete and accessible
- ✅ Backup restoration tested and successful

### User Experience
- ✅ <5% user-reported errors
- ✅ <500ms response time for standard operations
- ✅ All core workflows completed successfully
- ✅ Supervisor feedback positive
- ✅ Resident feedback positive

### Compliance & Security
- ✅ No unauthorized access attempts
- ✅ No data breaches
- ✅ RBAC enforced correctly
- ✅ All incidents logged and reviewed

---

## Pilot Exit Criteria (Completion/Rollback Decision)

### Successful Pilot → Production Phase
- All success criteria met for 2+ weeks
- Zero critical issues unresolved
- Stakeholder approval received
- Coverage improvements validated
- Scaling plan approved

### Pilot Failure → Rollback
- Critical data loss incident
- RBAC bypass (unauthorized access)
- >3 unplanned downtimes in one week
- >50% of core workflows failing
- Unresolvable performance issue

---

## Key Contacts

| Role | Name | Email | Phone | Backup |
|------|------|-------|-------|--------|
| UTRMC Lead | TBD | TBD | TBD | TBD |
| Pilot Support | TBD | TBD | TBD | TBD |
| Technical Lead | TBD | TBD | TBD | TBD |
| Supervisor 1 | TBD | TBD | TBD | TBD |
| Supervisor 2 | TBD | TBD | TBD | TBD |
| Supervisor 3 | TBD | TBD | TBD | TBD |

---

**Created**: 2025-05-13 10:00 UTC
**Approved By**: TBD (UTRMC Lead)
**Activation Date**: TBD
