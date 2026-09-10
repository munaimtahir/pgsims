# PostgreSQL verification

Disposable PostgreSQL 15 verification: PASS. A tmpfs-backed `postgres:15-alpine` container was
migrated from zero with all project migrations; Django check passed; initial counts were 0 users and
0 assignments; the container was removed. The VPS production database was not accessed or mutated.

Follow-up execution completed: with one resident and two synthetic supervisors, the database
rejected both a duplicate active assignment and a second active primary assignment (`PASS` for
both constraints). The tmpfs container was removed afterward.
