<<<<<<< HEAD
# SIMS Testing Guide - Stage 1 Full Green

## Overview
This document provides patterns and fixes for achieving 100% test coverage with 0 failures and 0 errors.

## Current Status (Starting Point)
- Tests: 184 total (100 pass, 9 fail, 75 errors)
- Coverage: 43.28%
- Issues: ValidationErrors from missing user fields, IntegrityErrors, form validation failures

## Test Infrastructure Improvements

### 1. Factories (✅ Complete)
All models now have comprehensive factories:
- **User factories**: AdminFactory, SupervisorFactory, PGFactory
- **Logbook factories**: DiagnosisFactory, ProcedureFactory, LogbookEntryFactory, LogbookReviewFactory
- **Case factories**: CaseCategoryFactory, ClinicalCaseFactory  
- **Certificate factories**: CertificateTypeFactory, CertificateFactory
- **Rotation factories**: HospitalFactory, DepartmentFactory, RotationFactory, RotationEvaluationFactory

### 2. Deterministic Test Configuration (✅ Complete)
- `conftest.py`: Pytest fixtures for reproducible tests
- Random seed: 42 (set in conftest.py)
- Temporary media storage configured
- Freezegun integration for time-based tests

## Common Error Patterns and Fixes

### Pattern 1: ValidationError - Missing User Fields

**Error:**
```python
ValidationError: {'specialty': ['This field is required for supervisors']}
ValidationError: {'year': ['This field is required for PG users']}
```

**Old Code:**
```python
self.supervisor = User.objects.create_user(
    username='supervisor', 
    role='supervisor'
)
```

**Fixed Code:**
```python
from sims.tests.factories import SupervisorFactory, PGFactory

self.supervisor = SupervisorFactory()
self.pg = PGFactory(supervisor=self.supervisor)
```

### Pattern 2: IntegrityError - Future Date Validation

**Error:**
```python
IntegrityError: CHECK constraint failed: logbook_entry_date_not_future
```

**Fix:**
Use freezegun or ensure dates are in the past:
```python
from datetime import date, timedelta

# Option 1: Use past date
entry = LogbookEntryFactory(date=date.today() - timedelta(days=5))

# Option 2: Freeze time
from freezegun import freeze_time

@freeze_time("2024-01-15")
def test_logbook_entry(self):
    entry = LogbookEntryFactory(date=date(2024, 1, 10))
```

### Pattern 3: Form Validation Failures

**Error:**
```python
AssertionError: False is not true  # form.is_valid() failed
```

**Debug approach:**
```python
form = SomeForm(data=form_data)
if not form.is_valid():
    print(f"Form errors: {form.errors}")  # Debug what's wrong
self.assertTrue(form.is_valid())
```

**Common fixes:**
- Ensure all required fields are provided
- Use correct field names (check model fields)
- Provide valid foreign key IDs, not objects
- Use correct date format: 'YYYY-MM-DD'

### Pattern 4: Redirect Status Code Mismatches

**Error:**
```python
AssertionError: 200 != 302  # Expected redirect, got success
AssertionError: 301 != 302  # Permanent vs temporary redirect
```

**Fix:**
Check the actual view behavior:
```python
# If form is invalid, view returns 200 (re-renders form)
# If form is valid, view returns 302 (redirect)
response = self.client.post(url, data)
if response.status_code == 200:
    # Form failed validation, check errors
    form = response.context.get('form')
    if form:
        print(f"Form errors: {form.errors}")
```

### Pattern 5: Import Test Base Classes

**Error:**
```python
ImportError: cannot import name 'TestCase'
```

**Fix:**
```python
from django.test import TestCase, Client
from django.urls import reverse
```

## Systematic Test Fixing Workflow

### Step 1: Fix User Creation (Priority: CRITICAL)
Replace all manual user creation with factories:

```python
# Find all instances of:
User.objects.create_user(...)

# Replace with:
from sims.tests.factories import PGFactory, SupervisorFactory, AdminFactory

# In setUp():
self.supervisor = SupervisorFactory()
self.pg = PGFactory(supervisor=self.supervisor)
self.admin = AdminFactory()
```

### Step 2: Fix Date Validation (Priority: HIGH)
Ensure all dates are valid:

```python
from datetime import date, timedelta

# For past dates:
date=date.today() - timedelta(days=5)

# For future dates (where allowed):
date=date.today() + timedelta(days=30)
```

