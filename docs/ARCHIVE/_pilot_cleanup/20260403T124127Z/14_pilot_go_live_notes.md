# Pilot Go-Live Notes

What is already complete:
- Demo/test runtime data removed from the live database
- Canonical hospital/department structure preserved
- Backend no longer auto-runs `create_superadmin` at startup
- App boots and admin login works
- Fill-ready pilot source files and workbook now exist under `pilot_data/first_pilot_run/`

Minimal remaining work before real pilot use:
1. Enter the real finalized supervisor/resident/program/link values into the files under `pilot_data/first_pilot_run/`.
2. Run the reusable import path from a backend image or execution context that includes `import_pilot_bundle.py`.
3. Verify supervisors, residents, and links in the live UI and API.
4. Configure real email delivery if invites / password resets / notifications are required during pilot.
5. Rotate the preserved `admin` credentials away from the known default before actual go-live.

Recommended safe path for completion:
- Controlled backend image rebuild after reviewing unrelated dirty worktree changes, or
- temporary controlled execution path that runs the repo checkout against the live DB without changing the deployed web image

Do not do:
- do not import from `PGSIMS_Demo_CaseSeed_3Months.*`
- do not rebuild and redeploy the whole dirty worktree without first isolating unrelated changes
- do not re-enable startup seeding or auto-admin creation
