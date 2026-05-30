# UI_VERIFICATION — Backup Center

Date (UTC): 2026-05-30

## Route verified
- Backup Center route: `/dashboard/utrmc/backup`

## What was verified (automated)
1. **Frontend unit tests**
   - Backup Center page renders key sections/actions:
     - Create Regular System Backup
     - Create Full Server Recovery Backup
     - Backup History table
     - Restore Wizard section
     - Audit Log section
   - Restore Wizard safety UX:
     - Final restore button stays disabled until:
       - password provided
       - typed confirmation `RESTORE`
       - acknowledgement checkbox checked

2. **Playwright smoke**
   - `npm run test:e2e:smoke:local` includes `frontend/e2e/smoke/backup_center.spec.ts`:
     - confirms Backup Center route loads and key controls are visible for a trained UTRMC admin user
     - confirms restore control is not exposed to non-superadmin roles (UI shows “Restore is Super Admin only.”)

## Operator usability notes (plain language)
- Backup History provides “Download”, “Check File”, and “View Details”.
- Restore is presented as a wizard/modal with an explicit warning, dry-run validation step, and a triple-lock confirm (password + typed RESTORE + checkbox).

