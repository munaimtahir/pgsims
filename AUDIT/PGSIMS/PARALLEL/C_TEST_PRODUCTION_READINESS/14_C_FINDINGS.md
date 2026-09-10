# Session C Findings

## Finding PGSIMS-C-001
- **Severity:** FALSE_POSITIVE
- **Area:** Frontend Tooling & Testing
- **Description:** Audit environment initially used non-canonical dependency installation (`npm i --legacy-peer-deps`), which corrupted the test dependency tree. A canonical `npm ci` cleanly restores dependencies and passes all typechecks and unit tests.
- **Evidence:** `npm ci` followed by `npm run test` executes 243 passing tests successfully.
- **Status:** CLOSED

## Finding PGSIMS-C-002
- **Severity:** P1 High
- **Area:** Backend Dependencies
- **Description:** Django 4.2 security support ended in April 2026. PGSIMS remains pinned to Django 4.2.30 and therefore depends on an unsupported core framework branch that no longer receives security updates. Note: `pip-audit` flags 7 specific CVE advisories against this version, but these are scanner-only advisories not individually confirmed to be exploitable via the PGSIMS codebase configuration. The core risk is the unsupported framework status.
- **Evidence:** `pip-audit` scan. `requirements.txt` hardcodes `<5.0`.
- **Reproduction/command:** `pip-audit`
- **Impact:** Framework vulnerabilities will no longer be patched by the Django team.
- **Recommended correction:** Migrate to a currently supported Django release (e.g. 5.2 or 6.0) following compatibility testing.
- **Status:** OPEN

## Finding PGSIMS-C-003
- **Severity:** P2 Medium
- **Area:** Frontend Dependencies
- **Description:** 20 npm vulnerabilities exist in the frontend project (1 Critical, 14 High), largely in Next.js build-chain dev dependencies.
- **Evidence:** `npm audit` returned 20 vulnerabilities requiring force upgrades.
- **Reproduction/command:** `npm audit` in the `frontend` folder.
- **Impact:** Build chain or development server vulnerabilities. Lower runtime risk because the Next.js standalone server does not expose these build dependencies at runtime.
- **Recommended correction:** Run `npm audit fix` and plan a major upgrade for `next`.
- **Status:** OPEN

## Finding PGSIMS-C-004
- **Severity:** P3 Low
- **Area:** Backend Static Code Quality
- **Description:** `ruff` found 234 linting errors (153 autofixable), primarily unused imports and E701 multiple statements on one line.
- **Evidence:** `ruff check .` output.
- **Reproduction/command:** `ruff check .` in `backend` directory.
- **Impact:** Technical debt. Does not cause runtime defects or indicate substantive correctness problems.
- **Recommended correction:** Run `ruff check --fix .` and manually format the remaining E701 errors.
- **Status:** OPEN

## Finding PGSIMS-C-005
- **Severity:** P3 Low
- **Area:** Failure Modes / Exception Handling
- **Description:** Broad exception catching (`except Exception:`) in `sims/users/userbase_views.py`.
- **Evidence:** Static inspection reveals multiple instances of generic catch blocks that could mask true 500 errors as generic 400 responses.
- **Reproduction/command:** `grep -i "except" backend/sims/users/userbase_views.py`
- **Impact:** Technical debt making runtime debugging more difficult.
- **Recommended correction:** Narrow exception catching to specifically expected classes.
- **Status:** OPEN

## Finding PGSIMS-C-006
- **Severity:** P2 Medium
- **Area:** Backend Testing
- **Description:** `FAILED sims/backup_center/tests.py::TestBackupCenterServices::test_create_disaster_backup`. The test fails deterministically with `FileNotFoundError` because the backup destination directory may not exist before the disaster ZIP is created.
- **Evidence:** Pytest trace outputs `FileNotFoundError: [Errno 2] No such file or directory: '/app/backend/backups/PGSIMS_DISASTER_BACKUP...pgsimsdr'`.
- **Reproduction/command:** `pytest sims/backup_center/tests.py -k test_create_disaster_backup`
- **Impact:** A real weakness where the disaster backup module assumes a pre-existing directory structure that might not exist in an ephemeral production mount.
- **Recommended correction:** Ensure the backup destination directory is reliably created via `os.makedirs(exist_ok=True)` prior to ZIP generation.
- **Status:** OPEN
