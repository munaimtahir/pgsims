# 01_TRUTHMAP

## High-level matrix
| Section | Check | Status | Severity |
|---|---|---|---|
| Proxy/Caddy | CADDY-01 | FAIL | major |
| Proxy/Caddy | CADDY-02 | PASS | info |
| Proxy/Caddy | CADDY-03 | PASS | info |
| Proxy/Caddy | CADDY-04 | WARN | major |
| Docker/Runtime | DOCKER-01 | PASS | info |
| Docker/Runtime | DOCKER-02 | FAIL | blocker |
| Docker/Runtime | DOCKER-03 | WARN | minor |
| Docker/Runtime | DOCKER-04 | SKIP | info |
| Backend/API | API-01 | PASS | info |
| Backend/API | API-02 | PASS | info |
| Backend/API | API-03 | PASS | info |
| Backend/API | API-04 | FAIL | major |
| Backend/API | API-05 | FAIL | minor |
| Backend/API | API-06 | FAIL | blocker |
| Auth/RBAC | AUTH-01 | PASS | info |
| Auth/RBAC | AUTH-02 | PASS | info |
| Auth/RBAC | AUTH-03 | FAIL | blocker |
| Auth/RBAC | AUTH-04 | PASS | info |
| Frontend/UI | FE-01 | PASS | info |
| Frontend/UI | FE-02 | WARN | minor |
| Frontend/UI | FE-03 | PASS | info |
| Frontend/UI | FE-04 | FAIL | major |
| Logbook Workflow | WF-01 | PASS | info |
| Logbook Workflow | WF-02 | PASS | info |
| Logbook Workflow | WF-03 | FAIL | major |
| Import/Export | IMEX-01 | PASS | info |
| Import/Export | IMEX-02 | FAIL | major |
| Import/Export | IMEX-03 | FAIL | major |
| Import/Export | IMEX-04 | SKIP | info |
| Analytics | AN-01 | PASS | info |
| Analytics | AN-02 | FAIL | major |
| Analytics | AN-03 | WARN | minor |
| Static/Media | SM-01 | PASS | info |
| Static/Media | SM-02 | WARN | minor |
| Static/Media | SM-03 | PASS | info |
| Tests/E2E | TEST-01 | PASS | info |
| Tests/E2E | TEST-02 | FAIL | major |
| Security Basics | SEC-01 | PASS | info |
| Security Basics | SEC-02 | FAIL | blocker |
| Security Basics | SEC-03 | PASS | info |
| Performance Smoke | PERF-01 | PASS | info |
| Performance Smoke | PERF-02 | FAIL | major |

## Blockers first
- **DOCKER-02** (Docker/Runtime): web container repeatedly restarts; final state shows Restarting (1).
  Evidence: evidence/Docker/11_compose_ps_final.txt, evidence/Docker/14_compose_ps_unstable.txt, evidence/Docker/13_compose_logs_unstable.txt
- **API-06** (Backend/API): Login endpoint intermittently returns 502 when backend restarts.
  Evidence: evidence/Auth/AUTH-login-admin.json, evidence/Docker/13_compose_logs_unstable.txt
- **AUTH-03** (Auth/RBAC): RBAC probes returned 502 during backend instability, preventing reliable authorization verification.
  Evidence: evidence/Auth/AUTH-rbac-admin.json, evidence/Auth/AUTH-rbac-pg.json, evidence/Docker/14_compose_ps_unstable.txt
- **SEC-02** (Security Basics): Compose warns SECRET_KEY/DB_PASSWORD unset; backend crashes with RuntimeError: SECRET_KEY environment variable is required.
  Evidence: evidence/Docker/04_compose_ps.txt, evidence/Docker/13_compose_logs_unstable.txt

## Major issues
- **CADDY-01** (Proxy/Caddy): caddy validate failed due permission denied opening /var/log/caddy/mediq.log.
  Evidence: evidence/Proxy/01_caddy_validate.txt
- **API-04** (Backend/API): Domain /api/healthz/ returns 404.
  Evidence: evidence/Backend/08_external_api_healthz_headers.txt, evidence/Backend/13_external_api_healthz_headers_final.txt
- **FE-04** (Frontend/UI): Same-origin API health returns 404.
  Evidence: evidence/Frontend/FE-03_same_origin_api_healthz.txt
