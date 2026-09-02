# Feature Workflow Verification Matrix

| Workflow | Role | UI Route | Backend API | Action Tested | Result | Category | Evidence |
|---|---|---|---|---|---|---|---|
| Login + dashboard entry | admin / utrmc_admin / supervisor / pg | `/login` → role home | `/api/auth/login/`, `/api/auth/me/` | login, redirect, logout | PASS | A | smoke/auth suites |
| Resident schedule | pg | `/dashboard/resident/schedule` | schedule API | view schedule | PASS | A | workflows/resident-training |
| Resident leave | pg + supervisor | `/dashboard/resident/schedule` / `/dashboard/supervisor` | leave APIs | draft → submit → approve | PASS | A | workflow-gate/stabilized-workflows |
| Resident logbook | pg + supervisor | `/dashboard/resident` / `/dashboard/supervisor` | logbook APIs | submit/return/approve | PASS | A | active-surface/logbook |
| Supervisor review queue | supervisor | `/dashboard/supervisor` | review APIs | queue visibility and access | PASS | A | workflows/supervisor-review |
| UTRMC management | utrmc_admin | `/dashboard/utrmc/*` | userbase/training APIs | hospitals, departments, users, supervision, matrix | PASS | A | dashboard/pages + workflows/utrmc-management |
| Bulk setup dry run | utrmc_admin | `/dashboard/utrmc` | bulk API | dry-run import | PASS | A | workflow-gate/bulk-setup |
| Resident research page | pg | `/dashboard/resident/research` | research API exists | wizard steps | PARTIAL | F | page is a deferred notice, not the wizard asserted by legacy test |
| Admin dashboard/reports | admin | `/dashboard/admin` | n/a | widgets/reports preview | FAIL | G | route not implemented in app route tree |
| Admin analytics live feed | admin | `/dashboard/admin/analytics` | analytics live-feed API | live feed | SKIPPED / legacy | F | test marked outside current accepted baseline |

## Notes

- Categories: `A` fully working, `F` placeholder/demo only, `G` not implemented.
- The active release surface is broadly healthy; the remaining gaps are legacy admin coverage and a deferred research page.
