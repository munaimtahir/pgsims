# Demo Walkthrough Script (60–90 Minutes)

**For**: Stakeholders, pilot team, and participants
**Duration**: 60–90 minutes with Q&A
**Created**: 2025-05-13

---

## Pre-Demo Setup (15 min before)

**Preparation**:
- [ ] Ensure backend, frontend, and all services are running: `./scripts/pgsims_ps.sh`
- [ ] Run health check: `./scripts/pgsims_health.sh` (all green)
- [ ] Open browser to http://localhost:3000 (or pilot URL)
- [ ] Test login with test accounts (if available):
  - [ ] UTRMC admin account
  - [ ] Supervisor account
  - [ ] Resident account
- [ ] Clear browser cache to ensure fresh load
- [ ] Have Issue Log template ready (see 06_ISSUE_LOG_TEMPLATE.md)
- [ ] Have Troubleshooting Guide ready (see 07_USER_SUPPORT_SCRIPT.md)
- [ ] Share screen setup confirmed

---

## Demo Agenda (with timing)

### 1. Welcome & Scope Setting (5 min)

**Say**:
> "Welcome to the PGSIMS controlled pilot launch demo. This is a new digital platform for managing postgraduate medical training at UTRMC. Today we'll walk through what's included in this pilot and what's not yet available. This is a READ-ONLY demo for most of you—we'll show workflows, but won't make permanent changes today."

**Cover**:
- [ ] Pilot cohort: 1 department, 2–3 supervisors, 5–10 residents
- [ ] Duration: TBD (select date)
- [ ] Support person: TBD (assign)
- [ ] Key principle: Daily backups, health checks, issue logging
- [ ] What's in pilot: See 00_PILOT_SCOPE.md
- [ ] What's NOT in pilot: Research, analytics, /dashboard/admin

**Q&A**: Take questions (5 min)

---

### 2. Login Flow (5 min)

**Demo**:
1. Show login page: http://localhost:3000/login
   - Email/password fields
   - "Forgot Password" link
   - "Remember me" checkbox (if available)

2. Login as different roles to show different starting dashboards:
   - [ ] UTRMC admin → show /dashboard/utrmc
   - [ ] Supervisor → show /dashboard/supervisor
   - [ ] Resident → show /dashboard/resident

**Key Points**:
- "Role-based access: each user sees only what they need"
- "Different dashboard for each role"
- "Never share passwords; always use 'Forgot Password' if stuck"

**Q&A**: (2 min)

---

### 3. UTRMC Admin Dashboard (10 min)

**Login as UTRMC admin**

**Show**:
- [ ] Dashboard overview (key metrics, if available)
  - Total residents in pilot
  - Total supervisors
  - Pending approvals
  - Recent activity

- [ ] Resident list view
  - Search and filter by department/program
  - View resident details: program, year, supervisor, schedule

- [ ] Supervisor list view
  - View assigned residents for each supervisor
  - Contact information

- [ ] Reports or exports (if available)
  - Export resident list
  - Export supervisor assignments
  - Pilot participant roster

**Key Points**:
- "UTRMC admin has oversight of all pilot users"
- "Can see who's supervising whom"
- "Can pull reports for compliance"
- "This is a READ-ONLY view in this demo"

**Q&A**: (3 min)

---

### 4. Resident Dashboard & Schedule (15 min)

**Logout and login as resident**

**Show**:
- [ ] Resident home dashboard
  - My schedule
  - My logbook entries (pending, submitted, returned, approved)
  - My leave requests
  - My supervisor(s)

- [ ] View schedule
  - Daily/weekly calendar view
  - Rotation details: department, hospital, supervisor, dates
  - Shift times (if available)
  - Export to calendar

**Key Points**:
- "This is where residents see their assignments and can submit work"
- "Schedule is read-only (set by UTRMC admin)"
- "Logbook and leave are where residents submit work for review"

**Q&A**: (2 min)

---

### 5. Resident Logbook Submission (15 min)

**Demo logbook workflow**:

**Step 1: Create new entry**
- [ ] Click "New Logbook Entry" or similar
- [ ] Show form fields:
  - Date of entry
  - Procedures performed
  - Learning points
  - Reflection (optional)

