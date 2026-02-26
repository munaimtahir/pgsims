# SIMS Stage 1 Testing Guide

## Overview
This guide provides instructions for running tests, measuring coverage, and maintaining code quality for the SIMS application.

## Prerequisites
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install black flake8 pytest pytest-django pytest-cov factory-boy faker
```

## Running Tests

### Basic Test Execution
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test sims.users
python manage.py test sims.cases
python manage.py test sims.logbook

# Run with verbosity
python manage.py test --verbosity=2

# Run specific test class
python manage.py test sims.users.tests.UserModelTestCase

# Run specific test method
python manage.py test sims.users.tests.UserModelTestCase.test_user_creation
```

### Using Pytest
```bash
# Run all tests with pytest
pytest

# Run with coverage
pytest --cov=sims --cov-report=html --cov-report=term-missing

# Run specific tests
pytest sims/users/tests.py
pytest sims/users/tests.py::UserModelTestCase
pytest sims/users/tests.py::UserModelTestCase::test_user_creation

# View coverage report
open htmlcov/index.html  # On macOS
xdg-open htmlcov/index.html  # On Linux
```

## Code Quality

### Formatting with Black
```bash
# Check formatting
black --check sims/ --line-length 100

# Format code
black sims/ --line-length 100

# Format specific file
black sims/users/models.py --line-length 100
```

### Linting with Flake8
```bash
# Run linting
flake8 sims/

# Check specific file
flake8 sims/users/models.py

# Get statistics
flake8 sims/ --count --statistics
```

### Pre-commit Hooks
```bash
# Install pre-commit hooks
pre-commit install

# Run manually on all files
pre-commit run --all-files

# Run on staged files
pre-commit run
```

## Django Checks

### Development Check
```bash
# Basic check
python manage.py check

# Deployment check
python manage.py check --deploy
```

### Database Management
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput
```

## Writing Tests

### Using Factory-Boy
```python
from tests.factories.user_factory import AdminFactory, SupervisorFactory, PGFactory

class MyTestCase(TestCase):
    def setUp(self):
        # Create test users using factories
        self.admin = AdminFactory()
        self.supervisor = SupervisorFactory(specialty="surgery")
        self.pg = PGFactory(
            specialty="medicine",
            year="2",
            supervisor=self.supervisor
        )

    def test_something(self):
        # Your test logic
        self.assertEqual(self.pg.role, "pg")
```

### Required Fields for User Creation

When creating users manually in tests, ensure required fields are provided:

**Admin Users:**
```python
admin = User.objects.create_user(
    username="admin_test",
    password="testpass123",
    role="admin"
)
```

**Supervisor Users:**
```python
supervisor = User.objects.create_user(
    username="supervisor_test",
    password="testpass123",
    role="supervisor",
    specialty="medicine"  # Required!
)
```

**PG Users:**
```python
pg = User.objects.create_user(
    username="pg_test",
    password="testpass123",
    role="pg",
    specialty="medicine",  # Required!
    year="1",              # Required!
    supervisor=supervisor   # Required!
)
```

## Coverage Targets

- **Overall Coverage:** ≥80%
- **Core Modules:** ≥90%
  - sims/users/
  - sims/cases/
  - sims/logbook/
- **Views:** ≥70%
- **Models:** ≥80%

## Continuous Integration

Tests run automatically on:
- Push to `main` branch
- Pull requests
- Manual workflow dispatch

### CI Pipeline
1. Code formatting check (Black)
2. Linting (Flake8)
3. Django check
4. Test execution with coverage
5. Coverage reporting

## Troubleshooting

### Common Issues

**Issue:** ValidationError: Specialty is required for Supervisors
```python
# Solution: Add specialty field
supervisor = User.objects.create_user(
    ...,
    role="supervisor",
    specialty="medicine"  # Add this
)
```

**Issue:** Tests fail with "No module named 'factory'"
```bash
# Solution: Install factory-boy
pip install factory-boy faker
```

**Issue:** Coverage report not generated
```bash
# Solution: Install pytest-cov
pip install pytest-cov
pytest --cov=sims --cov-report=html
```

## Best Practices

1. **Run tests before committing:**
   ```bash
   pre-commit run --all-files
   python manage.py test
   ```

2. **Check coverage regularly:**
   ```bash
   pytest --cov=sims --cov-report=term-missing
   ```

3. **Use factories for test data:**
   - More consistent
   - Easier to maintain
   - Handles required fields automatically

4. **Write descriptive test names:**
   ```python
   def test_pg_cannot_access_other_pg_cases(self):
       # Clear what is being tested
   ```

5. **Test one thing per test:**
   - Easier to debug
   - Clearer intent
   - Better error messages

## Resources

- [Django Testing Documentation](https://docs.djangoproject.com/en/4.2/topics/testing/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Factory Boy Documentation](https://factoryboy.readthedocs.io/)
- [Black Documentation](https://black.readthedocs.io/)
- [Flake8 Documentation](https://flake8.pycqa.org/)

## Support

For questions or issues:
1. Check [CONTRIBUTING.md](../CONTRIBUTING.md)
2. Review [STAGE1_READINESS_REPORT.md](./reports/STAGE1_READINESS_REPORT.md)
3. Contact the development team
