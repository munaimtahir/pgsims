# Frontend Route Truthmap

| Route | Source file | Linked in UI? | Role/User type | Status | Notes |
| --- | --- | ---: | --- | --- | --- |
| `/` | `frontend/app/page.tsx` | Yes | Public | Working | Dashboard redirect hub; routes authenticated users to role home. |
| `/login` | `frontend/app/login/page.tsx` | Yes | Public | Working | Auth entry point. |
| `/register` | `frontend/app/register/page.tsx` | Yes | Public | Working | Public registration exists, but backend blocks it by config in the current baseline. |
| `/forgot-password` | `frontend/app/forgot-password/page.tsx` | Yes | Public | Working | Recovery entry point. |
| `/unauthorized` | `frontend/app/unauthorized/page.tsx` | Yes | Public | Working | Used by role redirect flow. |
| `/dashboard` | `frontend/app/dashboard/page.tsx` | No | All authenticated | Working | Redirect hub to role-specific dashboard. |
| `/dashboard/pg` | `frontend/app/dashboard/pg/page.tsx` | No | PG / Resident | Working | Redirects to `/dashboard/resident`; no real content. |
| `/dashboard/utrmc` | `frontend/app/dashboard/utrmc/page.tsx` | Yes | UTRMC / Admin | Partial | Loads and is useful, but the page is dominated by import/setup workflows. |
| `/dashboard/utrmc/hospitals` | `frontend/app/dashboard/utrmc/hospitals/page.tsx` | Yes | UTRMC / Admin | Partial | CRUD table works, but it is a raw management screen with limited guidance. |
| `/dashboard/utrmc/departments` | `frontend/app/dashboard/utrmc/departments/page.tsx` | Yes | UTRMC / Admin | Partial | CRUD table works, same density issue as hospitals. |
| `/dashboard/utrmc/users` | `frontend/app/dashboard/utrmc/users/page.tsx` | Yes | UTRMC / Admin | Partial | Search helps, but this is still a dense admin table. |
| `/dashboard/utrmc/matrix` | `frontend/app/dashboard/utrmc/matrix/page.tsx` | Yes | UTRMC / Admin | Partial | Functional, but the checkbox grid is dense and hard to scan. |
| `/dashboard/utrmc/supervision` | `frontend/app/dashboard/utrmc/supervision/page.tsx` | Yes | UTRMC / Admin | Partial | Functional roster table, not visually polished. |
| `/dashboard/utrmc/hod` | `frontend/app/dashboard/utrmc/hod/page.tsx` | Yes | UTRMC / Admin | Partial | Works, but it is a thin CRUD table. |
| `/dashboard/utrmc/programs` | `frontend/app/dashboard/utrmc/programs/page.tsx` | Yes | UTRMC / Admin | Partial | Works, but the left-list/right-detail pattern is sparse and highly technical. |
| `/dashboard/utrmc/eligibility-monitoring` | `frontend/app/dashboard/utrmc/eligibility-monitoring/page.tsx` | Yes | UTRMC / Admin | Partial | Loads; useful operationally, but still table-heavy. |
| `/dashboard/utrmc/data-quality` | `frontend/app/dashboard/utrmc/data-quality/page.tsx` | No | UTRMC / Admin | Partial | Hidden from sidebar; loads but shows a warning banner in the current baseline. |
| `/dashboard/utrmc/postings` | `frontend/app/dashboard/utrmc/postings/page.tsx` | No | UTRMC / Admin | Partial | Hidden from sidebar; functional posting queue. |
| `/dashboard/utrmc/departments/[id]/roster` | `frontend/app/dashboard/utrmc/departments/[id]/roster/page.tsx` | No | UTRMC / Admin | Working | Hidden roster page; not surfaced in navigation. |
| `/dashboard/supervisor` | `frontend/app/dashboard/supervisor/page.tsx` | Yes | Supervisor / Faculty / Admin | Partial | Loads and is readable, but the baseline has no active residents so the page is mostly empty. |
| `/dashboard/supervisor/research-approvals` | `frontend/app/dashboard/supervisor/research-approvals/page.tsx` | No | Supervisor / Faculty / Admin | Deferred | Explicit deferred-workflow notice. |
| `/dashboard/supervisor/residents/[id]/progress` | `frontend/app/dashboard/supervisor/residents/[id]/progress/page.tsx` | No | Supervisor / Faculty / Admin | Working | Hidden but usable read-only snapshot route. |
| `/dashboard/resident` | `frontend/app/dashboard/resident/page.tsx` | Yes | PG / Resident | Broken | Client-side exception in the current baseline when `training_record` is null. |
| `/dashboard/resident/schedule` | `frontend/app/dashboard/resident/schedule/page.tsx` | Yes | PG / Resident | Broken | In the current baseline it fails to load schedule data for the admin token. |
| `/dashboard/resident/progress` | `frontend/app/dashboard/resident/progress/page.tsx` | Yes | PG / Resident | Working | Loadable and visually coherent; best resident-facing page in the current baseline. |
| `/dashboard/resident/workshops` | `frontend/app/dashboard/resident/workshops/page.tsx` | No | PG / Resident | Deferred | Explicit deferred-workflow notice. |
| `/dashboard/resident/research` | `frontend/app/dashboard/resident/research/page.tsx` | No | PG / Resident | Deferred | Explicit deferred-workflow notice. |
| `/dashboard/resident/thesis` | `frontend/app/dashboard/resident/thesis/page.tsx` | No | PG / Resident | Deferred | Explicit deferred-workflow notice. |
| `/dashboard/resident/postings` | `frontend/app/dashboard/resident/postings/page.tsx` | No | PG / Resident | Deferred | Explicit deferred-workflow notice. |
| `/dashboard/pg/departments/[id]/roster` | `frontend/app/dashboard/pg/departments/[id]/roster/page.tsx` | No | PG / Resident | Working | Hidden roster page, no dashboard link. |

## Route Truthmap Notes

- The nav registry is the source of truth for visible sidebar links: [`frontend/lib/navRegistry.ts`](/home/munaim/srv/apps/pgsims/frontend/lib/navRegistry.ts)
- The app has hidden but reachable routes for data-quality, postings, rosters, and supervisor progress snapshots
- The resident landing route is the only major dashboard route that is currently broken in the live baseline
- The PG dashboard is just a redirect shell, so it is not a meaningful destination by itself

