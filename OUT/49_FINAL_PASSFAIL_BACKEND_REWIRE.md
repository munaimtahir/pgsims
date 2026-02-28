# Final PASS/FAIL — Backend Rewire (web -> backend)

## Verdict: **PASS**

## Gate Checks
- Backend service healthy in compose ps: **True** (`OUT/docker_ps_after.txt`)
- `manage.py check`: **True** (`OUT/manage_check_after.txt`)
- `manage.py migrate --noinput`: **True** (`OUT/migrate_after.txt`)
- `manage.py test --failfast`: **True** (`OUT/tests_failfast_after.txt`)
- Admin registry captured: **True** (`OUT/admin_registry_after.txt`)
- External route `/`: **200** (`OUT/curl_root_after.txt`)
- External route `/admin/`: **302** (`OUT/curl_admin_after.txt`)
- API login `/api/auth/login/`: **200** (`OUT/curl_login_headers.txt`)
- API `/api/logbook/my/`: **200** (`OUT/curl_logbook_my_headers.txt`)
- API `/api/logbook/pending/`: **200** (`OUT/curl_logbook_pending_headers.txt`)
- API `/api/notifications/unread-count/`: **200** (`OUT/curl_notifications_unread_headers.txt`)
- Strict `web` service/host references remaining: **0** (`OUT/rg_web_after.txt`)

## Notes
- Caddy upstream remained unchanged because active config uses localhost upstream targets, not Docker DNS names.
- No temporary `web` network alias was introduced.
