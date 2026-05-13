# Issue Log Template

**Pilot Date**: TBD
**Created**: 2025-05-13

---

## Instructions

1. Log EVERY issue encountered during pilot, no exceptions
2. Fill in all fields immediately when issue is reported
3. Update status as issue is investigated and resolved
4. Include screenshots/logs for all technical issues
5. Weekly review meeting to discuss all issues
6. Archive after pilot completion

---

## Active Issue Log

| Date | Time | User | Role | Issue | Workflow | Severity | Screenshot/Log | Status | Assigned To | Resolution | Resolved Date | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| YYYY-MM-DD | HH:MM UTC | Name | resident/supervisor/admin | Description | logbook/leave/schedule/dashboard | Critical/High/Medium/Low | Yes/No | open/in-progress/resolved/escalated | Support Person | TBD | TBD | |
| 2025-05-13 | 09:00 | TBD | resident | Cannot submit logbook entry | logbook | High | Yes | in-progress | Tech Lead | Database lock detected, restarting backend | TBD | Temporary workaround: try again in 5 min |

---

## Severity Levels

| Level | Definition | Response Time | Example |
|---|---|---|---|
| **Critical** | System down or data loss | Immediate (< 5 min) | Backend not responding, data corruption, auth bypass |
| **High** | Core workflow blocked | <1 hour | Cannot submit logbook, cannot approve leave |
| **Medium** | Workflow degraded | <4 hours | Slow performance, UI bug, minor data inconsistency |
| **Low** | Cosmetic or informational | <1 day | UI text wrong, help link broken, typo |

---

## Issue Reporting Template

When reporting an issue, provide:

```
Date: YYYY-MM-DD
Time: HH:MM UTC
User: [Name]
User Role: [resident/supervisor/admin]
Affected Workflow: [logbook/leave/schedule/dashboard]
Severity: [Critical/High/Medium/Low]

ISSUE DESCRIPTION:
[What happened? What was user trying to do?]

EXACT ERROR MESSAGE (if applicable):
[Copy-paste full error text]

STEPS TO REPRODUCE:
1. [Step 1]
2. [Step 2]
3. [Step 3]

EXPECTED BEHAVIOR:
[What should have happened?]

ACTUAL BEHAVIOR:
[What actually happened?]

IMPACT:
- User(s) affected: [How many? Which roles?]
- Data at risk: [Yes/No - any data corruption?]
- Blocking: [Yes/No - blocks core workflow?]

SCREENSHOT/LOG ATTACHED: Yes/No
  [If yes, include file path or attach]

WORKAROUND (if any):
[Temporary fix the user can try]
```

---

## Investigation Checklist (For Tech Lead)

When assigned an issue:

- [ ] Reproduce issue in test environment
- [ ] Check backend logs: `./scripts/pgsims_logs.sh backend`
- [ ] Check frontend logs: `./scripts/pgsims_logs.sh frontend`
- [ ] Check database: `docker compose exec db psql ...`
- [ ] Check Redis: `docker compose exec redis redis-cli ...`
- [ ] Review related code changes
- [ ] Identify root cause
- [ ] Determine fix strategy
- [ ] Update issue status to "in-progress"
- [ ] Notify reporter of status
- [ ] Test fix in staging (if applicable)
- [ ] Deploy fix (if applicable)
- [ ] Verify issue resolved
- [ ] Update issue status to "resolved"
- [ ] Document root cause and fix

---

## Resolution Categories

| Category | Example | Action |
|---|---|---|
| **Code Bug** | Logic error in backend/frontend | Create fix, test, deploy |
| **Configuration** | Missing env variable, wrong setting | Update config, restart |
| **Database** | Stale data, lock, constraint violation | Manual correction + log |
| **Infrastructure** | Container crash, disk full | Restart, scale, or debug |
| **User Error** | Forgot password, wrong role | Educate user, no code change |
| **Design Issue** | Confusing UI, missing feature | Document limitation, defer to post-pilot |
| **Third-Party** | External service down | Wait for service restoration |

---

## Weekly Issue Review Meeting

**Every Friday at 17:00 UTC**

Attendees: Support Person, Technical Lead, UTRMC Lead, Pilot Lead

Agenda:
1. Review all issues logged this week
2. Classify by root cause
3. Identify patterns or systemic issues
4. Discuss resolved issues
5. Discuss open/unresolved issues
6. Escalate critical issues
7. Plan fixes for next week
8. Update risk register (see docs for risk tracking)

Outcome: Documented meeting notes + action items

---

## Issue Escalation Path

```
CRITICAL ISSUE
     ↓
Support Person notifies Technical Lead (immediately)
     ↓
Tech Lead investigates (within 5 min)
     ↓
If ROOT CAUSE UNKNOWN after 15 min:
  → Escalate to UTRMC Lead
  → May pause pilot operations
     ↓
If ROOT CAUSE FOUND:
  → Implement fix
  → Verify fix
  → Update issue log
  → Resume operations
```

---

## Post-Pilot Issue Archive

After pilot completes:
1. Mark all remaining open issues as "deferred"
2. Export entire issue log as CSV
3. Save to: `docs/_pilot_launch/20260513_controlled_pilot/issue_log_archive_[DATE].csv`
4. Create summary report:
   - Total issues: [#]
   - By severity: Critical [#], High [#], Medium [#], Low [#]
   - By category: Code [#], Config [#], DB [#], Infra [#], User [#]
   - Resolution rate: [%]
   - Mean time to resolution: [hours]
   - Most common issue: [description]
5. Recommendations for production deployment

---

**Template Version**: 1.0
**Last Updated**: 2025-05-13
