# 16 — Next Sprint Recommendation

## RECOMMENDED IMMEDIATE IMPLEMENTATION SPRINT

**"Logbook Canonicalization and Workflow Reachability"**

### Primary outcome
Every logbook-adjacent data path in the platform reads and writes the same model, and every
already-built academics workflow page (Logbook, Evaluations, reports, progress/monitoring views) is
reachable through real in-app navigation for the roles that need it.

### Backend scope
- Resolve BE-2: repoint `_evaluate_logbook_thresholds()` (`sims/training/views.py`) and
  `sims/bulk/services.py`'s logbook import path at `sims.academics.LogbookEntry`. Decide whether
  `sims.training.LogbookEntry` is retired outright or explicitly re-scoped to a narrower purpose
  (if any real reason to keep it separately is found during implementation — none was found in this
  discovery pass).
- Fix `get_documents_pending_count()` (`sims/users/models.py`) to query the correct model, or retire
  it alongside a decision on BE-3 (legacy dashboard views).
- BE-4: add `os.makedirs(..., exist_ok=True)` (or equivalent) before
  `create_disaster_recovery_backup()` writes its zip file.
- Confirm/close the file-upload content-validation gap (security P2).

### Web scope
- WEB-1: add `navRegistry.ts` entries and dashboard links for Logbook, Evaluations,
  my-progress, monitoring, supervisor-workload, reports/*, workflow-overview, workflow-data-quality
  — scoped per role per the existing RBAC matrix, not blanket-exposed.
- Route Logbook's status display through `lib/ui/status.ts`/`WorkflowStatusBadge` instead of the raw
  backend enum (bundled with the BE-2 work since both touch the same feature).
- Repair `docs/contracts/API_CONTRACT.md` (logbook + roles sections), `docs/TERMINOLOGY.md`
  (logbook aliasing), `docs/CANONICAL_ROUTE_MAP.md`/`CANONICAL_FRONTEND_ROLE_MATRIX.md`
  (regenerate from `frontend/app/`), and `CLAUDE.md`'s stale `ResidentTrainingRecord` warning.

### Android scope
- AND-1/AND-2: update `android/README.md` and `ANDROID_PLAY_STORE_UPLOAD_CHECKLIST.md` for `1.1.4`.
- AND-4: run the live document-upload success path once against the existing synthetic resident.
- No new Android feature work in this sprint — Android is release-ready and its next real
  work (Assessments/Research/Workshops UI) is correctly gated on a separate product decision (see
  parallel work below), not on anything in this sprint.

### Production scope
- No deploy strictly required to *start* this sprint (production is healthy, 1 commit behind on
  docs only). Once the backend/web fixes above are merged and tested, bundle them into one routine
  deploy rather than piecemeal hotfixes.
- Separately and in parallel: clean up the dangling `pgr.fmu.edu.pk` Caddy route, review gunicorn
  worker headroom.

### Dependencies
- None of this sprint's items block on each other in a hard sense except: the web status-label fix
  is best sequenced alongside the BE-2 backend fix (same feature, same PR is reasonable); BE-3's
  disposition is best decided after BE-2 lands (its symptom changes once BE-2 is fixed).

### Parallel work
See "PARALLEL ANDROID WORK" below — Android's doc/verification items run fully in parallel with the
backend/web work above; the Play Console upload can happen as soon as the doc-checklist fix lands,
independent of everything else in this sprint.

### Acceptance gates
- `pytest sims -q` stays green (currently 1190/1191 passing; BE-4's fix should bring it to
  1191/1191).
- `npm run typecheck && npm run lint && npm test && npm run build` stay green (currently all pass).
- Manual/E2E check: a RESIDENT-role test user can navigate to Logbook and Evaluations from their
  dashboard without typing a URL; a SUPERVISOR-role test user's "pending review" count reflects a
  real submitted-and-unreviewed logbook entry created through the actual UI (not the old, wrong
  count).
- `:app-companion:testDebugUnitTest :app-companion:lintDebug` stay green (currently 24/24, 0 lint errors).
- `docs/contracts/API_CONTRACT.md`'s logbook and roles sections match `sims/academics/serializers.py`
  / `sims/users/models.py` verbatim (spot-checked, not just self-attested).

---

## PARALLEL ANDROID WORK

While the primary sprint runs (Lane A: backend + web), Android (Lane B) should:
1. Land the AND-1/AND-2 doc fixes and AND-4 verification (small, independent, no coordination
   needed with Lane A).
2. Begin incremental ViewModel + Navigation-Compose adoption (AND-3) — architectural groundwork that
   doesn't depend on anything in the primary sprint and reduces risk for the *next* Android sprint
   (Assessments/Research/Workshops UI, once that's product-approved).
3. Upload the signed `1.1.4` AAB to Play Console once its checklist is current (step 1 above).

This is explicitly the moment Android can move independently: its current scope has no live
dependency on the LogbookEntry/nav-reachability work happening in Lane A, since Android already
reads/writes the correct `academics.LogbookEntry` model directly and doesn't touch web navigation at
all.

**Blocked until completion of this sprint (or a separate decision):**
- Any new backend/web work that extends milestone/eligibility reporting should wait for BE-2 to
  land — building on top of the currently-wrong dependency edge would just create more to unwind
  later.
- Android's Assessments/Research/Workshops full-CRUD UI work should wait not for this sprint, but
  for the separate product decision on reactivating that surface (Build Wave 2, item 13 in
  `15_BUILD_ORDER_AND_ROADMAP.md`) — independent of this sprint's timeline either way.

---

## FOLLOWING 3-5 SPRINTS

### Sprint 2 — "Contract Self-Verification"
- **Outcome**: `API_CONTRACT.md` can no longer silently drift the way it did for logbook this cycle.
- **Backend/Web**: either wire `API_CONTRACT.md` generation into the existing
  `integration-truth-map` CI job (so it's checked the same way `INTEGRATION_TRUTH_MAP.md` already
  is), or formally deprecate it in favor of the auto-generated truth map as CLAUDE.md's designated
  integration source of truth.
- **Android**: none.
- **Production**: none.
- **Dependencies**: none on Sprint 1, can start in parallel once scoped.
- **Parallel work**: Android can continue its architecture groundwork.
- **Acceptance gates**: CI fails if `API_CONTRACT.md` (or its replacement) disagrees with the live
  truth-map extraction.

### Sprint 3 — "Rotation Contract Standardization + Legacy Dashboard Retirement"
- **Outcome**: one rotation field shape everywhere; a decision executed on `BE-3`'s legacy
  server-rendered dashboards.
- **Backend**: standardize `ResidentSummaryView`'s embedded rotation payload against
  `RotationAssignmentViewSet`'s serializer (P2-1); execute the BE-3 decision (retire or fix).
- **Web**: remove any now-unnecessary defensive handling if web ever needed similar fallbacks
  (verify during implementation).
- **Android**: remove the now-unnecessary `.ifBlank` fallback chains in
  `ResidentWorkflowScreens.kt` once the backend shape is unified (small, low-risk cleanup).
- **Dependencies**: Sprint 1 (BE-2/BE-3 context).
- **Acceptance gates**: Android unit tests still pass with fallback chains removed; no behavior
  change observed in a synthetic-resident E2E pass.

### Sprint 4 — "Product Decision: Deferred Training Surface"
- **Outcome**: an explicit, documented decision on research/thesis/workshops/submissions/deputation
  postings — reactivate for real client use, or formally retire from `API_CONTRACT.md` as dead
  surface rather than "IMPLEMENTED, DEPRECATED-FROM-UI" indefinitely.
- This is a decision sprint, not primarily an implementation one — output is a DECISION_LOCK doc
  per the repo's existing `docs/implementation/` convention, plus whatever minimal code follows
  from it (e.g. actually deleting dead routes if the decision is to retire).
- **Dependencies**: none technical; needs the product owner.
- **Parallel work**: both Lane A and Lane B continue whatever's left from Sprints 1-3.

### Sprint 5 (conditional on Sprint 4's decision) — "PGR Companion Assessments/Research/Workshops Parity"
- **Outcome**: if Sprint 4 decides to reactivate the deferred surface, Android gets real
  submission/detail screens for Assessments, Research, and Workshops (currently read-only summaries)
  against the already-stable backend endpoints identified in `06_PLATFORM_API_CONTRACT_MATRIX.md`.
- **Android**: build on top of the ViewModel/Navigation-Compose groundwork from Sprint 1's parallel
  work; no backend blocker expected given current API maturity.
- **Web**: symmetric consideration — decide whether these should also get web nav entries (they
  currently don't exist as web pages at all beyond `evaluation-templates`).
- **Dependencies**: Sprint 4's decision.
- **Acceptance gates**: full E2E on a synthetic resident for each newly-activated domain, same rigor
  as the logbook E2E work in the just-closed 1.1.4 sprint.