### Step 3: Fix Form Tests (Priority: HIGH)
Update form test data:

```python
# Check model fields first
# Ensure data dictionary has all required fields
# Use correct field types and formats

form_data = {
    'title': 'Test Title',
    'date': '2024-01-15',  # String format for form data
    'pg': self.pg.id,  # Use .id for foreign keys in forms
    'supervisor': self.supervisor.id,
    # ... all other required fields
}

form = MyForm(data=form_data)
if not form.is_valid():
    self.fail(f"Form validation failed: {form.errors}")
```

### Step 4: Fix View Tests (Priority: MEDIUM)
Ensure proper authentication and permissions:

```python
def test_view_requires_login(self):
    response = self.client.get(reverse('view-name'))
    self.assertEqual(response.status_code, 302)  # Redirect to login

def test_view_with_auth(self):
    self.client.force_login(self.pg)
    response = self.client.get(reverse('view-name'))
    self.assertEqual(response.status_code, 200)
```

## Module-Specific Fixes

### Cases Module
- Replace User.objects.create_user() with factories
- Ensure all foreign keys (category, diagnosis) are created
- Fix date fields to use past dates

### Logbook Module
- Add rotation factory usage where needed
- Fix date validation (no future dates)
- Ensure supervisor is assigned

### Certificates Module
- Add certificate_file in test data (use SimpleUploadedFile)
- Fix expiry_date to be after issue_date
- Use factories for certificate_type

### Rotations Module
- Use hospital and department factories
- Fix date ranges (start_date < end_date)
- Ensure duration_weeks matches date range

## Coverage Improvement Strategy

### Phase 1: Views (Target: 90%+)
1. Test all CRUD operations
2. Test permission checks (admin, supervisor, pg)
3. Test form validation
4. Test redirects
5. Test context data

### Phase 2: Admin (Target: 80%+)
1. Test admin list views
2. Test admin filters
3. Test admin actions
4. Test custom admin methods

### Phase 3: API (Target: 90%+)
1. Test all endpoints
2. Test authentication
3. Test permissions
4. Test response formats

### Phase 4: Forms (Target: 90%+)
1. Test valid data
2. Test invalid data
3. Test field validations
4. Test clean methods

## Testing Best Practices

### 1. Use Factories Consistently
```python
# Good
pg = PGFactory()

# Bad  
pg = User.objects.create_user(...)
```

### 2. Test One Thing Per Test
```python
# Good
def test_user_creation(self):
    user = PGFactory()
    self.assertEqual(user.role, 'pg')

def test_user_has_supervisor(self):
    user = PGFactory()
    self.assertIsNotNone(user.supervisor)

# Bad
def test_user(self):
    user = PGFactory()
    self.assertEqual(user.role, 'pg')
    self.assertIsNotNone(user.supervisor)
    # ... many more assertions
```

### 3. Use Descriptive Test Names
```python
# Good
def test_pg_cannot_access_other_pg_cases(self):
    ...

# Bad
def test_access(self):
    ...
```

### 4. Clean Up After Tests
```python
def tearDown(self):
    # Factories handle this automatically with django TestCase
    # But for manual cleanup:
    User.objects.all().delete()
```

## Running Tests

### Run all tests:
```bash
python manage.py test
```

### Run specific module:
```bash
python manage.py test sims.users
python manage.py test sims.cases
```

### Run with coverage:
```bash
coverage run --source=sims manage.py test
coverage report
coverage html
```

### Run specific test:
```bash
python manage.py test sims.users.tests.UserModelTests.test_pg_creation
```

## Quality Checks

### Before committing:
```bash
# Format code
black sims/ --line-length 100

# Check linting
flake8 sims/

# Run Django checks
python manage.py check

# Run tests
python manage.py test

# Check coverage
coverage run --source=sims manage.py test
coverage report --skip-empty
```

## Next Steps

1. ✅ Code quality (black, flake8) - DONE
2. ✅ Factory infrastructure - DONE
3. ⏳ Fix test errors (75 errors) - IN PROGRESS
4. ⏳ Fix test failures (9 failures) - PENDING
5. ⏳ Improve coverage to 100% - PENDING
6. ⏳ Add E2E tests - PENDING
7. ⏳ Documentation updates - PENDING