- **WF-03** (Logbook Workflow): /api/audit/activity/ returned 403 for tested roles; transition audit entries could not be directly verified via API.
  Evidence: evidence/Workflow/04_workflow_full_attempt.json, evidence/Workflow/05_audit_activity_probe.json
- **IMEX-02** (Import/Export): /api/reports/export/logbook/?format=csv returned 404.
  Evidence: evidence/ImportExport/02_export_headers.txt
- **IMEX-03** (Import/Export): Role probes failed with 401 due failed/expired auth during probe window.
  Evidence: evidence/ImportExport/05_role_probes.json
- **AN-02** (Analytics): Probed analytics endpoints returned 401 in captured runs; prior RBAC probes also showed 500 on dashboard overview.
  Evidence: evidence/Analytics/02_endpoints_admin.json, evidence/Analytics/02_endpoints_pg.json
- **TEST-02** (Tests/E2E): 7/7 tests failed, mostly ECONNREFUSED to localhost:3000 and localhost:8000.
  Evidence: evidence/Tests/02_playwright_serial.txt
- **PERF-02** (Performance Smoke): /api/healthz returned 404 (timing captured but endpoint unhealthy).
  Evidence: evidence/Perf/03_api_healthz_timing.txt

## Minor issues
- **DOCKER-03** (Docker/Runtime): Expected listener 8082 present; 8014 intermittently missing when web restarts.
  Evidence: evidence/Docker/09_ss_tulpn.txt
- **API-05** (Backend/API): /api/schema/, /api/docs/, /api/openapi.json all return 404.
  Evidence: evidence/Backend/09_schema_headers.txt, evidence/Backend/10_docs_headers.txt, evidence/Backend/11_openapi_headers.txt
- **FE-02** (Frontend/UI): /dashboard/* routes return 307 redirect to /login when unauthenticated; authenticated UI route render not proven.
  Evidence: evidence/Frontend/FE-01_pages.txt
- **AN-03** (Analytics): Workflow actions succeeded, but direct analytics event count verification was not available through exposed endpoints.
  Evidence: evidence/Workflow/04_workflow_full_attempt.json, evidence/ImportExport/06_backend_logs_after_probe.txt
- **SM-02** (Static/Media): /media/ returned 404 (no index/object at root path).
  Evidence: evidence/StaticMedia/02_media_head.txt

## What is confirmed working
- CADDY-02 (Proxy/Caddy): systemd reports caddy active (running).
- CADDY-03 (Proxy/Caddy): Active and template pgsims.alshifalab.pk blocks both target 127.0.0.1:8014 and 127.0.0.1:8082.
- DOCKER-01 (Docker/Runtime): Compose file present and config resolved with warnings.
- API-01 (Backend/API): System check identified no issues during healthy window.
- API-02 (Backend/API): showmigrations --plan reports applied migrations.
- API-03 (Backend/API): /healthz/ returns HTTP 200.
- AUTH-01 (Auth/RBAC): seed_e2e command located with role usernames; passwords kept redacted in evidence.
- AUTH-02 (Auth/RBAC): All five roles received HTTP 200 in successful login sample.
- AUTH-04 (Auth/RBAC): Set-Cookie header absent in sampled JWT login responses.
- FE-01 (Frontend/UI): / and /login return 200.
- FE-03 (Frontend/UI): No localhost:8000 or 127.0.0.1:8014 hit in .next grep output.
- WF-01 (Logbook Workflow): draft/pending/returned/approved flow and verify/submit routes are present.
- WF-02 (Logbook Workflow): Workflow completed successfully with entry_id 281 and expected statuses.
- IMEX-01 (Import/Export): Bulk, reports, and module export/import surfaces discovered.
- AN-01 (Analytics): Analytics models, views, and routes are present in codebase.
- SM-01 (Static/Media): Sample static asset returned HTTP 200.
- SM-03 (Static/Media): staticfiles directory exists and compose includes static/media mounts.
- TEST-01 (Tests/E2E): Targeted backend truth test passed.
- SEC-01 (Security Basics): HSTS, X-Frame-Options, and X-Content-Type-Options present.
- SEC-03 (Security Basics): No Set-Cookie token observed across sampled logins.
- PERF-01 (Performance Smoke): Root ~0.125s, login ~0.011s in sampled curls.