- [ ] Fill in example data
- [ ] Show "Save as Draft" button
- [ ] Save as draft (DON'T SUBMIT YET)

**Key Points**:
- "Residents can save as draft multiple times"
- "Submit only when ready"
- "Supervisor will review and can ask for changes"

**Step 2: Review entry**
- [ ] Show entry in "My Entries" list
- [ ] Show status: "Draft"
- [ ] Show "Edit" and "Submit" buttons

**Step 3: Submit entry**
- [ ] Click "Submit"
- [ ] Show confirmation dialog
- [ ] Confirm submission
- [ ] Show status changed to "Submitted" (and icon change, if available)

**Key Points**:
- "Once submitted, resident cannot edit until supervisor returns it"
- "Supervisor will review within TBD hours"

**Q&A**: (3 min)

---

### 6. Supervisor Dashboard & Review Workflow (15 min)

**Logout and login as supervisor**

**Show supervisor dashboard**:
- [ ] My residents list
- [ ] Pending items for review
  - New logbook entries to review
  - New leave requests to approve

**Demo logbook review**:
- [ ] Click on pending logbook entry
- [ ] Show entry details (submitted by resident)
- [ ] Show review options:
  - [ ] Add feedback comment
  - [ ] "Approve" button
  - [ ] "Return for Revision" button
  - [ ] "Reject" button (rare)

- [ ] Add sample feedback:
  ```
  Good summary of the procedure. 
  Please elaborate on learning points next time.
  ```

- [ ] Click "Return for Revision"
- [ ] Show confirmation
- [ ] Show entry status changed to "Returned"

**Key Points**:
- "Supervisor can see all assigned residents' submissions"
- "Supervisor can give feedback before approving"
- "Resident can revise and resubmit"
- "This is the core workflow of the logbook"

**Q&A**: (3 min)

---

### 7. Leave Approval Workflow (10 min)

**Continue as supervisor**

**Show leave requests**:
- [ ] Click on "Leave Requests" or similar
- [ ] Show list of pending leave requests
- [ ] Show leave request details:
  - Dates requested
  - Reason (vacation, sick, training, etc.)
  - Days requested
  - Current leave balance

**Demo approval**:
- [ ] Click "Approve"
- [ ] Show confirmation dialog
- [ ] Confirm approval
- [ ] Show status changed to "Approved"

**Demo rejection** (optional):
- [ ] Show different pending request
- [ ] Click "Reject"
- [ ] Add reason: "Conflict with rotation schedule"
- [ ] Confirm rejection
- [ ] Show status changed to "Rejected"

**Key Points**:
- "Supervisor approves leave for assigned residents"
- "Supervisor can see leave balance and history"
- "Resident receives notification of decision"

**Q&A**: (2 min)

---

### 8. RBAC Demonstration (5 min)

**Show access control in action**:

**Demo 1: Supervisor cannot see other supervisors' residents**
- [ ] As Supervisor A, show "My Residents" list
  - Only shows residents assigned to Supervisor A
  - Cannot see Supervisor B's residents

**Demo 2: Resident cannot access supervisor views**
- [ ] Logout, login as resident
- [ ] Try to navigate to supervisor URL (if applicable)
  - Show "403 Forbidden" or redirect to resident dashboard
  - Cannot access supervisor-only pages

**Demo 3: Admin can see everyone**
- [ ] Logout, login as UTRMC admin
- [ ] Show admin can view all residents, all supervisors
- [ ] Show admin can filter by department

**Key Points**:
- "Each role has defined permissions"
- "Residents only see their own data"
- "Supervisors only see their assigned residents"
- "UTRMC admin has full visibility"
- "System enforces permissions automatically"

**Q&A**: (2 min)

---

### 9. What's NOT Included (Defer for Later) (5 min)

**Explicitly state what's NOT in this pilot**:

| Feature | Status | Why Deferred |
|---|---|---|
| Research workflow | ❌ Not included | Requires additional design |
| Analytics dashboard | ❌ Not included | Deferred to Phase 2 |
| /dashboard/admin | ❌ Not included | Deferred to Phase 2 |
| Mobile app | ❌ Not included | Browser-only for pilot |
| SMS notifications | ❌ Not included | Email only for pilot |
| External integrations | ❌ Not included | Manual data entry for pilot |

**Key Points**:
- "This pilot is focused on core workflows only"
- "These features are planned for Phase 2"
- "We need to learn from this pilot before adding more"

---

### 10. Monitoring & Support (5 min)

**Show support resources**:

- [ ] Daily health checks: `./scripts/pgsims_health.sh`
- [ ] Issue logging: 06_ISSUE_LOG_TEMPLATE.md
- [ ] Troubleshooting: 07_USER_SUPPORT_SCRIPT.md
- [ ] Support contact: [TBD name and email]
- [ ] Escalation contacts: [List]
- [ ] Backup verification: 05_DAILY_BACKUP_CHECK.md

**Key Points**:
- "We check system health every morning"
- "All issues are logged and tracked"
- "Support person available during business hours"
- "Emergency escalation procedure in place"
- "Database backed up daily"

---

### 11. Q&A & Feedback (10 min)

**Open floor for questions**:
- [ ] "Any questions about workflows?"
- [ ] "Any concerns about the pilot scope?"
- [ ] "Any technical questions?"
- [ ] "Anything unclear?"

**Collect feedback**:
- [ ] "Is this what you expected?"
- [ ] "Are there critical features missing?"
- [ ] "Any concerns about going live?"

**Distribute feedback form**:
- [ ] Collect written feedback
- [ ] Note any blockers or concerns
- [ ] Document for post-pilot review

**Next Steps**:
- [ ] Pilot start date: [TBD]
- [ ] User provisioning: [TBD]
- [ ] Dry-run data import: [TBD]
- [ ] GO-LIVE checklist review: [TBD]

---

## Demo Troubleshooting

If system is down or slow during demo:

1. **Check health**: `./scripts/pgsims_health.sh`
2. **Try restart**: `./scripts/pgsims_restart.sh` (only if authorized)
3. **Share troubleshooting**: "We're experiencing a temporary issue. While we investigate, let's discuss the workflows instead of clicking through the UI."
4. **Have backup**: Print 00_PILOT_SCOPE.md and walk through it manually
5. **Reschedule if necessary**: "We want to give this a proper demo. Can we reschedule for tomorrow when the system is back to normal?"

---

## Post-Demo Follow-Up

1. **Send summary email** with:
   - Attendee list
   - Topics covered
   - Feedback collected
   - Next steps and dates
   - Support contact information

2. **Address concerns** raised:
   - Document any blockers
   - Create action items
   - Assign owners
   - Track to completion

3. **Prepare for GO-LIVE**:
   - Confirm pilot scope (any changes?)
   - Finalize user list
   - Prepare data import
   - Review 09_GO_LIVE_CHECKLIST.md

---

**Demo Duration**: 60–90 min (depending on Q&A)
**Version**: 1.0
**Created**: 2025-05-13
