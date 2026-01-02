# Feature Flags

This document lists all feature flags in the SIMS application and their current status.

## Overview

Feature flags allow us to enable/disable features without code changes. They can be configured in `settings.py` or via environment variables.

## Configuration

Add to your `.env` file or environment:

```bash
# Feature Flags (set to 'True' or 'False')
FEATURE_ADVANCED_ANALYTICS=True
FEATURE_EMAIL_NOTIFICATIONS=True
FEATURE_IN_APP_NOTIFICATIONS=True
FEATURE_BULK_OPERATIONS=True
FEATURE_PDF_REPORTS=True
FEATURE_EXCEL_REPORTS=True
FEATURE_REPORT_SCHEDULING=True
FEATURE_GLOBAL_SEARCH=True
FEATURE_SEARCH_AUTOCOMPLETE=True
FEATURE_AUDIT_TRAIL=True
FEATURE_AUDIT_EXPORTS=True
FEATURE_DATA_VALIDATION=True
FEATURE_PERFORMANCE_MONITORING=True
FEATURE_REDIS_CACHE=True
```

## Feature Flags

### Module 1: Advanced Analytics

| Flag | Default | Description | Status |
|------|---------|-------------|--------|
| `FEATURE_ADVANCED_ANALYTICS` | `True` | Enable advanced analytics dashboards with trends and comparisons | 🟢 Enabled |

**Components**:
- 12-month trend analysis
- Cohort comparisons
- Department grouping
- Performance metrics
- Cached query results

**Dependencies**: Redis (optional, for caching)

---

### Module 2: Notifications

| Flag | Default | Description | Status |
|------|---------|-------------|--------|
| `FEATURE_EMAIL_NOTIFICATIONS` | `True` | Enable email notifications for events | 🟢 Enabled |
| `FEATURE_IN_APP_NOTIFICATIONS` | `True` | Enable in-app notification center | 🟢 Enabled |

**Components**:
- Email templates (TXT/HTML)
- In-app notification center
- User preferences
- Scheduled reminders via Celery

**Events**:
- New logbook entry
- Verification pending/done
- Rotation start/end
- Certificate expiry warnings

**Dependencies**: Celery, Redis, Email backend configuration

---

### Module 3: Bulk Operations

| Flag | Default | Description | Status |
|------|---------|-------------|--------|
| `FEATURE_BULK_OPERATIONS` | `True` | Enable bulk operations for assignments, reviews, imports | 🟢 Enabled |

**Components**:
- Chunked processing (200 records per batch)
- CSV import with validation
- Preview and dry-run mode
- Progress tracking UI
- Rollback on failure
- Retry mechanisms

**Dependencies**: Celery (for async processing)

---

### Module 4: Reporting

| Flag | Default | Description | Status |
|------|---------|-------------|--------|
| `FEATURE_PDF_REPORTS` | `True` | Enable PDF report generation | 🟢 Enabled |
| `FEATURE_EXCEL_REPORTS` | `True` | Enable Excel export with formatting | 🟢 Enabled |
| `FEATURE_REPORT_SCHEDULING` | `True` | Enable scheduled report generation | 🟢 Enabled |

**Components**:
- PDF generation (ReportLab)
- Excel export (openpyxl)
- Report templates
- Report builder UI
- Celery Beat scheduler
- Secure file delivery

**Dependencies**: ReportLab, openpyxl, Celery Beat

---

### Module 5: Global Search

| Flag | Default | Description | Status |
|------|---------|-------------|--------|
| `FEATURE_GLOBAL_SEARCH` | `True` | Enable cross-module search | 🟢 Enabled |
| `FEATURE_SEARCH_AUTOCOMPLETE` | `True` | Enable search autocomplete and suggestions | 🟢 Enabled |

**Components**:
- PostgreSQL full-text search
- Cross-module unified search
- RBAC-aware filtering
- Autocomplete for diagnoses/procedures
- Search history per user
- Keyboard navigation

**Dependencies**: PostgreSQL with FTS extensions, Redis (for caching)

---

### Module 6: Audit Trail

| Flag | Default | Description | Status |
|------|---------|-------------|--------|
| `FEATURE_AUDIT_TRAIL` | `True` | Enable audit trail and history tracking | 🟢 Enabled |
| `FEATURE_AUDIT_EXPORTS` | `True` | Enable audit log exports | 🟢 Enabled |

**Components**:
- django-simple-history integration
- Model versioning
- ActivityLog for non-CRUD events
- Audit UI with filtering
- Diff views
- CSV/PDF exports

