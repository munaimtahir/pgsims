# Restart/Reseed Smoke Blocker 4 Scope

Date: 2026-05-17
Branch: `codex/dead-code-cleanup`
Commit: `e21ec23`

## PRIMARY PURPOSE

Fix blocker #4: restart/reseed smoke status unknown.

## IN-SCOPE

- Ensure Docker local env has required variables for local restart/reseed.
- Rebuild backend/frontend/worker/beat images from current code.
- Start the stack from a stopped state.
- Run seed commands through `scripts/e2e_seed.sh`.
- Verify health checks.
- Run Playwright smoke and active-surface tests.

## OUT-OF-SCOPE

- Coverage gate closure.
- Route/contract changes.
- New workflows.
- Production deployment changes.

