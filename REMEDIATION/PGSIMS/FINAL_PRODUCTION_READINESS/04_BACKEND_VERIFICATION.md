# Backend verification

Using disposable `/tmp/pgsims-final-readiness-venv` with Django 5.2.17:

- `manage.py check`: PASS, 0 issues.
- `manage.py makemigrations --check --dry-run`: PASS, no changes.
- `manage.py check --deploy`: runs, but reports existing security/schema-generation warnings.
- Backup orchestration tests: PASS, 22 tests.
- Full Django suite: PASS, 921 tests.
- `repair_identity_profiles`: PASS; 37 users scanned, 0 invalid users, 0 duplicate profiles.
- Disposable PostgreSQL 15 migration from zero: PASS; all migrations applied, Django check passed,
  and the empty database contained 0 users / 0 assignments. Container used tmpfs and was removed.
- VPS checkout verification: PASS for `manage.py check`, migration drift, and the 22-test backup
  orchestration suite using an isolated `/tmp` virtualenv; production containers were not restarted.

The deploy warnings are not hidden: they include `SECURE_SSL_REDIRECT`, short test secret
configuration, and existing drf-spectacular serializer warnings. Full-suite status is recorded in
`TEST_RESULTS.md` after execution.
