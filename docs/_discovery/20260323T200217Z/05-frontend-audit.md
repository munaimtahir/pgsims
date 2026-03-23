# Frontend Audit

## Page and navigation inventory

App Router areas found:

- Public: `/`, `/login`, `/register`, `/forgot-password`, `/unauthorized`
- Dashboard groups: `/dashboard/resident/*`, `/dashboard/supervisor/*`, `/dashboard/utrmc/*`, plus `/dashboard/pg` redirect shim.

Nav registry (`frontend/lib/navRegistry.ts`) is role-driven and aligns with present resident/supervisor/utrmc pages.

## Functional classification

- **Fully functional (code-wired):** login page, resident research, supervisor research approvals, UTRMC users/hospitals/departments/matrix/programs/postings.
- **Partially wired:** several UTRMC/resident pages with broad error handling and `any` types.
- **UI shell / placeholder risk:** regression docs explicitly flag not-ready features (logbook UI hooks, analytics/import dashboards).
- **Broken/inaccessible:** contract/test-referenced logbook routes not present in `frontend/app`.

## Frontend quality findings

- `npm run lint` fails with many `no-explicit-any` and unused var/expression errors.
- Middleware + ProtectedRoute both implement role gating (good defense-in-depth), but there is route-home mismatch:
  - middleware sends `pg/resident` to `/dashboard/pg`
  - `getDashboardPathForRole` sends `pg/resident` to `/dashboard/resident`
  - `/dashboard/pg/page.tsx` immediately redirects to resident.

## API calling pattern

- Mostly centralized API modules under `frontend/lib/api`.
- Some direct component-level calls still exist (e.g., research page patterns noted in docs).
- Next API catch-all proxy (`app/api/[...path]/route.ts`) forwards to backend using `INTERNAL_API_URL` and appends trailing slash.

## UX and consistency gaps

- Strong visual consistency across dashboard pages.
- Missing pages for some documented/tested workflows create a false perception of coverage.
- Some error handling uses generic fallback strings and broad catches; good for UX continuity but weak for diagnosis.
