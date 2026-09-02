# UI Smoke Results

## Verified Routes

The smoke test logged in as the preserved admin account and verified these routes rendered without crashing:

- `/dashboard/utrmc`
- `/dashboard/utrmc/hospitals`
- `/dashboard/utrmc/departments`
- `/dashboard/utrmc/users`
- `/dashboard/utrmc/matrix`
- `/dashboard/utrmc/hod`
- `/dashboard/utrmc/programs`
- `/dashboard/utrmc/eligibility-monitoring`

## Login Path

- Auth endpoint: `http://127.0.0.1:8014/api/auth/login/`
- Credentials used in live smoke: `admin / admin123`

## Notes

- The project currently uses the route names `programs` and `eligibility-monitoring`.
- The smoke test validated the real live routes present in the application.

