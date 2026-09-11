# E2E verification

Status: CONDITIONAL / NOT CLEARED.

An isolated canonical PostgreSQL 15 → Django → Next.js stack was built and started with disposable
test-only environment values. Migration completed from an empty database, synthetic seed data was
loaded, and the stack was removed with its project-scoped volumes after testing. No VPS production
service, database, or volume was touched.

Playwright Chromium was installed locally. After migrating the smoke fixtures to the canonical
four-role routes, labels, credentials, and disabled public-registration contract, smoke passed
25/25. Workflow-gate executed 4 tests: 1 passed and 3 failed on stale contracts targeting retired
UTRMC onboarding routes/labels and the retired resident schedule leave-entry flow. RBAC,
cross-supervisor denial, and resulting database-state suites remain pending until those workflow
fixtures are migrated to the canonical architecture.