## Estimated Timeline

- Fix test errors: 2-3 hours (systematic replacement)
- Fix test failures: 1-2 hours (form/redirect fixes)
- Improve coverage: 3-4 hours (new test cases)
- E2E tests: 2-3 hours (integration scenarios)
- Documentation: 1 hour

Total: 9-13 hours of focused work
=======
# SIMS Testing Documentation

## Stage-1 "Full-Green" Execution Status

**Last Updated:** 2025-10-11  
**Test Runner:** Django unittest / pytest  
**Coverage Tool:** coverage.py

## Current Test Status

### Overall Metrics
- **Total Tests:** 177
- **Passing:** 107 (60.5%)
- **Failing:** 10 (5.6%)
- **Errors:** 60 (33.9%)
- **Code Coverage:** 43.29%

### Module Breakdown

#### ✅ Users Module (100% passing)
- **Tests:** 30
- **Status:** All passing
- **Coverage:** 100% (tests.py), 85.48% (models.py)

#### 🟡 Cases Module (Partial)
- **Tests:** 21
- **Passing:** 11
- **Errors:** 10
- **Coverage:** Models 60-70%, Views 30-40%

#### 🟡 Logbook Module (Partial)
- **Tests:** 61
- **Passing:** 30+
- **Errors:** 30+
- **Coverage:** Models 44%, Views 24%

#### 🟡 Certificates Module (Partial)
- **Tests:** 35
- **Coverage:** Models 57%, Admin 35%

#### 🟡 Rotations Module (Partial)
- **Tests:** 30
- **Coverage:** Models 76%, Views 50%, Forms 59%

## Infrastructure Improvements

### ✅ Test Factories Created
All main models now have factory-boy factories for consistent test data:

```python
# User factories
from sims.tests.factories.user_factories import AdminFactory, SupervisorFactory, PGFactory

# Case factories
from sims.tests.factories.case_factories import ClinicalCaseFactory, CaseCategoryFactory

# Logbook factories
from sims.tests.factories.logbook_factories import LogbookEntryFactory, DiagnosisFactory, ProcedureFactory

# Certificate factories
from sims.tests.factories.certificate_factories import CertificateFactory, CertificateTypeFactory

# Rotation factories
from sims.tests.factories.rotation_factories import RotationFactory, HospitalFactory, DepartmentFactory
```

### ✅ Code Quality Tools Applied

#### Black Formatting
- **Files Reformatted:** 33
- **Status:** ✅ Complete
- **Command:** `black sims/ --exclude migrations`

#### Flake8 Linting
- **Initial Issues:** 100+
- **Current Issues:** 36
- **Main Categories:**
  - Unused imports: 19
  - Complexity warnings (C901): 14
  - Other: 3

### ✅ Model Enhancements
Added missing methods to support test assertions:
- `ClinicalCase.can_be_submitted()` 
- `ClinicalCase.can_be_reviewed()`
- `ClinicalCase.is_complete()`
- `ClinicalCase.can_edit(user)`

## Known Issues & Solutions

### Issue 1: Date Constraint Violations
**Problem:** Models with date fields have CHECK constraints preventing future dates  
**Solution:** Factories now use `date.today() - timedelta(days=X)` for all date fields  
**Status:** ✅ Fixed

### Issue 2: Manual User Creation
**Problem:** Tests creating users manually without required fields  
**Solution:** Replaced with factory-based user creation  
**Status:** ✅ Fixed in most tests

### Issue 3: Login Authentication
**Problem:** Tests using `client.login()` with hardcoded credentials  
**Solution:** Switched to `client.force_login(user_object)`  
**Status:** ✅ Fixed in case tests, needs fixing in other modules

### Issue 4: Missing Model Fields
**Problem:** Views referencing non-existent fields (e.g., `competencies_achieved`)  
**Solution:** Removed from prefetch_related queries  
**Status:** ✅ Fixed

### Issue 5: Form Submission Tests
**Problem:** Form tests expecting 302 redirects but getting 200  
**Solution:** Need to review form payloads and validation  
**Status:** ⚠️ In Progress

## Test Execution

### Running All Tests
```bash
# Django test runner
python manage.py test sims.users sims.cases sims.logbook sims.certificates sims.rotations

# Pytest
pytest sims/

# With coverage
coverage run --source=sims manage.py test
coverage report --skip-empty
coverage html  # Generates htmlcov/ directory
```

