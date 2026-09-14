# SPRINT_STATE.md — Android parity Stages 1–6 handoff

## Scope

Feature branch `feature/android-parity-stages-1-6` from `13f1bb7`. Push only; do not merge,
deploy, mutate VPS/production, enable FCM or change Caddy.

## Completed Work

- Reviewed `AGENTS.md` and `docs/PROJECT_ENVIRONMENT_CONTEXT.md`; laptop checkout is
  `/media/munaim/shared1/Documents/github/pgsims`, VPS is `ssh test` at
  `/home/munaim/srv/apps/pgsims`. Both began at `13f1bb7`; VPS was clean and unchanged.
- Stage 1: authoritative `/api/auth/me/` routing, password change/reset/app link, dynamic all-role
  completion, declaration, own profile and all-role Inbox with exact typed targets/nested-scroll fix.
- Stages 2–3: full logbook create/cancel, dynamic evaluation create/cancel, document defer,
  canonical progress, supervisor full detail/scoring and canonical rotation review.
- Stage 4 increment: ADMIN totals, paged/searchable/filterable universal users/details/create;
  SUPPORT_STAFF remains own-account/Inbox only.
- Stage 6 increment: synchronous owner-bound encrypted draft/upload metadata, retry state, stable
  client request IDs and orphan cleanup.
- Verification: Android 37 unit tests/lint/debug/debugAndroidTest PASS; rebuilt 1.1.8/code 8 APKs
  installed on `pgsims`; noncredentialed instrumentation `OK (10 tests)` and cold reset app link
  PASS. Backend focused 21 and full isolated 922 tests PASS; deployment-domain 3, Django check,
  Update 0 gate, disposable identity repair (`Users scanned: 0`, `Final status: PASS`) and canonical
  compose render PASS.
- Updated `android.md`, implementation status, canonical test addendum and verification ledger with
  precise completed/deferred/runtime boundaries.

## Pending Work

1. Before release, resolve the existing `makemigrations --check --dry-run` drift: notification
   index rename and historical leave `client_request_id` alteration. Do not generate them blindly.
2. With approved demo identities, run the authenticated four-role matrix in `android.md`: route
   gates, Inbox isolation/targets, workflow transitions, lost-response exactly-once and upload
   recovery. Never retain credentials/tokens.
3. Implement remaining unchecked roadmap rows: returned evaluation/leave edits, canonical
   supervisor queue/workload, role directories, document/supervision administration, reports/CSV
   and complete pagination. Academic master authoring, bulk mapping/import and backup/restore remain
   explicitly deferred.
4. Produce signed APK/AAB only after owner-controlled signing properties become available; physical
   device and Play validation remain deferred.

## Verdict

**CONDITIONAL GO** for branch review only. No merge or deployment authorization.
