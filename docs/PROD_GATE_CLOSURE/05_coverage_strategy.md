# Coverage Improvement Strategy

**Last Updated**: 2026-04-23  
**Focus**: Blockers #5 & #6 - Backend & Frontend Code Coverage  
**Current State**: Backend 54.38% / Frontend 8.71%  
**Target**: Backend ≥95% / Frontend ≥90%  
**Time to Read**: 15-20 minutes  

---

## Quick Summary

**Why Coverage Matters**:
- Coverage isn't about line count—it's about confidence
- 95% backend coverage = most permission checks, workflows, and edge cases are tested
- 90% frontend coverage = most UI paths, error handling, and user interactions are tested
- Low coverage indicates untested logic = untested bugs = production risk

**The Gap**:
- Backend: 41 percentage points to 95% (HUGE)
- Frontend: 81 percentage points to 90% (ENORMOUS)
- This is NOT filling small gaps—this is systematic test infrastructure

**Reality Check**:
- Adding 50-100 meaningful backend tests = 8-15 hours
- Adding 100-200 meaningful frontend tests = 15-20 hours
- "Meaningful" = tests that verify behavior, not just "status is 200"

**Priority Strategy**:
1. Identify which modules have the LOWEST coverage
2. Test the highest-impact, lowest-hanging-fruit first
3. Focus on permission checks and state machines (high ROI)
4. Avoid testing trivial getters/setters

---

## Understanding Coverage Metrics

### Branch Coverage vs Line Coverage

```
Line coverage = Did this line execute? (Simpler metric)
Branch coverage = Did all code paths in this line execute? (Stricter metric)

Example:
if permission_ok:        # Line 1
    return Response()    # Line 2
else:                    # Line 3
    return Error()       # Line 4

Line coverage test: Run either if-block or else-block once
Branch coverage test: Must run BOTH if-block AND else-block separately

Current state:
- Backend: 54% line / 28% branch (gap = permission checks untested)
- Frontend: 8% line / 7% branch (gap = conditional rendering untested)
```

### Why Branch Coverage Is More Realistic

Production bugs usually happen in the `else` branch that was never tested.

```python
# Example with bad branch coverage

if user.role == 'pg':
    # This path is tested
    return Response(summarize_pg_data(user))
else:
    # This path is NOT tested (supervisor/admin branch)
    return Response(summarize_admin_data(user))

# Test result: 50% line coverage ✓, but 0% branch coverage ✗
# Production: Supervisor users get 500 error
```

---

## Backend Coverage Improvement

### Step 1: Identify Low-Coverage Modules

```bash
cd backend

# Run coverage report
pytest sims --cov=sims --cov-report=html --cov-report=term 2>&1 | \
  tail -100

# Look for modules with <50% coverage
# Sample output:
# sims/training/permissions.py      30%  ← PRIORITY 1
# sims/rotations/views.py           35%  ← PRIORITY 1
# sims/notifications/views.py       40%  ← PRIORITY 1
# sims/analytics/endpoints.py       45%  ← PRIORITY 1
```

### Step 2: Analyze What's NOT Tested

For each low-coverage module, ask:

```python
# Example: sims/training/permissions.py (30% coverage)

# What's NOT tested?
# 1. Supervisor permission checks (supervisor role)
# 2. Admin permission checks (admin role)
# 3. Cross-hospital permission denials
# 4. Logbook state machine transitions
# 5. Error cases

# What SHOULD be tested?
# ✓ PG can view own logbook (existing)
# ✗ PG cannot view other's logbook (missing)
# ✗ Supervisor can view assigned PG's logbook (missing)
# ✗ Admin can view any logbook (missing)
# ✗ PG cannot modify approved entry (missing)
```

### Step 3: Write High-Impact Tests

**Focus Areas** (in order of ROI):

1. **Permission Classes** (3-5 hours)
   - Each permission class needs: allowed + denied test
   - Example: `IsOwnerOrSupervisor`
     - ✓ Owner can access
     - ✗ Non-owner denied
     - ✗ Supervisor can access (if applicable)
     - ✗ Admin can access (if applicable)

2. **State Machines** (3-5 hours)
   - Logbook entry lifecycle: draft → submitted → reviewed → approved
   - Rotation lifecycle: draft → requested → approved → active → completed
   - Leave lifecycle: requested → approved/rejected → completed

3. **Viewset Actions** (2-3 hours)
   - Test `.list()`, `.create()`, `.update()`, `.destroy()` with various roles
   - Test custom actions like `.approve()`, `.reject()`, `.submit()`

