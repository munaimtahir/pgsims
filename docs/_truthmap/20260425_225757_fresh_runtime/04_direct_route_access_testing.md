# Stage 4: Direct Route Access Testing

Source evidence: `../_truthmap_docker_fix/20260425_223918/json/stage4_route_smoke.json`

## Result Matrix

| Role | Route | HTTP | Heading | Verdict |
|---|---|---:|---|---|
| Resident | `/dashboard/resident` | 200 | `My Training Dashboard` | PASS |
| Resident | `/dashboard/resident/progress` | 200 | `Logbook` | PASS |
| Resident | `/dashboard/resident/schedule` | 200 | `My Schedule` | PASS |
| Supervisor | `/dashboard/supervisor` | 200 | `Supervisor Dashboard` | PASS |
| UTRMC Admin | `/dashboard/utrmc` | 200 | `UTRMC Overview` | PASS with failing data-quality XHR |
| UTRMC Admin | `/dashboard/utrmc/users` | 200 | `Users` | PASS |
| UTRMC Admin | `/dashboard/utrmc/programs` | 200 | `Programs` | PASS |
| UTRMC Admin | `/dashboard/utrmc/supervision` | 200 | `Supervision Links` | PASS |
| UTRMC Admin | `/dashboard/utrmc/data-quality` | 200 | `Data Quality Dashboard` | PAGE LOADS, DATA FAILS |

## Route Verdict

### False positives from stale runtime

These were previously treated as runtime `404`s but are now confirmed to load:

- resident dashboard
- resident logbook
- resident schedule
- supervisor dashboard
- UTRMC overview shell
- UTRMC users
- UTRMC programs
- UTRMC supervision

### Real remaining route/config issue

- Data Quality route shell loads, but its API requests fail through the frontend proxy.

## Console / network notes

- Clean pages showed no console/network failures in this smoke run.
- Data Quality-related routes produced browser-visible `404` responses for:
  - `/api/admin/data-quality/summary`
  - `/api/admin/data-quality/users`
  - `/api/admin/data-quality/audit`
