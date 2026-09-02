# Route Smoke Test From Fresh Runtime

- Source evidence: `json/stage4_route_smoke.json`
- Screenshots: `screenshots/`

## Summary

The broad frontend `404` claims from the previous audit do not reproduce after a verified clean frontend rebuild.

### Routes that loaded successfully

| Role | Route | Status | Heading |
|---|---|---:|---|
| Resident | `/dashboard/resident` | 200 | `My Training Dashboard` |
| Resident | `/dashboard/resident/progress` | 200 | `Logbook` |
| Resident | `/dashboard/resident/schedule` | 200 | `My Schedule` |
| Supervisor | `/dashboard/supervisor` | 200 | `Supervisor Dashboard` |
| UTRMC Admin | `/dashboard/utrmc` | 200 | `UTRMC Overview` |
| UTRMC Admin | `/dashboard/utrmc/users` | 200 | `Users` |
| UTRMC Admin | `/dashboard/utrmc/programs` | 200 | `Programs` |
| UTRMC Admin | `/dashboard/utrmc/supervision` | 200 | `Supervision Links` |
| UTRMC Admin | `/dashboard/utrmc/data-quality` | 200 | `Data Quality Dashboard` |

## Console / Network Findings

### Clean routes

These routes loaded without console errors or failed network requests in the smoke run:

- `/dashboard/resident`
- `/dashboard/resident/progress`
- `/dashboard/resident/schedule`
- `/dashboard/supervisor`
- `/dashboard/utrmc/users`
- `/dashboard/utrmc/programs`
- `/dashboard/utrmc/supervision`

### Real failing integration

`/dashboard/utrmc` and `/dashboard/utrmc/data-quality` loaded the page shell, but the browser captured `404` XHR failures for data-quality APIs:

- `/api/admin/data-quality/summary`
- `/api/admin/data-quality/users`
- `/api/admin/data-quality/audit`

Observed browser behavior:

- `UTRMC Overview` page logs a `404` against data-quality summary
- `Data Quality Dashboard` page shows a user-facing load failure

## Classification

### Discarded as stale-build contamination

- Previous claims that resident, supervisor, programs, supervision, users, and the main UTRMC pages were runtime `404`s

### Confirmed as real route/config issue

- Data Quality frontend integration failure

Root cause from fresh runtime evidence:

- frontend proxy route `frontend/app/api/[...path]/route.ts` always appends a trailing slash
- backend `data-quality` endpoints work without trailing slash
- backend returns `404` for slash-appended versions

So the page shell exists and loads, but the frontend-to-backend proxy path is mismatched for this module.
