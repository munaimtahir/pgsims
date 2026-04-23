# Troubleshooting Decision Tree

**Last Updated**: 2026-04-23  
**Use This When**: Something is broken and you need to find the root cause  
**Format**: Follow the decision tree, make yes/no choices, reach solution  

---

## START HERE

```
    Have you read the error message carefully?
            ↙ NO                    YES ↘
    Read it again!           Continue below
   (Often the answer
    is in the message)
```

---

## Branch 1: Backend Test Failures

```
                    BACKEND TEST FAILS
                           ↓
                    What is the error?
                    ↙ ↓ ↓ ↓ ↓ ↓ ↘
         ┌──────────────────────────────────────────────────────────┐
         ↓                                      ↓              ↓
    "Permission                         "Field not                "JSON decode
     Denied (403)"                      found"              error" / Parsing
         ↓                                  ↓                      ↓
      TREE 1.1                          TREE 1.2                 TREE 1.3
```

### TREE 1.1: Permission Denied (403)

```
Problem: Test expects 200 but got 403

Root Cause Questions:
  Q1: Is the user authenticated?
    → NO: Add self.client.force_authenticate(user=test_user)
    → YES: Continue
    
  Q2: Does the user have the correct role?
    → NO: Create user with correct role (role='pg', 'supervisor', 'admin')
    → YES: Continue
    
  Q3: Is the user scoped correctly?
    (Example: Supervisor needs SupervisorAssignment to PG)
    → NO: Create the required relationship
    → YES: Continue
    
  Q4: Check permission class in view
    → The view uses @permission_classes([IsAuthenticated, IsScopeOwner])
    → Verify test user matches scope requirement

SOLUTION: See 07_known_issues.md → Backend Test Failure section
```

### TREE 1.2: Field Not Found

```
Problem: "KeyError: 'field_name'" or "AssertionError: field not in response"

Root Cause Questions:
  Q1: Is the field documented in the API contract?
    → NO: Check docs/contracts/API_CONTRACT.md, might be wrong field name
    → YES: Continue
    
  Q2: Did you mock the API call?
    → NO: Add @patch('sims.app.api_function') to test
    → YES: Continue
    
  Q3: Does the mock return the right data structure?
    → NO: Fix mock to return correct fields
    → YES: Continue
    
  Q4: Check if field is conditional
    → Maybe field only appears in certain scenarios
    → Print actual response to see what's there: print(response.json())

SOLUTION: Print the actual response, compare to expected, find mismatch
```

### TREE 1.3: JSON Decode Error

```
Problem: "json.JSONDecodeError" or "response is not valid JSON"

Root Cause Questions:
  Q1: Did you forget to call .json() on response?
    → NO: You did, add .json()
    → YES: Continue
    
  Q2: Is the endpoint returning HTML error page instead of JSON?
    → Check: response.text[:100]
    → If starts with "<html>", backend error occurred
    → Go check backend logs: docker compose logs backend
    → YES: Go to TREE 2 (Backend Errors)
    
  Q3: Is it a Django admin URL instead of API?
    → Check: response.status_code
    → 302 redirect? URL is wrong
    → Fix URL to /api/... not /admin/

SOLUTION: Print response.text, look for HTML/error message, fix URL
```

---

## Branch 2: Backend Errors

```
                    BACKEND CRASHES/ERRORS
                           ↓
                    Check backend logs
                  docker compose logs backend
                           ↓
                    What error do you see?
```

### Backend Error Categories

```
ERROR PATTERN                          SOLUTION
────────────────────────────────────────────────────────────
ImproperlyConfigured:                → Missing Django setting or import
ModuleNotFoundError:                  → Missing pip dependency
DatabaseError:                        → DB connection issue
IntegrityError:                       → Foreign key constraint violated
ValidationError:                      → Input validation failed
```

**Diagnostic Steps**:

```bash
# Check backend logs
docker compose logs backend | tail -50

# If you see Python traceback:
# 1. Note the file and line number
# 2. Open that file in your editor
# 3. Look at the code context
# 4. Usually the fix is obvious from there

# If still stuck, search for error
grep -r "ValidationError" backend/sims/ | grep -v ".pyc"
```

---

## Branch 3: Frontend Test Failures

```
                    FRONTEND TEST FAILS
                           ↓
                    What is the error?
                    ↙ ↓ ↓ ↓ ↘
         ┌──────────────────────────────────────┐
         ↓                    ↓            ↓
    "Timeout waiting"   "Element not   "Snapshot
     "for selector"      found"        mismatch"
         ↓                    ↓            ↓
      TREE 3.1            TREE 3.2      TREE 3.3
```

### TREE 3.1: Timeout Waiting for Selector

