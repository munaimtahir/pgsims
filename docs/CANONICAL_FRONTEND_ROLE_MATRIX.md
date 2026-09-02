# Canonical Frontend Role Matrix

| Route | Module | ADMIN | RESIDENT | SUPERVISOR | SUPPORT_STAFF | Status | Notes |
|---|---|---|---|---|---|---|---|
| `/dashboard/utrmc` | Admin Dashboard | YES | NO | NO | YES | canonical | Support staff sees restricted shell only. |
| `/dashboard/resident` | Resident Dashboard | NO | YES | NO | NO | canonical | Shows My Training, My Supervisor, My Academic Summary. |
| `/dashboard/supervisor` | Supervisor Dashboard | NO | NO | YES | NO | canonical | Shows My Residents and Academic Review Queue. |
| `/users` | Users | YES | NO | NO | NO | canonical | Universal identity directory. |
| `/residents` | Residents | YES | NO | NO | NO | canonical | Canonical resident directory. |
| `/supervisors` | Supervisors | YES | NO | NO | NO | canonical | Canonical supervisor directory. |
| `/support-staff` | Support Staff | YES | NO | NO | NO | canonical | Canonical support-staff directory. |
| `/admins` | Admins | YES | NO | NO | NO | canonical | Canonical admin directory. |
| `/masters` | Masters | YES | NO | NO | NO | canonical | Canonical master-data hub only. |
| `/supervision/*` | Supervision | YES | NO | NO | NO | canonical | Canonical supervision module. |
| `/academics` except `/academics/review-queue` | Academics Admin Setup | YES | NO | NO | NO | canonical | Admin-only academic setup routes. |
| `/academics/review-queue` | Academic Review Queue | YES | NO | YES | NO | canonical | Supervisor sees assigned queue only. |
| `/complete-profile` | Complete Profile | YES | YES | YES | YES | canonical | Shared onboarding/profile flow. |
| `/change-password` | Change Password | YES | YES | YES | YES | canonical | Shared password flow. |
| `/dashboard/pg*` | Old PG Dashboard Family | NO | NO | NO | NO | redirect | Redirects to `/dashboard/resident`. |
| `/dashboard/resident/(progress|schedule|research|thesis|workshops|postings)` | Old Resident Workflows | NO | NO | NO | NO | redirect | Redirects to `/dashboard/resident`. |
| `/dashboard/supervisor/(research-approvals|residents/[id]/progress)` | Old Supervisor Workflows | NO | NO | NO | NO | redirect | Redirects to `/dashboard/supervisor`. |
| `/dashboard/utrmc/(users|supervisors|hospitals|departments|matrix|programs|backup|eligibility-monitoring|postings|onboarding)` | Old UTRMC Subpages | NO | NO | NO | NO | redirect | Redirect-only compatibility pages. |
