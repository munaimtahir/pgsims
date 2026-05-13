# Pilot Deployment Checklist

## Before pilot

- Docker restart proof completed
- Backend check and migrations completed
- Frontend build completed
- Smoke E2E passed
- Active-surface E2E passed
- Critical E2E passed or expected skips documented
- Backup created
- Restore procedure written
- Rollback procedure written
- Pilot users prepared
- Supervisor mappings verified
- Support person assigned
- Issue reporting channel created
- Out-of-scope features communicated

## During pilot

- Daily health check
- Daily DB backup
- Daily issue log
- No direct DB edits unless documented
- Manual corrections recorded
- User login issues tracked
- Workflow failures categorized

## After pilot

- Export issue list
- Review user feedback
- Classify issues as bug, data issue, training issue, or feature request
- Decide next sprint
- Decide whether to expand pilot
