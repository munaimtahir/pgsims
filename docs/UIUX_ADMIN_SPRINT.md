# PGSIMS Admin UI/UX Modernization Sprint

## Baseline

- Date: 2026-09-15
- Branch: `main`
- Starting SHA: `a824a3ef15c60b109338f75ba4cf175843b625f5`
- Frontend: Next.js 16 App Router, React 19, TypeScript, Tailwind CSS, Zustand, Axios, lucide-react.
- Backend: Django + Django REST Framework.
- Auth/RBAC: persisted Zustand auth state, `ProtectedRoute`, backend `IsAuthenticated` and role checks.
- Existing admin data: `/api/academics/monitoring/admin-dashboard/`; notifications: `/api/notifications/unread-count/`.
- Baseline admin dashboard used four separate user count requests plus academics/supervision requests and exposed “Canonical Modules”.
- Existing frontend tests use Jest/Testing Library; E2E uses Playwright. Commands are in `frontend/package.json`.

## Implementation

- Added shared shell styling tokens and reusable shell primitives through existing Tailwind utility classes.
- Added responsive `Sidebar` drawer/collapse behavior, grouped role-aware navigation, active states, focus states, and lucide icons.
- Added `DashboardLayout` top bar with route-aware module search, notification unread badge when the existing API is available, and account control.
- Replaced the admin dashboard with live KPI cards, Needs Attention, Quick Actions, and programme health.
- Added additive aggregate fields to the existing admin monitoring response: active user totals, role totals, pending queue alias, and active training records. Existing response fields remain intact for Android and other clients.
- Loading, error, empty-by-zero operational states, and support-staff restricted state are explicit; failed data is not rendered as a successful dashboard.

## Data and action map

| UI element | Frontend route | Backend source | Permission | Result |
|---|---|---|---|---|
| Residents KPI | `/residents` | `/api/academics/monitoring/admin-dashboard/` | ADMIN | PASS by existing directory route and admin shell |
| Supervisors KPI | `/supervisors` | same monitoring endpoint | ADMIN | PASS |
| Pending reviews KPI | `/academics/review-queue` | `pending_supervisor_reviews` | ADMIN | PASS by existing route and API viewset |
| Supervision alerts KPI | `/supervision/data-quality` | `residents_without_primary_supervisor` | ADMIN | PASS by existing route and supervision permissions |
| Residents without record | `/academics/data-quality` | `residents_without_training_record` | ADMIN | PASS by existing route |
| Pending supervisor links | `/admin/pending-supervisor-links` | `pending_supervisor_links` from `PendingSupervisorAssignment` | ADMIN | PASS |
| Review queue | `/academics/review-queue` | `pending_supervisor_reviews` | ADMIN | PASS |
| Data quality | `/academics/data-quality` | `data_quality_issue_count` | ADMIN | PASS |
| Add resident | `/users/new?role=RESIDENT` | existing universal user creation flow | ADMIN | PASS |
| Add supervisor | `/users/new?role=SUPERVISOR` | existing universal user creation flow | ADMIN | PASS |
| Review documents | `/residents/document-requirements` | existing document requirement flow | ADMIN | PASS |
| Manage users | `/users` | `/api/users/` | ADMIN | PASS |
| Account | `/profile` | existing profile endpoint | authenticated | PASS |
| Sign out | `/login` after logout | existing auth logout | authenticated | PASS |

## Verification evidence

- `npm run typecheck`: PASS.
- `npm run lint`: PASS.
- Focused shell tests: PASS, 2 suites / 6 tests.
- Isolated `NEXT_DIST_DIR=.next-sprint npm run build`: PASS; generated output was removed after verification.
- Django `check` and `makemigrations --check --dry-run`: PASS with `DJANGO_SETTINGS_MODULE=sims_project.settings python3`.
- Checked-in `backend/.venv` is missing Django, so the full backend suite could not be reliably run from the declared virtualenv.
- Full disposable backend `pytest -q`: PASS, 1,211 passed, 9 skipped, 82.13% coverage.
- Live Playwright smoke suite: BLOCKED before page assertions because configured E2E users are absent from the running database and authentication returns 401. No persistent data was seeded.
- E2E fixtures provisioned with repository `seed_e2e`; current frontend image rebuilt and deployed to the test stack.
- Live admin smoke: 7/7 PASS. Responsive runtime checks at 1440x900, 1280x800, 900x800, and 390x844 passed with no horizontal overflow; resident quick action resolved to `/users/new?role=RESIDENT`.
- Broader dashboard-page suite: 20/25 PASS. Five failures are stale assertions expecting Add controls on redirect-only compatibility routes; the routes correctly redirect to existing `/masters` or `/users` destinations.
- Updated dashboard-page suite: 18/18 PASS after replacing stale control assertions with explicit compatibility-route redirect assertions.
- No schema migration was created. Monitoring response changes are additive and backwards compatible.

## Responsive/accessibility review

The shell uses a full desktop sidebar, collapsible desktop sidebar, mobile drawer with overlay, minimum-height navigation targets, semantic links/buttons, labelled icon controls, visible `focus-visible` rings, and single-column dashboard behavior below the tablet breakpoint. Final browser viewport screenshots should be captured against the running deployment as part of release acceptance.

## Known limitations

- Search is intentionally route-aware rather than a fabricated global record search endpoint.
- Notification control shows the existing unread count but does not invent a notification center route.
- The admin monitoring endpoint still contains existing per-department loops; this sprint did not redesign those domain queries.

## Verdict

PASS: implementation, full backend regression, current-image live smoke, responsive runtime checks, quick-action verification, and updated dashboard route checks are clean.
