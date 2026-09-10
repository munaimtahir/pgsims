# 01 — Repository Baseline

## Local repository (workstation)

```
Repository path: /media/munaim/shared1/Documents/github/pgsims
Current branch:  main
Local HEAD:      5686112 4aa6a9a73122c1e5f56f85fb5e6914cfb  "Freeze PGR Companion 1.1.4 release"
                 (2026-09-08 23:39:18 +0500)
origin/main:     in sync with local HEAD (git fetch --all --tags run at sprint start; "up to date")
Working tree:    clean except untracked `.claude/` (preserved, untouched, per SPRINT_STATE.md instruction)
```

Recent commit history on `main` (most recent first):
```
5686112 Freeze PGR Companion 1.1.4 release
4f8e276 Verify production logbook correction and release 1.1.4
26e0a21 Stabilize isolated backend test configuration
b8fe2db Prepare version 1.1.4 correction workflow E2E
eed072f Document PGR Companion production verification
```

## Branches

```
main                              — active, canonical
worktree-agent-a9805bd1ad56751c0  — stale local worktree branch, 25 commits BEHIND main, 0 commits
                                     ahead. Last commit f4e1938 "Document the verified 1.1.0
                                     candidate and the signing-key trap". Abandoned mid-sprint
                                     artifact from an earlier Android 1.1.0 cycle; safe to delete
                                     once confirmed unneeded — not touched in this discovery pass.
remotes/origin/HEAD -> origin/main
remotes/origin/main
```
No other remote branches exist. This is a single-branch working model in practice (`main`-only),
not a multi-branch dev/release flow — relevant to the branch/worktree strategy recommendation later
in this report.

## Tags (PGR Companion / platform relevant)

```
pgsims-utrmc-freeze-20260226      — pre-clean-room-model freeze point (historical)
play-closed-testing-baseline-1.0.0 — Android closed-testing baseline
v1.1.4                             — current Android release tag, matches HEAD
```

## Production baseline (cross-reference)

Full detail in `09_PRODUCTION_BASELINE.md` (separately verified via `ssh test`, read-only). Summary:
production is at `4f8e276` (1 commit behind local `main`; the gap is docs/scripts-only — Android
release notes + a gate script — no code or migration drift). All services healthy.

## Sprint context (from `SPRINT_STATE.md`)

The most recent completed sprint (documented in root `SPRINT_STATE.md`) expanded
`android/app-companion` from resident-foundation commit `ed1d137c` into a production resident client
(commits `96a5c4c`, `f081a6d`, both on `main`), verified end-to-end against production with a
synthetic resident/supervisor, and froze Android release `versionCode 4` / `1.1.4`. This is the
most current, most authoritative statement of "what just happened" in this repository and is
consistent with what this discovery pass independently found in `android/` (see
`09_ANDROID_ARCHITECTURE_AND_RELEASE.md`) and in production (see `09_PRODUCTION_BASELINE.md`).

## Untracked/uncommitted state

Only `.claude/` is untracked (tooling directory, intentionally out of scope, preserved per standing
instruction in `SPRINT_STATE.md`). No other uncommitted changes existed at the start of this
discovery sprint. No destructive git operations were run at any point during this sprint.
