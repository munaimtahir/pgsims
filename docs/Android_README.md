# PGR SIMS Android Documentation Pack

This pack contains the locked product policy, MVP scope, production roadmap, initial scaffold prompt, and Phase M0 discovery prompt for the PGR SIMS Android application.

## Intended placement

Copy the contents of this pack into the project repository as follows:

- `docs/ANDROID_MOBILE_PRODUCT_POLICY_AND_PRODUCTION_PLAN.md`
- `docs/ANDROID_PHASE_M0_DISCOVERY_PROMPT.md`
- `docs/ANDROID_INITIAL_SCAFFOLD_PROMPT.md`
- `docs/ANDROID_MOBILE_HANDOFF.md`

The README may remain in the pack or be copied into `docs/ANDROID_README.md`.

## Locked direction

PGR SIMS Android is a first-class client of the same canonical PGR SIMS backend used by the web application.

The MVP is intentionally resident-first and onboarding-first, primarily to improve onboarding compliance.

The long-term goal is progressive functional parity between Android and web, with both clients using the same canonical backend, data, permissions, workflows, and business rules.

## Recommended execution order

1. Run the scaffold prompt from the repository root.
2. Add the documentation files to `/docs`.
3. Commit or otherwise establish the documentation baseline.
4. Run the Phase M0 discovery prompt.
5. Do not begin broad Android feature implementation until M0 returns a GO or CONDITIONAL GO verdict.
