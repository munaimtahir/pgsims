# SIMS Development Guidelines

This document provides comprehensive guidelines for developing and maintaining the SIMS (Surgical Information Management System) project.

## Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Code Organization](#code-organization)
- [Coding Standards](#coding-standards)
- [Database Guidelines](#database-guidelines)
- [Frontend Development](#frontend-development)
- [API Development](#api-development)
- [Security Best Practices](#security-best-practices)
- [Performance Guidelines](#performance-guidelines)
- [Testing Strategy](#testing-strategy)
- [Documentation Standards](#documentation-standards)
- [Version Control](#version-control)
- [Deployment Process](#deployment-process)

## Project Overview

SIMS is a Django-based web application designed for managing postgraduate medical training programs. The system supports three primary user roles (Admin, Supervisor, Postgraduate) and provides modules for user management, rotations, certificates, logbook, and clinical cases.

**Tech Stack:**
- Backend: Django 4.2+
- Database: SQLite (development), PostgreSQL (production)
- Frontend: Bootstrap 5, JavaScript, jQuery
- Python: 3.11+

## Architecture

### Design Patterns

The application follows these architectural patterns:

1. **MVT Pattern** (Model-View-Template)
   - Models define database structure
   - Views handle business logic
   - Templates render the UI

2. **Class-Based Views** (CBVs)
   - Preferred over function-based views for CRUD operations
   - Use Django's generic views (ListView, DetailView, CreateView, etc.)
   - Override methods to customize behavior

3. **Role-Based Access Control** (RBAC)
   - Custom mixins for permission checking
   - Decorators for function-based views
   - Permissions enforced at view and template levels

### Application Structure

```
sims/
├── users/          # User management and authentication
├── cases/          # Clinical case management
├── logbook/        # Digital logbook
├── certificates/   # Certificate tracking
└── rotations/      # Rotation scheduling
```

Each app follows Django's standard structure:
- `models.py` - Data models
- `views.py` - View logic
- `urls.py` - URL routing
- `forms.py` - Form definitions
- `admin.py` - Admin configuration
- `tests.py` - Unit tests

## Code Organization

### File Structure

```python
# models.py
from django.db import models

class MyModel(models.Model):
    """Model docstring"""
    # Fields
    name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = "My Model"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    # Custom methods
    def custom_method(self):
        """Method docstring"""
        pass
```

```python
# views.py
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import MyModel

class MyModelListView(LoginRequiredMixin, ListView):
    """List view for MyModel"""
    model = MyModel
    template_name = 'app/mymodel_list.html'
    context_object_name = 'items'
    paginate_by = 25
    
    def get_queryset(self):
        """Customize queryset"""
        return super().get_queryset().select_related('related_field')
    
    def get_context_data(self, **kwargs):
        """Add extra context"""
        context = super().get_context_data(**kwargs)
        context['extra_data'] = 'value'
        return context
```

### Import Organization

Order imports as follows:

```python
# Standard library imports
import json
from datetime import datetime, timedelta

# Django imports
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

# Third-party imports
from crispy_forms.helper import FormHelper

# Local imports
from .models import MyModel
from .forms import MyForm
```

## Coding Standards

### Python Style Guide

Follow PEP 8 with these specifics:

1. **Line Length**: 100 characters maximum
2. **Indentation**: 4 spaces (no tabs)
3. **Naming Conventions**:
   - Classes: `PascalCase`
   - Functions/Variables: `snake_case`
   - Constants: `UPPER_SNAKE_CASE`
   - Private: `_leading_underscore`

4. **Docstrings**: Use for all classes and functions

```python
def calculate_percentage(numerator, denominator):
    """
    Calculate percentage from numerator and denominator.
    
    Args:
        numerator (int): The numerator value
        denominator (int): The denominator value
        
    Returns:
        float: Percentage value (0-100)
        
    Raises:
        ValueError: If denominator is zero
    """
    if denominator == 0:
        raise ValueError("Denominator cannot be zero")
    return (numerator / denominator) * 100
```

### Django Best Practices

1. **Use QuerySet Methods**
   ```python
   # Good
   users = User.objects.filter(role='pg').select_related('supervisor')
   
   # Bad
   users = User.objects.all()
   for user in users:
       if user.role == 'pg':
           supervisor = user.supervisor  # N+1 query problem
   ```

2. **Avoid Raw SQL**
   ```python
   # Good
   User.objects.filter(role='pg', is_active=True)
   
   # Bad
   User.objects.raw("SELECT * FROM users WHERE role='pg' AND is_active=1")
   ```

3. **Use Django Forms**
   ```python
   # Good
   form = UserProfileForm(request.POST, instance=user)
   if form.is_valid():
       form.save()
   
   # Bad
   user.name = request.POST.get('name')
   user.save()  # No validation
   ```

### Code Formatting

Use Black for automatic formatting:

```bash
# Format specific file
black sims/users/views.py

# Format entire directory
black sims/ --line-length 100

# Check without modifying
black sims/ --check
```

Use Flake8 for linting:

```bash
# Check entire project
flake8 sims/ --count --statistics

# Check specific file
flake8 sims/users/views.py
```

## Database Guidelines

### Model Design

1. **Use Appropriate Field Types**
   ```python
   class Rotation(models.Model):
       pg = models.ForeignKey(User, on_delete=models.CASCADE)
       start_date = models.DateField()  # Not CharField
       duration = models.IntegerField()  # Not CharField
       is_active = models.BooleanField(default=True)  # Not CharField
   ```

2. **Add Indexes**
   ```python
   class LogbookEntry(models.Model):
       pg = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
       created_at = models.DateTimeField(auto_now_add=True, db_index=True)
       
       class Meta:
           indexes = [
               models.Index(fields=['pg', '-created_at']),
           ]
   ```

3. **Use Constraints**
   ```python
   class Certificate(models.Model):
       name = models.CharField(max_length=200, unique=True)
       
       class Meta:
           constraints = [
               models.CheckConstraint(
                   check=models.Q(expiry_date__gte=models.F('issue_date')),
                   name='expiry_after_issue'
               )
           ]
   ```

### Migrations

1. **Create Meaningful Migrations**
   ```bash
   # Good
   python manage.py makemigrations --name add_expiry_date_to_certificate
   
   # Bad
   python manage.py makemigrations
   ```

2. **Test Migrations**
   ```bash
   # Test forward migration
   python manage.py migrate
   
   # Test rollback
   python manage.py migrate app_name previous_migration_name
   ```

3. **Never Edit Old Migrations** (unless absolutely necessary)

### Query Optimization

1. **Use select_related() for Foreign Keys**
   ```python
   # Good - Single query
   entries = LogbookEntry.objects.select_related('pg', 'supervisor')
   
   # Bad - N+1 queries
   entries = LogbookEntry.objects.all()
   ```

2. **Use prefetch_related() for Many-to-Many**
   ```python
   # Good
   users = User.objects.prefetch_related('assigned_pgs')
   
   # Bad
   users = User.objects.all()
   ```

3. **Use only() and defer()**
   ```python
   # Fetch only needed fields
   users = User.objects.only('username', 'email', 'role')
   
   # Defer large fields
   users = User.objects.defer('bio', 'profile_picture')
   ```

## Frontend Development

### Template Organization

```django
{# templates/app/model_list.html #}
{% extends "base/base.html" %}
{% load static %}

{% block title %}Model List{% endblock %}

{% block extra_css %}
<link rel="stylesheet" href="{% static 'css/custom.css' %}">
{% endblock %}

{% block content %}
<div class="container">
    <h1>Model List</h1>
    <!-- Content here -->
</div>
{% endblock %}

{% block extra_js %}
<script src="{% static 'js/custom.js' %}"></script>
{% endblock %}
```

### Bootstrap 5 Usage

1. **Use Bootstrap Classes**
   ```html
   <!-- Good -->
   <div class="container">
       <div class="row">
           <div class="col-md-6">Content</div>
       </div>
   </div>
   
   <!-- Bad - Custom CSS for layout -->
   <div style="width: 80%; margin: auto;">
       <div style="float: left; width: 50%;">Content</div>
   </div>
   ```

2. **Responsive Design**
   ```html
   <div class="d-none d-md-block">Desktop only</div>
   <div class="d-block d-md-none">Mobile only</div>
   ```

### JavaScript Guidelines

1. **Use jQuery Sparingly**
   ```javascript
   // Modern approach with vanilla JS
   document.getElementById('myButton').addEventListener('click', function() {
       // Handle click
   });
   
   // jQuery only when necessary
   $('#mySelect').select2({
       // Select2 plugin
   });
   ```

2. **Organize JavaScript**
   ```javascript
   // static/js/logbook.js
   (function() {
       'use strict';
       
       // Module-level variables
       const API_URL = '/api/logbook/';
       
       // Initialize on DOM ready
       document.addEventListener('DOMContentLoaded', function() {
           initializeForm();
           attachEventHandlers();
       });
       
       function initializeForm() {
           // Initialization code
       }
       
       function attachEventHandlers() {
           // Event handlers
       }
   })();
   ```

## API Development

### RESTful API Guidelines

1. **URL Structure**
   ```python
   # Good
   path('api/users/', views.user_list, name='api_user_list')
   path('api/users/<int:pk>/', views.user_detail, name='api_user_detail')
   
   # Bad
   path('get-users/', views.get_users)
   path('user-by-id/<int:id>/', views.get_user_by_id)
   ```

2. **Response Format**
   ```python
   # Success response
   return JsonResponse({
       'status': 'success',
       'data': {
           'users': user_list,
           'total': count
       }
   })
   
   # Error response
   return JsonResponse({
       'status': 'error',
       'message': 'User not found',
       'code': 'USER_NOT_FOUND'
   }, status=404)
   ```

3. **Use HTTP Methods Correctly**
   - GET: Retrieve data
   - POST: Create new resource
   - PUT/PATCH: Update resource
   - DELETE: Delete resource

## Security Best Practices

### Authentication & Authorization

1. **Always Check Permissions**
   ```python
   @login_required
   @role_required('admin')
   def admin_view(request):
       # Only accessible by admins
       pass
   ```

2. **Use CSRF Protection**
   ```html
   <form method="post">
       {% csrf_token %}
       <!-- form fields -->
   </form>
   ```

3. **Validate User Input**
   ```python
   # Use Django forms for validation
   form = MyForm(request.POST)
   if form.is_valid():
       data = form.cleaned_data
   ```

### Data Protection

1. **Never Store Passwords in Plain Text**
   ```python
   # Good - Django handles hashing
   user.set_password('password')
   
   # Bad
   user.password = 'password'
   ```

2. **Sanitize User Input**
   ```python
   from django.utils.html import escape
   
   safe_input = escape(user_input)
   ```

3. **Use Environment Variables**
   ```python
   import os
   
   SECRET_KEY = os.environ.get('SECRET_KEY')
   DEBUG = os.environ.get('DEBUG', 'False') == 'True'
   ```

## Performance Guidelines

### Caching

1. **Cache Expensive Operations**
   ```python
   from django.core.cache import cache
   
   def get_statistics():
       stats = cache.get('dashboard_stats')
       if stats is None:
           stats = calculate_statistics()  # Expensive operation
           cache.set('dashboard_stats', stats, 300)  # Cache for 5 minutes
       return stats
   ```

2. **Use Template Fragment Caching**
   ```django
   {% load cache %}
   {% cache 500 sidebar request.user.username %}
       <!-- Expensive template code -->
   {% endcache %}
   ```

### Database Optimization

1. **Use Database Aggregation**
   ```python
   from django.db.models import Count, Avg
   
   # Good
   stats = User.objects.filter(role='pg').aggregate(
       total=Count('id'),
       avg_entries=Avg('logbookentry__id')
   )
   
   # Bad
   users = User.objects.filter(role='pg')
   total = len(users)
   avg_entries = sum(u.logbookentry_set.count() for u in users) / total
   ```

2. **Paginate Large Result Sets**
   ```python
   from django.core.paginator import Paginator
   
   paginator = Paginator(object_list, 25)  # 25 items per page
   page_obj = paginator.get_page(page_number)
   ```

## Testing Strategy

### Test Structure

```python
from django.test import TestCase, Client
from django.contrib.auth import get_user_model

User = get_user_model()

class UserViewsTestCase(TestCase):
    """Test cases for user views"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_login_view(self):
        """Test user can login"""
        response = self.client.post('/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)
    
    def tearDown(self):
        """Clean up after tests"""
        self.user.delete()
```

### Test Coverage Goals

- **Critical Features**: 90%+ coverage
- **Business Logic**: 80%+ coverage
- **Views**: 70%+ coverage
- **Models**: 80%+ coverage

## Documentation Standards

### Code Comments

```python
# Use comments for complex logic
def complex_calculation(data):
    # Convert data to normalized form (0-1 range)
    normalized = [(x - min(data)) / (max(data) - min(data)) for x in data]
    
    # Apply weighted average with exponential decay
    weights = [0.9 ** i for i in range(len(normalized))]
    result = sum(n * w for n, w in zip(normalized, weights))
    
    return result
```

### Docstrings

```python
class UserManager:
    """
    Custom manager for User model.
    
    Provides methods for creating users and handling user queries.
    """
    
    def create_pg_user(self, username, email, supervisor, **kwargs):
        """
        Create a new postgraduate user.
        
        Args:
            username (str): The username for the new user
            email (str): The email address
            supervisor (User): The assigned supervisor
            **kwargs: Additional user fields
            
        Returns:
            User: The created user instance
            
        Raises:
            ValidationError: If supervisor is not a valid supervisor
        """
        # Implementation
        pass
```

## Version Control

### Git Workflow

1. **Branch Naming**
   - `feature/feature-name` - New features
   - `fix/bug-description` - Bug fixes
   - `docs/update-name` - Documentation
   - `refactor/component-name` - Refactoring

2. **Commit Messages**
   ```
   feat(logbook): add bulk entry creation
   
   - Add form for bulk entry creation
   - Implement validation for bulk data
   - Add tests for bulk creation
   
   Closes #123
   ```

3. **Pull Request Guidelines**
   - Keep PRs focused and small
   - Write clear descriptions
   - Link related issues
   - Request reviews from maintainers

## Deployment Process

### Pre-Deployment Checklist

- [ ] All tests pass
- [ ] Code formatted with Black
- [ ] Flake8 checks pass
- [ ] Migrations created and tested
- [ ] Documentation updated
- [ ] Environment variables configured
- [ ] Static files collected
- [ ] Database backup created

### Deployment Steps

1. **Update Code**
   ```bash
   git pull origin main
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

4. **Collect Static Files**
   ```bash
   python manage.py collectstatic --noinput
   ```

5. **Restart Application Server**
   ```bash
   sudo systemctl restart gunicorn
   ```

---

**These guidelines should be followed by all contributors to maintain code quality and consistency.**

For questions or clarifications, please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) document or contact the maintainers.
