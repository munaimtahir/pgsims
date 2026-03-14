# Workflow E2E Run Log

## 1) Seed deterministic workflow data

```bash
cd /home/munaim/srv/apps/pgsims
docker compose -f docker/docker-compose.yml --env-file .env exec -T backend python manage.py seed_e2e
```

Observed:
- `seed_e2e completed successfully.`
- DB verification:
  - active `ResidentTrainingRecord` for `e2e_pg`
  - research status `SUBMITTED_TO_SUPERVISOR` with title `E2E Baseline Research Project`
  - program `E2E-FCPS`
  - milestones `IMM` and `FINAL`

## 2) Smoke gate verification

```bash
cd frontend
npm run test:e2e:smoke:local -- --reporter=line
```

Observed:
- `17 passed`

## 3) Workflow gate verification

```bash
cd /home/munaim/srv/apps/pgsims
docker compose -f docker/docker-compose.yml --env-file .env exec -T backend python manage.py seed_e2e
cd frontend
npm run test:e2e:workflow:local -- --reporter=line
```

Observed:
- `3 passed`

## 4) Environment notes encountered during execution

- First workflow run failed while services were still on stale container images.
- After rebuilding backend/frontend from the current workspace and reseeding, both gates passed.
