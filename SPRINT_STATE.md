# SPRINT_STATE.md — Urology workflow approval demo

## Scope

Populate the existing Urology resident/supervisor approval workflows with marked,
idempotent demonstration records and a live-demo runbook.

## Completed work

- Inventoried logbook, evaluation, research, profile-review, documents, rotation, leave, and submission workflows.
- Added `seed_urology_workflow_demo` with dry-run, transaction, marker, and cleanup support.
- Seeded 4 pending/1 approved/1 returned logbooks, 2 pending/1 approved/1 returned evaluations, 3 research states, 3 leave states, and 1 pending/1 approved rotation.
- Took `/tmp/pgsims_pre_urology_workflow_20260910.dump` before workflow writes.
- Verified actual supervisor logbook API approval, then cleaned and reseeded pending demo records.
- Verified actual evaluation API transition from submitted through under-review to approved, then cleaned and reseeded pending demo records.
- Verified second seeder run is idempotent and `python manage.py check` plus 15 academic tests pass.
- Added approval inventory and presentation runbook under `docs/implementation/20260910_urology_institutional_demo/`.

## Pending work

1. Perform authenticated browser smoke testing with supervisor credentials when available; Android workflow exposure remains to be checked.

## Closure state

Seeder, deployment, API smoke test, and database verification are complete; authenticated browser and Android UI checks remain pending account access/device availability.
