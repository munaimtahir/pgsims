# Cleanup Sprint — Phase A Reset Scope

Date (UTC): 2026-04-21T05:39:06Z

## Objective
Controlled destructive reset for truth alignment: remove test/demo/runtime clutter, preserve required baseline structures, rebuild a trusted baseline, and verify frontend-backend truth without feature expansion.

## Safety Boundaries
1. **Runtime/data purge first**, repository cleanup second, verification third.
2. **No feature additions** and no UX route/terminology changes.
3. **No silent claims**: status must be evidence-based and explicitly classified.
4. **Backup created and verified before purge**.

## Snapshot Verification (Pre-Purge)
- Snapshot directory: `docs/_archive/_snapshots/cleanup-20260421T053906Z`
- Contents:
  - `postgres.sql` (runtime PostgreSQL dump)
  - `backend-db.sqlite3` (local SQLite copy)
  - `runtime-artifacts.tar.gz` (logs/output/screenshots bundle)
  - `docker-compose-ps.txt` (runtime service state)
  - `SHA256SUMS.txt` (integrity checksums)
- Verification status: **present and readable**

## Current Runtime Audit (Pre-Purge)
- Active stack detected (`backend`, `frontend`, `db`, `redis`, `worker`, `beat`) via Docker compose.
- Runtime/generated artifact footprint found:
  - `output/` (~69M)
  - `OUT/` (~9.2M)
  - `frontend/e2e/output/` (~16M)
  - `frontend/e2e/screenshots/` (~44K)
  - `frontend/.next/` (~126M)
- DB observed with mixed state:
  - Users: 68
  - Training transactional and historical rows present
  - Multiple `demo_*`, `e2e_*`, `pg_p6-*`, `sup_p6-*`, `res_e2e-*` accounts present

## Execution Guardrails for Next Phases
- Purge demo/test/runtime data and generated runtime artifacts only.
- Preserve schema/migrations/contracts/config/baseline authority docs.
- Recreate minimum baseline data and minimum verification users only.
- Re-classify active features truthfully after rebuild and verification.