**Dependencies**: django-simple-history

---

### Module 7: Data Validation

| Flag | Default | Description | Status |
|------|---------|-------------|--------|
| `FEATURE_DATA_VALIDATION` | `True` | Enable enhanced data validation | 🟢 Enabled |

**Components**:
- Cross-field validation rules
- Consistent error schema
- Server-side validators
- Client-side mirroring
- Localized error messages

**Dependencies**: None (core Django)

---

### Module 8: Performance

| Flag | Default | Description | Status |
|------|---------|-------------|--------|
| `FEATURE_PERFORMANCE_MONITORING` | `True` | Enable performance monitoring and metrics | 🟢 Enabled |
| `FEATURE_REDIS_CACHE` | `True` | Enable Redis caching for hot paths | 🟢 Enabled |

**Components**:
- Query optimization
- Database indexes
- Redis caching
- Asset optimization
- Performance benchmarks
- Cache-busting strategies

**Dependencies**: Redis

---

## Usage in Code

### Python (Settings)

```python
# In settings.py or a feature_flags.py module
import os

FEATURES = {
    'ADVANCED_ANALYTICS': os.getenv('FEATURE_ADVANCED_ANALYTICS', 'True') == 'True',
    'EMAIL_NOTIFICATIONS': os.getenv('FEATURE_EMAIL_NOTIFICATIONS', 'True') == 'True',
    'IN_APP_NOTIFICATIONS': os.getenv('FEATURE_IN_APP_NOTIFICATIONS', 'True') == 'True',
    'BULK_OPERATIONS': os.getenv('FEATURE_BULK_OPERATIONS', 'True') == 'True',
    'PDF_REPORTS': os.getenv('FEATURE_PDF_REPORTS', 'True') == 'True',
    'EXCEL_REPORTS': os.getenv('FEATURE_EXCEL_REPORTS', 'True') == 'True',
    'REPORT_SCHEDULING': os.getenv('FEATURE_REPORT_SCHEDULING', 'True') == 'True',
    'GLOBAL_SEARCH': os.getenv('FEATURE_GLOBAL_SEARCH', 'True') == 'True',
    'SEARCH_AUTOCOMPLETE': os.getenv('FEATURE_SEARCH_AUTOCOMPLETE', 'True') == 'True',
    'AUDIT_TRAIL': os.getenv('FEATURE_AUDIT_TRAIL', 'True') == 'True',
    'AUDIT_EXPORTS': os.getenv('FEATURE_AUDIT_EXPORTS', 'True') == 'True',
    'DATA_VALIDATION': os.getenv('FEATURE_DATA_VALIDATION', 'True') == 'True',
    'PERFORMANCE_MONITORING': os.getenv('FEATURE_PERFORMANCE_MONITORING', 'True') == 'True',
    'REDIS_CACHE': os.getenv('FEATURE_REDIS_CACHE', 'True') == 'True',
}
```

### Python (Views)

```python
from django.conf import settings

def my_view(request):
    if settings.FEATURES.get('GLOBAL_SEARCH'):
        # Show search feature
        pass
```

### Templates

```django
{% if settings.FEATURES.GLOBAL_SEARCH %}
    <div class="search-bar">...</div>
{% endif %}
```

---

## Migration Strategy

When deploying new features:

1. **Deploy with flag OFF**: Deploy code with feature flag disabled
2. **Test in staging**: Enable flag in staging environment, test thoroughly
3. **Gradual rollout**: Enable for subset of users first
4. **Monitor**: Check logs, performance, errors
5. **Full rollout**: Enable for all users
6. **Remove flag**: After feature is stable, remove flag from code

---

## Rollback Procedure

If a feature causes issues:

1. Set the feature flag to `False` in environment
2. Restart application servers
3. Monitor for recovery
4. Fix issues
5. Re-enable when ready

---

## Testing

Feature flags should be tested in both enabled and disabled states:

```python
from django.test import TestCase, override_settings

class MyFeatureTests(TestCase):
    @override_settings(FEATURES={'GLOBAL_SEARCH': True})
    def test_feature_enabled(self):
        # Test with feature on
        pass
    
    @override_settings(FEATURES={'GLOBAL_SEARCH': False})
    def test_feature_disabled(self):
        # Test with feature off
        pass
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-01-XX | Initial feature flags documentation |

---

## See Also

- [MIGRATION_NOTES.md](MIGRATION_NOTES.md) - Database migration notes
- [CHANGELOG.md](CHANGELOG.md) - Version history
- [.env.example](.env.example) - Environment variable examples
