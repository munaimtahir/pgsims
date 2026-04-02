# Roadmap Direction

## Next Milestone Recommendation

P1: harden the already-active but only lightly verified administration and academic-depth surfaces.

This is the correct next move because the project now has a believable verified core, but still has too many active pages that look ready without matching workflow-grade evidence.

## Immediate Priorities

### P1. UTRMC administration hardening

- Category: hardening / debugging
- Why it matters:
  - hospitals, departments, users, matrix, supervision, and HOD pages are promoted in navigation
  - they influence the data integrity of all downstream workflows
- Dependency:
  - none beyond current recovered baseline
- Recommended order:
  1. docs/runtime cleanup for actual route set
  2. CRUD verification for hospitals/departments/users
  3. matrix/supervision/HOD lifecycle verification

### P1. Secondary academic workflow verification

- Category: hardening / debugging
- Why it matters:
  - thesis, workshops, resident progress, supervisor resident progress, and UTRMC eligibility monitoring are already exposed as active product surfaces
  - they currently have weaker truth evidence than leave/rotations/postings/research
- Dependency:
  - stable userbase/program admin truth
- Recommended order:
  1. thesis
  2. workshops
  3. resident progress + eligibility monitor
  4. supervisor resident progress

### P1. Documentation and contract cleanup

- Category: hardening
- Why it matters:
  - route docs and README still overstate scope
  - stale claims create roadmap drift and false readiness
- Dependency:
  - none
- Recommended order:
  1. remove/mark overclaims in README
  2. fix stale route references in `docs/contracts/ROUTES.md`
  3. explicitly keep deferred modules deferred

## Sequencing Plan

1. Clean docs/runtime drift around active routes and overclaimed modules.
2. Add runtime-grade verification to UTRMC admin/userbase surfaces.
3. Add runtime-grade verification to thesis/workshops/progress/eligibility.
4. Tighten auth/build harness weak points.
5. Re-run discovery and only then consider broader functional expansion.

## What NOT To Work On Yet

- logbook
- cases
- legacy analytics
- certificates reactivation
- global search reactivation
- broad reporting/results/attendance rebuild
- broad UI redesign
- speculative new scheduling ecosystems

## Future Roadmap

### a. Stabilization / Hardening

- P1: UTRMC admin/userbase workflow verification and fixes
- P1: thesis/workshops/progress/eligibility verification and fixes
- P1: auth throttling clarity and protected-route confidence
- P1: frontend build/start harness cleanup

### b. Operational Depth

- P2: richer programme/policy/template admin validation
- P2: non-seeded data behavior checks on rotation/postings/admin surfaces
- P2: stronger negative-path coverage for role boundaries and validation errors

### c. Deferred Modules

- P3: maintain explicit deferral for logbook, cases, legacy analytics, certificates, search, reports/results/attendance

### d. Long-Term Expansion

- P3: only after hardening, decide whether any deferred legacy domains are worth rebuilding on current contracts

## Compact Summary Table

| Priority | Item | Category | Why Next | Dependency |
|----------|------|----------|----------|------------|
| P1 | UTRMC admin/userbase hardening | debugging | Promoted active pages still lack workflow-grade proof | None |
| P1 | Thesis/workshops/progress verification | debugging | Active resident surfaces should not remain “looks ready” only | Stable active baseline |
| P1 | Docs/runtime truth cleanup | hardening | README and route docs still overclaim scope | None |
| P1 | Auth/build harness cleanup | hardening | Prevent hidden instability in delivery and repeated-login behavior | Stable current runtime |
| P2 | Program admin depth | completion | Programs/policies/templates are active but only lightly proven | P1 admin hardening |
| P2 | Broader negative-path/runtime coverage | hardening | Prevent seeded happy-path illusions | P1 workflow verification |
| P3 | Legacy module decisions | deferred | Keep deferred modules out of active planning until intentionally revived | P1 and P2 complete |
