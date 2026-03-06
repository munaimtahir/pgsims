# PGSIMS Playwright Suite — Architecture

## Overview

The E2E suite lives in `frontend/e2e/` and tests the live Next.js + Django application via Playwright Chromium. It targets `https://pgsims.alshifalab.pk` by default (configurable via `E2E_BASE_URL`).

## Suite Structure

```
frontend/e2e/
├── auth.setup.ts               # Saves admin storageState for critical suite
├── helpers/
│   ├── auth.ts                 # loginAs(context, page, role) — JWT cookie setter
│   └── navigation.ts           # ROLE_HOME, ROLE_FORBIDDEN, gotoHome()
├── smoke/                      # Fast sanity (no data dependency)
│   ├── public.spec.ts          # 5 tests — public pages
│   ├── auth_flow.spec.ts       # 5 tests — login form
│   └── dashboards.spec.ts      # 7 tests — role dashboards
├── auth/                       # Auth/session lifecycle
│   └── session.spec.ts         # 11 tests — login, logout, guard
├── rbac/                       # Role-based access control
│   └── access-control.spec.ts  # 17 tests — cross-role routing
├── navigation/                 # Sidebar navigation
│   └── sidebar.spec.ts         # 16 tests — nav items per role
├── dashboard/                  # Dashboard page renders
│   └── pages.spec.ts           # 20 tests — all dashboard pages
├── workflows/                  # Core user workflows
│   ├── utrmc-management.spec.ts # CRUD: hospital, dept, user, supervision
│   ├── supervisor-review.spec.ts # Supervisor research approvals
│   └── resident-training.spec.ts # Resident schedule, research, thesis, workshops
├── negative/                   # Validation and error handling
│   └── validation.spec.ts      # 12 tests — form validation, API auth
├── critical/                   # Complex multi-step flows
│   ├── userbase_foundation.spec.ts
│   └── phase6_research_eligibility.spec.ts
└── regression/                 # Graduated from backlog
    └── README.md
```

## Playwright Projects

| Project | Pattern | Depends On | Purpose |
|---------|---------|-----------|---------|
| `setup` | `auth.setup.ts` | — | Saves admin storageState |
| `smoke` | `smoke/*.spec.ts` | — | Fast public + auth sanity |
| `auth` | `auth/*.spec.ts` | — | Session lifecycle |
| `rbac` | `rbac/*.spec.ts` | — | Cross-role access control |
| `navigation` | `navigation/*.spec.ts` | — | Sidebar nav per role |
| `dashboard` | `dashboard/*.spec.ts` | — | Dashboard page renders |
| `workflows` | `workflows/*.spec.ts` | — | Core user workflows |
| `negative` | `negative/*.spec.ts` | — | Form validation / API auth |
| `critical` | `critical/*.spec.ts` | `setup` | Complex multi-step flows |

## Auth Strategy

All tests use `loginAs(context, page, role)` which:
1. POSTs to `/api/auth/login/` directly (bypasses UI)
2. Sets `pgsims_access_token`, `pgsims_user_role`, `pgsims_access_exp` cookies
3. Writes full auth state to localStorage via `page.addInitScript()`

This makes auth deterministic and fast — no UI click-through needed.

## Test Data

Seed users are created by `python manage.py seed_e2e` in the backend:

| Role | Username | Password | Purpose |
|------|----------|----------|---------|
| admin | e2e_admin | Admin123! | Admin/UTRMC flows |
| utrmc_admin | e2e_utrmc_admin | UtrmcAdmin123! | UTRMC management |
| utrmc_user | e2e_utrmc_user | Utrmc123! | Read-only UTRMC |
| supervisor | e2e_supervisor | Supervisor123! | Supervisor workflows |
| pg | e2e_pg | Pg123456! | Resident/PG workflows |

Additional demo data from `python manage.py seed_demo_data` provides rich
urology scenario data for analytics/dashboard tests.

## Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `E2E_BASE_URL` | `https://pgsims.alshifalab.pk` | Frontend base URL |
| `E2E_API_URL` | _(falls back to E2E_BASE_URL)_ | Backend API base URL |
