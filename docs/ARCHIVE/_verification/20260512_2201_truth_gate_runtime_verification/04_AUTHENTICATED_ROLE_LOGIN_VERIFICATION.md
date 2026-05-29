# Authenticated Role Login Verification

## API-level login

Command used:

```bash
python3 - <<'PY'
...
PY
```

| Role | Login | `/api/auth/me/` | Redirect | Dashboard | Logout | Status | Notes |
|---|---|---|---|---|---|---|---|
| admin | PASS | PASS | PASS | `/dashboard/utrmc` | PASS | PASS | canonical admin landing is UTRMC surface |
| utrmc_admin | PASS | PASS | PASS | `/dashboard/utrmc` | PASS | PASS |  |
| utrmc_user | PASS | PASS | PASS | `/dashboard/utrmc` | PASS | PASS | read-only behavior verified elsewhere |
| supervisor | PASS | PASS | PASS | `/dashboard/supervisor` | PASS | PASS |  |
| pg | PASS | PASS | PASS | `/dashboard/resident` | PASS | PASS |  |

## Browser login

`npm run test:e2e:smoke:local` passed 17/17, including the valid credential redirect checks for all three primary roles.

## Notes

- The app uses `/dashboard/utrmc` as the admin/UTRMC landing page, not `/dashboard/admin`.
- `admin` auth is present and works, but the current UI baseline is the UTRMC dashboard.
