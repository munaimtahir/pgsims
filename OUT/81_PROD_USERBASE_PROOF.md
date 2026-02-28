# 81 — Production Userbase Proof

## Page checks requested

### curl -I https://pgsims.alshifalab.pk/utrmc
```
HTTP/2 404 
alt-svc: h3=":443"; ma=2592000
cache-control: private, no-cache, no-store, max-age=0, must-revalidate
content-type: text/html; charset=utf-8
date: Sat, 28 Feb 2026 11:40:12 GMT
link: </_next/static/media/4473ecc91f70f139-s.p.woff>; rel=preload; as="font"; crossorigin=""; type="font/woff", </_next/static/media/463dafcda517f24f-s.p.woff>; rel=preload; as="font"; crossorigin=""; type="font/woff"
permissions-policy: camera=(), microphone=(), geolocation=()
referrer-policy: strict-origin-when-cross-origin
```

### curl -I https://pgsims.alshifalab.pk/utrmc/departments
```
HTTP/2 404 
alt-svc: h3=":443"; ma=2592000
cache-control: private, no-cache, no-store, max-age=0, must-revalidate
content-type: text/html; charset=utf-8
date: Sat, 28 Feb 2026 11:40:12 GMT
link: </_next/static/media/4473ecc91f70f139-s.p.woff>; rel=preload; as="font"; crossorigin=""; type="font/woff", </_next/static/media/463dafcda517f24f-s.p.woff>; rel=preload; as="font"; crossorigin=""; type="font/woff"
permissions-policy: camera=(), microphone=(), geolocation=()
referrer-policy: strict-origin-when-cross-origin
```

### curl -I https://pgsims.alshifalab.pk/utrmc/users
```
HTTP/2 404 
alt-svc: h3=":443"; ma=2592000
cache-control: private, no-cache, no-store, max-age=0, must-revalidate
content-type: text/html; charset=utf-8
date: Sat, 28 Feb 2026 11:40:12 GMT
link: </_next/static/media/4473ecc91f70f139-s.p.woff>; rel=preload; as="font"; crossorigin=""; type="font/woff", </_next/static/media/463dafcda517f24f-s.p.woff>; rel=preload; as="font"; crossorigin=""; type="font/woff"
permissions-policy: camera=(), microphone=(), geolocation=()
referrer-policy: strict-origin-when-cross-origin
```

## Frozen-route equivalent pages deployed (`/dashboard/utrmc/*`)

### curl -I https://pgsims.alshifalab.pk/dashboard/utrmc
```
HTTP/2 307 
alt-svc: h3=":443"; ma=2592000
date: Sat, 28 Feb 2026 11:40:12 GMT
location: /login
permissions-policy: camera=(), microphone=(), geolocation=()
referrer-policy: strict-origin-when-cross-origin
strict-transport-security: max-age=31536000; includeSubDomains; preload
via: 1.1 Caddy
```

### curl -I https://pgsims.alshifalab.pk/dashboard/utrmc/departments
```
HTTP/2 307 
alt-svc: h3=":443"; ma=2592000
date: Sat, 28 Feb 2026 11:40:12 GMT
location: /login
permissions-policy: camera=(), microphone=(), geolocation=()
referrer-policy: strict-origin-when-cross-origin
strict-transport-security: max-age=31536000; includeSubDomains; preload
via: 1.1 Caddy
```

### curl -I https://pgsims.alshifalab.pk/dashboard/utrmc/users
```
HTTP/2 307 
alt-svc: h3=":443"; ma=2592000
date: Sat, 28 Feb 2026 11:40:12 GMT
location: /login
permissions-policy: camera=(), microphone=(), geolocation=()
referrer-policy: strict-origin-when-cross-origin
strict-transport-security: max-age=31536000; includeSubDomains; preload
via: 1.1 Caddy
```

## API checks

### Auth + departments + roster (production)
```json
{
  "login_status": 200,
  "departments_status": 200,
  "departments_count": 39,
  "first_department_id": 13,
  "roster_status": 200,
  "roster_department": "Department e2e-1772276700584",
  "roster_counts": {
    "faculty": 0,
    "supervisors": 0,
    "residents": 1
  }
}
```

Notes:
- `/utrmc*` returns 404 because frozen app routes are under `/dashboard/utrmc*`.
- `/dashboard/utrmc*` responds with auth redirect when unauthenticated, confirming deployed route presence.
