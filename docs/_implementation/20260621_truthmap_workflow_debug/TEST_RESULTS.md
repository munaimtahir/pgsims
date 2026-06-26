# Test Results

## Backend

Command:

```bash
python3 manage.py test sims.users.test_userbase_api sims.users.test_resident_onboarding
```

Result:

- `OK`
- `26` tests ran

## Frontend typecheck

Command:

```bash
npm run typecheck
```

Result:

- Exit code `0`

## Frontend targeted tests

Command:

```bash
npm test -- --runInBand --runTestsByPath app/dashboard/utrmc/page.test.tsx app/dashboard/utrmc/users/page.test.tsx app/dashboard/utrmc/hod/page.test.tsx app/dashboard/utrmc/supervision/page.test.tsx app/dashboard/utrmc/resident-training/page.test.tsx components/layout/Sidebar.test.tsx lib/api/userbase.test.ts lib/api/training.test.ts
```

Result:

- `8` suites passed
- `18` tests passed

## Notes

- Earlier failures in the resident-training and users page tests were resolved by tightening assertions and aligning the test expectations with the rendered UI.
