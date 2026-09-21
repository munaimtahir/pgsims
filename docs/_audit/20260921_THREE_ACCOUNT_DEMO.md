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

## Deployed verification

- Source `822fab8` pushed to origin/main and fast-forwarded on the VPS at
  `/home/munaim/srv/apps/pgsims`. The one new command module was copied from that
  checkout to the running backend container; no service restart or image rebuild
  was necessary for this administrative command. Runtime application code was
  otherwise unchanged.
- Live preview: 20 missing examples, valid existing profiles 36/3, training 11,
  primary assignment 4. Admin/supervisor/resident accounts were already active,
  profile-complete and free of password-change gates; no flags were altered.
- First apply: 20 records created, 0 missing, all initial states as requested.
- Second apply: 0 created, 20 existing, no states reset. Four optional synthetic
  image files were uploaded through the normal document upload handler.
- IDs: logbook 34–37; evaluation 22–25; leave 22–25; rotation 7–10; documents 5–8.
- All 60 direct role-specific retrieve-handler checks passed on the deployed
  dataset, with stored attachment existence checked.
- 120 authenticated public HTTPS retrievals passed across both web and Android
  hosts (20 records × 3 accounts × 2 hosts). Short-lived access tokens were created
  in memory and were neither logged nor persisted; account passwords were unchanged.
- Seven real Android list/queue endpoints were checked, including paginated
  traversal: resident rotations/leaves/documents; supervisor pending leave,
  rotation, academic logbook and evaluation feeds. All expected seeded IDs found.
- A before/after state comparison confirms the verification did not consume
  pending workflow actions. User count remains 70. Academic review queue total
  for this pair is 9, including 4 new pending reviews.
- Production `/api/health/`: HTTP 200, database OK.
- Local `manage.py check`: 0 issues; `makemigrations --check --dry-run`: no changes;
  `scripts/check_update_0_identity_cleanup.sh`: PASS; `git diff --check`: PASS.

## Verdict and limitations

**GO for the requested dataset preparation and API availability.** This is not a
new production-readiness certification or full browser/physical-device acceptance.
No installed-device or browser mutation rehearsal was performed; existing UI
limitations are explicitly mapped in `DEMO_WALKTHROUGH.md`. In particular document
review is API-only, web returned-entry editing is limited, and the installed
Android app may lag current source. Public-URL privacy and other production audit
items remain outside this seed task.

No schema or public-contract change. No legacy directory modified or recreated.
Unrelated untracked `docs/_audit/20260921_GOOGLE_WORKSPACE_SSO_SPEC.md` preserved.
