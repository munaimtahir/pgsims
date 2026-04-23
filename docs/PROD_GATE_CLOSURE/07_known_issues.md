# Known Issues & Solutions

**Last Updated**: 2026-04-23  
**Focus**: Problems found during investigation + solutions  
**Time to Read**: 10-15 minutes  

---

## Critical Issues (Found in Session 3)

### Issue 1: E2E Dashboard Rendering Failures

**Symptom**:
- E2E tests pass login
- Dashboard page loads but shows "Failed to load dashboard. Please refresh."
- Error boundary displayed
- 4 out of 7 E2E tests fail

**Status**: Unresolved (root cause unknown)

**Investigation Done**:
- ✓ Verified backend APIs work (curl successful)
- ✓ Verified test data exists (users, programs, etc.)
- ✓ Verified auth token injection works
- ✓ Verified services are healthy
- ✓ Added 5 root cause hypotheses (token timing, ALLOWED_HOSTS, etc.)
- ✗ Root cause still unknown after 1.5 hours investigation

**Likely Root Causes** (ranked by probability):
1. Token not injected in time (40%) - API calls before localStorage ready
2. API returns 401/403 (20%) - Auth header missing or malformed
3. ALLOWED_HOSTS rejects request (15%) - Host header mismatch
4. Session state cleared (15%) - Playwright context doesn't persist auth
5. Race condition (10%) - Component mounts/unmounts before API response

**Recommended Fix**:
- Use Playwright Inspector to examine network traces
- See `04_e2e_debugging.md` for detailed diagnosis procedure
- If unresolvable quickly, refactor E2E to use browser UI login instead of token injection

**Related Files**:
- `frontend/e2e/feature-layer/helpers/session.ts` - Auth setup
- `frontend/app/dashboard/resident/page.tsx` - Dashboard page
- `frontend/e2e/feature-layer/auth-and-smoke.spec.ts` - Failing test

---

### Issue 2: Schema Gate 315 Errors

**Symptom**:
```
drf-spectacular warning: Unable to guess serializer for <function>
```
Hundreds of times.

**Status**: Partially fixed (18 eliminated, 315 remain)

**Root Cause**:
- 65 APIViews don't have `@extend_schema()` decorators
- drf-spectacular can't infer serializers
- Each missing serializer = multiple errors

**Session 3 Fix**:
- ✓ Removed duplicate Department imports (eliminated 18 warnings)
- Still need: Add @extend_schema() decorators to all 65 APIViews

**Next Fix**:
- See `03_schema_gate_fix.md` for step-by-step guide
- Estimated time: 3-5 hours

---

### Issue 3: Docker Stale Code

**Symptom**:
- Tests pass locally
- Same tests fail in Docker container
- Code changes don't take effect

**Root Cause**:
- Docker image has cached Python bytecode (.pyc files)
- Container restart doesn't clear bytecode
- Must rebuild image from scratch

**Solution Applied**:
```bash
docker compose down backend
docker image rm docker-backend
docker compose build --no-cache backend
docker compose up -d backend
```

**Prevention**:
- Use `--no-cache` when code changes in container context
- Or add cleanup to Dockerfile: `find /app -name "*.pyc" -delete`

**Related Issue**: Docker volume mounting can also cause issues if .git is mounted

---

### Issue 4: Backend Coverage Only 54%

**Symptom**:
```
Backend coverage: 54.38% line / 28.69% branch
```

**Root Cause**:
- Many permission checks untested
- State machine workflows untested
- Admin-only code paths untested
- Role-based variants not tested

**Why It's Low**:
```python
# Example: This is 50% branch coverage

if user.role == 'pg':      # Tested (PG path)
    return Response(pg_data)
else:                      # NOT tested (Supervisor/admin)
    return Response(admin_data)
```

**Fix Strategy**:
- Add permission tests (allow + deny pairs)
- Add state machine tests (full workflows)
- Add role-variant tests (each role + each variant)
- See `05_coverage_strategy.md` for details

