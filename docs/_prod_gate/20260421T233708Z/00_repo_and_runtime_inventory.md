# Repo And Runtime Inventory

Timestamp (UTC): 20260421T233708Z

## Structure
| Item | Classification | Evidence |
|---|---|---|
| Django backend | present and working | `backend/manage.py`, `backend/sims_project/settings.py`, `backend/pytest.ini` |
| Next.js frontend | present and working | `frontend/package.json`, `frontend/app`, `frontend/playwright.config.ts` |
| Docker runtime | present and working | `docker/docker-compose.yml`; `docker compose ... ps` showed db, redis, backend, frontend healthy/running |
| Same-origin API proxy | present and working | `frontend/app/api/[...path]/route.ts`; curl `/api/auth/profile/` via frontend returned backend `401` |
| Seed/reset path | present and working | `scripts/e2e_seed.sh` runs migrate, org seed, active baseline seed, E2E seed, cache clear |
| Contracts | present and working as handwritten docs | `docs/contracts/*.md`; no wired OpenAPI generator endpoint found |
| Playwright | present and working | `frontend/playwright.config.ts`, projects: smoke, workflow-gate, active-surface, rbac, navigation, dashboard, negative |
| Coverage tooling | present but required harness setup | frontend Jest coverage works; backend coverage required isolated venv install from `requirements-dev.txt` |

## Active Runtime Scope Inventory
Active mounted scope includes public auth pages, resident dashboard/schedule/logbook, supervisor dashboard/resident progress, and UTRMC admin/read-only pages visible in sidebar or CTA paths.

Deferred mounted routes remain out of active release scope: resident research, thesis, workshops, postings; supervisor research approvals; UTRMC postings direct URL.