4. **Serializer Validation** (2-3 hours)
   - Invalid input handling
   - Required field validation
   - Cross-field validation (e.g., end_date > start_date)

5. **Dashboard Endpoints** (1-2 hours)
   - Resident dashboard (my summary)
   - Supervisor dashboard (my assignees)
   - Admin dashboard (system overview)

### Example: Permission Test Template

```python
# File: backend/sims/training/test_permissions.py

from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

class LogbookPermissionTests(APITestCase):
    def setUp(self):
        # Create test users
        self.resident_pg = User.objects.create_user(
            username='pg1', 
            role='pg',
            home_department=self.dept
        )
        self.supervisor = User.objects.create_user(
            username='sup1',
            role='supervisor'
        )
        self.admin = User.objects.create_user(
            username='admin1',
            role='admin'
        )
        
        # Create test logbook entry
        self.entry = LogbookEntry.objects.create(
            pg=self.resident_pg,
            title='Test Entry',
            status='submitted'
        )
    
    def test_owner_can_view_own_entry(self):
        """PG can view their own logbook entry"""
        self.client.force_authenticate(user=self.resident_pg)
        response = self.client.get(f'/api/logbook/{self.entry.id}/')
        self.assertEqual(response.status_code, 200)
    
    def test_non_owner_denied(self):
        """Other PG cannot view someone else's entry"""
        other_pg = User.objects.create_user(
            username='pg2',
            role='pg'
        )
        self.client.force_authenticate(user=other_pg)
        response = self.client.get(f'/api/logbook/{self.entry.id}/')
        self.assertEqual(response.status_code, 403)
    
    def test_supervisor_can_view_assignee(self):
        """Supervisor can view assigned PG's entry"""
        # Link supervisor to resident
        SupervisorAssignment.objects.create(
            supervisor=self.supervisor,
            pg=self.resident_pg
        )
        self.client.force_authenticate(user=self.supervisor)
        response = self.client.get(f'/api/logbook/{self.entry.id}/')
        self.assertEqual(response.status_code, 200)
    
    def test_supervisor_denied_unassigned(self):
        """Supervisor cannot view non-assigned PG's entry"""
        self.client.force_authenticate(user=self.supervisor)
        response = self.client.get(f'/api/logbook/{self.entry.id}/')
        self.assertEqual(response.status_code, 403)
```

### Step 4: Test Execution Command

```bash
cd backend

# Run with detailed coverage per file
pytest sims \
  --cov=sims \
  --cov-report=html \
  --cov-report=term-missing \
  --cov-fail-under=95 \
  -v

# Generate HTML coverage report
# View: htmlcov/index.html

# Run specific test module
pytest sims/training/test_permissions.py -v

# Run with verbose output
pytest sims/training/test_permissions.py::LogbookPermissionTests::test_owner_can_view_own_entry -vv
```

---

## Frontend Coverage Improvement

### Step 1: Identify Low-Coverage Modules

```bash
cd frontend

# Run coverage
npm run test:coverage 2>&1 | tail -50

# Look for components/pages with <10% coverage
# Sample output:
# app/dashboard/resident/page.tsx      2%  ← PRIORITY 1
# app/logbook/create/page.tsx          5%  ← PRIORITY 1
# components/LogbookForm.tsx           8%  ← PRIORITY 1
# lib/hooks/useDashboard.ts            0%  ← PRIORITY 1
```

### Step 2: Write Component Behavior Tests

**DO** focus on these:
- ✓ Rendering with different props
- ✓ User interactions (clicks, form fills)
- ✓ Loading/error/success states
- ✓ Navigation behavior
- ✓ Role-based visibility

**DON'T** do these:
- ✗ Snapshot tests (brittle)
- ✗ Prop type tests (TypeScript already does this)
- ✗ "Component renders" (too trivial)
- ✗ UI library tests (let them handle it)

### Example: Component Test Template

