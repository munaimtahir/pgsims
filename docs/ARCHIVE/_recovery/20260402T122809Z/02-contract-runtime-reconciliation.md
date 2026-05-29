# Contract Runtime Reconciliation

## Major mismatches found and resolved

| Drift item | Pre-fix truth | Action taken | Outcome | Evidence |
|---|---|---|---|---|
| Resident leave workflow existed in backend but not in active frontend | Resident schedule showed leave counts but had no live create/submit path | Added leave draft, list, and submit UI on `/dashboard/resident/schedule`; wired training API client methods | Fixed | `frontend/app/dashboard/resident/schedule/page.tsx`, `frontend/lib/api/training.ts` |
| Supervisor leave approvals were implied by summary counts but not available in dashboard workflow | Supervisor dashboard did not expose actionable leave approval behavior | Added pending leave request list with approve/reject actions | Fixed | `frontend/app/dashboard/supervisor/page.tsx`, `frontend/lib/api/training.ts` |
| Resident summary contract lacked the training record identifier needed by the leave create payload | FE needed `resident_training`; summary response only exposed display fields | Added `training_record.id` to the resident summary response and tests | Fixed | `backend/sims/training/views.py`, `backend/sims/training/test_phase6.py`, `docs/contracts/API_CONTRACT.md` |
| Supervisor scoping drift between direct `resident.supervisor` assignment and `SupervisorResidentLink` matrix | Research workflow could work while summary/leave workflows missed the same resident | Added `_get_supervised_resident_ids()` and reused it across summary, leave, record, and posting queries; updated seed data | Fixed | `backend/sims/training/views.py`, `backend/sims/users/management/commands/seed_e2e.py` |
| Forgot-password path failed the real UI workflow when mail transport was unavailable | Endpoint returned `500` on mail send exception in local runtime | Changed endpoint to generic success response for all non-validation failures; added test | Fixed | `backend/sims/users/api_views.py`, `backend/sims/users/tests.py` |
| README and status notes over-signaled logbook/cases readiness | Historical docs still looked stronger than runtime truth | Repointed authority docs to the new recovery pack and explicitly marked legacy/deferred surfaces | Downgraded to truthful state | `README.md`, `docs/README.md` |
| Integration truth map looked like an active runtime inventory despite including legacy surfaces | Historical file could be mistaken for the current active include set | Added an authority warning and redirected readers to contracts + recovery pack | Downgraded to truthful state | `docs/contracts/INTEGRATION_TRUTH_MAP.md` |

## Major drift items intentionally not "fixed" in code

| Drift item | Reason not activated now | Classification |
|---|---|---|
| Logbook workflow | No active frontend route/nav and no active backend include path in the current runtime boundary; activating it would be scope expansion, not stabilization | Deferred |
| Cases workflow | Same boundary problem as logbook | Deferred |
| Legacy analytics claims | Historical docs and endpoint inventories exist, but they are not the authoritative active surface | Legacy |

## Unresolved drift items
- Docker containers can present stale code relative to the working tree if they are not rebuilt after source changes. The verified workflow gate for this pass used local current-tree processes instead of the already-running Docker frontend/backend pair.
- Next.js production build is green, but `frontend/next.config.mjs` still allows builds to ignore lint/type failures. That weakens build truth if CI relies only on `npm run build`.
- Historical docs outside `docs/contracts/` and the new recovery pack still exist and should continue to be treated as archive material, not planning authority.

## Evidence notes
- Active backend include set does not include legacy logbook/cases runtime activation: `backend/sims_project/urls.py`
- Active frontend navigation does not expose logbook/cases: `frontend/lib/navRegistry.ts`
- Active dashboard route inventory contains resident, supervisor, and UTRMC pages but no logbook/cases pages: `frontend/app/dashboard/*`
