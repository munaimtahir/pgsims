# Documentation

## 🚨 CRITICAL: Production Gate Closure Sprint

**BEFORE READING ANYTHING ELSE**, go to: `docs/PROD_GATE_CLOSURE/`

This package contains complete documentation for closing all 11 remaining production gate blockers:
- **Start here**: `docs/PROD_GATE_CLOSURE/00_README.md` (15 min)
- **Quick reference**: `docs/PROD_GATE_CLOSURE/QUICK_REFERENCE.md` (5 min)
- **Full index**: `docs/PROD_GATE_CLOSURE/INDEX.md` (navigation guide)

All agents/developers must read this before executing any task that affects:
- Tests or test coverage
- Schema generation or OpenAPI
- E2E testing
- Backend/frontend integration

Current status: **NO-GO** with 11 identified blockers (ready for closure)
Mandatory gates: Schema, E2E, coverage, routes, CTAs, roles, workflows

---

## Canonical contracts

Canonical contracts live in `docs/contracts/` and are the only authoritative docs for backend/frontend integration.

Current delivery truth baseline:
- Discovery pack: `docs/_discovery/20260402T215202Z-functionality-categorization/`
- Recovery pack (authoritative for current active/deferred surface): `docs/_recovery/20260402T122809Z/`
- Bulk setup/import-export contract: `docs/contracts/BULK_SETUP_IMPORT_EXPORT.md`

`docs/TERMINOLOGY.md`, `docs/ROUTES.md`, `docs/DATA_MODEL.md`, `docs/API_CONTRACT.md`, `docs/MIGRATION_PLAN.md`, `docs/TRUTH_TESTS.md`, and `docs/RBAC_MATRIX.md` are links/stubs to the canonical contract files.

`docs/_archive/` stores historical docs, audit runs, snapshots, and patches.
`docs/_audit/` is for local-only working outputs (do not commit contents except `README.md`).

Authority note:
- `docs/contracts/INTEGRATION_TRUTH_MAP.md` is a historical/generated inventory, not the active-surface authority.
- Older recovery packs and `docs/FEATURES_STATUS.md` are historical context only.

Analytics documentation:
- `docs/ANALYTICS_BLUEPRINT.md`
- `docs/ANALYTICS_OPENAPI.md`
- `docs/ANALYTICS_UI_SPEC.md`
- `docs/ARCHITECTURE/ANALYTICS.md`
