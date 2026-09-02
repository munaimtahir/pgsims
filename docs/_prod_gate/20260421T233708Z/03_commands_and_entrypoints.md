# Commands And Entrypoints

## Dry Run
```bash
cd backend && python3 -m pip check
cd backend && SECRET_KEY=test-secret python3 manage.py makemigrations --check --dry-run
cd backend && SECRET_KEY=test-secret python3 manage.py check
cd backend && SECRET_KEY=test-secret python3 -m pytest sims -q
cd backend && SECRET_KEY=test-secret ../OUT/prod_gate_artifacts/20260421T233708Z/backend-venv/bin/python -m pytest sims -q --cov=sims --cov-branch --cov-report=json:../OUT/prod_gate_artifacts/20260421T233708Z/coverage/backend_coverage.json --cov-report=term-missing:skip-covered
cd frontend && npm ci --dry-run
cd frontend && npm run lint
cd frontend && npm run typecheck
cd frontend && npm test -- --watch=false
cd frontend && npm test -- --watch=false --coverage --coverageReporters=json-summary --coverageReporters=text --coverageDirectory=../OUT/prod_gate_artifacts/20260421T233708Z/coverage/frontend
cd frontend && npm run build
```

## Runtime
```bash
docker compose -f docker/docker-compose.yml --env-file .env up -d db redis backend frontend
curl -si http://127.0.0.1:8014/health/
curl -si http://127.0.0.1:8014/healthz/
curl -si http://127.0.0.1:8082/login
curl -si http://127.0.0.1:8082/api/auth/profile/
cd frontend && npm run test:e2e:active-surface:local
cd frontend && npm run test:e2e:feature-layer:seed && E2E_BASE_URL=http://127.0.0.1:8082 E2E_API_URL=http://127.0.0.1:8014 npx playwright test --project=smoke --project=workflow-gate --project=rbac --project=negative --project=navigation --project=dashboard
```

## Restart / Reseed
```bash
docker compose -f docker/docker-compose.yml --env-file .env restart backend frontend
cd frontend && npm run test:e2e:active-surface:local
```

