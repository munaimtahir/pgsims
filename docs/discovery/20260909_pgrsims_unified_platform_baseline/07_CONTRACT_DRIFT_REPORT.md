# Contract Drift Report

Compares `docs/contracts/API_CONTRACT.md` / `docs/contracts/TERMINOLOGY.md` against verified
current source (`backend/sims/*/urls.py`, `views.py`, `serializers.py`, `models.py`,
`frontend/lib/api/*.ts`, `android/app-portal/**/*.kt`) at HEAD `5686112` on 2026-09-09.
**All findings below were verified by reading actual code, not inferred.** Ranked P0 (highest) to
P3.

## P1-1 — `docs/contracts/API_CONTRACT.md` "LogbookEntry (Feature Layer Active Surface)" section is entirely stale for the route, status-action, and field surface

- **Doc claims** (`API_CONTRACT.md:14-42`): base route `/api/logbook/`; fields
  `feedback` (alias of `supervisor_feedback`), `submitted_to_supervisor_at` (alias of
  `submitted_at`), `returned_at`, `approved_at`; review endpoint `POST /api/logbook/{id}/review/`
  with payload `{action: "approved"|"returned", feedback}`; `GET /api/logbook/review-queue/`,
  `GET /api/logbook/my-threshold/`.
- **Actual code**: real route is `/api/academics/logbook-entries/` (mounted via
  `sims/academics/workflow_urls.py` router, included at `path("api/academics/", ...)` in
  `sims_project/urls.py:174`). `LogbookEntrySerializer`
  (`backend/sims/academics/serializers.py:347-373`) exposes `submitted_at`, `verified_at`,
  `supervisor_comments` — there is no `feedback`, `supervisor_feedback`,
  `submitted_to_supervisor_at`, `returned_at`, or `approved_at` field anywhere on this serializer.
  State transitions are five separate actions on `LogbookEntryViewSet`
  (`backend/sims/academics/views.py:598-637`): `submit`, `verify`, `return_revision`, `reject`,
  `cancel` — not a single `review` action with an `action` payload discriminator. There is no
  `review-queue` or `my-threshold` route registered anywhere in `workflow_urls.py`.
- **Impact**: this is the single most recently-shipped and most actively developed feature in the
  repo (per `SPRINT_STATE.md`, the just-closed sprint centered on Android logbook draft/edit/submit
  against production). The web client (`frontend/lib/api/academics.ts:347-355`) and the actual
  backend are fully consistent with each other and with each other's real route/fields/actions —
  **only the contract document is wrong**. Any future agent or developer reading
  `API_CONTRACT.md` for logbook integration (including a future Android reviewer) would build
  against a nonexistent API.
- **Recommendation**: rewrite `API_CONTRACT.md`'s LogbookEntry section from
  `sims/academics/serializers.py:347` / `views.py:493-637` directly. This is small, low-risk,
  discovery-blocking-adjacent documentation repair — a reasonable candidate for the "small
  remediation" allowance in this sprint if the user wants it fixed immediately; otherwise it is
  BUILD WAVE 0/1 work (see `15_BUILD_ORDER_AND_ROADMAP.md`).

## P1-2 — `docs/contracts/API_CONTRACT.md` "Roles (locked)" section names a role model that no longer exists in code

- **Doc claims** (`API_CONTRACT.md:7-12`): roles are `pg`, `supervisor`, `admin`, `utrmc_user`,
  `utrmc_admin`.
