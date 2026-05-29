# PGSIMS Testing and QA Guide

Quality Assurance in PGSIMS is driven by backend unit tests, frontend component tests, and Playwright E2E integration tests.

## Running Tests

### 1. Backend Pytest
Run unit tests with:
```bash
cd backend
SECRET_KEY=test-secret pytest sims -v
```
To run backend test coverage:
```bash
cd backend
pytest sims --cov=sims --cov-report=html
```

### 2. Frontend Checks
Run tests, linter, typecheck, and build:
```bash
cd frontend
npm test -- --watch=false
npm run lint
npx tsc --noEmit
npm run build
```

### 3. E2E Playwright Tests
To execute E2E tests:
1. Seed E2E database:
   ```bash
   cd backend && python3 manage.py seed_e2e
   ```
2. Run Playwright:
   ```bash
   cd frontend
   npm run test:e2e:smoke:local
   ```

## Gates and Thresholds
Before declaring a release ready, the codebase must pass all validation gates:
- **Strict OpenAPI Schema**: 0 errors.
- **E2E Integration Suite**: 100% tests passing.
- **Backend Line Coverage**: >=95%.
- **Frontend Line Coverage**: >=90%.
- **Unauthorized Paths**: All secured routes redirect or deny access appropriately.
