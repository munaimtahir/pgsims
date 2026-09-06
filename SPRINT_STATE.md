# SPRINT_STATE.md — Live Sprint Ledger

> **Purpose.** This file is the single resumable snapshot of the active sprint. If the current
> agent/session runs out of usage, crashes, or is otherwise cut off, the next agent should be able
> to read this file alone (plus the referenced docs) and continue without re-discovering context.
>
> **This is a living document, not a history log.** See "Maintenance rules" below — this is not a
> place to accumulate a permanent record; that belongs in `docs/implementation/` or `docs/_audit/`
> per `AGENTS.md` / `CLAUDE.md`. Keep this file short enough that reading it in full costs nothing.

## Maintenance rules (binding — see AGENTS.md §26 / CLAUDE.md / GEMINI.md §19)

1. **Update this file as part of the work, not after it.** When a pending task is finished, move it
   out of "Pending Work" immediately and collapse it to a one-line entry under "Completed Work" —
   do not leave both a stale pending item and a finished one describing the same thing.
2. **Prune aggressively.** Once a completed item is no longer load-bearing context for what's left
   (i.e. no pending task depends on knowing the detail), delete the line entirely rather than
   archiving it here. Detailed history lives in git log and `docs/implementation/`/`docs/_audit/`,
   not in this file.
3. **Pending Work must be step-wise and concrete** — each item should be something a fresh agent
   with no memory of this conversation could pick up and execute: what file/branch/command, not
   just a goal.
4. **One sprint, one file.** When a sprint ends (its scope statement is fully satisfied and Pending
   Work is empty), replace the whole file's content with the next sprint's scope rather than
   appending — do not let this file grow across sprints.
5. **This exists to avoid excessive commit/push churn.** Update this file freely without needing a
   commit for every edit; commit it alongside whatever code change it's tracking.

---

## Current Sprint Scope

**Sprint:** PGR Companion Android — Closed Testing Stabilization → Institutional Workspace →
FMU Onboarding (milestones A–H; non-negotiable rule: the generic offline app stays the stable
baseline, institutional/FMU connectivity is optional and never gates it behind login).

**Repo location:** `android/` (package `pk.vexel.pgrcompanion`). Canonical backend:
`https://android.pgsims.alshifalab.pk` (production).

## Completed Work

- **Merged to `main`** at `ce1d636` (release candidate code) + `d08d320` (gate script fix) — no
  longer sitting on a worktree branch. `versionCode 2` / `versionName "1.1.0"`.
- Milestones A–H complete: baseline tag `play-closed-testing-baseline-1.0.0` → `f37469a`;
  Institutional Workspace foundation, FMU auth/onboarding client (`InstitutionalRepository.kt`,
  `InstitutionalScreen.kt`, `Onboarding.kt`), optional "Institution" tab, credential redaction,
  generic-app stabilization — detail in `ANDROID_CURRENT_STATE.md`,
  `INSTITUTIONAL_WORKSPACE_ARCHITECTURE.md`, `PGR_SIMS_ANDROID_API_INTEGRATION.md`.
- **Re-verified on `main` post-merge (2026-09-06):** `./gradlew clean :app:testDebugUnitTest
  :app:lintDebug` — BUILD SUCCESSFUL, all tests/lint pass. `:app:assembleRelease
  :app:bundleRelease -PpgrCompanionSigningPropertiesFile=/home/munaim/.config/pgr-companion/signing/signing.properties`
  — BUILD SUCCESSFUL. `apksigner verify --print-certs` confirms SHA-256
  `a858f42c4460feab688e3e9fce28b3e9e0d5af03a555133e5e134f890b61f010`, `CN=Vexel Consultants` —
  the correct upload key (not either of the two wrong lookalikes documented in
  `ANDROID_RELEASE_VERIFICATION.md`). Signature verified VALID. Artifacts at
  `android/app/build/outputs/apk/release/app-release.apk` and
  `android/app/build/outputs/bundle/release/app-release.aab`.
- Fixed `scripts/check_pgr_companion_release.sh`: (a) updated its version/label checks for 1.1.0
  and the institutional workspace surface, (b) fixed a real bug where the forbidden-pattern check
  used `rg` via `xargs`, and on a machine without ripgrep installed the `!`-negated pipeline
  silently reported a false pass instead of actually failing. Now uses `grep`, verified working.
- Backend production config audited and fixed: `android.pgsims.alshifalab.pk`'s Caddy reverse-proxy
  timeout raised from the shared 30s default to a domain-scoped 120s (for large mobile document
  uploads), applied and verified live; no other production site affected.
- Superseded worktree/branch `worktree-agent-a30c2d2abf06f0794` deleted.

## Pending Work

1. **Diff the release signing certificate against the Play Console registered upload key.**
   No Play Console access from this environment — needs a human to compare SHA-256
   `a858f42c4460feab688e3e9fce28b3e9e0d5af03a555133e5e134f890b61f010` against the registered
   upload key fingerprint before the AAB (`android/app/build/outputs/bundle/release/app-release.aab`)
   is uploaded.
2. **Run one real document upload against a dedicated staging resident** (not the shared
   production demo account, which is in `APPROVED` review status). This is the one write-path
   verified only by unit test + code reading, not a live `200` end-to-end run — see
   `PGR_SIMS_ANDROID_API_INTEGRATION.md`. If no staging resident exists, provisioning one is step
   zero.
3. **Update the Play Data Safety declaration** to match 1.1.0's actual behavior (optionally
   transmits name/email/phone/user-ID, uploaded files, and auth credentials for authentication —
   credentials are not stored, only the encrypted session token is). Draft text in
   `PGR_SIMS_ANDROID_API_INTEGRATION.md`. Needs a human with Play Console access.
4. **Housekeeping (trivial, no rush):** `.claude/worktrees/agent-a9805bd1ad56751c0` is still
   present/lock-held by its (now-completed) agent record even though its branch is fully merged —
   remove it with `git worktree remove -f -f .claude/worktrees/agent-a9805bd1ad56751c0 && git branch -D worktree-agent-a9805bd1ad56751c0`
   once you've confirmed no agent is still attached to it.

**Once items 1–3 are done, this sprint is complete** — replace this file's content with the next
sprint's scope per Maintenance rule 4 rather than appending to it.