**Time to 95%**: 8-15 hours

---

### Issue 5: Frontend Coverage Only 8%

**Symptom**:
```
Frontend coverage: 8.71% line / 7.56% branch
```

**Root Cause**:
- Most components/pages not covered
- No tests for dashboard, logbook, supervisor pages
- Conditional rendering paths not tested
- Error states not tested

**Why It's So Low**:
- Frontend test infrastructure minimal
- Tests exist for ~5 pages out of 20+
- Many components have no tests at all

**Fix Strategy**:
- Test all active pages (dashboard, logbook, etc.)
- Test loading/error/success states
- Test role-based visibility
- See `05_coverage_strategy.md` for details

**Time to 90%**: 15-20 hours

---

## Known Workarounds

### Workaround 1: Token Injection Timing

**If**: Token is null in E2E test logging

**Workaround**:
```typescript
// Add explicit delay before API calls
await new Promise(resolve => setTimeout(resolve, 500));

// Or wait for token explicitly
await page.evaluate(() => {
  return new Promise((resolve) => {
    const check = setInterval(() => {
      if (localStorage.getItem('access_token')) {
        clearInterval(check);
        resolve(true);
      }
    }, 50);
  });
});
```

**Proper Fix**: Investigate why token isn't injected in time

---

### Workaround 2: ALLOWED_HOSTS Rejection

**If**: Backend logs show `Invalid HTTP_HOST header`

**Workaround**:
```python
# backend/sims_project/settings.py
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'testserver',  # Add this
    'api.pgsims.alshifalab.pk',
]
```

**Proper Fix**: Use correct host header or configure CSRF properly

---

### Workaround 3: Stale Test Data

**If**: Tests fail saying data doesn't exist

**Workaround**:
```bash
# Reseed test data
docker compose down
docker compose up -d
./scripts/e2e_seed.sh
```

**Proper Fix**: Seed is deterministic, shouldn't need repeating

---

## Environment-Specific Issues

### Local Development

| Issue | Symptom | Fix |
|-------|---------|-----|
| `ModuleNotFoundError` | Import error in backend | `cd backend && pip install -r requirements.txt` |
| Port in use | `Address already in use :8014` | `lsof -i :8014` then `kill <PID>` |
| DB connection error | Can't connect to database | Verify Docker postgres is running and healthy |
| Node modules missing | `Cannot find module '@tanstack/react-query'` | `cd frontend && npm install` |

### Docker

| Issue | Symptom | Fix |
|-------|---------|-----|
| Container won't start | Service shows "restarting" | Check `docker compose logs <service>` |
| Health check fails | Status shows "unhealthy" | Restart service, check logs |
| Network issues | Can't reach API from frontend | Verify `127.0.0.1` vs `backend` hostname |

### Database

| Issue | Symptom | Fix |
|-------|---------|-----|
| Migration fails | `ProgrammingError: column does not exist` | Check pending migrations: `python manage.py showmigrations` |
| Foreign key error | `IntegrityError: foreign key constraint` | Ensure referenced object exists |
| Test data missing | User/program doesn't exist | Run `./scripts/e2e_seed.sh` |

---

## Common Test Failures & Fixes

### Backend Test Failure: "AssertionError: 200 != 403"

**Symptom**: Permission test expects 200 but got 403

**Likely Cause**: User doesn't have permission or is not authenticated

**Fix**:
```python
# Ensure user is authenticated
self.client.force_authenticate(user=test_user)

# Ensure user has correct role
assert test_user.role == 'pg'

# Ensure user has correct scoping (e.g., supervisor relationship)
SupervisorAssignment.objects.create(supervisor=sup, pg=pg)
```

---

### Frontend Test Failure: "Timeout waiting for selector"

**Symptom**: Element never appears on page

