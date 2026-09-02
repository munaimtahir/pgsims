# Documentation Authority Map

## Authoritative (read first)
1. `AGENTS.md` (governance constraints and contract-first rules)
2. `docs/contracts/*` (integration and truth gates)
3. `docs/_recovery/20260323T205357Z/*` (current recovery truth baseline)
4. `docs/_discovery/20260323T200217Z/*` (prior evidence baseline)

## Secondary references
- `docs/README.md` (index-level pointer document)
- Module-specific docs that do not contradict contracts/recovery pack.

## Stale / historical / archive signals
- Historical claims in root `README.md` overstate legacy module readiness (logbook/cases/analytics as active-ready).
- Any docs describing legacy modules as currently active should be treated as historical until explicit reactivation milestone.

## Source-of-truth hierarchy for future agents
1. Runtime code truth (`settings.py`, `urls.py`, App Router pages, nav registry)
2. Contract docs (`docs/contracts/*`)
3. Recovery pack (this folder)
4. Discovery pack (context/history)
5. Legacy/historical docs (non-authoritative)
