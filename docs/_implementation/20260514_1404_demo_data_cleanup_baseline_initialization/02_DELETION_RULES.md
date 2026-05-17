# Deletion Rules

## Command

- `python manage.py reset_demo_data --dry-run`
- `python manage.py reset_demo_data --confirm`

## Safety Rules

- Dry-run is the default.
- Destructive cleanup requires `--confirm`.
- The command prints planned deletion counts before deleting anything.
- The command refuses to run if it would leave no admin/superuser account behind.
- The command preserves at least one admin/superuser account.
- The command accepts `--keep-user` and `--keep-email` for explicit preservation overrides.

## Removal Patterns

The cleanup targets rows with clear test/demo markers, including:

- names, usernames, emails, or codes containing:
  - `e2e`
  - `test`
  - `WF`
  - `Feature`
  - `dummy`
  - `sample`
  - `fake`
  - `demo`
  - generated timestamp-like IDs
- emails ending with:
  - `@test.com`
  - `@example.com`
  - `@pgsims.local`
- hospitals named like:
  - `Hospital e2e-...`
  - `Test Hospital WF-...`
- departments named like:
  - `Department e2e-...`
  - `Test Dept WF-...`

## Dependency Cleanup Order

Cleanup was executed in dependency-safe order:

1. Operational and audit rows tied to fake entities
2. Link tables and assignments
3. Profile and staff rows
4. Users
5. Hospital-department matrix rows
6. Departments
7. Hospitals

## Baseline Rules

- Create only minimum real master data.
- Do not create fake residents or fake supervisors.
- Leave the matrix empty unless a real canonical mapping already exists.
- Leave HOD assignments empty unless a real non-test HOD already exists.

