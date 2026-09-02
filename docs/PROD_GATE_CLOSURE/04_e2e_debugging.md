# E2E Debugging & Dashboard Rendering Fix

**Last Updated**: 2026-04-23  
**Focus**: Blocker #2 - E2E Dashboard Rendering Failures  
**Scope**: Diagnostic procedures and fix strategies  
**Time to Read**: 20-30 minutes  

---

## Quick Summary

3 E2E tests fail with message "Failed to load dashboard. Please refresh."

- **Root cause**: Unknown (requires investigation)
- **Difficulty**: Medium (diagnosis is hard, fix depends on cause)
- **Time to fix**: 1-4 hours (diagnosis: 15-30 min, fix: 1-6 hours)
- **Blocking**: 6 other blockers depend on this being fixed

---

## The Failure Pattern

### What Happens
```
1. E2E test starts
2. Test logs in as a user (authentication works)
3. Test navigates to dashboard
4. Page loads, but shows error:
   "Failed to load dashboard. Please refresh."
5. Test times out waiting for expected element
```

### Failing Tests
```
✗ e2e/feature-layer/auth-and-smoke.spec.ts:18 - 
  core feature roles can login and reach their dashboard surfaces

✗ e2e/feature-layer/auth-and-smoke.spec.ts:27 - 
  key feature-layer routes render without fatal console crashes

✗ e2e/feature-layer/logbook.spec.ts:9 - 
  resident draft -> submit -> supervisor return -> resident resubmit -> supervisor approve

✗ e2e/feature-layer/regression-smoke.spec.ts:6 - 
  resident core pages still load

✗ e2e/feature-layer/regression-smoke.spec.ts:25 - 
  supervisor and HOD entry routes still load
```

### Passing Tests (for reference)
- ✓ Permission boundaries - resident is blocked
- ✓ Permission boundaries - unauthenticated direct access
- ✓ Permission boundaries - supervisor scope limited
- ✓ Permission boundaries - read-only access

**Observation**: Permission tests that don't render dashboard pass. Only tests that try to render dashboard fail.

---

## Diagnostic Phase (15-30 minutes)

### Step 1: Check Service Health

```bash
# Verify all services are running
docker compose ps
# Should show: all services with "healthy" or "up" status

# Sample output:
# pgsims_backend    docker-backend    up 5 minutes (healthy)
# pgsims_frontend   docker-frontend   up 5 minutes (healthy)
# pgsims_db         postgres:15       up 6 hours (healthy)
# pgsims_redis      redis:7           up 6 hours (healthy)
```

If any service is not healthy, restart it:
```bash
docker compose up -d [service_name]
```

### Step 2: Verify Test Data

```bash
# Seed test data
./scripts/e2e_seed.sh

# Should complete with:
# "E2E seed completed."

# Verify test user exists
docker compose exec -T backend python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
resident = User.objects.filter(role='pg').first()
print(f'Test user: {resident.username if resident else \"NONE\"} (role={resident.role if resident else \"N/A\"})')
"
```

### Step 3: Test Backend API Directly

```bash
# Test if backend API works
curl -s http://127.0.0.1:8014/api/residents/me/summary/ \
  -H "Authorization: Bearer test-token" | head -20

# Should return JSON (even if 401 auth error, at least shows endpoint works)
# Not expected to succeed with fake token, but should reach endpoint

# Test without auth to verify endpoint exists
curl -s http://127.0.0.1:8014/api/residents/me/summary/ | head -20
# May return 401, but shows endpoint is reachable
```

### Step 4: Run E2E Tests with Detailed Output

```bash
cd frontend

# Run single test with verbose output
npx playwright test e2e/feature-layer/auth-and-smoke.spec.ts:18 --debug

# This will:
# 1. Open Playwright Inspector
# 2. Allow stepping through test
# 3. Show network requests
# 4. Show browser console
# 5. Pause at breakpoints

# Alternative: Run with full output
npx playwright test e2e/feature-layer/auth-and-smoke.spec.ts:18 -v 2>&1 | tee /tmp/e2e_debug.txt
```

### Step 5: Check Test Output Files

```bash
# Find most recent test result
ls -lt frontend/output/playwright/results/ | head -5

# Examine error context
find frontend/output/playwright/results -name "error-context.md" -mmin -5 -exec cat {} \;

# Look for page snapshot showing what happened when test failed
# Should show "Failed to load dashboard. Please refresh." in the page
```

---

## Hypothesis Testing (20-60 minutes)

### Hypothesis A: Token Not Injected (40% probability)

**Test This**:
```typescript
// In e2e/feature-layer/helpers/session.ts, add logging:
await page.goto(APP_BASE_URL, { waitUntil: 'domcontentloaded' });

// Add logging
console.log('About to check token...');
const token = await page.evaluate(() => localStorage.getItem('access_token'));
console.log('Token from localStorage:', token);

// If token is null, then injection failed!
```

