# Production domain migration — 2026-10-17

## Scope
Migrate production to https://pg.vexel.pk; validate and include existing workspace
changes, commit/push, redeploy, and verify HTTPS/backend health. Preserve data and
other hosted applications. Prior Android/coverage backlogs are retained in
`docs/implementation/20261017_domain_migration/PREVIOUS_SPRINT_HANDOFF.md`.

## Completed Work
- Inspected live Compose/Caddy, DNS, runtime domain settings, and existing changes.
- Updated repository domain references and runtime domain values; preserved both conflicted backlogs.
- Scoped Caddy sync and regression checks implemented; complete shared candidate validates.
- Django check/schema drift, five domain tests, identity/brick 6–12 gates, frontend typecheck/lint and all 421 frontend tests pass.
- Previous images/configuration saved privately; production database recovery archive catalog verified.
- Full Django 5.2 suites, frontend production build and Android build/lint are running.

## Pending Work
2. Validate included backend/frontend/Android changes and document results.
3. Commit/push reviewed source; build and redeploy production PGSIMS services.
4. Update shared Caddy; verify TLS, login, API, assets, origin security, aliases and health.
5. Commit/push final verification evidence with deployed source hash.