```typescript
// File: frontend/app/dashboard/__tests__/resident.test.tsx

import { render, screen, waitFor } from '@testing-library/react';
import ResidentDashboard from '../resident/page';
import * as api from '@/lib/api/training';

// Mock the API
jest.mock('@/lib/api/training');

describe('Resident Dashboard Page', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders dashboard title when data loads', async () => {
    const mockData = {
      name: 'John Doe',
      programs: [],
      hours: 0
    };
    
    (api.getResidentSummary as jest.Mock).mockResolvedValue(mockData);

    render(<ResidentDashboard />);

    await waitFor(() => {
      expect(screen.getByText('My Training Dashboard')).toBeInTheDocument();
    });
  });

  it('shows loading state while fetching', () => {
    (api.getResidentSummary as jest.Mock).mockImplementation(
      () => new Promise(() => {}) // Never resolves
    );

    render(<ResidentDashboard />);
    expect(screen.getByText(/Loading/i)).toBeInTheDocument();
  });

  it('shows error message on API failure', async () => {
    (api.getResidentSummary as jest.Mock).mockRejectedValue(
      new Error('API Error')
    );

    render(<ResidentDashboard />);

    await waitFor(() => {
      expect(screen.getByText(/Failed to load dashboard/i)).toBeInTheDocument();
    });
  });

  it('displays resident programs when loaded', async () => {
    const mockData = {
      name: 'John Doe',
      programs: [
        { id: '1', name: 'General Surgery', progress: 75 },
        { id: '2', name: 'Pediatrics', progress: 50 }
      ],
      hours: 500
    };

    (api.getResidentSummary as jest.Mock).mockResolvedValue(mockData);

    render(<ResidentDashboard />);

    await waitFor(() => {
      expect(screen.getByText('General Surgery')).toBeInTheDocument();
      expect(screen.getByText('Pediatrics')).toBeInTheDocument();
    });
  });

  it('shows empty state when no programs assigned', async () => {
    const mockData = {
      name: 'John Doe',
      programs: [],
      hours: 0
    };

    (api.getResidentSummary as jest.Mock).mockResolvedValue(mockData);

    render(<ResidentDashboard />);

    await waitFor(() => {
      expect(screen.getByText(/No programs assigned/i)).toBeInTheDocument();
    });
  });
});
```

### Step 3: Test Execution Command

```bash
cd frontend

# Run all tests with coverage
npm run test:coverage

# Run specific test file
npm test -- app/dashboard/__tests__/resident.test.tsx --watch=false

# Run with verbose output
npm test -- --verbose --watch=false

# Check coverage for specific module
npm run test:coverage -- --collectCoverageFrom="app/dashboard/**/*.tsx"
```

---

## Realistic Coverage Targets

### Phase 1 Target (Quick Win)
- Backend: 65% line coverage (add ~30 tests)
- Frontend: 30% line coverage (add ~50 tests)
- Time: 1-2 days

### Phase 2 Target (Production Ready)
- Backend: 85% line / 80% branch (add ~50 more tests)
- Frontend: 60% line / 55% branch (add ~50 more tests)
- Time: 2-3 days

### Phase 3 Target (Strict Gate - 95/90)
- Backend: 95% line / 90% branch (add ~30 more tests)
- Frontend: 90% line / 85% branch (add ~80 more tests)
- Time: 3-4 days

---

## Quick Coverage Wins

If you're in a time crunch, focus on these high-ROI areas:

**Backend** (3-4 hours for +20% coverage):
1. Permission classes - Write allow/deny test pairs (2 hours)
2. Dashboard view tests - Mock API, test response structure (1 hour)
3. Serializer validation tests - Invalid input + edge cases (1 hour)

**Frontend** (3-4 hours for +30% coverage):
1. Dashboard page rendering - Mock API, test UI states (1 hour)
2. Logbook form interactions - Test form fills and submissions (1 hour)
3. Error boundary tests - Test error states (1 hour)

---

## Help Commands

```bash
# Find lowest-coverage files
cd backend && pytest sims --cov=sims --cov-report=term | \
  grep -E "^\s+[0-9]+" | sort -t' ' -k2 -n | head -20

# Find frontend files with no tests
cd frontend && find app components lib -name "*.tsx" -o -name "*.ts" | \
  while read f; do
    if [ ! -f "${f%.tsx}.test.tsx" ] && [ ! -f "${f%.ts}.test.ts" ]; then
      echo "No test: $f"
    fi
  done | head -20

# Run only critical path tests
cd backend && pytest sims/training/ sims/rotations/ -v
cd frontend && npm test -- app/dashboard app/logbook --watch=false
```

---

## Next Steps

1. **Identify low-coverage modules** using grep commands above
2. **Prioritize by impact** - Dashboard > Logbook > Admin > Other
3. **Write permission tests first** - Highest ROI
4. **Add state machine tests** - Verify workflows
5. **Add component tests** - Frontend UI paths
6. **Measure regularly** - Track progress toward thresholds

