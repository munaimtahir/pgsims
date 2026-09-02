# Frontend-Backend Linkage Map

| Frontend page | API used | API exists? | Response shape known? | UI handles loading? | UI handles error? | Notes |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `/dashboard/utrmc` | `/api/hospitals/`, `/api/departments/`, `/api/users/`, `/api/hospital-departments/`, `/api/dashboard/utrmc/`, `/api/admin/data-quality/summary`, `/api/resident-training/`, `/api/rotations/`, `/api/submissions/synopsis/review-queue/`, `/api/submissions/thesis/review-queue/`, `/api/rotations/completions/` | Yes | Yes | Yes | Yes | Import/setup content dominates the overview and pushes the operational summary down the page. |
| `/dashboard/utrmc/hospitals` | `/api/hospitals/` | Yes | Yes | Yes | Yes | Raw CRUD table, no search or empty-state guidance. |
| `/dashboard/utrmc/departments` | `/api/departments/` | Yes | Yes | Yes | Yes | Same density pattern as hospitals. |
| `/dashboard/utrmc/users` | `/api/users/` | Yes | Yes | Yes | Yes | Search exists, but the page is still a dense admin table. |
| `/dashboard/utrmc/matrix` | `/api/hospitals/`, `/api/departments/`, `/api/hospital-departments/` | Yes | Yes | Yes | Yes | Dense grid of toggle buttons; readable on desktop, but not senior-friendly. |
| `/dashboard/utrmc/supervision` | `/api/supervision-links/`, `/api/users/` | Yes | Yes | Yes | Yes | Works, but is still a data-entry table. |
| `/dashboard/utrmc/hod` | `/api/hod-assignments/`, `/api/departments/`, `/api/users/` | Yes | Yes | Yes | Yes | Functional, but very utilitarian. |
| `/dashboard/utrmc/programs` | `/api/programs/`, `/api/programs/{id}/policy/`, `/api/programs/{id}/milestones/`, `/api/program-templates/` | Yes | Yes | Yes | Yes | Detail pane is readable, but still very technical. |
| `/dashboard/utrmc/eligibility-monitoring` | `/api/utrmc/eligibility/` | Yes | Yes | Yes | Yes | Loaded cleanly in the live baseline. |
| `/dashboard/utrmc/data-quality` | `/api/admin/data-quality/summary`, `/api/admin/data-quality/users`, `/api/admin/data-quality/audit`, `/api/admin/data-quality/recompute`, `/api/users/{id}/`, `/api/residents/{id}/` | Yes | Yes | Yes | Yes | Live baseline shows a load error banner because there are no resident records to inspect. |
| `/dashboard/utrmc/postings` | `/api/postings/` | Yes | Yes | Yes | Yes | Hidden from nav; empty baseline. |
| `/dashboard/supervisor` | `/api/supervisors/me/summary/`, `/api/dashboard/supervisor/`, `/api/utrmc/approvals/leaves/`, `/api/logbook/review-queue/` | Yes | Yes | Yes | Yes | Clean visual shell, but currently empty because no resident records are active. |
| `/dashboard/supervisor/research-approvals` | none; deferred notice only | N/A | N/A | N/A | N/A | Intentionally deferred screen. |
| `/dashboard/supervisor/residents/[id]/progress` | `/api/supervisors/residents/{id}/progress/` | Yes | Yes | Yes | Yes | Hidden but functional read-only snapshot. |
| `/dashboard/resident` | `/api/residents/me/summary/`, `/api/dashboard/resident/` | Yes | Yes | Yes | Yes | Broken in the live baseline because `summary.training_record` is null and the page dereferences it. |
| `/dashboard/resident/schedule` | `/api/residents/me/summary/`, `/api/my/leaves/`, `/api/my/rotations/` | Yes | Yes | Yes | Yes | Current baseline shows a load failure for the admin token; resident-only data is absent. |
| `/dashboard/resident/progress` | `/api/my/eligibility/`, `/api/dashboard/resident/`, `/api/logbook/`, `/api/logbook/my-threshold/` | Yes | Yes | Yes | Yes | Best resident-facing page in the current baseline. |
| `/dashboard/resident/workshops` | none; deferred notice only | N/A | N/A | N/A | N/A | Intentionally deferred screen. |
| `/dashboard/resident/research` | none; deferred notice only | N/A | N/A | N/A | N/A | Intentionally deferred screen. |
| `/dashboard/resident/thesis` | none; deferred notice only | N/A | N/A | N/A | N/A | Intentionally deferred screen. |
| `/dashboard/resident/postings` | none; deferred notice only | N/A | N/A | N/A | N/A | Intentionally deferred screen. |
| `/dashboard/pg/departments/[id]/roster` | `/api/departments/{id}/roster/` | Yes | Yes | Yes | Yes | Hidden roster route; not exposed in nav. |
| `/dashboard/utrmc/departments/[id]/roster` | `/api/departments/{id}/roster/` | Yes | Yes | Yes | Yes | Hidden roster route; not exposed in nav. |
| `/dashboard/pg` | none; redirect only | N/A | N/A | N/A | N/A | Redirect shell to resident dashboard. |

## Linkage Notes

- The visible sidebar is driven by [`frontend/lib/navRegistry.ts`](/home/munaim/srv/apps/pgsims/frontend/lib/navRegistry.ts)
- The main dashboard guard is [`frontend/middleware.ts`](/home/munaim/srv/apps/pgsims/frontend/middleware.ts)
- The resident landing page breaks because it assumes `summary.training_record` is always present
- UTRMC overview is the largest consumer surface and includes the broadest API fan-out

