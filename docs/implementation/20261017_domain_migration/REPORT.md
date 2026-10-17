# Production domain migration — 2026-10-17

## Decision and scope

The canonical production web address is **https://pg.vexel.pk**. The retired
institutional web hostname is removed rather than redirected. Existing aliases
`pgsims.alshifalab.pk` and `pgsims.pmc.edu.pk` remain; dedicated Android and staging
hostnames are unchanged. The user authorized including the existing workspace
changes after review and relevant validation, without completing their broader
coverage or Android backlogs.

Historical repository reports have had their URL text replaced at the user's
request. Their original dates and test outcomes are historical evidence, not
claims that this new hostname was tested at those dates. This report records the
actual migration and fresh verification.

## Preflight

- Workspace: `/home/munaim/srv/apps/pgsims`, branch `main`, starting commit `c8ac8ff`.
- DNS: `pg.vexel.pk` resolves to `34.46.17.200` from the VPS.
- Before migration, HTTPS failed with a TLS internal-error alert; Caddy had no new-host route.
- Production project: `docker`, `docker/docker-compose.prod.yml`, root `.env`.
- Backend/frontend loopback ports: 8014 / 8082.
- Six production containers were running; PostgreSQL/Redis/backend/frontend healthy.
- Existing `.env` explicitly overrode Compose defaults with the retired domain in
  allowed hosts, CSRF trusted origins and CORS allowed origins. Those individual
  domain values were updated; the intentional frontend `/api` value was preserved.
- The existing sprint ledger contained an unresolved stash conflict. Both sides
  were preserved in `PREVIOUS_SPRINT_HANDOFF.md`; the live ledger tracks this task.

## Implementation

- Replaced old domain references throughout repository text, including historical
  reports, Compose variants, Django defaults, examples, tests and handoff docs.
- Updated agent instructions and canonical infrastructure/deployment guidance.
- Reworked Caddy sync to replace only the PGSIMS site block, validate the complete
  shared configuration before installation, back up both maintained/active files,
  and restore both if reload fails. Dedicated Android routes and unrelated apps
  are preserved. Regression checks cover exact-host matching, nested handlers,
  unrelated sites, and ambiguous/missing-block refusal.
- Canonical routing includes database health and protected media through Django.
  This corrects drift in the former shared site, where health fell through to the
  frontend and media was served directly.
- Added backend Docker context exclusions for runtime credentials, media, logs,
  databases, virtual environments and generated files.
- Reviewed existing onboarding validation, form-field correction, canonical
  logbook queries, frontend credential/error handling and coverage tooling/tests.
  Restored simultaneous leave-replay coverage alongside the supplied sequential
  replay test so the existing concurrency guarantee remains exercised.
- No new database schema or API payload changes are introduced by the domain migration.

## Validation and deployment

Pending completion. Results and deployed commit will be recorded here before closure.

## Recovery

Previous application images are tagged under `pgsims-rollback/*:20261017`.
Private runtime configuration/container snapshots and pre-change shared Caddyfiles
are retained in `/tmp/pgsims-domain-rollback` (mode 0700; not committed). The Caddy
sync script also creates timestamped backups beside maintained/active files.
Application rollback uses those images and restores only the previous domain
settings; database volumes must not be removed or reset.

## Remaining prior-sprint limitations

The coverage hardening targets and authenticated/physical-device Android work
remain separate pending work; see `PREVIOUS_SPRINT_HANDOFF.md` and
`../20260921_coverage_95/`. This migration does not publish an Android release,
activate external integrations, or seed/reset production records.
