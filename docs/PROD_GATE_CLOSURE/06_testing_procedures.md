# Testing Procedures & Gate Commands

**Last Updated**: 2026-04-23  
**Focus**: How to run all tests, verify fixes, and track progress  
**Time to Read**: 10-15 minutes  

---

## Quick Reference

### All Tests (Full Gate)

```bash
# From project root
make clean
make build
make migrate
make test-backend-coverage
make test-frontend
make schema-gate
make e2e-smoke

# Or manually:
cd backend && SECRET_KEY=test-secret pytest sims -q --cov=sims --cov-report=term
cd frontend && npm test -- --watch=false && npm run lint && npx tsc --noEmit && npm run build
cd backend && python manage.py spectacular_settings --validate
./scripts/e2e_seed.sh && cd frontend && npm run test:e2e:feature-layer:local
```

### Single Component Tests

```bash
# Backend unit tests
cd backend && pytest sims/training/ -v

# Backend with coverage for one app
cd backend && pytest sims/training/ --cov=sims.training --cov-report=html

# Frontend unit tests
cd frontend && npm test -- app/dashboard --watch=false

# E2E tests
cd frontend && npm run test:e2e:feature-layer:local

# Schema validation
cd backend && python manage.py spectacular_settings --validate
```

---

## Phase 1: Dependency Sanity

```bash
# Check Python dependencies
cd backend
python -m pip list | grep -E "django|djangorestframework|drf-spectacular"

# Check Node dependencies
cd frontend
npm list | head -30

# Expected: No errors or "missing peer dependency" messages
```

---

## Phase 2: Database Setup

```bash
# Verify database exists and is healthy
docker compose ps db

# Run migrations
cd backend
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Expected: All migrations applied, no errors
```

---

## Phase 3: System Checks

```bash
cd backend

# Django system check
python manage.py check

# Expected output:
# System check identified no issues (0 silenced).
```

---

## Phase 4: Backend Tests with Coverage

### Full Coverage Report

```bash
cd backend

# Run all tests with full coverage report
SECRET_KEY=test-secret pytest sims \
  --cov=sims \
  --cov-report=html \
  --cov-report=term-missing \
  --cov-report=json \
  -v

# Output files:
# htmlcov/index.html - Interactive coverage report
# .coverage - Coverage data
# coverage.json - Machine-readable format

# View coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

### Coverage by App

```bash
# Coverage for specific app
cd backend && pytest sims/training/ --cov=sims.training --cov-report=term

# Sample output:
# sims/training/permissions.py      45%   (lines 5/11)
# sims/training/views.py            52%   (lines 26/50)
# sims/training/serializers.py      78%   (lines 39/50)
# TOTAL                             58%
```

### Quick Test (No Coverage)

```bash
cd backend

# Fast test run without coverage
pytest sims -q

# Or verbose
pytest sims -v

# Run specific test
pytest sims/training/test_permissions.py::TestLogbookPermissions::test_owner_can_view -v

# Run tests matching pattern
pytest -k "logbook" -v
```

### Test with Specific Markers

```bash
cd backend

# Run only integration tests
pytest -m integration -v

# Run only fast unit tests
pytest -m "not slow" -v

# Run only permission-related tests
pytest -k "permission" -v
```

---

## Phase 5: Frontend Lint

```bash
cd frontend

# Run ESLint
npm run lint

# Fix auto-fixable issues
npm run lint -- --fix

# Expected: 0 errors and warnings
```

---

## Phase 6: Frontend Type Checking

```bash
cd frontend

# Run TypeScript compiler
npx tsc --noEmit

# Expected: 0 errors
```

---

## Phase 7: Frontend Unit Tests with Coverage

```bash
cd frontend

# Full coverage report
npm run test:coverage -- --watch=false

# Output:
# ======= Coverage summary =======
# Statements   : XX.XX%
# Branches     : XX.XX%
# Functions    : XX.XX%
# Lines        : XX.XX%

