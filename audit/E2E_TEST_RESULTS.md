# E2E Test Results

## Canonical smoke gate

Command:

```bash
cd frontend && npm run test:e2e:smoke:local
```

Result: **PASS**

Summary:
- `17 passed`
- 0 failed

## Functional verification highlights

- Login form success path works for:
  - `e2e_utrmc_admin` -> `/dashboard/utrmc`
  - `e2e_supervisor` -> `/dashboard/supervisor`
  - `e2e_pg` -> `/dashboard/resident`
- Invalid login remains on `/login` with visible error.
- Public-route guards redirect unauthenticated users to `/login`.
- Dashboard smoke pages load for seeded roles.

## Regression against prior baseline

Prior stabilization baseline recorded:
- smoke suite runnable, but `7 passed / 10 failed`
- failures included `/login` loops and `localhost:8000` fallback `ECONNREFUSED`

Current milestone outcome:
- smoke auth/environment path is deterministic and green under canonical local model.