**If True** (token is null):
- Token injection via `addInitScript()` is not working
- Solution: Add explicit wait for token, or increase delay
- Fix time: 30-60 minutes

**If False** (token exists):
- Token is being injected correctly
- Problem is elsewhere

### Hypothesis B: API Returns Unexpected Format (20% probability)

**Test This**:
```typescript
// Add logging to API call
const res = await page.request.get('/api/residents/me/summary/', {
  headers: { 'Authorization': `Bearer ${token}` }
});
console.log('API response status:', res.status());
const body = await res.text();
console.log('API response body:', body.substring(0, 500));
```

**If API returns error**:
- Status code 4xx or 5xx indicates API issue
- Check backend logs
- Fix time: 30-90 minutes

**If API returns success**:
- Problem is in frontend parsing/rendering
- Continue to next hypothesis

### Hypothesis C: ALLOWED_HOSTS Rejects Request (15% probability)

**Test This**:
```bash
# Check backend logs for host header errors
docker compose logs backend 2>&1 | grep -i "disallowed\|host" | tail -20

# If you see "Invalid HTTP_HOST header: testserver"
# Then this is the problem
```

**If Found** (DisallowedHost error):
- Backend is rejecting request due to HTTP_HOST header
- Solution: Add 'testserver' or test domain to ALLOWED_HOSTS
- Fix time: 5-10 minutes

**If Not Found**:
- Not this issue

### Hypothesis D: Session State Cleared (15% probability)

**Test This**:
```typescript
// After login, verify session persists across navigation
const token1 = await page.evaluate(() => localStorage.getItem('access_token'));
await page.goto('/dashboard/resident/');
const token2 = await page.evaluate(() => localStorage.getItem('access_token'));
if (token1 === token2) {
  console.log('Token persisted ✓');
} else {
  console.log('Token was cleared ✗');
}
```

**If Token is Cleared**:
- Session not persisting between navigations
- Playwright context might be isolated
- Solution: Refactor auth to use browser UI login instead of token injection
- Fix time: 2-4 hours

**If Token Persists**:
- Not this issue

### Hypothesis E: Race Condition (10% probability)

**Test This**:
```typescript
// Add explicit waits before and after API calls
await new Promise(r => setTimeout(r, 500)); // Extended delay
await page.goto('/dashboard/resident/');
// Wait for specific elements
await page.waitForSelector('h1:has-text("My Training Dashboard")', { timeout: 10000 });
```

**If Longer Delays Help**:
- There's a race condition or timing issue
- Solution: Add more robust wait conditions
- Fix time: 1-2 hours

**If Delays Don't Help**:
- Not this issue

---

## Deep Debugging (Playwright Inspector Method)

### Step 1: Install/Update Playwright Inspector

```bash
cd frontend
npx playwright install
```

### Step 2: Run Test with Inspector

```bash
# Run single failing test
npx playwright test e2e/feature-layer/auth-and-smoke.spec.ts:18 --debug

# This opens Playwright Inspector with:
# - Debugger on the left
# - Browser on the right
# - Allows step-through execution
```

### Step 3: Key Things to Check in Inspector

While test is paused:

1. **Check Network Requests**:
   - Look for `/api/residents/me/summary/` requests
   - Check response status (200 is good, 401/403/500 is bad)
   - Check request headers (is Authorization header present?)

2. **Check Console Errors**:
   - Look for JavaScript errors
   - Check for network/CORS errors
   - Look for your custom logging messages

3. **Check Browser Storage**:
   - Inspect localStorage for `access_token`
   - Should be present after login
   - Token should look like `eyJ0...` (JWT format)

4. **Check Page DOM**:
   - Look for error message in HTML
   - Check if error boundary rendered
   - Look for actual error details

### Step 4: Screenshot Key Points

While paused at test failure, take screenshots:
```javascript
// At failure point, capture what's on screen
// File will be saved to output/playwright/results/[test-name]/failed-N.png
```

---

## Fix Strategies by Hypothesis

### Fix A: Token Injection Timing

```typescript
// In frontend/e2e/feature-layer/helpers/session.ts

// BEFORE:
await page.goto(APP_BASE_URL);
await page.evaluate(() => { /* token injection */ });

// AFTER:
await page.goto(APP_BASE_URL);
await page.evaluate(() => { /* token injection */ });

// Explicit wait for token to be available
await page.evaluate(() => {
  return new Promise((resolve) => {
    const checkToken = setInterval(() => {
      if (localStorage.getItem('access_token')) {
        clearInterval(checkToken);
        resolve(true);
      }
    }, 50);
  });
});

// Increased delay before API calls
await new Promise(resolve => setTimeout(resolve, 300));
```

### Fix B: API Response Parsing

```typescript
// In frontend/lib/api/training.ts

// BEFORE:
async getResidentSummary(): Promise<ResidentSummary> {
  const r = await apiClient.get<ResidentSummary>('/api/residents/me/summary/');
  return r.data;
}

// AFTER (with error handling):
async getResidentSummary(): Promise<ResidentSummary> {
  const r = await apiClient.get<ResidentSummary>('/api/residents/me/summary/');
  if (!r.data) {
    throw new Error('API returned empty data');
  }
  if (!r.data.programs) {
    console.warn('Unexpected API response structure:', r.data);
  }
  return r.data;
}
```

