# PostgreSQL verification

Disposable PostgreSQL 15 verification: PASS. A tmpfs-backed `postgres:15-alpine` container was
migrated from zero with all project migrations; Django check passed; initial counts were 0 users and
0 assignments; the container was removed. The VPS production database was not accessed or mutated.

Synthetic assignment uniqueness and duplicate-primary rejection were not separately exercised in
this pass and remain follow-up coverage.
