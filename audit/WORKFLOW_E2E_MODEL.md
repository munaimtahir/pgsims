# Workflow E2E Model

Date: 2026-03-14

## Canonical Workflow Gate

Project:
- Playwright project: `workflow-gate`

Spec set:
- `frontend/e2e/workflow-gate/stabilized-workflows.spec.ts`

Promoted browser tests:
1. Forgot-password request submits through the real public UI and renders the success response.
2. Supervisor approvals page renders canonical `resident_name` and supports the `supervisor-return` action path.
3. Resident dashboard renders canonical eligibility reason strings from seeded data.

## Seeded Roles and Preconditions

Seed command:

```bash
docker compose -f docker/docker-compose.yml --env-file .env exec -T backend python manage.py seed_e2e
```

Seeded users used by the workflow gate:
- `e2e_pg / Pg123456!`
- `e2e_supervisor / Supervisor123!`

Deterministic state created by `seed_e2e`:
- single canonical hospital mode remains active
- deterministic `E2E-FCPS` training program exists
- active `ResidentTrainingRecord` exists for `e2e_pg`
- seeded research project exists for `e2e_pg`
- seeded research project starts in `SUBMITTED_TO_SUPERVISOR`
- eligibility recomputation runs, leaving deterministic unmet reasons:
  - `Synopsis not yet approved by supervisor`
  - `Thesis not yet submitted`

## Gate Commands

Smoke gate:

```bash
docker compose -f docker/docker-compose.yml --env-file .env exec -T backend python manage.py seed_e2e
cd frontend && npm run test:e2e:smoke:local
```

Workflow gate:

```bash
docker compose -f docker/docker-compose.yml --env-file .env exec -T backend python manage.py seed_e2e
cd frontend && npm run test:e2e:workflow:local
```

## Smoke vs Workflow

- Smoke gate responsibility: availability, login, route protection, dashboard entry reachability.
- Workflow gate responsibility: contract-critical browser verification for seeded forgot-password, supervisor approvals/return, and resident eligibility display.
- Excluded on purpose: broad regression suites, mutation-heavy org-management flows, screenshot tours, and speculative reviewed-history assertions not backed by the current approvals contract.
