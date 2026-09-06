# SPRINT_STATE.md — Live Sprint Ledger

> **Purpose.** This file is the single resumable snapshot of the active sprint. If the current
> agent/session runs out of usage, crashes, or is otherwise cut off, the next agent should be able
> to read this file alone (plus the referenced docs) and continue without re-discovering context.
>
> **This is a living document, not a history log.** See "Maintenance rules" below — this is not a
> place to accumulate a permanent record; that belongs in `docs/implementation/` or `docs/_audit/`
> per `AGENTS.md` / `CLAUDE.md`. Keep this file short enough that reading it in full costs nothing.

## Maintenance rules (binding — see AGENTS.md §26a / CLAUDE.md / GEMINI.md)

1. **Update this file as part of the work, not after it.** When a pending task is finished, move it
   out of "Pending Work" immediately and collapse it to a one-line entry under "Completed Work" —
   do not leave both a stale pending item and a finished one describing the same thing.
2. **Prune aggressively.** Once a completed item is no longer load-bearing context for what's left
   (i.e. no pending task depends on knowing the detail), delete the line entirely rather than
   archiving it here. Detailed history lives in git log and `docs/implementation/`/`docs/_audit/`,
   not in this file.
3. **Pending Work must be step-wise and concrete** — each item should be something a fresh agent
   with no memory of this conversation could pick up and execute: what file/branch/command, not
   just a goal. Vague entries ("finish onboarding") are not acceptable; write the actual next
   action ("run X against staging resident Y, see doc Z for the request shape").
4. **One sprint, one file.** When a sprint ends (its scope statement is fully satisfied and Pending
   Work is empty), replace the whole file's content with the next sprint's scope rather than
   appending — do not let this file grow across sprints.
5. **This exists to avoid excessive commit/push churn.** Update this file freely without needing a
   commit for every edit; commit it alongside whatever code change it's tracking, not as a
   standalone "update status doc" commit unless nothing else changed.

---

## Current Sprint Scope

**Sprint:** PGR Companion Android — Closed Testing Stabilization → Institutional Workspace →
FMU Onboarding (full spec: milestones A–H, non-negotiable rules in §4 of the original spec —
preserve the generic offline app as a stable baseline; institutional/FMU connectivity is optional
and must never gate the generic app behind login).

**Repo location:** `android/` (package `pk.vexel.pgrcompanion`). Canonical backend:
`https://android.pgsims.alshifalab.pk` (production; source at `/home/munaim/srv/apps/pgsims` on the
`ssh test` VM, read-only reference only — never write there).

**Working branch:** `worktree-agent-a9805bd1ad56751c0` (worktree at
`.claude/worktrees/agent-a9805bd1ad56751c0`, currently **not merged into `main`**). Branch
`worktree-agent-a30c2d2abf06f0794` is a superseded earlier draft, already merged into the working
branch (commit `83a64f3`) — safe to delete once the working branch lands on `main`.

## Completed Work

- Milestones A–H all complete on the working branch (latest commit `f4e1938`).
- Baseline preserved: tag `play-closed-testing-baseline-1.0.0` → commit `f37469a` (versionCode 1 /
  versionName 1.0.0).
- Institutional Workspace foundation, FMU auth/onboarding client (`InstitutionalRepository.kt`),
  optional "Institution" tab, credential redaction, generic-app stabilization fixes — see
  `ANDROID_CURRENT_STATE.md`, `INSTITUTIONAL_WORKSPACE_ARCHITECTURE.md`,
  `PGR_SIMS_ANDROID_API_INTEGRATION.md` for detail (all up to date as of `f4e1938`).
- 1.1.0 (versionCode 2) release candidate: builds clean, 46 unit tests / lint pass, signed
  APK+AAB verified (`apksigner`/`keytool` cert digest `a858f42c...b61f010` confirmed correct),
  device-verified end-to-end on the **adforge (API 36) emulator only** — see
  `ANDROID_RELEASE_VERIFICATION.md`. **Final verdict: GO.**
- Backend production config audited for Android support (separate from the Android code work):
  confirmed `ALLOWED_HOSTS`/`DEBUG`/JWT/upload-size-limits/throttling/TLS were already correct;
  fixed one real gap — Caddy reverse-proxy timeout to `android.pgsims.alshifalab.pk` raised from
  the shared 30s default to a domain-scoped 120s (other sites on the shared VM untouched, verified
  via `caddy validate` + reload). Live on production.

## Pending Work

1. **Merge `worktree-agent-a9805bd1ad56751c0` into `main`.** Fast-forward or PR — branch is
   verified GO, working tree clean at `f4e1938`. Do this before anything else in this sprint;
   everything else is a follow-up on top of a merged `main`, not the worktree branch.
2. **Diff the release signing certificate against the Play Console registered upload key.**
   No Play Console access from this environment — needs a human with Play Console access to
   compare SHA-256 `a858f42c4460feab688e3e9fce28b3e9e0d5af03a555133e5e134f890b61f010` against the
   registered upload key fingerprint before the AAB is uploaded.
3. **Run one real document upload against a dedicated staging resident** (not the shared
   production demo account, which is in `APPROVED` review status and shouldn't be mutated for
   test purposes). This is the one write-path in `PGR_SIMS_ANDROID_API_INTEGRATION.md` that has
   only been verified by unit test + code reading, not a live `200` end-to-end run. If no staging
   resident exists yet, that's step zero here — check with backend owner or provision one via
   `manage.py` on a non-production instance.
4. **Update the Play Data Safety declaration** to match 1.1.0's actual behavior (now optionally
   transmits name/email/phone/user-ID, uploaded files, and auth credentials — credentials are
   not stored, only the encrypted session token is). Draft text is in
   `PGR_SIMS_ANDROID_API_INTEGRATION.md`. Needs a human with Play Console access to apply it.
5. **Housekeeping (low priority, do after 1–4):** delete the superseded worktree/branch
   `worktree-agent-a30c2d2abf06f0794` and its `.claude/worktrees/agent-a30c2d2abf06f0794` worktree
   directory once step 1 is done and nothing else references it.

**Once items 1–4 are done, this sprint is complete** — replace this file's content with the next
sprint's scope per Maintenance rule 4 rather than appending to it.
