# REMEDIATION PLAN

## 1. P1: Unsupported Django Framework
* **Finding ID:** PGSIMS-C-002
* **Target:** Upgrade `requirements.txt` from Django `4.2.x` to `5.2` (or current LTS).
* **Dependency:** Codebase compatibility checks.
* **Production Blocker:** YES.

## 2. P2: Disaster Backup Missing Directory
* **Finding ID:** PGSIMS-C-006
* **Target:** `backend/sims/backup_center/services.py`
* **Change:** Add `backup_dir.mkdir(parents=True, exist_ok=True)` before `zipfile.ZipFile` write.
* **Production Blocker:** YES.

## 3. P2: Frontend Build Dependencies
* **Finding ID:** PGSIMS-C-003
* **Target:** `package.json`
* **Change:** `npm audit fix` for build-chain tooling.

## 4. P3: Legacy Dummy Routes & Fields
* **Finding ID:** F-A-002, F-B-001
* **Target:** `sims_project.urls.py`, `User.supervisor` model definition.
* **Change:** Deprecate and remove safely.

## 5. P3: Technical Code Debt
* **Finding ID:** PGSIMS-C-004, PGSIMS-C-005, F-B-002
* **Target:** Broad sweep using `ruff --fix`, narrowing try/except blocks, removing hardcoded text in tests.