- **Actual code**: `backend/sims/users/models.py:11-13` — `User.role` choices are exactly
  `RESIDENT`, `SUPERVISOR`, `ADMIN`, `SUPPORT_STAFF` (matches CLAUDE.md's declared clean-room
  4-role model). `utrmc_admin` and `utrmc_user` survive only as **semantic labels in code
  comments/test helper names** mapped onto `ADMIN`/`SUPPORT_STAFF` respectively — e.g.
  `sims/training/test_feature_layer_ops.py:59-60`:
  `make_user("fl_utrmc_admin", "ADMIN")`, `make_user("fl_utrmc_user", "SUPPORT_STAFF")`. `pg` does
  not appear as a live role value anywhere in `sims/training/*.py` role-gating logic (it does
  appear later in `API_CONTRACT.md` itself, e.g. "Roles: pg/resident" — internally inconsistent
  with its own opening section, since `pg` isn't a role value at all in the current model).
- **Impact**: medium — code correctly enforces the real 4-role model regardless of what this doc
  says, so no live security exposure. But it is misleading for anyone using this file as the
  integration source of truth (its literal purpose per CLAUDE.md's "Contract-first integration"
  section), and directly contradicts CLAUDE.md and `docs/CANONICAL_SOURCE_OF_TRUTH.md` in the same
  repo without any cross-reference or deprecation note.
- **Recommendation**: replace the "Roles (locked)" section with the 4-role model and add a note
  that `utrmc_admin`/`utrmc_user`/`hod` are semantic labels for `ADMIN`/`SUPPORT_STAFF`/
  `SupervisorProfile.designation`, not literal enum values, matching CLAUDE.md's own framing.

## P2-1 — Dual rotation-field shape is real but only reconciled defensively on the Android side

- Web's `RotationAssignment` type (`frontend/lib/api/rotations.ts:34-52`) declares
  `hospital_name`/`department_name` as flat serializer fields. The embedded
  `rotation.current` object inside `/api/residents/me/summary/` (the endpoint Android actually
  consumes, per `training/views.py::ResidentSummaryView`) is not guaranteed to carry the same flat
  field names consistently — Android's `ResidentWorkflowScreens.kt` defends against this with
  `.ifBlank { rotation.value("department_name") }` fallback chains at lines 65, 124, 126, 144
  (verified by reading the file). This matches what `SPRINT_STATE.md` describes as "corrected" —
  but the fix was a client-side defensive read, not a backend serializer unification. The
  underlying two-shapes-for-one-concept condition still exists in the backend and will resurface
  for any next Android consumer (or a future summary-endpoint refactor) that doesn't know to
  defend against it the same way.
- **Recommendation**: either standardize `ResidentSummaryView`'s embedded rotation payload to the
  same field set as the standalone `RotationAssignmentViewSet` serializer, or explicitly document
  the divergence in `docs/contracts/DATA_MODEL.md` so it's a known, intentional contract rather
  than tribal knowledge encoded only in Android fallback chains.

## P2-2 — Dual current-user endpoints, undocumented as a client-selection rule

`/api/auth/profile/` (web) and `/api/auth/me/` (Android + admin tooling) are two different
payload shapes for "who am I," which `API_CONTRACT.md:369-371` does explain exists intentionally —
but nothing tells a new Android or web developer *which one their client should call and why*.
Low risk since both are stable and already correctly used by their respective clients today; worth
a one-line rule in `docs/contracts/API_CONTRACT.md` ("web uses `/profile/`, native clients use
`/me/`") so the next client integration doesn't guess.

## P3 — Deferred/legacy surface still fully routed

Research, thesis, workshops, submissions/synopsis/certificates, deputation postings, and rotation
phase-1 completion-verification endpoints are still live in `sims/training/urls.py` (confirmed,
not stubs) but intentionally dark from both web and Android navigation. `API_CONTRACT.md` already
labels these "not part of active release-gated UI" — no drift here, just a reminder for
`13_FEATURE_DEPENDENCY_GRAPH.md` and `15_BUILD_ORDER_AND_ROADMAP.md` not to plan new client work
against this surface without an explicit reactivation decision.

## Terminology aliasing check (`docs/TERMINOLOGY.md`)

The `pending`→"Submitted" UI-display aliasing and `supervisor_feedback`→`feedback` aliasing that
`docs/TERMINOLOGY.md` and `API_CONTRACT.md:18-19` describe as canonical **do not correspond to any
live field on the actual `LogbookEntry` model** (see P1-1) — the real field is
`supervisor_comments`, never renamed/aliased anywhere in `academics/serializers.py`. This
aliasing description appears to be inherited from an earlier logbook implementation that predates
the current `sims.academics.LogbookEntry` surface. Recommend auditing `docs/TERMINOLOGY.md` in the
same pass as `API_CONTRACT.md`'s logbook section.

## Contract surface verdict

**NOT STABLE FOR CLIENTS as currently documented** — not because the live API is unstable (it
verifiably is not: web and Android both work against the real logbook/rotation surface correctly
today, per source and per `SPRINT_STATE.md`'s production E2E verification) but because the
written contract (`API_CONTRACT.md`) that's supposed to be the integration source of truth per
CLAUDE.md is wrong for the two domains (logbook, roles) most likely to be touched next. Any new
client work (Android parity expansion, a new web feature) that trusts this doc instead of reading
source will build against the wrong shape. This elevates P1-1/P1-2 into BUILD WAVE 0/1 candidates
despite being "just documentation," per CLAUDE.md's own rule: "If a code change alters a payload
shape, route, or user-facing term, update the relevant contract file in the same change — don't
ship silent drift" — that rule was violated by the logbook work in the just-closed sprint (correct
code shipped, contract doc never updated to match).
