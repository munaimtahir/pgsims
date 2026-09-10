# 14 — Parallel Development Matrix

| Workstream | Can Start Now | Can Run Parallel With | Must Wait For | Owner |
|---|---|---|---|---|
| XC-1 credential rotation + git-history scrub | Yes (deferred by user instruction, not a technical block) | Everything | Nothing technical — owner availability only | Lane C |
| BE-2 fix (unify LogbookEntry dependency: point milestone/threshold logic and bulk import at `academics.LogbookEntry`, retire or explicitly re-scope `training.LogbookEntry`) | Yes | WEB-1 nav fix, contract doc fixes, Android UI work | Nothing upstream | Lane A |
| WEB-1 nav wiring (add Logbook/Evaluations/reports/my-progress/monitoring/supervisor-workload/workflow-overview to `navRegistry.ts` + dashboard links) | Yes | BE-2, contract docs, Android work | Nothing — page/API layers already complete | Lane A |
| Contract doc repair (`API_CONTRACT.md` logbook + roles sections, `TERMINOLOGY.md` logbook aliasing, `CANONICAL_ROUTE_MAP.md`/`CANONICAL_FRONTEND_ROLE_MATRIX.md` regeneration, `CLAUDE.md` BE-1 correction) | Yes | Everything (pure docs) | Nothing | Lane A |
| BE-4 (disaster-backup directory creation fix) | Yes | Everything | Nothing | Lane A |
| Backend file-upload content/magic-byte validation (security P2) | Yes | Everything | Nothing | Lane A |
| Production: remove/fix dangling `pgr.fmu.edu.pk` Caddy route | Yes | Everything | Confirmation from domain owner (fmu.edu.pk) on intent — otherwise safe to remove | Lane C |
| Production: gunicorn worker-count/timeout review | Yes (review); load-testing should be scheduled, not run casually against prod | Everything | A deliberate maintenance window if the fix requires a restart | Lane C |
| Web page-level test coverage for rotations/leave/logbook/evaluations/supervision | Should wait until WEB-1 nav fix lands (test what a real user can reach) | Contract docs, BE-2, Android | WEB-1 (logical, not technical — testing an unreachable page first is low value) | Lane A |
| Web: consolidate duplicate change-password routes, resolve `/register` orphan policy | Yes | Everything | A product decision (which route survives; whether self-registration should ever be enabled) | Lane A |
| Web: logbook status label reconciliation (`status.ts`/`WorkflowStatusBadge` vs raw enum) | Best done alongside BE-2 (both touch logbook) | Everything else | Loosely coupled to BE-2 for context, not a hard technical dependency | Lane A |
| `android/README.md` + `ANDROID_PLAY_STORE_UPLOAD_CHECKLIST.md` update for 1.1.4 | Yes | Everything | Nothing | Lane B |
| Android: verify live document-upload success path against a synthetic/staging resident | Yes | Everything | A safe synthetic resident account (already exists per `SPRINT_STATE.md`'s prior E2E work) | Lane B |
| Android: introduce ViewModels + Navigation-Compose (incremental) | Yes, can start now | Everything | Ideally lands before a 3rd/4th full CRUD domain is added (soft dependency, not hard) | Lane B |
| Android: full Assessments/Research/Workshops submission UI (beyond current read-only summaries) | **No — scope decision needed first** | N/A until unblocked | A product decision to reactivate the "deferred/legacy" training surface for real use (see `06_PLATFORM_API_CONTRACT_MATRIX.md`) — the API itself is already stable and not the blocker | Lane B (blocked on Lane A/product owner decision) |
| Backend: standardize `RotationAssignmentViewSet` vs `ResidentSummaryView` rotation field shape (P2-1) | Yes | Everything | Nothing — but should happen before any *new* Android/web consumer of the summary endpoint is built, to avoid propagating another defensive-fallback pattern | Lane A |
| Backend: decide fate of legacy server-rendered dashboard views (BE-3) | Should follow BE-2 (their most visible symptom is BE-2's wrong count) | Everything else | BE-2 (logical — fixing BE-2 first tells you whether the legacy views become correct-by-fix or should just be retired) | Lane A |
| Play Console upload of already-signed 1.1.4 AAB | External, owner-only action | Everything | The 1.1.4-specific checklist item above (AND-1) should land first so the upload isn't done against a stale checklist | Lane C (external) |
| Full Playwright e2e regression run (currently not run in this pass) | Yes, whenever convenient | Everything | Ideally after WEB-1 nav fix, so e2e specs can be extended to assert real nav-reachability, not just `page.goto()` correctness | Lane A |

## LANE A — PGR SIMS BACKEND / WEB

**Current priority:** BE-2 (LogbookEntry canonical-model fix) and WEB-1 (nav wiring for
already-shipped Logbook/Evaluations) — both high-value, both low-risk, both immediately actionable,
together closing the platform's two most significant "real work already done but not fully
connected" gaps.

**Can start immediately:** BE-2, WEB-1, all contract-doc repairs, BE-4, file-upload validation
check, rotation field-shape standardization (P2-1), Caddy/gunicorn cleanup coordination with Lane C.

**Must wait:** page-level test authoring for the newly-nav-wired pages (logically follows WEB-1);
BE-3's disposition (logically follows BE-2).

## LANE B — PGR COMPANION ANDROID

**Current priority:** doc currency fixes (AND-1, AND-2 — cheap, unblocks a safe Play Console
upload) and closing the one unverified surface (AND-4, live document-upload path) before any new
feature work, since the app is otherwise release-ready.

**Can start immediately:** AND-1/AND-2 doc fixes, AND-4 verification, ViewModel/Navigation-Compose
incremental adoption (AND-3), Play Console upload itself once AND-1 lands.

**Must wait:** full Assessments/Research/Workshops CRUD UI — blocked on a product scope decision,
not on Lane A or the API surface (which is already stable and IMPLEMENTED). Android should not
independently build business logic for a domain the product hasn't decided to reactivate — matches
the sprint's own "Android should not independently recreate PGR SIMS business logic" rule.

## LANE C — PRODUCTION / RELEASE

**Current priority:** XC-1 credential rotation (deferred per explicit user instruction, tracked as
build-plan item 1) and the two low-risk production cleanups found in this pass (dangling Caddy
route, gunicorn headroom review).

**Trigger for deployment:** production is already 1 commit behind main with only docs/scripts
changes pending — no urgent deploy is required by this discovery pass. The next deploy should
bundle: the Wave 0/1 backend fixes (BE-2, BE-4, security P2), once merged and tested, in one
routine release rather than one-off hotfixes, given none of them are currently causing live user
impact.