```
Problem: Test times out, element never appears

Root Cause Questions:
  Q1: Is the selector correct?
    → Run: screen.debug() in test
    → Look at output, find exact text/role
    → YES: Continue
    
  Q2: Did the API mock return data?
    → Add: console.log(mockResponse)
    → Check: mockAPI.mockResolvedValue({data: [...]})
    → YES: Continue
    
  Q3: Is the component rendering at all?
    → Query for parent div: screen.getByTestId('dashboard')
    → If not found, component isn't mounting
    → Reason: Error in parent component
    → FIX: Check component code for errors
    
  Q4: Is the data processing correct?
    → Component receives data → processes it → renders
    → Maybe processing has bug
    → Check: component console.log for errors

SOLUTION: Use screen.debug() to see actual DOM, verify selector
```

### TREE 3.2: Element Not Found

```
Problem: "Unable to find element" / "screen.getByText(...) didn't find"

Root Cause Questions:
  Q1: Did mock API call resolve?
    → No: Mock rejected with error
    → Fix: mockAPI.mockResolvedValue({data: ...})
    
  Q2: Is component showing error boundary?
    → screen.debug() shows "Error loading..." message
    → Component caught an exception
    → Check: component try/catch blocks
    
  Q3: Is element in wrong place?
    → Element exists but not where expected
    → Check: element is in correct container
    → Maybe it's in a modal or dropdown you didn't see

SOLUTION: Print screen.debug(), search for element name, check mocks
```

### TREE 3.3: Snapshot Mismatch

```
Problem: "Snapshot doesn't match"

Root Cause:
  Q1: Did you intentionally change the UI?
    → YES: Update snapshot: npm test -- -u
    → NO: Continue
    
  Q2: Did dependencies change?
    → Run: npm install again
    → Run: npm test -- -u to regenerate
    
  Q3: Did component behavior change?
    → Find exact line that changed
    → Decide: Is this OK?
    → If yes: npm test -- -u
    → If no: Revert component change

SOLUTION: Review snapshot diff, decide OK or revert, update with -u flag
```

---

## Branch 4: E2E Test Failures

```
                    E2E TEST FAILS
                           ↓
                    What happens?
                    ↙ ↓ ↓ ↓ ↘
         ┌──────────────────────────────────────┐
         ↓           ↓           ↓          ↓
    "Failed to    "Login     "404 on    "Navigation
     load          timeout"   page"     timeout"
     dashboard"
         ↓           ↓           ↓          ↓
      TREE 4.1    TREE 4.2    TREE 4.3   TREE 4.4
```

### TREE 4.1: Failed to Load Dashboard

```
Problem: E2E passes login, dashboard shows "Failed to load dashboard"

ROOT CAUSE: See 07_known_issues.md Issue 1

Hypotheses (ranked by probability):
  1. Token not injected in time (40%)
     → FIX: Increase delay or wait for token explicitly
     → See: 04_e2e_debugging.md → Hypothesis A
     
  2. API returns 401/403 (20%)
     → FIX: Check auth header is present in API call
     → See: 04_e2e_debugging.md → Hypothesis B
     
  3. ALLOWED_HOSTS rejects (15%)
     → FIX: Add testserver to ALLOWED_HOSTS
     → See: 04_e2e_debugging.md → Hypothesis C
     
  4. Session cleared (15%)
     → FIX: Refactor to browser UI login
     → See: 04_e2e_debugging.md → Hypothesis D
     
  5. Race condition (10%)
     → FIX: Add more robust waits
     → See: 04_e2e_debugging.md → Hypothesis E

SOLUTION: Follow diagnostic procedure in 04_e2e_debugging.md
```

### TREE 4.2: Login Timeout

```
Problem: Test hangs on login, never progresses

Root Cause Questions:
  Q1: Is the login form visible?
    → Check test screenshot
    → If visible: Continue
    → If not visible: Form didn't load
    
  Q2: Did test fill username/password correctly?
    → Check: page.fill selector matches input
    → Maybe ID or class changed
    
  Q3: Does login form work locally?
    → Open http://127.0.0.1:3000 in browser
    → Try login manually
    → If manual works, E2E issue
    → If manual fails, backend issue

SOLUTION: Check form selectors, verify backend running, manual test
```

### TREE 4.3: 404 on Page

```
Problem: Test navigates to page, gets 404 error

Root Cause Questions:
  Q1: Is URL correct?
    → Check: /dashboard vs /dashboard/resident
    → Check: docs/contracts/ROUTES.md for correct path
    
  Q2: Is frontend build fresh?
    → npm run build
    → docker compose up -d frontend
    
  Q3: Is page route defined?
    → Check: frontend/app/[page]/page.tsx exists
    → If not, it's not implemented yet

SOLUTION: Verify URL, rebuild frontend, check route exists
```

### TREE 4.4: Navigation Timeout

```
Problem: page.goto() hangs, never completes

Root Cause Questions:
  Q1: Is backend running?
    → docker compose ps backend
    → Should show "healthy"
    
  Q2: Is frontend running?
    → curl http://127.0.0.1:3000
    → Should return HTML
    
  Q3: Is there an infinite loop?
    → Browser stuck loading
    → Check: Network tab in Playwright Inspector
    → Look for requests that never complete

SOLUTION: Verify services running, check network tab, reduce timeout
```

