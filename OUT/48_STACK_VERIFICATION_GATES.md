# Stack Verification Gates (post web->backend rewire)

## Django Gates
- manage.py check: `OUT/manage_check_after.txt`
- migrate --noinput: `OUT/migrate_after.txt`
- test --failfast: `OUT/tests_failfast_after.txt`
- admin registry: `OUT/admin_registry_after.txt`

## External Routing
- `/` status: **200** (`OUT/curl_root_after.txt`)
- `/admin/` status: **302** (`OUT/curl_admin_after.txt`)

## API Auth + Core Endpoint Smokes
- Login PG `/api/auth/login/`: **200**
- Login Supervisor `/api/auth/login/`: **200**
- `/api/logbook/my/`: **200**
- `/api/logbook/pending/`: **200**
- `/api/notifications/unread-count/`: **200**

## Token Handling
- PG token saved to `OUT/token.txt` (sensitive; not inlined)
- Supervisor token saved to `OUT/token_sup.txt` (sensitive; not inlined)
