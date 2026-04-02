# Documentation Authority Map

## Authoritative docs
- `docs/contracts/`
  - Canonical contract and route authority
- `docs/_recovery/20260402T122809Z/`
  - Current status pack for the active/deferred surface after this recovery pass
- `docs/_discovery/20260323T200217Z/`
  - Historical discovery baseline that explains how the current recovery scope was chosen

## Historical but still useful
- `docs/_recovery/20260323T205357Z/`
  - Previous recovery snapshot; no longer the current planning baseline
- `docs/_discovery/*`
  - Historical evidence and discovery reasoning
- `docs/FEATURES_STATUS.md`
  - Historical inventory, not an authority for current runtime truth

## Stale or non-authoritative unless regenerated
- `docs/contracts/INTEGRATION_TRUTH_MAP.md`
  - Useful as historical/generated inventory only
  - Not the active-surface authority for current planning
- Any legacy docs that imply active logbook/cases/analytics readiness without matching the current route/include set

## Source-of-truth hierarchy
1. Current checked-out runtime code
2. `docs/contracts/`
3. `docs/_recovery/20260402T122809Z/`
4. `docs/_discovery/20260323T200217Z/`
5. Historical/archive docs

## What future agents should read first
1. `AGENTS.md`
2. `docs/contracts/ROUTES.md`
3. `docs/contracts/API_CONTRACT.md`
4. `docs/contracts/TRUTH_TESTS.md`
5. `docs/_recovery/20260402T122809Z/00-executive-recovery-summary.md`
6. `docs/_recovery/20260402T122809Z/01-active-surface-map.md`
7. `docs/_recovery/20260402T122809Z/07-open-blockers-and-deferred-items.md`
