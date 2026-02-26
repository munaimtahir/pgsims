# Contributing to SIMS

Thank you for considering contributing to the SIMS (Surgical Information Management System) project! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Making Changes](#making-changes)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)

## Code of Conduct

### Our Standards

- Be respectful and inclusive
- Accept constructive criticism gracefully
- Focus on what is best for the project and community
- Show empathy towards other community members

### Unacceptable Behavior

- Use of sexualized language or imagery
- Trolling, insulting/derogatory comments, and personal attacks
- Public or private harassment
- Publishing others' private information without permission

## Getting Started

### Prerequisites

Before contributing, ensure you have:

- Python 3.11 or higher installed
- Git installed and configured
- Basic understanding of Django framework
- Familiarity with HTML, CSS, and JavaScript
- Understanding of medical training workflows (helpful but not required)

### Finding Issues to Work On

1. Check the [Issues](https://github.com/munaimtahir/sims/issues) page
2. Look for issues labeled `good first issue` or `help wanted`
3. Read the issue description and comments carefully
4. Comment on the issue to express your interest

## Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/sims.git
cd sims
```

### 2. Set Up Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
# Install project dependencies
pip install -r requirements.txt

# Install development dependencies
pip install black flake8 pytest pytest-django
```

### 4. Configure Database

```bash
# Run migrations
python manage.py migrate

# Create a superuser for testing
python manage.py createsuperuser
```

### 5. Run Development Server

```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000 to verify the setup.

## Coding Standards

### Python Code Style

We follow PEP 8 style guidelines with some modifications:

- **Line Length**: Maximum 100 characters (not 79)
- **Formatting**: Use [Black](https://github.com/psf/black) for automatic formatting
- **Linting**: Use [Flake8](https://flake8.pycqa.org/) for code quality checks
- **Imports**: Organize imports in the following order:
  1. Standard library imports
  2. Django imports
  3. Third-party imports
  4. Local application imports

### Django Conventions

- Use class-based views where appropriate
- Follow Django naming conventions for models, views, and URLs
- Use Django's built-in authentication and permissions
- Write descriptive docstrings for all classes and functions
- Use Django's translation framework for user-facing strings

### HTML/CSS/JavaScript

- Use Bootstrap 5 classes consistently
- Keep custom CSS minimal and organized
- Write semantic HTML
- Use Font Awesome for icons
- Keep JavaScript modular and commented

### Database

- Always create migrations for model changes: `python manage.py makemigrations`
- Test migrations before committing
- Never commit database files (db.sqlite3)
- Write descriptive migration names

## Making Changes

### Branch Naming

Create a descriptive branch name:

- `feature/add-notification-system` - New features
- `fix/login-redirect-issue` - Bug fixes
- `docs/update-api-documentation` - Documentation updates
- `refactor/optimize-queries` - Code refactoring
- `test/add-user-tests` - Adding tests

```bash
git checkout -b feature/your-feature-name
```

### Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, missing semicolons, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**

```bash
# Good commit messages
git commit -m "feat(logbook): add bulk entry creation feature"
git commit -m "fix(users): resolve login redirect issue for supervisors"
git commit -m "docs(readme): update installation instructions"

# Bad commit messages (avoid these)
git commit -m "fixed stuff"
git commit -m "updates"
git commit -m "WIP"
```

### Code Formatting

Before committing, format your code:

```bash
# Format Python code with Black
black sims/ --line-length 100

# Check code quality with Flake8
flake8 sims/ --count --statistics

# Or run both
black sims/ --line-length 100 && flake8 sims/
```

## Testing Guidelines

### Writing Tests

- Write tests for all new features
- Update tests when modifying existing features
- Aim for good test coverage (70%+ is ideal)
- Test both success and error cases

### Test Structure

```python
from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserModelTestCase(TestCase):
    """Test cases for User model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_user_creation(self):
        """Test user can be created"""
        self.assertEqual(self.user.username, 'testuser')
        self.assertTrue(self.user.check_password('testpass123'))
    
    def tearDown(self):
        """Clean up after tests"""
        self.user.delete()
```

### Running Tests

```bash
# Run all tests
python manage.py test

# Run tests for a specific app
python manage.py test sims.users

# Run with verbose output
python manage.py test --verbosity=2

# Run with pytest (if configured)
pytest
pytest sims/users/tests.py
```

### Test Coverage

```bash
# Install coverage tool
pip install coverage

# Run tests with coverage
coverage run --source='sims' manage.py test

# View coverage report
coverage report

# Generate HTML coverage report
coverage html
```

## Documentation

### Code Documentation

- Write clear docstrings for all classes, methods, and functions
- Use Google-style or NumPy-style docstrings
- Include parameter types and return types
- Provide usage examples for complex functions

**Example:**

```python
def calculate_completion_percentage(completed, total):
    """
    Calculate the percentage of completed items.
    
    Args:
        completed (int): Number of completed items
        total (int): Total number of items
    
    Returns:
        float: Completion percentage (0-100)
    
    Raises:
        ValueError: If total is zero or negative
    
    Example:
        >>> calculate_completion_percentage(7, 10)
        70.0
    """
    if total <= 0:
        raise ValueError("Total must be positive")
    return (completed / total) * 100
```

### Project Documentation

- Update relevant documentation when adding features
- Keep README.md up to date
- Document API endpoints in docs/API.md
- Add troubleshooting steps for common issues

## Pull Request Process

### Before Submitting

1. **Test your changes**: Ensure all tests pass
2. **Format your code**: Run Black and Flake8
3. **Update documentation**: Reflect your changes in docs
4. **Commit all changes**: Make sure working directory is clean
5. **Rebase if needed**: Keep your branch up to date with main

```bash
# Update your branch with latest main
git fetch origin
git rebase origin/main

# If there are conflicts, resolve them and continue
git add .
git rebase --continue
```

### Creating Pull Request

1. Push your branch to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

2. Go to the original repository on GitHub
3. Click "New Pull Request"
4. Select your fork and branch
5. Fill in the PR template:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
Describe the tests you ran and how to reproduce them

## Checklist
- [ ] My code follows the code style of this project
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes

## Screenshots (if applicable)
Add screenshots to help explain your changes
```

### PR Review Process

- Maintainers will review your PR
- Address any comments or requested changes
- Keep the PR focused on a single issue/feature
- Be patient and respectful during review

### After PR is Merged

```bash
# Update your local main branch
git checkout main
git pull origin main

# Delete your feature branch (optional)
git branch -d feature/your-feature-name
```

## Issue Reporting

### Bug Reports

When reporting a bug, include:

1. **Description**: Clear description of the bug
2. **Steps to Reproduce**: Detailed steps to reproduce the issue
3. **Expected Behavior**: What you expected to happen
4. **Actual Behavior**: What actually happened
5. **Environment**: Python version, Django version, OS, browser
6. **Screenshots**: If applicable
7. **Error Messages**: Full error traceback

**Template:**

```markdown
**Bug Description**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected Behavior**
A clear and concise description of what you expected to happen.

**Actual Behavior**
What actually happened.

**Environment**
- OS: [e.g. Windows 10, macOS 12.0, Ubuntu 20.04]
- Python Version: [e.g. 3.11.2]
- Django Version: [e.g. 4.2.1]
- Browser: [e.g. Chrome 120, Firefox 115]

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Additional Context**
Add any other context about the problem here.
```

### Feature Requests

When requesting a feature:

1. **Use Case**: Explain why this feature is needed
2. **Description**: Detailed description of the feature
3. **Benefits**: Who will benefit and how
4. **Alternatives**: Alternative solutions considered
5. **Examples**: Examples from other applications

## Development Resources

### Useful Links

- [Django Documentation](https://docs.djangoproject.com/)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.0/)
- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Black Code Formatter](https://black.readthedocs.io/)
- [Flake8 Documentation](https://flake8.pycqa.org/)

### Project-Specific Resources

- [FEATURES_STATUS.md](FEATURES_STATUS.md) - Current feature status
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Project overview
- [SYSTEM_STATUS.md](SYSTEM_STATUS.md) - System status
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues

## Questions?

If you have questions:

1. Check existing documentation in `docs/` directory
2. Search for similar issues in the issue tracker
3. Ask in the issue or pull request
4. Contact the maintainers

---

**Thank you for contributing to SIMS!**

Your contributions help improve medical training management for institutions worldwide.