### Running Specific Modules
```bash
# Individual modules
python manage.py test sims.users --verbosity=2
python manage.py test sims.cases --verbosity=2

# Specific test class
python manage.py test sims.cases.tests.ClinicalCaseModelTest

# Specific test method
python manage.py test sims.cases.tests.ClinicalCaseModelTest.test_case_creation
```

### Code Quality Checks
```bash
# Format code
black sims/ --exclude migrations

# Check formatting
black --check sims/

# Lint code
flake8 sims/ --count --max-complexity=10 --max-line-length=127

# Django system check
python manage.py check
python manage.py check --deploy
```

## Coverage Analysis

### High Coverage Modules (>70%)
- ✅ **users/tests.py:** 100%
- ✅ **users/models.py:** 85.48%
- ✅ **rotations/tests.py:** 95.71%
- ✅ **rotations/models.py:** 75.91%
- ✅ **search/models.py:** 100%

### Low Coverage Modules (<40%)
- ⚠️ **logbook/views.py:** 24%
- ⚠️ **cases/views.py:** 30-40%
- ⚠️ **users/views.py:** 37%
- ⚠️ **users/admin.py:** 39%
- ⚠️ **certificates/admin.py:** 35%

### Recommendations for Improvement

#### Priority 1: Fix Existing Test Failures
1. Review and fix form submission tests
2. Update test data to match model requirements
3. Fix view tests using correct payloads

#### Priority 2: Increase View Coverage
1. Add tests for view permission checks
2. Test view context data
3. Test form submission flows
4. Test redirect behaviors

#### Priority 3: Increase Admin Coverage
1. Test admin actions
2. Test admin filters
3. Test admin search
4. Test custom admin methods

#### Priority 4: API Endpoint Tests
1. Test API permissions
2. Test API response formats
3. Test API error handling

## Test Organization

### Directory Structure
```
sims/
├── users/
│   └── tests.py           # User model and view tests
├── cases/
│   └── tests.py           # Case model, form, and view tests
├── logbook/
│   └── tests.py           # Logbook entry tests
├── certificates/
│   └── tests.py           # Certificate tests
├── rotations/
│   └── tests.py           # Rotation tests
└── tests/
    └── factories/
        ├── user_factories.py
        ├── case_factories.py
        ├── logbook_factories.py
        ├── certificate_factories.py
        └── rotation_factories.py
```

### Test Naming Conventions
- Test files: `tests.py` or `test_*.py`
- Test classes: `*TestCase` or `Test*`
- Test methods: `test_*`

## Continuous Integration

### GitHub Actions Workflow
Tests run automatically on:
- Push to `main` branch
- Pull requests
- Manual workflow dispatch

### CI Pipeline Steps
1. Code formatting check (Black)
2. Linting (Flake8)
3. Django check
4. Test execution with coverage
5. Coverage reporting

## Next Steps

### Immediate Actions (High Priority)
1. ✅ Create comprehensive factories for all models
2. ✅ Apply black formatting
3. ✅ Fix date constraint issues
4. ⏳ Fix remaining test errors (60)
5. ⏳ Fix test failures (10)

### Short-term Actions (Medium Priority)
6. ⏳ Replace all manual user creation with factories
7. ⏳ Fix form submission tests
8. ⏳ Add missing view permission tests
9. ⏳ Increase overall coverage to 60%+

### Long-term Actions (Low Priority)
10. Add E2E workflow tests
11. Make tests deterministic (seed RNG, freeze time)
12. Add performance tests
13. Add API integration tests
14. Target 80%+ overall coverage

## Resources

- **Django Testing Documentation:** https://docs.djangoproject.com/en/4.2/topics/testing/
- **Factory Boy Documentation:** https://factoryboy.readthedocs.io/
- **Coverage.py Documentation:** https://coverage.readthedocs.io/
- **Black Code Style:** https://black.readthedocs.io/
- **Flake8 Linting:** https://flake8.pycqa.org/

## Support

For questions or issues related to testing:
1. Check this documentation
2. Review existing test examples
3. Consult the Testing Guide in `docs/TESTING_GUIDE.md`
4. Check CI logs for detailed error messages

---

**Note:** This is a living document. Update it as the test suite evolves.
>>>>>>> origin/main
