# Dashboard Readiness Review

| Route | Loads? | Visually ready? | User-ready? | Main issue | Priority |
| --- | ---: | ---: | ---: | --- | --- |
| `/dashboard/utrmc` | Yes | Partial | Partial | Import/control center dominates the page; the overview is not yet a simple operations dashboard. | High |
| `/dashboard/utrmc/hospitals` | Yes | Partial | Partial | Raw CRUD table; useful for admins, but too dense for non-technical users. | Medium |
| `/dashboard/utrmc/departments` | Yes | Partial | Partial | Same pattern as hospitals, with limited context and little guidance. | Medium |
| `/dashboard/utrmc/users` | Yes | Partial | Partial | Search helps, but the page still reads like a data grid, not an operational tool. | Medium |
| `/dashboard/utrmc/matrix` | Yes | Partial | Partial | Dense checkbox matrix is hard to scan and too small for touch-first use. | High |
| `/dashboard/utrmc/supervision` | Yes | Partial | Partial | Functional, but there is no summary or workflow guidance. | Medium |
| `/dashboard/utrmc/hod` | Yes | Partial | Partial | Simple assignment table; usable, but not friendly. | Medium |
| `/dashboard/utrmc/programs` | Yes | Partial | Partial | Technically correct, visually sparse, and very domain-specific. | Medium |
| `/dashboard/utrmc/eligibility-monitoring` | Yes | Partial | Partial | Useful output, but still a list of cards and filters with little prioritization. | Medium |
| `/dashboard/utrmc/data-quality` | Yes | Partial | Partial | Loads in the live baseline, but the dashboard starts with a failure banner and no resident records. | High |
| `/dashboard/utrmc/postings` | Yes | Partial | Partial | Hidden route with a workable queue UI, but not surfaced as an important admin task. | Medium |
| `/dashboard/utrmc/departments/[id]/roster` | Yes | Partial | Partial | Hidden roster page is readable, but the route is buried. | Medium |
| `/dashboard/supervisor` | Yes | Partial | Partial | Good structural layout, but the baseline is empty and not clearly role-focused enough. | Medium |
| `/dashboard/supervisor/research-approvals` | Yes | Yes | No | Explicit deferred notice; useful as a stub, not as a pilot route. | Low |
| `/dashboard/supervisor/residents/[id]/progress` | Yes | Yes | Partial | Readable snapshot, but hidden and not discoverable from the main dashboard. | Medium |
| `/dashboard/resident` | Yes | No | No | Client-side exception in the live baseline. | P0 |
| `/dashboard/resident/schedule` | Yes | Partial | Partial | In the current baseline the resident-only APIs are missing, so the page fails to load. | High |
| `/dashboard/resident/progress` | Yes | Yes | Partial | Best resident page; still sparse because there is no real resident dataset in the live baseline. | Medium |
| `/dashboard/resident/workshops` | Yes | Yes | No | Deferred workflow notice only. | Low |
| `/dashboard/resident/research` | Yes | Yes | No | Deferred workflow notice only. | Low |
| `/dashboard/resident/thesis` | Yes | Yes | No | Deferred workflow notice only. | Low |
| `/dashboard/resident/postings` | Yes | Yes | No | Deferred workflow notice only. | Low |
| `/dashboard/pg` | Yes | No | No | Redirect spinner has no meaningful content. | Low |

## Readiness Summary

- UTRMC/admin routes are mostly reachable and mostly usable
- The resident landing dashboard is broken
- The resident schedule page fails in the live baseline because resident-only data is absent
- The supervisor dashboard is usable, but it is thin because the baseline has no active residents
- Hidden pages exist and work, but they are not discoverable from the sidebar

