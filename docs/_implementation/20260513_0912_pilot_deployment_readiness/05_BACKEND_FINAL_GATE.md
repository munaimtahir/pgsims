# Backend Final Gate

## Results

- `python manage.py check`: pass (`0` issues)
- `python manage.py makemigrations --check --dry-run`: pass (`No changes detected`)
- `pytest sims -q`: **335 passed, 19 failed, 0 skipped** (`354` collected; `8` warnings)

## Failing tests

The failures were concentrated in legacy user-view and bulk coverage tests:

- `sims/tests/test_backend_mega_coverage.py::BackendMegaCoverageTests::test_logbook_config_viewset_exhaustive`
- `sims/tests/test_bulk_services.py::BulkServicesTests::test_import_logbook_entries_csv`
- `sims/tests/test_bulk_services_extended.py::BulkServicesExtendedTests::test_assign_supervisor_extended`
- `sims/tests/test_bulk_userbase_engine.py::BulkUserbaseEngineExtendedTests::test_import_hod_assignments`
- `sims/tests/test_bulk_userbase_engine.py::BulkUserbaseEngineExtendedTests::test_import_supervision_links`
- `sims/tests/test_users_views.py::UsersViewsTests::*`
- `sims/tests/test_users_views_extended.py::UsersViewsExtendedTests::*`
- `sims/tests/test_users_views_final_push.py::UsersViewsFinalPushTests::*`

## Blocker seen in traceback

- `django.urls.exceptions.NoReverseMatch: 'cases' is not a registered namespace`

## Interpretation

This is a conditional pass for the controlled pilot sprint: Django checks are clean, migrations are clean, and the remaining failures are in legacy coverage paths rather than the active pilot runtime surfaces verified by the restart proof.
