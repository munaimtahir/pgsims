# 15 — Build Order and Roadmap

Every item below is evidence-sourced from files `01`-`14` in this directory. No item was invented
to fill out the wave template — several template categories (e.g. "unsafe migrations," "broken
auth") have no entries because this pass found none.

## Required build-order table

| Order | Workstream / Feature | Why This Order | Backend | Web | Android | Dependency | Can Parallelize |
|---:|---|---|:---:|:---:|:---:|---|---|
| 1 | XC-1: rotate `SECRET_KEY`/`DB_PASSWORD`, scrub `docs/ARCHIVE/.../.env.active` from git | Real, present-tense credential exposure in a shared repo; deferred per explicit user instruction (2026-09-09) but tracked as the first item in the remediation plan | — | — | — | None | Yes, with everything |
| 2 | BE-2: resolve dual `LogbookEntry` models — point milestone/threshold evaluation and bulk import at the real, shipped `academics.LogbookEntry`, retire or clearly re-scope `training.LogbookEntry` | Canonical-model conflict upstream of milestone eligibility and progress reporting; silently wrong data today | Yes | — | — | None (backend-only) | Yes |
| 3 | WEB-1: wire Logbook/Evaluations/reports/my-progress/monitoring/supervisor-workload/workflow-overview into `navRegistry.ts` and role dashboards | Fully-built, fully-tested, API-correct features are currently unreachable by real users — highest value-per-effort item in the whole discovery | — | Yes | — | None | Yes |
| 4 | Contract doc repair: `API_CONTRACT.md` logbook section (P1-1) and roles section (P1-2), `TERMINOLOGY.md` logbook aliasing, `CANONICAL_ROUTE_MAP.md`/`CANONICAL_FRONTEND_ROLE_MATRIX.md` regeneration, `CLAUDE.md` BE-1 correction | Pure documentation, zero code risk, prevents the next agent/developer (including a future Android reviewer) from building against a nonexistent API shape | — | — | — | None | Yes |
| 5 | BE-4: `create_disaster_recovery_backup()` — ensure target directory exists before write | Small, isolated fix to a DR mechanism whose own test currently fails | Yes | — | — | None | Yes |
| 6 | Security P2: confirm/add server-side content (magic-byte) validation for resident document uploads | Closes the one open item from an otherwise clean RBAC/security review | Yes | — | — | None | Yes |
| 7 | AND-1/AND-2: update `android/README.md` and `ANDROID_PLAY_STORE_UPLOAD_CHECKLIST.md` for `1.1.4` | Cheap, and a real process gap — whoever uploads the already-signed 1.1.4 AAB currently has no correct checklist | — | — | Yes (docs) | None | Yes |
| 8 | AND-4: verify the live document-upload success path against a synthetic/staging resident | Closes the single largest unverified surface in an otherwise fully-verified Android release | — | — | Yes | A safe synthetic resident account (already exists per prior sprint) | Yes |
| 9 | Production: remove/redirect the dangling `pgr.fmu.edu.pk` Caddy route | Config drift, currently 502ing, cheap cleanup | — | — | — | Confirm intent with fmu.edu.pk if in doubt | Yes |
| 10 | Production: review gunicorn worker count/timeout | Observed thin headroom under concurrent load during this pass's own inspection | — | — | — | A maintenance window if a restart is needed | Yes, review; schedule the change |
| 11 | P2-1: standardize the rotation field shape between `RotationAssignmentViewSet` and `ResidentSummaryView`'s embedded `rotation.current` | Removes a defensive-fallback pattern before a third client has to reinvent it | Yes | maybe (web already reads the standalone endpoint) | benefits (removes need for `.ifBlank` fallbacks) | None | Yes |
| 12 | Decide fate of legacy server-rendered dashboard views (BE-3, `/users/*-dashboard/`) | Best decided once BE-2 is fixed, since their most visible current symptom is BE-2's wrong count | Yes | — | — | Item 2 (BE-2) | After #2 |
| 13 | Web: page-level Jest tests for rotation-assignments, leave-requests, logbook, evaluations, supervision pages | Test what a real user can now reach | — | Yes | — | Item 3 (WEB-1), logically not technically | After #3 preferred |
| 14 | Web: consolidate duplicate change-password routes; resolve `/register` orphan (retire or formally re-enable) | Duplicated/dead UI surface, product decision needed | — | Yes | — | A product decision | Yes (decision), then implementation |
| 15 | Web: logbook status label — route through `lib/ui/status.ts`/`WorkflowStatusBadge` instead of raw enum | Terminology-lock compliance; naturally bundled with item 2 (both touch logbook) | — | Yes | — | Loosely coupled to #2 | Yes |
| 16 | Android: incrementally introduce ViewModels + Navigation-Compose | Soft architectural prerequisite before a 3rd/4th full CRUD domain is added; not a rewrite | — | — | Yes | None (soft: should precede #18) | Yes |
| 17 | Product decision: reactivate deferred training surface (research/thesis/workshops/submissions) for real client use, or formally retire it from contract docs | Currently "IMPLEMENTED, DEPRECATED-FROM-UI" — an explicit decision, not a technical task | decision | decision | decision | None | Yes (it's a decision, not code) |
| 18 | Android: build real Assessments/Research/Workshops submission UI (beyond current read-only summaries) | API already stable server-side; purely a scope/priority call once #17 is decided | — | — | Yes | Item 17 (product decision) | After #17 |
| 19 | Play Console upload of the already-signed `1.1.4` AAB | External console action | — | — | external | Item 7 (updated checklist) | After #7 |
| 20 | Full Playwright e2e regression run, extended to assert nav-reachability not just route response | Confirms items 3/13 end-to-end; establishes an ongoing regression gate | — | Yes | — | Item 3 preferred | After #3 preferred |

## Wave view

```
BUILD WAVE 0 — CRITICAL PLATFORM SAFETY
1. Rotate SECRET_KEY / DB_PASSWORD; scrub the committed .env.active from git history (deferred
   per user instruction, tracked as item 1 of the remediation plan)
2. Resolve the dual-LogbookEntry canonical-model conflict (BE-2)

BUILD WAVE 1 — EXISTING WORKFLOW HARDENING
3. Wire Logbook/Evaluations/reports/my-progress/monitoring/etc. into web navigation (WEB-1)
4. Repair contract documentation (API_CONTRACT.md logbook + roles sections, TERMINOLOGY.md,
   CANONICAL_ROUTE_MAP.md, CLAUDE.md's stale ResidentTrainingRecord warning)
5. Fix the disaster-backup directory-creation gap (BE-4)
6. Confirm/add file-upload content validation (security P2)
7. Update Android release docs for 1.1.4 (AND-1, AND-2)
8. Verify the live Android document-upload success path (AND-4)
9. Clean up the dangling pgr.fmu.edu.pk Caddy route
10. Review gunicorn worker headroom

BUILD WAVE 2 — DOMAIN & API COMPLETION
11. Standardize the rotation-field shape (P2-1)
12. Decide the fate of legacy server-rendered dashboard views (BE-3)
13. Reach an explicit product decision on the deferred research/thesis/workshops surface (item 17)

BUILD WAVE 3 — WEB COMPLETION
14. Page-level test coverage for the newly-nav-wired academics workflow pages
15. Consolidate duplicate change-password routes; resolve the /register orphan page
16. Logbook status-label reconciliation with the shared terminology system

BUILD WAVE 4 — PGR COMPANION PARITY
17. Incremental ViewModel + Navigation-Compose adoption in app-portal
18. Play Console upload of the signed 1.1.4 AAB (after Wave 1 item 7)
19. If Wave 2 item 13 decides to reactivate the deferred training surface: build Assessments/
    Research/Workshops submission UI against the already-stable backend endpoints

BUILD WAVE 5 — NEW FEATURE EXPANSION
20. Extend the Playwright e2e suite to assert nav-reachability, not just route-response
    correctness, and run it as a standing regression gate
21. Any genuinely new feature work — none was identified as blocked-and-ready in this pass beyond
    what's already listed above; new scope should be evaluated against this same dependency graph
    (`13_FEATURE_DEPENDENCY_GRAPH.md`) before being added to a future roadmap
```

## Why this order, in one paragraph

The platform is fundamentally healthy — clean tests, clean builds, sound RBAC, healthy production,
no P0s anywhere — so this is not a "stop and fix everything" situation. But two structural issues
sit upstream of a lot of otherwise-good work: a resolved-looking-but-actually-unresolved data model
split (BE-2, the same shape as the already-fixed `ResidentTrainingRecord` duplicate) that silently
corrupts milestone/reporting data, and a fully-built, fully-tested feature (Logbook + Evaluations
web UI) that's invisible to real users because of one missing wiring step (WEB-1). Both are cheap to
fix and disproportionately high-value, which is why they lead Wave 0/1 ahead of lower-stakes,
purely-additive work like Android's Assessments/Research/Workshops UI (which is explicitly gated on
a product decision, not a technical blocker, and can wait without cost).
