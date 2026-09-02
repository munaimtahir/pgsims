# Prioritized UI Repair List

| Priority | Area | Issue | Why it matters | Recommended fix | Risk |
| --- | --- | --- | --- | --- | --- |
| P0 | Resident dashboard | Client-side crash on `/dashboard/resident` | The primary resident landing page is unusable. | Guard against null resident training data and render a safe empty state. | Medium |
| P0 | Dashboard discovery | Missing frontend shell for HOD | Backend supports HOD operations, but the UI does not expose a proper dashboard. | Add a dedicated HOD dashboard page or route it into supervisor/admin summaries. | High |
| P1 | Overview | Import engine dominates the UTRMC overview | Non-technical users see setup tooling before they see their work. | Move imports to a dedicated onboarding page and keep overview operational. | Medium |
| P1 | Resident schedule | Current baseline fails to load resident schedule | Residents need a reliable place to request leave and inspect rotation status. | Add a resident-safe fallback and align the page with resident-only data expectations. | Medium |
| P1 | Matrix | Dense checkbox grid | Hard for non-technical staff to manage safely. | Replace with a larger, labeled matrix editor or guided workflow. | Medium |
| P1 | Data quality | Hidden failure state and empty baseline | Admins need a clear sense of whether there is real data to work on. | Add a clearer empty state and a safer no-data path. | Low |
| P2 | Hospitals/departments/users | Dense CRUD tables | Usability drops fast for older users. | Increase spacing, reduce columns, and add clearer section summaries. | Low |
| P2 | Programs | Technical detail pane | The page is accurate but too technical to scan quickly. | Add summaries, task cards, and better defaults. | Low |
| P2 | Supervisor dashboard | Empty operational summary | The page is readable but not action-oriented enough. | Add a “today’s work” panel and priority ordering. | Low |
| P3 | Hidden pages | Roster and workflow routes are not discoverable | Users cannot find useful pages without guessing URLs. | Surface them in the navigation model or link to them from the relevant dashboard. | Low |

