# Login Verification

Date: 2026-06-26

## Django Auth Verification

Executed inside backend container with `authenticate(...)`:

```text
admin  True admin      True False /dashboard/utrmc
pgr001 True resident   True False /dashboard/resident
sup001 True supervisor True False /dashboard/supervisor
```

## Domain API Login Verification

All logins were tested through `https://pg.fmu.edu.pk/api/auth/login/`.
Tokens were returned and masked in evidence.

```text
admin/admin -> token response; role admin; full_name "Super Admin"
pgr001/pgfmu123 -> token response; role resident; full_name "Sample Resident"
sup001/pgfmu123 -> token response; role supervisor; full_name "Sample Supervisor"
```

## Dashboard Reachability

Unauthenticated dashboard route checks return `307 Location: /login`, which is expected for protected frontend routes:

```text
/dashboard/utrmc      -> 307 /login
/dashboard/resident   -> 307 /login
/dashboard/supervisor -> 307 /login
```

## Supervision Link Verification

Authenticated admin API check:

```text
GET /api/supervision-links/
active sample link:
  supervisor_user.username = sup001
  resident_user.username = pgr001
  department.code = MED
  active = true
```

Note: the list endpoint also returns inactive historical links. The active link is correct and visible.

