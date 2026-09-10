# Backend Verification Audit

## Tests
- **Command:** `pytest --tb=short`
- **Exit Status:** 1 (FAILED)
- **Results:**
  - 1202 passed
  - 8 skipped
  - 1 failed
  - 11 subtests passed
  - **Coverage:** 82.23% (Target 70% reached)
  - **Duration:** 278.66s
  - **Failed Test:** `sims/backup_center/tests.py::TestBackupCenterServices::test_create_disaster_backup`

## Static Analysis (Lint/Formatting)
- **Command:** `ruff check .`
- **Exit Status:** 1 (FAILED)
- **Results:** 234 errors found (153 autofixable). Issues consist mostly of unused imports, multiple statements on one line (E701), redefined unused modules, and some unused local imports.

## Type Checking
- No explicit `mypy` or `pyright` script was found in the CI configuration or `requirements.txt` specifically for full project type checking, though Python 3 types are used in the source code.