# View detailed HTML report (if generated)
open coverage/lcov-report/index.html
```

### Coverage for Specific Component

```bash
cd frontend

# Test specific path
npm test -- app/dashboard --watch=false --coverage

# Test specific file
npm test -- app/dashboard/resident.test.tsx --watch=false --coverage
```

---

## Phase 8: Frontend Build

```bash
cd frontend

# Build for production
npm run build

# Expected: 0 errors, build succeeds
# Output: .next/ folder created

# Test production build locally
npm start

# Visit http://localhost:3000 (should work)
```

---

## Phase 9: Schema Gate

```bash
cd backend

# Validate schema generation
python manage.py spectacular_settings --validate

# Generate schema file
python manage.py spectacular_settings \
  --file /tmp/openapi_schema.yaml

# Check file
file /tmp/openapi_schema.yaml
head -20 /tmp/openapi_schema.yaml

# Expected: Valid YAML, 0 errors, <10 warnings
```

---

## Phase 10: Docker Runtime

```bash
# Start all services
docker compose up -d

# Verify all healthy
docker compose ps

# Check logs
docker compose logs -f backend

# Test backend endpoint
curl http://127.0.0.1:8014/api/schema/

# Test frontend
curl http://127.0.0.1:3000/

# Stop services
docker compose down
```

---

## Phase 11: Seed Baseline

```bash
# Seed test data
./scripts/e2e_seed.sh

# Expected output:
# Creating test users...
# Creating test data...
# E2E seed completed.

# Verify data exists
docker compose exec -T backend python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
count = User.objects.count()
print(f'Total users: {count}')
print(f'Sample: {list(User.objects.values_list(\"username\", \"role\")[:5])}')
"
```

---

## Phase 12: Active-Surface E2E

```bash
cd frontend

# Ensure seed completed
../scripts/e2e_seed.sh

# Run feature-layer tests
npm run test:e2e:feature-layer:local

# Expected: 7 passed, 0 failed

# If failures, run with debug
npx playwright test e2e/feature-layer/auth-and-smoke.spec.ts --debug

# View failure details
ls output/playwright/results/ | head -5
cat output/playwright/results/[test-name]/error-context.md
```

---

## Phase 13: Broader Role/CTA/API Suite

```bash
cd frontend

# Run all E2E tests (not just feature-layer)
npm run test:e2e

# Or run specific test suites
npx playwright test e2e/role-based-access.spec.ts
npx playwright test e2e/cta-coverage.spec.ts
npx playwright test e2e/api-integration.spec.ts

# Expected: All passing
```

---

## Phase 14: Restart/Reseed Smoke

```bash
# Test complete restart sequence
docker compose down
docker compose up -d
sleep 10

# Verify healthy
docker compose ps

# Reseed
./scripts/e2e_seed.sh

# Run smoke tests
cd frontend && npx playwright test e2e/feature-layer/regression-smoke.spec.ts

# Expected: All passing
```

---

## Phase 15: Coverage Validation

```bash
# Backend coverage check
cd backend
pytest sims --cov=sims --cov-fail-under=95

# Frontend coverage check
cd frontend
npm run test:coverage -- --watch=false --coverage-threshold="{'global':{'lines':90}}"
```

---

## Troubleshooting Test Failures

### Backend Test Failure

```bash
# Verbose output
cd backend
pytest sims/training/ -v --tb=short

# Verbose with print statements
pytest sims/training/ -v -s

# Run single test with full traceback
pytest sims/training/test_api.py::TestLogbookAPI::test_create -vvv --tb=long

# Debug with pdb
pytest sims/training/ --pdb

# (In pdb, use 'c' to continue, 'l' to list, 'n' to next line)
```

### Frontend Test Failure

```bash
# Verbose Jest output
cd frontend
npm test -- --verbose --watch=false app/dashboard

# Debug mode
npm test -- --debug app/dashboard

