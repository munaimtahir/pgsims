# Known Issues (This Run)

1. `/healthz/` returned `405` instead of required `200` in both local and external checks.
   - Evidence:
     - `/srv/apps/pgsims/OUT/RELEASE_LOCK/evidence/01_curl_backend_healthz_local.txt`
     - `/srv/apps/pgsims/OUT/RELEASE_LOCK/evidence/01_curl_https_healthz.txt`

2. Backend test verification failed in non-interactive mode due existing test DB and confirmation prompt EOF.
   - Evidence:
     - `/srv/apps/pgsims/OUT/RELEASE_LOCK/evidence/02_backend_tests_verify.txt`

3. Compose warning indicates obsolete top-level `version` key and missing env vars when compose is invoked without explicit env file.
   - Evidence:
     - `/srv/apps/pgsims/OUT/RELEASE_LOCK/evidence/01_compose_ps.txt` (captured command context)
     - `/srv/apps/pgsims/OUT/RELEASE_LOCK/evidence/01_compose_logs_tail.txt`

4. Caddy journal includes historical upstream refusal and prior log permission noise.
   - Evidence:
     - `/srv/apps/pgsims/OUT/RELEASE_LOCK/evidence/01_caddy_journal_tail.txt`
