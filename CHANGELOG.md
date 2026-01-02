# Changelog

All notable changes to the SIMS project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Analytics app to INSTALLED_APPS for API analytics endpoints
- Bulk operations app to INSTALLED_APPS
- Notifications app to INSTALLED_APPS
- Reports app to INSTALLED_APPS
- API routing for analytics at `/api/analytics/`
- Comprehensive Stage 1 completion status documentation
- Factory fixtures for all major models (User, Case, Logbook, etc.)

### Changed
- Improved test pass rate from 54% to 71% (+36 passing tests)
- Formatted all Python code with Black (113 files)
- Organized all imports with isort
- Updated test fixtures to include all required model fields
- Removed hardcoded username assertions in favor of flexible matching

### Fixed
- Analytics API URL routing (analytics_api namespace)
- Missing apps in INSTALLED_APPS causing module errors
- Problematic database CHECK constraints with dynamic dates
- CaseViewsTest setUp missing required fields
- CaseFormsTest setUp missing pg user
- Duplicate imports in logbook/models.py
- Import ordering across all modules
- Date validation constraint in LogbookEntry model
- Date validation constraint in ClinicalCase model

### Removed
- Database CHECK constraint `logbook_entry_date_not_future` (handled in clean() instead)
- Database CHECK constraint `case_date_not_future` (handled in clean() instead)
- Unused imports from audit, notifications, and reports modules

### Technical Debt
- 55 test failures/errors remaining (target: 0)
- Test coverage at 43% (target: 80%+)
- Need to implement review status update signals
- Need to fix form validation logic
- Need to add more view and integration tests

## [1.0.0] - 2025-06-25

### Initial Release
- User management with role-based access control
- Clinical cases submission and review system
- Digital logbook with entries and reviews
- Certificate management and tracking
- Rotation scheduling and management
- Comprehensive admin interface
- RESTful API endpoints
- Search functionality
- Audit trail system

---

## Categories
- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security improvements
- **Technical Debt**: Known issues to address
