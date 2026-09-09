# SPRINT_STATE.md — Urology institutional demonstration bootstrap

## Scope

Bootstrap the canonical FMU → Allied Hospital-I → Urology hierarchy and import the approved 28-row
Urology demonstration workbook into the VPS runtime, with idempotency and evidence.

## Completed work

- Read environment context and established baseline: laptop and VPS are now synchronized at the current implementation SHA after fast-forward deployment.
- Validated the finalized workbook: five sheets and exactly 28 approved master rows.
- Added `bootstrap_urology_demo` with transactional, title-normalized, idempotent master/resident/workshop/research import.
- Took `/tmp/pgsims_pre_urology_20260910.dump` on the VPS before writes and applied the import.
- Verified 28 residents, 21 MS, 7 FCPS, 28 dates, 28 assignments, 45 workshop completions, and 28 research stages; corrected duplicate supervisors.
- Configured MS Urology with 60 months, policy, month-24/month-60 milestones, six workshop requirements, five programme-relative rotation templates, research gates, and logbook requirements.
- Added programme configuration documentation and `DEMO_RUNBOOK.md`; documented absent curriculum PDF, unsupported programme-linked portfolio/exam blueprint, and FCPS source boundary.

## Pending work

1. Commit and push the programme configuration/importer/docs, then fast-forward the VPS checkout and rebuild only the backend image.
2. Run authenticated backend/API and web UI smoke checks if a suitable admin session is available.
3. If Android emulator `pgsims` is available, verify the same resident/master data via canonical API.

## Closure state

Database population and programme configuration are complete and reproducible; authenticated
application/API/mobile verification and source deployment of the final commit remain open.
