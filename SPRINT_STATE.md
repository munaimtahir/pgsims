# SPRINT_STATE.md — Urology institutional demonstration bootstrap

## Scope

Bootstrap the canonical FMU → Allied Hospital-I → Urology hierarchy and import the approved 28-row
Urology demonstration workbook into the VPS runtime, with idempotency and evidence.

## Completed work

- Read environment context and established baseline: laptop `c1d8c1e`, VPS `6ed50a4`; checkouts are not synchronized.
- Validated the finalized workbook: five sheets and exactly 28 approved master rows.
- Added `bootstrap_urology_demo` with transactional, title-normalized, idempotent master/resident/workshop/research import.
- Took `/tmp/pgsims_pre_urology_20260910.dump` on the VPS before writes and applied the import.
- Verified 28 residents, 21 MS, 7 FCPS, 28 dates, 28 assignments, 45 workshop completions, and 28 research stages; corrected duplicate supervisors.

## Pending work

1. Run backend/API and web UI smoke checks against the VPS deployment.
2. If Android emulator `pgsims` is available, verify the same resident/master data via canonical API.
3. Commit and push the importer/docs, then transfer the commit to the VPS checkout and rebuild the backend image.

## Closure state

Database population is complete and reproducible; application/API/mobile verification and source
deployment remain open.
