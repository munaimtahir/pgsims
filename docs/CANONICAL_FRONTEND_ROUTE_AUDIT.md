# Canonical Frontend Route Audit

| Frontend Route | File Path | Current Status | Role Access | Canonical Replacement | Action Taken | Can Delete Later? |
|---|---|---|---|---|---|---|
| `/users` | `frontend/app/users/page.tsx` | CANONICAL | ADMIN | — | Kept canonical directory page. | NO |
| `/users/new` | `frontend/app/users/new/page.tsx` | CANONICAL | ADMIN | — | Kept universal identity creation page. | NO |
| `/residents` | `frontend/app/residents/page.tsx` | CANONICAL | ADMIN | — | Kept canonical resident directory. | NO |
| `/residents/[id]` | `frontend/app/residents/[id]/page.tsx` | CANONICAL | ADMIN/LIMITED | — | Kept canonical resident detail. | NO |
| `/supervisors` | `frontend/app/supervisors/page.tsx` | CANONICAL | ADMIN | — | Kept canonical supervisor directory. | NO |
| `/supervisors/[id]` | `frontend/app/supervisors/[id]/page.tsx` | CANONICAL | ADMIN/LIMITED | — | Kept canonical supervisor detail. | NO |
| `/support-staff` | `frontend/app/support-staff/page.tsx` | CANONICAL | ADMIN | — | Kept canonical support-staff directory. | NO |
| `/support-staff/[id]` | `frontend/app/support-staff/[id]/page.tsx` | CANONICAL | ADMIN | — | Kept canonical support-staff detail. | NO |
| `/admins` | `frontend/app/admins/page.tsx` | CANONICAL | ADMIN | — | Kept canonical admin directory. | NO |
| `/admins/[id]` | `frontend/app/admins/[id]/page.tsx` | CANONICAL | ADMIN | — | Kept canonical admin detail. | NO |
| `/masters` | `frontend/app/masters/page.tsx` | CANONICAL | ADMIN | — | Kept canonical masters hub and removed duplicate subpage links. | NO |
| `/supervision/*` | `frontend/app/supervision/*` | CANONICAL | ADMIN | — | Kept canonical supervision route family. | NO |
| `/academics/*` | `frontend/app/academics/*` | CANONICAL | ADMIN or ADMIN/SUPERVISOR where applicable | — | Kept canonical academics route family. | NO |
| `/dashboard/utrmc` | `frontend/app/dashboard/utrmc/page.tsx` | CANONICAL | ADMIN/SUPPORT_STAFF | — | Kept canonical admin/support-staff shell. | NO |
| `/dashboard/resident` | `frontend/app/dashboard/resident/page.tsx` | CANONICAL | RESIDENT | — | Kept canonical resident shell. | NO |
| `/dashboard/supervisor` | `frontend/app/dashboard/supervisor/page.tsx` | CANONICAL | SUPERVISOR | — | Kept canonical supervisor shell. | NO |
| `/complete-profile` | `frontend/app/complete-profile/page.tsx` | CANONICAL | ALL | — | Kept canonical onboarding page. | NO |
| `/change-password` | `frontend/app/change-password/page.tsx` | CANONICAL | ALL | — | Kept canonical password page. | NO |
| `/dashboard/change-password` | `frontend/app/dashboard/change-password/page.tsx` | REDIRECT_ALIAS | ALL | `/change-password` | Retained alias. | YES |
| `/dashboard/pg` | `frontend/app/dashboard/pg/page.tsx` | REDIRECT | RESIDENT/ADMIN | `/dashboard/resident` | Reduced to redirect-only. | YES |
| `/dashboard/pg/departments/[id]/roster` | `frontend/app/dashboard/pg/departments/[id]/roster/page.tsx` | REDIRECT | RESIDENT/ADMIN | `/dashboard/resident` | Reduced to redirect-only. | YES |
| `/dashboard/resident/(progress|schedule|research|thesis|workshops|postings)` | `frontend/app/dashboard/resident/*` | REDIRECT | RESIDENT | `/dashboard/resident` | Reduced to redirect-only. | YES |
| `/dashboard/supervisor/(research-approvals|residents/[id]/progress)` | `frontend/app/dashboard/supervisor/*` | REDIRECT | SUPERVISOR | `/dashboard/supervisor` | Reduced to redirect-only. | YES |
| `/dashboard/utrmc/(academics|data-quality|supervision)` | `frontend/app/dashboard/utrmc/*` | REDIRECT | ADMIN | `/academics`, `/academics/data-quality`, `/supervision` | Kept as canonical compatibility redirects. | YES |
| `/dashboard/utrmc/(backup|eligibility-monitoring|postings|onboarding)` | `frontend/app/dashboard/utrmc/*` | REDIRECT | ADMIN | `/dashboard/utrmc`, `/users/new` | Reduced to redirect-only. | YES |
| `/dashboard/utrmc/(users|supervisors|hospitals|departments|matrix|programs)` | `frontend/app/dashboard/utrmc/*` | REDIRECT | ADMIN | `/users`, `/supervisors`, `/masters` | Reduced to redirect-only. | YES |
| `/dashboard/utrmc/departments/[id]/roster` | `frontend/app/dashboard/utrmc/departments/[id]/roster/page.tsx` | REDIRECT | ADMIN | `/masters` | Reduced to redirect-only. | YES |
