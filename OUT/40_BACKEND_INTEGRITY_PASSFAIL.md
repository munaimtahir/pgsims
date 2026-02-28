# Backend Integrity PASS/FAIL Report

## Final Verdict: **PASS**

All requested integrity gates have evidence and currently pass under the active production compose stack.

## Gate Matrix
1. **Single deployment proof (Compose + Caddy + domain routing)**: PASS  
   Evidence: `OUT/41_DOCKER_DEPLOYMENT_SINGLE_SUITE_PROOF.md`, `OUT/compose_rendered.yml`, `OUT/docker_ps.txt`, `OUT/Caddyfile.active`, `OUT/caddy_validate.txt`, `OUT/curl_*_headers.txt`

2. **Backend health (check/migrations/tests/admin registry)**: PASS  
   Evidence: `OUT/42_MIGRATIONS_ADMIN_REGISTRY_PROOF.md`, `OUT/manage_check_final.txt`, `OUT/showmigrations_plan.txt`, `OUT/migrate_output.txt`, `OUT/test_failfast_final.txt`, `OUT/admin_registry_models.txt`

3. **Env integrity (non-blank secrets/runtime vars)**: PASS  
   Evidence: `OUT/backend_logs_tail.txt`, `OUT/runtime_env_check.txt`, `OUT/env_integrity_context.txt`

4. **API smoke (unauth + auth + key endpoints)**: PASS  
   Evidence: `OUT/43_API_SMOKE_PROOF.md`, login/token files, endpoint headers/bodies in `OUT/`

5. **Jobs drift + schema export**: PASS  
   Evidence: `OUT/44_JOBS_SCHEMA_PROOF.md`, `OUT/periodic_tasks_disable.txt`, `OUT/openapi.json`

## Notes
- `/api/` root returns 404, but key API endpoints are reachable and authenticated requests pass.
- Compose emits a non-blocking warning about obsolete `version` field in compose YAML.