---

## Branch 5: Docker Issues

```
                    DOCKER SERVICE ISSUES
                           ↓
                    Check status
                  docker compose ps
                           ↓
                    What do you see?
```

### Docker Status Codes

```
STATUS                              NEXT STEP
────────────────────────────────────────────────────────────
"Up X hours (healthy)"          → Service is OK
"Up X hours (unhealthy)"        → Restart: docker compose restart [svc]
"restarting"                    → Waiting for service, try again in 10s
"Exited (1)"                    → Service crashed, check logs
"Cannot connect to Docker"      → Docker daemon not running
```

**Diagnostic**:

```bash
# Check service logs
docker compose logs backend | tail -50

# Check specific service
docker compose ps backend

# Restart service
docker compose restart backend

# Rebuild service
docker compose up -d --build backend

# Nuclear option: restart everything
docker compose down
docker compose build --no-cache
docker compose up -d
docker compose ps  # Wait for healthy
```

---

## Branch 6: Coverage Issues

```
                    COVERAGE BELOW THRESHOLD
                           ↓
                    What's the coverage?
                    ↙ Backend          Frontend ↘
                    ↙                              ↘
              TREE 6.1                        TREE 6.2
```

### TREE 6.1: Backend Coverage Low

```
Problem: Backend coverage 54% (need 95%)

Question: Which module is lowest?
  → Run: pytest sims --cov=sims --cov-report=term
  → Look for: Modules with <30% coverage
  
Example low modules:
  - sims/training/permissions.py (30%)
  - sims/rotations/views.py (35%)
  
Fix Strategy:
  1. Identify what's NOT tested
     → Print code: grep -A 10 "class PermissionClass" backend/sims/...
  2. Write allow + deny test pair
     → See: 05_coverage_strategy.md → Example template
  3. Run with coverage: pytest sims/training/ --cov=sims.training
  4. Repeat for next low module

SOLUTION: Follow 05_coverage_strategy.md coverage plan
```

### TREE 6.2: Frontend Coverage Low

```
Problem: Frontend coverage 8% (need 90%)

Question: Which component has no tests?
  → Run: npm run test:coverage
  → Look for: Files with 0% coverage
  
Fix Strategy:
  1. Identify all components: find app components lib -name "*.tsx"
  2. For each with 0% coverage:
     → Create [name].test.tsx in __tests__ folder
     → Test rendering with props
     → Test user interactions
     → Test error states
  3. Run: npm run test:coverage
  4. Target: 30% → 60% → 90%

SOLUTION: Follow 05_coverage_strategy.md coverage plan
```

---

## Branch 7: Unclear/Weird Issues

```
                    SOMETHING IS VERY WRONG
                    But I can't categorize it
                           ↓
                    Try these steps
```

### Nuclear Debug Procedure

```
1. Clear everything
   docker compose down
   rm -rf backend/.pytest_cache frontend/node_modules/.cache
   rm -rf .git/index.lock
   
2. Rebuild from scratch
   docker compose build --no-cache
   docker compose up -d
   
3. Reseed from scratch
   docker compose exec -T backend python manage.py migrate
   ./scripts/e2e_seed.sh
   
4. Run single test
   cd backend && pytest sims/training/test_api.py::TestClass::test_method -vvv -s
   
5. If still broken
   → Document exact steps to reproduce
   → Copy full error message
   → Search 07_known_issues.md for similar
   → Ask on team chat
```

---

## When All Else Fails

**Document**:
- Exact error message (copy-paste)
- Exact steps to reproduce
- What you've already tried
- Which file/line is affected

**Search**:
- `07_known_issues.md` for similar problem
- GitHub issues in PGSIMS repo
- Team chat history

**Ask**:
- Post on team chat with full context
- Include screenshot if possible
- Include exact error message
- Include "I've already tried X, Y, Z"

**Escalate**:
- If stuck >2 hours on E2E dashboard (Blocker #2)
- If stuck >3 hours on coverage (Blockers #5 #6)
- Consider different approach or asking for help

---

## Reference: Error Message → Solution Map

| Error Message | See Section |
|---------------|------------|
| "Permission Denied (403)" | TREE 1.1 |
| "Field not found" | TREE 1.2 |
| "JSON decode error" | TREE 1.3 |
| "DatabaseError" | Branch 2 |
| "Timeout waiting for selector" | TREE 3.1 |
| "Element not found" | TREE 3.2 |
| "Snapshot mismatch" | TREE 3.3 |
| "Failed to load dashboard" | TREE 4.1 |
| "Login timeout" | TREE 4.2 |
| "404 on page" | TREE 4.3 |
| "Navigation timeout" | TREE 4.4 |
| "Docker unhealthy" | Branch 5 |
| "Coverage too low" | Branch 6 |

