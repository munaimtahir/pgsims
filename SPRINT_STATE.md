# Deferred coverage and Android backlog — handoff

## Scope
The domain migration is complete: https://pg.vexel.pk is live and healthy on
production source/config `b960af1`. Source was pushed before redeployment; final
verification is in `docs/implementation/20261017_domain_migration/REPORT.md`.
The owner authorized validating and including existing changes, while leaving
broader coverage/Android goals pending. No further backlog implementation is
part of the completed domain migration.

## Completed Work
- Migration checks pass: backend 1,256, frontend 421, Android 60 unit tests; builds/lint, identity and brick 6–12 gates pass.
- Production images, runtime origin settings, shared Caddy, agent instructions and docs updated; unrelated services and data preserved.

## Pending Work
1. For the next coverage sprint, read `docs/implementation/20260921_coverage_95/COVERAGE_TARGETS.md` and `scripts/coverage_manifest.json`; backend baseline is 84.22% lines / 69.19% branches, below 85% / 70% overall plus per-area requirements.
2. Provision supported test dependencies with `python3 -m venv /tmp/pgsims-coverage-venv` and `/tmp/pgsims-coverage-venv/bin/pip install -r backend/requirements.txt -r backend/requirements-dev.txt`. After committing new coverage changes, run `COVERAGE_PYTHON=/tmp/pgsims-coverage-venv/bin/python /tmp/pgsims-coverage-venv/bin/python scripts/coverage_gate.py backend`, then the named profile report. Current evidence has matching source content but pre-commit provenance; do not relabel it.
3. Follow the preserved Android scope in `docs/implementation/20260921_coverage_95/ANDROID_BACKLOG_SNAPSHOT.md`; authenticated/connected/physical-device acceptance requires the Laptop's dedicated `pgsims` AVD and authorized fixtures.
4. Read `docs/implementation/20261017_domain_migration/PREVIOUS_SPRINT_HANDOFF.md` for both prior ledger branches before choosing further work; reconcile obsolete items against committed demo evidence rather than re-seeding production.

## Environment Notes
This checkout is the VPS at `/home/munaim/srv/apps/pgsims`; the Laptop has not
been synchronized. The default local `.venv` has Django 4.2, while requirements
and production use 5.2. The migration used an isolated temporary Django 5.2 overlay on this VPS;
provision the supported test environment described above for future work. No Android release
or external integration activation was performed in the domain migration.