# View test file
cat app/dashboard/__tests__/resident.test.tsx

# Run specific test
npm test -- --testNamePattern="renders dashboard title" --watch=false
```

### E2E Test Failure

```bash
cd frontend

# Run with Playwright Inspector
npx playwright test e2e/feature-layer/auth-and-smoke.spec.ts --debug

# Check failure artifacts
ls -la output/playwright/results/

# View screenshot of failure
cat output/playwright/results/[test-name]/failed-1.png

# View trace
npx playwright show-trace output/playwright/results/[test-name]/trace.zip
```

### Docker Issue

```bash
# Check service status
docker compose ps

# View logs
docker compose logs backend  # Last 50 lines
docker compose logs -f backend  # Follow logs (Ctrl+C to exit)

# Restart specific service
docker compose restart backend

# Rebuild and restart
docker compose up -d --build backend

# Full rebuild
docker compose build --no-cache backend
docker compose up -d backend
```

---

## Performance Optimization

### Speed Up Backend Tests

```bash
# Use SQLite for tests (faster than Postgres)
cd backend
TEST_DATABASE_ENGINE=sqlite3 pytest sims -q

# Disable migrations if possible
pytest sims --nomigrations

# Parallel test execution
pytest sims -n auto  # Requires pytest-xdist
```

### Speed Up Frontend Tests

```bash
cd frontend

# Run only changed files
npm test -- --changedSince=HEAD

# Disable watch
npm test -- --watch=false

# Parallel execution
npm test -- --maxWorkers=4
```

### Speed Up E2E Tests

```bash
cd frontend

# Run tests in parallel
npx playwright test --workers=4

# Skip slow tests
npx playwright test -g "@slow" --invert
```

---

## Continuous Tracking

### Create a Test Dashboard

```bash
# Script to track test status over time

cd /home/munaim/srv/apps/pgsims

cat > /tmp/gate_check.sh << 'SCRIPT'
#!/bin/bash
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
echo "=== Gate Status: $TIMESTAMP ===" >> /tmp/gate_history.log

echo "Backend tests:" >> /tmp/gate_history.log
cd backend && SECRET_KEY=test-secret pytest sims -q 2>&1 | tail -3 >> /tmp/gate_history.log

echo "Backend coverage:" >> /tmp/gate_history.log
cd backend && pytest sims --cov=sims --co-report=term 2>&1 | tail -2 >> /tmp/gate_history.log

echo "Frontend tests:" >> /tmp/gate_history.log
cd frontend && npm test -- --watch=false 2>&1 | tail -3 >> /tmp/gate_history.log

echo "E2E tests:" >> /tmp/gate_history.log
cd frontend && npm run test:e2e:feature-layer:local 2>&1 | tail -3 >> /tmp/gate_history.log

echo "" >> /tmp/gate_history.log
SCRIPT

chmod +x /tmp/gate_check.sh

# Run periodically
# Add to crontab: */30 * * * * /tmp/gate_check.sh

# View history
tail -20 /tmp/gate_history.log
```

---

## Reference: Test Files Location

| Layer | Pattern | Location |
|-------|---------|----------|
| Backend Unit | `test_*.py` | `sims/*/test_*.py` |
| Backend Integration | `tests.py` | `sims/*/tests.py` |
| Frontend Unit | `*.test.tsx` / `*.test.ts` | `app/**/__tests__/*` |
| E2E Feature Layer | `*.spec.ts` | `e2e/feature-layer/*.spec.ts` |
| E2E Regression | `regression-*.spec.ts` | `e2e/feature-layer/regression-*.spec.ts` |

---

## Next Steps

1. **Run Phase 1-4 (dependency/DB setup)**
2. **Run Phase 5-8 (code quality)**
3. **Run Phase 9-12 (runtime & E2E)**
4. **Track failures** using troubleshooting section
5. **Fix issues** and re-run relevant phase
6. **Validate with Phase 15** (coverage checks)

