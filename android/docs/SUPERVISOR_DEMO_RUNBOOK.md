# Supervisor Android — Demo Runbook (Read-only MVP)

Scope: login → role routing → dashboard → residents → resident detail. No approve/reject actions —
see `SUPERVISOR_API_CAPABILITY_MATRIX.md` for what's deferred and why.

## Demo supervisor

Use the account below — verified live against production on 2026-09-10 (see Verification section).
Do not commit its password anywhere else; it's the shared seeded-demo default for all Urology demo
accounts (`pgfmu123`), already known to whoever manages that dataset.

```
Username: supmuhammadakmal   (Prof. Dr. Muhammad Akmal)
Department: Urology Department, Allied Hospital-I Faisalabad
Assigned residents: 5
Pending: 1 rotation approval (Rotations card), 0 elsewhere at time of verification
```

Any of the other four canonical Urology supervisors (usernames follow the same
`sup<firstlast>` pattern) will show the same UI shape with different counts.

## Demo A — Login and role routing

1. Open PGR Companion.
2. Sign in with the demo supervisor's username/password.
3. The app routes automatically to the Supervisor Home screen (bottom nav: Home / Residents /
   Profile) — no manual role selection. A resident account signing in the same way still lands on
   the existing resident Home/Training/Logbook/Requirements/Profile nav, unchanged.

## Demo B — Dashboard

On Supervisor Home, point out:
- "My Residents" and "Pending Approvals" stat cards, computed from the live backend, not hardcoded.
- The Workflows list (Logbook, Research/Synopsis, Leave Requests, Rotations, Evaluations), each
  showing "N pending" or "No pending items" — never "0 pending".
- The note under the list explaining that approve/reject live on web for now.

## Demo C — My Residents

1. Tap **Residents**.
2. Show the search box filtering by name.
3. Point out each resident's programme and (where available) IMM/Final eligibility and current
   rotation, all pulled from `/api/supervisors/me/summary/`.

## Demo D — Resident detail

1. Tap any resident row.
2. Show Training (programme, degree, induction date, month index), Current Posting, Progress
   (research/thesis/workshops), and Milestone Eligibility (IMM/Final) — all from
   `/api/supervisors/residents/{id}/progress/`, fetched fresh for that resident.
3. Tap "← Back to residents" to confirm the drill-down state resets cleanly.

## Demo E — Regression: resident login unaffected

Sign out, then sign back in as any resident account (e.g. `pgrdrmuhammadadeelbas` /
`pgfmu123`) to show the pre-existing resident experience is untouched by this change.

## Verification (2026-09-10)

```
Backend/Android build: c5a77c4 (laptop + VPS in sync, clean tree)
Android compile:                PASS  (:app-companion:compileDebugKotlin)
Android unit tests:              PASS  (24 tests, incl. 3 new supervisor-snapshot/detail tests)
Android debug APK assembled:     PASS
Emulator:                        pgsims, installed pk.vexel.pgrcompanion.debug
Supervisor login:                PASS (supmuhammadakmal)
Role routing to Supervisor Home: PASS
Dashboard counts vs live API:    PASS (5 residents, 1 pending rotation — matched curl against
                                  /api/supervisors/me/summary/ and
                                  /api/academics/monitoring/supervisor-dashboard/)
Residents list vs live API:      PASS (5 residents, names/programmes matched)
Resident detail vs live API:     PASS (training/rotation/research/thesis/workshops/eligibility
                                  matched /api/supervisors/residents/{id}/progress/)
Sign out:                        PASS
Resident login regression:       PASS (pgrdrmuhammadadeelbas — existing nav/screens unaffected)
Cross-client check:              N/A this pass — no mutations were made from Android to verify
                                  against web (read-only MVP)
Android instrumentation:         Not run (JVM unit tests + manual emulator walkthrough only)
```

## Known gaps (by design, this pass)

- No approve/reject/revision anywhere in Android yet — see capability matrix.
- Supervisor's own department/hospital name isn't shown on the header: `SupervisorProfileSerializer`
  returns `hospital`/`department_ref` as raw FK ids, not nested names, and no endpoint already
  fetched by this MVP resolves them to text. Resolving them would need an extra lookup call; skipped
  to keep this pass read-only-and-quick as scoped.
- `must_change_password` isn't surfaced on the Supervisor screens (it is on the resident Home
  screen). Cosmetic gap, not a blocker — the seeded demo account still authenticates and functions
  normally with `must_change_password: true`.
