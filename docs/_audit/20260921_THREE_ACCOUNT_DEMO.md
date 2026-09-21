# Three-account demo implementation evidence

Owner scope: populate existing `admin`, `supervisor`, `resident` profiles with
linked synthetic examples for web and Android. The owner explicitly confirmed
that deployed data is demonstration data. No new accounts or profile replacements.

## Implementation

`seed_three_account_demo` provides mutually exclusive `--dry-run`, `--apply`,
`--verify` modes. Fixed account/profile/training/assignment preflight, serialized
apply, stable dataset keys, transaction rollback, file-write tracking, outbound
transport suppression, and role-specific read-handler verification are included.
Canonical academic services create review queues and audit history. Existing
leave/rotation/document action handlers create and transition the other records.
No schema, public API, role, or frontend changes.

## Isolated verification

Python 3.12 / Django 5.2.17, disposable in-memory SQLite database:

```bash
SECRET_KEY=demo-test-only DATABASE_URL=sqlite:///:memory: \
  /tmp/pgsims-demo-venv/bin/python -m pytest \
  sims/users/test_three_account_demo.py --no-cov -q
```

Result: **15 passed**, 38.92 seconds. Focused run; full-suite coverage threshold
disabled because it is not a full-suite coverage measurement.

Coverage includes no-write preview; missing identity/profile/wrong role;
ambiguous training/missing assignment; no-fit dates; idempotent replay preserving
completed actions; unchanged users/profiles/requirements/training/assignment;
late transaction failure with attachment cleanup; ownership mismatch; missing
attachment detection; 60 role-specific retrieve-handler checks; live-handler
leave/rotation/logbook/evaluation/document actions; outbound transport suppression;
and valid/invalid academic-session import previews.

Production and client verification pending transfer/apply. No full browser or
physical-device acceptance is claimed by the isolated test result.
