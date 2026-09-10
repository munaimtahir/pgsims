# 00 — Executive Summary

## A. Repository baseline

```
Local HEAD:     56861124aa6a9a73122c1e5f56f85fb5e6914cfb "Freeze PGR Companion 1.1.4 release"
origin/main:    in sync with local HEAD
Working tree:   clean except untracked .claude/ (preserved, untouched)
Branches:       main (active); worktree-agent-a9805bd1ad56751c0 (stale, 25 behind, 0 ahead, abandoned)
PGR Companion:  tag v1.1.4 at HEAD, versionCode 4
```
Full detail: `01_REPOSITORY_BASELINE.md`.

## B. Production baseline

```
Production SHA:       4f8e276 (1 commit behind main; drift is docs/scripts-only, no code/migration)
Production web:       pgsims.alshifalab.pk, pgsims.pmc.edu.pk, pg.fmu.edu.pk
Production Android API: android.pgsims.alshifalab.pk / api.pgsims.alshifalab.pk / api.pgsims.pmc.edu.pk
Service health:        All 6 prod services healthy; 106/106 migrations applied, 0 pending
Repository drift:      Minimal, non-urgent (see above)
```
Full detail: `09_PRODUCTION_BASELINE.md`.

## C. Backend status

- **Stable**: identity/RBAC, org graph, rotations, leave requests, notifications, audit,
  backup/DR (except one directory-creation bug), the real (`academics`) logbook workflow. 1190/1191
  tests pass, `manage.py check`/`makemigrations --check` both clean.
- **Partial / needs hardening**: `ResidentMilestoneEligibility` and progress-threshold computation
  (BE-2 — reads the wrong, bulk-import-only `LogbookEntry` model, not the real one), disaster-backup
  directory creation (BE-4), one legacy server-rendered dashboard surface with stale output (BE-3).
- **Broken**: none found.
- **Missing**: nothing expected-and-absent found; the "deferred" research/thesis/workshops surface
  is intentionally dark, not missing.

## D. Web status

- **Stable**: Authentication, onboarding, profile, rotation-assignments, leave-requests,
  supervision, admin/masters CRUD, dashboards — all pass typecheck/lint/test/build cleanly.
- **Defective**: none functionally broken.
- **Partial**: Logbook and Evaluations (and 8 other academics pages) are fully built,
  fully API-correct, but **unreachable via navigation** (WEB-1) — the single most consequential web
  finding of this pass.
- **Missing**: research/thesis/workshops web UI (intentionally deferred, matches backend/product
  intent).

## E. PGR Companion status

- **Complete**: Authentication, Home, Profile, Training, Rotations, Supervision, Logbook —
  production-verified per the just-closed 1.1.4 sprint, independently reconfirmed in this pass.
- **Partial**: Documents (live upload success path never executed against production, AND-4).
- **Missing/read-only**: Assessments, Research, Workshops — summary counts only, no submission UI
  (a scope gap, not a backend blocker).
- **Production connectivity**: confirmed live and correct.
- **Quality gates**: 24/24 unit tests pass, 0 lint errors, CI (`android-companion-gates`) wired and
  current. Play Console upload of the signed `1.1.4` AAB is the one step not yet done, and its
  checklist doc is stale (AND-1).

## F. Critical issues

- **P0**: none found anywhere in this pass (backend, web, Android, production, security).
- **P1**:
  - XC-1 — a real-shaped `SECRET_KEY`/`DB_PASSWORD` committed to git, present at HEAD (deferred per
    explicit user instruction; tracked as remediation item 1, not resolved in this sprint).
  - BE-2 — dual, unsynced `LogbookEntry` models; the real product workflow's data is invisible to
    milestone-threshold logic and a legacy pending-count dashboard.
  - WEB-1 — Logbook/Evaluations/reports built but unreachable via any in-app navigation.
  - P1-1/P1-2 (contract drift) — `API_CONTRACT.md`'s logbook and roles sections are stale relative
    to shipped code.
  - AND-1 — Play Store upload checklist not updated for the already-signed `1.1.4` release.
- **P2 / P3**: see `12_BUG_TECH_DEBT_REGISTER.md` for the full itemized register (BE-1/BE-3/BE-4,
  WEB-2..9, AND-2..7, XC-2/XC-3, plus the security review's 4 low-severity items).

## G. Contract readiness

| Domain | Classification |
|---|---|
| Auth | STABLE |
| Profile / Onboarding | STABLE |
| Documents | NEEDS HARDENING (upload content-validation unconfirmed; Android live-path unverified) |
| Training | STABLE (post-BE-1 correction: the record model itself is fine; BE-2 is a downstream logbook issue, not a training-record issue) |
| Rotations | STABLE (P2-1 field-shape standardization recommended, not blocking) |
| Supervision | STABLE |
| Logbook | **INCOMPLETE as documented, STABLE as implemented** — the live code (both academics.LogbookEntry and its web/Android consumers) works correctly; the written contract and one backend-internal dependency (BE-2) do not match it |
| Assessments / Research / Workshops | INCOMPLETE by design (deferred-from-UI, backend IMPLEMENTED) |

## H. Exact build order

See `15_BUILD_ORDER_AND_ROADMAP.md` for the full 20-item table. Summary:
```
Wave 0: credential rotation (deferred) + resolve the dual-LogbookEntry model conflict
Wave 1: wire built-but-unreachable web pages into navigation; repair contract docs; small backend/
        Android/production hardening items
Wave 2: rotation field-shape standardization; legacy dashboard disposition; deferred-surface
        product decision
Wave 3: web test coverage + cleanup for newly-reachable pages
Wave 4: Android architecture groundwork (ViewModels/Nav-Compose), Play Console upload, conditional
        Assessments/Research/Workshops UI
Wave 5: e2e regression hardening; any new scope evaluated against the dependency graph first
```

## I. Parallel development plan

See `14_PARALLEL_DEVELOPMENT_MATRIX.md`. In short: Lane A (backend+web) and Lane B (Android) have
almost no live coupling right now — Android already reads/writes the correct backend models
directly and doesn't touch web navigation, so both lanes can run their Wave 0/1 items fully in
parallel. The one real cross-lane dependency is that Android's next *feature* sprint (Assessments/
Research/Workshops) needs a product decision that also affects Lane A's contract-doc scope.

## J. Immediate next sprint

**"Logbook Canonicalization and Workflow Reachability"** — fix BE-2 and WEB-1 together (both touch
logbook), repair the contract docs in the same pass, and close the small Android doc/verification
items in parallel. Full scope in `16_NEXT_SPRINT_RECOMMENDATION.md`.

## K. Following 3-5 sprints

1. Contract self-verification (stop `API_CONTRACT.md` from silently drifting again)
2. Rotation contract standardization + legacy dashboard retirement
3. Product decision on the deferred research/thesis/workshops surface
4. (Conditional) PGR Companion Assessments/Research/Workshops parity

Full detail in `16_NEXT_SPRINT_RECOMMENDATION.md`.
