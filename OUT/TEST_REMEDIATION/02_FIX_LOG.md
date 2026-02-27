# Fix Log

## Fix Batch 1
### Change 1: Add missing test dependency to runtime
- File: `backend/requirements.txt`
- Change: added `factory-boy>=3.3`
- Reason: test factories import `factory`, but prod-compose test runtime installs only `requirements.txt`.

### Change 2: Prevent import-time side effects in ad-hoc script
- File: `backend/test_frontend_create.py`
- Changes:
  - Wrapped script body into `main()` and guarded with `if __name__ == "__main__":`
  - Switched supervisor creation to `create_user(..., password=...)` for model validity
- Reason: unittest discovery imported this file and executed logic not intended as a test module.

### Change 3: Make user search deterministic for short partial terms
- File: `backend/sims/search/services.py`
- Change: in `_search_users`, when PostgreSQL full-text yields no ranked rows, fallback to scoped `icontains` query.
- Reason: short query `"pg"` can miss under FTS ranking; tests and expected behavior require partial matches.

## Runtime/Environment Stabilization
- Rebuilt `web` image to apply dependency changes.
- Restored stack with explicit env binding for stability:
  - `docker compose --env-file /srv/apps/pgsims/.env -f docker/docker-compose.prod.yml up -d ...`

## Validation Runs
### Targeted rerun
- Command: `python manage.py test sims.cases.tests sims.certificates.tests sims.logbook.tests sims.tests.factories sims.search.tests.SearchServiceTests test_frontend_create -v 2`
- Output file: `02_targeted_after_fix1.txt`
- Result: `Ran 142 tests` / `OK`

### Full rerun
- Command: `python manage.py test -v 2`
- Output file: `03_FINAL_RUN.txt`
- Result: `Ran 280 tests` / `OK`