**Likely Cause**: 
- API didn't return data
- Component didn't render
- Selector is wrong

**Fix**:
```typescript
// Verify API is mocked
expect(mockAPI).toHaveBeenCalled();

// Verify mock returned data
mockAPI.mockResolvedValue({ data: [...] });

// Check selector
screen.debug(); // Print entire DOM to see what's there
```

---

### E2E Test Failure: "Navigation timeout"

**Symptom**: Test times out waiting for page load

**Likely Cause**:
- Backend not responding
- Frontend has infinite loop
- Selector for "done loading" is wrong

**Fix**:
```typescript
// Use Playwright Inspector
npx playwright test --debug

// Add logging
console.log('Starting navigation...');
await page.goto(url);
console.log('Navigation complete');

// Wait for specific element
await page.waitForSelector('h1', { timeout: 5000 });
```

---

## Performance Issues

### Slow Backend Tests

**Symptom**: Test suite takes >5 minutes

**Likely Cause**: 
- Running migrations for each test
- Database heavy operations
- No test database optimization

**Fix**:
```bash
# Use in-memory database
cd backend && TEST_DATABASE_ENGINE=sqlite3 pytest sims -q

# Or use transactions to avoid migrations
pytest --nomigrations -q

# Or speed up with multiple workers
pytest -n auto -q
```

---

### Slow Frontend Tests

**Symptom**: Test suite takes >3 minutes

**Likely Cause**:
- Slow mocks/setup
- No parallelization
- Heavy component tree

**Fix**:
```bash
cd frontend

# Run in parallel
npm test -- --maxWorkers=4

# Or skip slow tests
npm test -- -g "@slow" --invert

# Or test specific file
npm test -- --testPathPattern="dashboard" --watch=false
```

---

### Slow E2E Tests

**Symptom**: Each E2E test takes >30 seconds

**Likely Cause**:
- Backend/frontend startup delays
- Long seed times
- Inefficient wait conditions

**Fix**:
```bash
# Run in parallel
npx playwright test --workers=4

# Keep services running between runs (don't restart)
docker compose up -d  # Once at start
# ... run tests ...
# Keep running until done

# Run with reduced timeout
npx playwright test --timeout=10000
```

---

## Debugging Tips

### For Backend Issues

```bash
# Add print statements to test
def test_something(self):
    print("\n\n=== TEST START ===")
    print(f"User: {self.user}")
    print(f"Role: {self.user.role}")
    result = some_function()
    print(f"Result: {result}")
    print("=== TEST END ===\n\n")

# Run with output
pytest sims/training/ -v -s  # -s = show print statements
```

### For Frontend Issues

```typescript
// Add debug logging
console.log('About to call API');
const response = await api.getResidentSummary();
console.log('API Response:', response);
console.log('Rendering with:', renderData);

// Run with verbose
npm test -- --verbose --watch=false

// Or use debugger
debugger; // Sets breakpoint when dev tools open
```

### For E2E Issues

```typescript
// Add screenshots
await page.screenshot({ path: '/tmp/debug.png' });

// Add logging
console.log('Page URL:', page.url());
console.log('Page title:', await page.title());

// Pause on failure
await page.pause(); // Freezes test, use Playwright Inspector to step through
```

---

## Reference: Error Messages Map

| Error | Likely Cause | See Section |
|-------|-------------|-------------|
| "Failed to load dashboard" | E2E token/auth issue | Issue 1 |
| "Unable to guess serializer" | Missing @extend_schema() | Issue 2 |
| "Cannot resolve dependency" | Stale Docker image | Issue 3 |
| "Permission Denied (403)" | User not authenticated/authorized | Backend Test Failure |
| "Element not found" | Mock didn't return data | Frontend Test Failure |
| "HTTP 500 on /api/" | Backend exception | Check backend logs |
| "CORS error" | Origin not allowed | ALLOWED_HOSTS |
| "Database connection refused" | DB not running | Docker section |

