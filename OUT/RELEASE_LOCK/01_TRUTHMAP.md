# TruthMap

## Blockers (First)
1. Backend/API health endpoint requirement not met.
   - Expected: `/healthz/` returns `200`
   - Actual: `405 Method Not Allowed` (both local and external)
   - Evidence:
     - `/srv/apps/pgsims/OUT/RELEASE_LOCK/evidence/01_curl_backend_healthz_local.txt`
     - `/srv/apps/pgsims/OUT/RELEASE_LOCK/evidence/01_curl_https_healthz.txt`
   - Snippet pointer:
     - grep pattern: `HTTP/1.1 405|HTTP/2 405`

2. Backend test verification failed in one-shot run.
   - Actual failure: `ProgrammingError: database "test_sims_db" already exists` followed by `EOFError` from interactive confirmation in non-interactive exec.
   - Evidence:
     - `/srv/apps/pgsims/OUT/RELEASE_LOCK/evidence/02_backend_tests_verify.txt`
   - Snippet pointer:
     - grep pattern: `ProgrammingError|EOFError|Creating test database`

## Confirmed Working
- Frontend root is healthy:
  - local `http://127.0.0.1:8082/` -> `200`
  - external `https://pgsims.alshifalab.pk/` -> `200`
  - Evidence:
    - `/srv/apps/pgsims/OUT/RELEASE_LOCK/evidence/01_curl_frontend_local.txt`
    - `/srv/apps/pgsims/OUT/RELEASE_LOCK/evidence/01_curl_https_root.txt`
- Docker runtime is up with expected core services and healthy statuses.
  - Evidence: `/srv/apps/pgsims/OUT/RELEASE_LOCK/evidence/01_compose_ps.txt`
- Caddy validates and is active.
  - Evidence:
    - `/srv/apps/pgsims/OUT/RELEASE_LOCK/evidence/01_caddy_validate.txt`
    - `/srv/apps/pgsims/OUT/RELEASE_LOCK/evidence/01_caddy_status.txt`

## What Changed In This Phase (Guardrails)
- No code guardrail changes were applied.
- Reason: fail-fast gate triggered in Phase 2 by backend test verification failure.
- Evidence: `/srv/apps/pgsims/OUT/RELEASE_LOCK/evidence/03_guardrails_skipped.txt`

## Additional Notes
- Caddy journal contains historical upstream refusal noise (`127.0.0.1:8014 connect: connection refused`) and prior log permission error records; these were observed but not remediated in this lock run.
- Evidence:
  - `/srv/apps/pgsims/OUT/RELEASE_LOCK/evidence/01_caddy_journal_tail.txt`
  - grep pattern: `permission denied|connect: connection refused|status":502`
