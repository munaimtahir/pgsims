# OUT/106 — Import/Export E2E Evidence

## Backend Tests

### Bulk Suite
```
python manage.py test sims.bulk --failfast
Ran 10 tests in 0.775s — OK
```

### Userbase Suite
```
python manage.py test sims.users.test_userbase_api --failfast
Ran 6 tests in 0.376s — OK
```

### Seed Command
```
python manage.py seed_org_data
- Created: AH (Allied Hospital), DHQ, GGH
- Created/Updated: 20 departments
- Linked: 45 matrix entries (AH×20 + DHQ×20 + GGH×5)
```

## Frontend Build
```
npm run build
Build completed successfully (exit code 0)
All 43 routes compiled including:
  /dashboard/utrmc/data-admin/departments
  /dashboard/utrmc/data-admin/export
  /dashboard/utrmc/data-admin/hospitals
  /dashboard/utrmc/data-admin/links
  /dashboard/utrmc/data-admin/matrix
  /dashboard/utrmc/data-admin/residents
  /dashboard/utrmc/data-admin/supervisors
  /dashboard/utrmc/data-admin/templates
```

## Production Smoke
```
curl -I https://pgsims.alshifalab.pk/dashboard/utrmc/data-admin/hospitals
→ 307 (redirect to login, page exists)

curl https://pgsims.alshifalab.pk/api/departments/
→ 401 (auth required, endpoint live)
```

## Playwright
```
npx playwright test e2e/critical/userbase_foundation.spec.ts
2 passed (7.1s) [setup + main test]
```

## Import/Export API Smoke (manual)
- `POST /api/bulk/import/hospitals/dry-run/` — returns 200 with summary
- `POST /api/bulk/import/hospitals/apply/` — upserts hospitals by code
- `GET /api/bulk/exports/hospitals/?file_format=csv` — returns CSV
- `GET /api/bulk/exports/hospitals/?file_format=xlsx` — returns XLSX
