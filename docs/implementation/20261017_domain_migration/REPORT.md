# Production domain migration — 2026-10-17

## Decision and scope

The canonical production web address is **https://pg.vexel.pk**. The retired
institutional web hostname is removed rather than redirected. Existing aliases
`pgsims.alshifalab.pk` and `pgsims.pmc.edu.pk` remain; dedicated Android and staging
hostnames are unchanged. Browser cookies are scoped to the hostname, so users
will sign in again at the new address. The user authorized including the existing workspace
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
  databases, virtual environments and generated files. Production cache backend,
  login throttling and file-logging settings are passed explicitly by Compose,
  preserving effective settings formerly supplied by the image dotenv file.
- Reviewed existing onboarding validation, form-field correction, canonical
  logbook queries, frontend credential/error handling and coverage tooling/tests.
  Restored simultaneous leave-replay coverage alongside the supplied sequential
  replay test so the existing concurrency guarantee remains exercised.
- No new database schema or API payload changes are introduced by the domain migration.

## Validation and deployment

**Verdict: GO for the requested domain migration.** Verified 2026-10-17 at
21:40–21:43 UTC. Production source/config revision:
`b960af16f185400091bf884193bbc201d53a2c0b` (application changes introduced in
`03858c8`). Both source commits were pushed before the production cutover.
Final documentation is committed separately; it does not change deployed code.

### Checks

| Check | Result |
| --- | --- |
| Full backend, normal migrated disposable SQLite database | 1,253 passed, zero failed/skipped |
| PostgreSQL replay/concurrency coverage run | 3 passed, zero failed/skipped |
| Production backend image regression subset | 36 passed on Python 3.11.17 / Django 5.2.18 |
| Domain/shared-proxy regression tests | 5 passed (also included in full backend/image suites) |
| Frontend | Typecheck, lint, production build; 421 tests in 49 suites passed |
| Android | 60 unit tests passed; lintDebug and assembleDebug passed |
| Coverage accounting | 11 tests passed; 318-file source manifest valid |
| Identity/project gates | Update 0 and existing brick 6–12 scripts passed |
| Production Compose | Explicit project/environment configuration validates |
| Production backend schema | System check clean; no missing or pending migrations |

Full backend tests used isolated Django 5.2.18 dependencies because the existing
local virtual environment contained unsupported Django 4.2. The exploratory full
`--no-migrations` run omitted migration-seeded specialty data and produced import
fixture failures; it was discarded in favor of the successful normal-migration
run. The final production-image regression subset also passed independently.

### Cutover and preservation

- Rebuilt backend/worker/beat images and the frontend image from committed code.
  The frontend build completed separately after the combined build stalled.
- Recreated only `pgsims_backend_prod`, `pgsims_frontend_prod`, `pgsims_worker`
  and `pgsims_beat`. Backend/frontend are healthy; worker is ready and beat runs.
- Database and Redis retain their original start times. All unrelated container
  start times are unchanged across the cutover.
- Applied the validated shared Caddy update at `20261017T213945Z`. Maintained and
  active Caddyfiles match exactly. Comparing against the saved pre-change file
  confirms that only the PGSIMS site block changed.
- Existing migrations were preserved; production startup applied no schema
  changes. No database reset, demo seeding, identity repair or volume deletion
  was performed. The database archive was created and its catalog verified.
- Counts before/after match: **70 users, 45 resident profiles, 32 training records**.
- No separate legacy checkout was created or modified; deferred modules were not revived.

### Public access and security

- HTTP `/login` redirects to HTTPS (308); HTTPS `/login` returns 200.
- A valid Let's Encrypt certificate names `pg.vexel.pk`, valid from
  2026-10-17 through 2027-01-15. HTTPS checks kept certificate verification enabled.
  Initial handshake failures during certificate issuance cleared automatically.
- `/healthz/` returns 200 with `status=healthy` and database/cache/Celery all `ok`.
  `/api/health/` returns 200 with database `ok`.
- `/api/auth/me/` and protected document download return 401 without credentials.
  `/media/` returns 404; media is no longer directly exposed by the shared proxy.
- Admin login form POST with the valid CSRF cookie/token and new origin returns
  the expected form validation response (200); an untrusted origin returns 403.
  The CSRF cookie is Secure. No account credentials were submitted.
- CORS preflight accepts the new origin and omits permission for an untrusted origin.
  Django rejects the retired Host header with 400.
- Headless Chrome renders the login form with zero script errors or failed
  JavaScript/CSS assets. All browser requests use `pg.vexel.pk`.
- Existing `pgsims.alshifalab.pk/login` remains accessible (200).
- Case-insensitive Git search finds no retired-domain URL text in tracked files.

Evidence: [public checks](PUBLIC_VERIFICATION.json),
[browser checks](BROWSER_VERIFICATION.json), [certificate](CERTIFICATE.txt),
[test summary](TEST_SUMMARY.json), and [login screenshot](login.png).
Generated full-suite logs/coverage remain under `output/coverage/backend/` on the VPS.

The tested source SHA-256 is
`15829bbedf7382370bfe93e8022e78344721e98c14f69fa7925f1033eaa6030f`,
which matches the deployed source/config revision's measured application/test files.
The test runner began while these changes were uncommitted on `c8ac8ff`; its
strict coverage-report gate correctly rejects the changed commit provenance even
though the source digest matches. No provenance record was rewritten to claim a pass.

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


## Known limitations and handoff

- Previous coverage completion remains pending as agreed: the fresh backend
  measurement is **84.22% lines / 69.19% branches**, below the current overall
  profile targets (85% / 70%), with further per-area work required. The strict
  manual coverage gate is BLOCKED, including the provenance condition above.
- `npm ci` reported 46 dependency audit findings (7 moderate, 38 high, 1 critical)
  across installed dependencies; the lockfile was unchanged. This task did not
  classify those findings or implement dependency remediation.
- `pgsims.pmc.edu.pk` already failed DNS resolution at preflight. Its existing
  alias is preserved; its DNS remains outside this hostname migration.
- Browser verification covers anonymous entry and security behavior. No
  credentialed business workflow or Android physical-device acceptance was run.
- The Laptop checkout was not accessed or synchronized. Fetch/pull the shared
  remote before treating these changes as available there.
- `SPRINT_STATE.md` hands off the deferred coverage/Android backlog after this
  migration. The full prior conflicted ledger is retained in the handoff file.
