# API Smoke Proof

## Baseline API Root (unauthenticated)
- Command: `curl -sS -D OUT/api_root_unauth_headers.txt -o OUT/api_root_unauth_body.txt https://pgsims.alshifalab.pk/api/`
- HTTP status: **404**
- Body snippet: `<!doctype html> <html lang="en"> <head>   <title>Not Found</title> </head> <body>   <h1>Not Found</h1><p>The requested resource was not found on this server.</p> </body> </html>`

## Auth Baseline (JWT login)
- `POST /api/auth/login/` (PG) HTTP: **200**
- `POST /api/auth/login/` (Supervisor) HTTP: **200**
- Evidence: `OUT/auth_login_pg_headers.txt`, `OUT/auth_login_pg_body.json`, `OUT/auth_login_sup_headers.txt`, `OUT/auth_login_sup_body.json`

## Authenticated Key Endpoints
1. `GET /api/logbook/my/` with PG token
   - HTTP: **200**
   - Body snippet: `{"count":1,"next":null,"previous":null,"results":[{"id":282,"case_title":"Integrity Smoke Case","date":"2026-02-28","location_of_activity":"Ward","patient_history_summary":"History","management_action":"Action","topic_su...`
2. `GET /api/logbook/pending/` with supervisor token
   - HTTP: **200**
   - Body snippet: `{"count":1,"results":[{"id":282,"case_title":"Integrity Smoke Case","date":"2026-02-28","user":{"id":43,"username":"integrity_pg","full_name":"Integrity PG"},"rotation":{"id":null,"department":null},"submitted_at":"2026-...`
3. `GET /api/notifications/unread-count/` with PG token
   - HTTP: **200**
   - Body snippet: `{"unread":0}`

## Seed Data Used
- `OUT/api_smoke_seed.txt`
- Users: `integrity_pg` (pg), `integrity_sup` (supervisor)