### Fix C: ALLOWED_HOSTS

```python
# In backend/sims_project/settings.py

# BEFORE:
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'api.pgsims.alshifalab.pk',
]

# AFTER:
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'testserver',  # For E2E tests
    'api.pgsims.alshifalab.pk',
]
```

### Fix D: Refactor to Browser Login

```typescript
// Instead of token injection, use browser UI login

// Replace addInitScript approach with actual browser login
export async function loginAsRole(
  context: BrowserContext,
  page: Page,
  role: Role
): Promise<void> {
  await page.goto(APP_BASE_URL);
  
  // Use browser UI to login
  const loginButton = page.getByRole('button', { name: /Login/i });
  await loginButton.click();
  
  // Fill login form
  const username = getRoleUsername(role);
  const password = getRolePassword(role);
  
  await page.fill('input[type="text"]', username);
  await page.fill('input[type="password"]', password);
  
  // Submit form
  await page.click('button[type="submit"]');
  
  // Wait for navigation to dashboard
  await page.waitForNavigation();
  await page.waitForSelector('h1:has-text("My Training Dashboard")');
}
```

### Fix E: Add Race Condition Waits

```typescript
// In E2E test

// BEFORE:
await loginAsRole(context, page, 'pg');
const heading = page.getByText(/My Training Dashboard/i);
await expect(heading).toBeVisible();

// AFTER:
await loginAsRole(context, page, 'pg');

// Wait for specific conditions
await page.waitForFunction(() => {
  const token = localStorage.getItem('access_token');
  return token !== null;
});

// Wait for API call to complete
await page.waitForResponse(
  response => response.url().includes('/api/residents/me/summary/') && response.status() === 200
);

// Now wait for UI
const heading = page.getByText(/My Training Dashboard/i);
await expect(heading).toBeVisible({ timeout: 5000 });
```

---

## Validation After Fix

### Step 1: Run Single Test
```bash
cd frontend
npx playwright test e2e/feature-layer/auth-and-smoke.spec.ts:18 -v
```

Should see: **1 passed**

### Step 2: Run All Feature-Layer Tests
```bash
npm run test:e2e:feature-layer:local
```

Should see: **7 passed (0 failed)**

### Step 3: Run Regression Smoke
```bash
npx playwright test e2e/feature-layer/regression-smoke.spec.ts
```

Should see: **3 passed (0 failed)**

### Step 4: Commit Fix
```bash
git add .
git commit -m "Fix E2E dashboard rendering - [brief description]

- Root cause: [token/ALLOWED_HOSTS/session/etc]
- Applied fix: [what changed]
- Validation: All 7 feature-layer tests passing, regression smoke passing

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

---

## If Diagnosis Takes Too Long

**Time Limit**: If you've spent more than 2 hours on diagnosis without finding root cause:

**Option 1: Skip E2E for Now**
- Skip Blocker #2 (E2E dashboard)
- Work on Blockers #1, #4, #5, #6 (independent blockers)
- Revisit E2E with fresh eyes later

**Option 2: Try Browser Login**
- Refactor E2E to use actual browser login UI
- This is more reliable than token injection
- Takes 2-3 hours but may solve problem entirely

**Option 3: Escalate**
- Document exact failure with screenshots/traces
- Ask for help from someone with Playwright expertise
- Meanwhile, work on other blockers

---

## Common Issues & Solutions

See `07_known_issues.md` for more.

| Issue | Symptom | Solution |
|-------|---------|----------|
| Docker stale code | Tests work locally, fail in container | `docker compose build --no-cache` |
| Token not in localStorage | Token is null in logging | Increase delay or verify addInitScript runs |
| ALLOWED_HOSTS rejection | Backend logs show DisallowedHost | Add test domains to ALLOWED_HOSTS |
| Playwright session isolated | Token exists but auth fails | Refactor to browser UI login |
| API 500 error | Backend error logs present | Fix backend bug first |
| Timeout on selector | Element never appears | Check if page is showing error boundary |

---

## Next Steps

1. **Read this guide** (done)
2. **Choose your hypothesis** based on symptoms
3. **Run diagnostic steps** for that hypothesis
4. **Apply fix** if hypothesis confirmed
5. **Validate** with test execution
6. **Commit** and move to Phase 3

---

## Reference Files

- `frontend/e2e/feature-layer/helpers/session.ts` - Auth setup
- `frontend/e2e/feature-layer/auth-and-smoke.spec.ts` - Failing test
- `frontend/app/dashboard/resident/page.tsx` - Dashboard page (error boundary here)
- `frontend/lib/api/client.ts` - API client configuration
- `backend/sims/training/views.py` - Backend API endpoints
