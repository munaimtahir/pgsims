# E2E verification

Status: CONDITIONAL / NOT CLEARED.

An isolated canonical PostgreSQL 15 → Django → Next.js stack was built and started with disposable
test-only environment values. Migration completed from an empty database, synthetic seed data was
loaded, and the stack was removed with its project-scoped volumes after testing. No VPS production
service, database, or volume was touched.

Playwright Chromium was installed locally. Smoke initially failed before launch because the browser
binary was absent; after installation it executed 25 tests with 11 passing and 14 failing. The
remaining failures are stale E2E contracts against the current clean-room UI: legacy UTRMC admin
role assumptions, retired duplicate UTRMC subroutes, old dashboard labels, old baseline admin
credentials, and UI-pilot spoofing of non-canonical roles. These are not certified as application
passes. Workflow-gate, RBAC, cross-supervisor denial, and resulting database-state suites remain
pending until the E2E fixture/contracts are migrated to the canonical four-role architecture.
