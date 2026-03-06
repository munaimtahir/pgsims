# PGSIMS Playwright — Feature Coverage Matrix

| Feature Area | Spec File | Tests | Status |
|---|---|---|---|
| **Public pages** | `smoke/public.spec.ts` | 5 | ✅ Covered |
| **Login form UI** | `smoke/auth_flow.spec.ts` | 5 | ✅ Covered |
| **Role dashboards load** | `smoke/dashboards.spec.ts` | 7 | ✅ Covered |
| **Valid login by role** | `auth/session.spec.ts` | 3 | ✅ Covered |
| **Invalid login rejection** | `auth/session.spec.ts` | 2 | ✅ Covered |
| **Logout + session clear** | `auth/session.spec.ts` | 2 | ✅ Covered |
| **Unauthenticated guard** | `auth/session.spec.ts` | 3 | ✅ Covered |
| **PG cross-role block** | `rbac/access-control.spec.ts` | 4 | ✅ Covered |
| **Supervisor cross-role block** | `rbac/access-control.spec.ts` | 4 | ✅ Covered |
| **UTRMC admin cross-role block** | `rbac/access-control.spec.ts` | 3 | ✅ Covered |
| **UTRMC user read-only** | `rbac/access-control.spec.ts` | 2 | ✅ Covered |
| **Direct URL unauthenticated** | `rbac/access-control.spec.ts` | 5 | ✅ Covered |
| **UTRMC sidebar nav items** | `navigation/sidebar.spec.ts` | 8 | ✅ Covered |
| **Supervisor sidebar nav items** | `navigation/sidebar.spec.ts` | 4 | ✅ Covered |
| **Resident sidebar nav items** | `navigation/sidebar.spec.ts` | 5 | ✅ Covered |
| **UTRMC overview page** | `dashboard/pages.spec.ts` | 1 | ✅ Covered |
| **UTRMC hospitals page** | `dashboard/pages.spec.ts` | 1 | ✅ Covered |
| **UTRMC departments page** | `dashboard/pages.spec.ts` | 1 | ✅ Covered |
| **UTRMC users page** | `dashboard/pages.spec.ts` | 1 | ✅ Covered |
| **UTRMC supervision page** | `dashboard/pages.spec.ts` | 1 | ✅ Covered |
| **UTRMC H-D matrix page** | `dashboard/pages.spec.ts` | 1 | ✅ Covered |
| **UTRMC programs page** | `dashboard/pages.spec.ts` | 1 | ✅ Covered |
| **UTRMC eligibility monitor** | `dashboard/pages.spec.ts` | 1 | ✅ Covered |
| **Supervisor overview** | `dashboard/pages.spec.ts` | 1 | ✅ Covered |
| **Supervisor research approvals** | `dashboard/pages.spec.ts` | 1 | ✅ Covered |
| **Resident main dashboard** | `dashboard/pages.spec.ts` | 1 | ✅ Covered |
| **Resident schedule page** | `dashboard/pages.spec.ts` | 1 | ✅ Covered |
| **Resident progress page** | `dashboard/pages.spec.ts` | 1 | ✅ Covered |
| **Resident research page** | `dashboard/pages.spec.ts` | 1 | ✅ Covered |
| **Resident thesis page** | `dashboard/pages.spec.ts` | 1 | ✅ Covered |
| **Resident workshops page** | `dashboard/pages.spec.ts` | 1 | ✅ Covered |
| **Hospital CRUD (UI)** | `workflows/utrmc-management.spec.ts` | 2 | ✅ Covered |
| **Department CRUD (UI)** | `workflows/utrmc-management.spec.ts` | 2 | ✅ Covered |
| **User management (UI)** | `workflows/utrmc-management.spec.ts` | 2 | ✅ Covered |
| **Supervision link management** | `workflows/utrmc-management.spec.ts` | 2 | ✅ Covered |
| **Supervisor research queue** | `workflows/supervisor-review.spec.ts` | 3 | ✅ Covered |
| **Supervisor resident API** | `workflows/supervisor-review.spec.ts` | 1 | ✅ Covered |
| **Resident schedule + API** | `workflows/resident-training.spec.ts` | 2 | ✅ Covered |
| **Resident eligibility API** | `workflows/resident-training.spec.ts` | 2 | ✅ Covered |
| **Resident research wizard** | `workflows/resident-training.spec.ts` | 2 | ✅ Covered |
| **Resident thesis** | `workflows/resident-training.spec.ts` | 1 | ✅ Covered |
| **Resident workshops + API** | `workflows/resident-training.spec.ts` | 2 | ✅ Covered |
| **Login form empty field** | `negative/validation.spec.ts` | 4 | ✅ Covered |
| **Hospital form validation** | `negative/validation.spec.ts` | 1 | ✅ Covered |
| **Department form validation** | `negative/validation.spec.ts` | 1 | ✅ Covered |
| **User form validation** | `negative/validation.spec.ts` | 1 | ✅ Covered |
| **Cross-role URL blocked** | `negative/validation.spec.ts` | 2 | ✅ Covered |
| **API unauthenticated 401** | `negative/validation.spec.ts` | 2 | ✅ Covered |
| **Userbase graph CRUD** | `critical/userbase_foundation.spec.ts` | 1 | ✅ Covered |
| **Phase 6 research + eligibility** | `critical/phase6_research_eligibility.spec.ts` | 2 | ✅ Covered |

## Not Yet Covered (Blockers)

| Feature | Reason |
|---------|--------|
| Logbook submit/review flow | Logbook frontend UI not built — legacy backend HTML only |
| Clinical cases workflow | Cases frontend UI not built — legacy backend only |
| Certificate management | Certificates frontend UI not built — legacy backend only |
| Leave request workflow | Leave module not present in frontend navigation |
| Analytics dashboard | Analytics page not in frontend nav registry |
| Notifications | Notifications page not in frontend nav registry |
| Duty roster | Not in frontend nav registry |
| HOD assignments | Page exists at `/dashboard/utrmc/hod` but not wired in nav |

See `OUT/playwright_blockers.md` for full details.
