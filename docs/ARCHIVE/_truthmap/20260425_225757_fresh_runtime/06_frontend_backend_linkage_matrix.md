# Stage 6: Frontend-Backend Linkage Matrix

## Matrix

| Frontend Surface | Frontend File | Frontend API Client | Backend Runtime | Fresh Verdict |
|---|---|---|---|---|
| Resident dashboard | `frontend/app/dashboard/resident/page.tsx` | `GET /api/dashboard/resident/`, `GET /api/residents/me/summary/` | 200 | Linked and working |
| Resident logbook | `frontend/app/dashboard/resident/progress/page.tsx` | `/api/logbook/*` | create/submit/review all worked | Linked and working |
| Supervisor dashboard | `frontend/app/dashboard/supervisor/page.tsx` | `/api/dashboard/supervisor/`, `/api/logbook/review-queue/`, `/api/utrmc/approvals/leaves/` | 200 | Linked and working |
| Resident schedule/leave | `frontend/app/dashboard/resident/schedule/page.tsx` | `/api/my/leaves/`, `/api/leaves/*` | create/submit/approve/reject all worked | Linked and working |
| Programs | `frontend/app/dashboard/utrmc/programs/page.tsx` | `/api/programs/`, `/api/programs/<id>/policy/`, `/api/programs/<id>/milestones/`, `/api/program-templates/` | 200 | Page works; create/edit program UI absent |
| Supervision links | `frontend/app/dashboard/utrmc/supervision/page.tsx` | posts `/api/supervision-links/` using `supervisor` and `resident` keys | backend expects `supervisor_user_id`, `resident_user_id` | Broken contract |
| Data Quality | `frontend/app/dashboard/utrmc/data-quality/page.tsx` | `/api/admin/data-quality/summary`, `/users`, `/audit` | direct backend 200; browser proxy 404 | Broken proxy/path integration |
| Bulk | `BulkSetupWorkspace` in `frontend/app/dashboard/utrmc/page.tsx` | `/api/bulk/templates/*`, `/api/bulk/exports/*`, `/api/bulk/import/*` | template/export 200, dry-run validated | Present and active |
| Workshops | `frontend/app/dashboard/resident/workshops/page.tsx` | `/api/workshops/`, `/api/my/workshops/` | 200 with empty data | Backend exists; frontend active workflow deferred |

## Key Integration Findings

- The biggest fresh-runtime problem is no longer “frontend routes missing”.
- The real remaining defects are narrower:
  - supervision-link payload drift
  - data-quality proxy/trailing-slash drift
  - missing create/edit program UI
  - deferred/non-nav workshops frontend
