# Documentation

## 🚨 CRITICAL: Production Gate Closure Sprint + Anti-Drift Guardrails

**BEFORE READING ANYTHING ELSE**, read these in order:

1. **Documentation Package**: `docs/PROD_GATE_CLOSURE/`
   - **Start**: `docs/PROD_GATE_CLOSURE/00_README.md` (15 min)
   - **Quick ref**: `docs/PROD_GATE_CLOSURE/QUICK_REFERENCE.md` (5 min)
   - **Navigation**: `docs/PROD_GATE_CLOSURE/INDEX.md`

2. **Anti-Drift Guardrails**: `docs/ANTI_DRIFT_GUARDRAILS.md` (MANDATORY)
   - Session window enforcement
   - 20 core guardrails (G1-G20)
   - Drift detection checklist
   - Scope creep prevention
   - Pre-session setup

All agents/developers must read BOTH packages before executing any task that affects:
- Tests or test coverage
- Schema generation or OpenAPI
- E2E testing
- Backend/frontend integration
- Configuration or deployments

**Why both files?**
- `docs/PROD_GATE_CLOSURE/` = WHAT needs to be done (11 blockers)
- `docs/ANTI_DRIFT_GUARDRAILS.md` = HOW to stay focused (guardrails enforcement)

Current status: **NO-GO** (11 blockers identified, all documented, ready for closure)
Mandatory gates: Schema, E2E, coverage, routes, CTAs, roles, workflows

**Before Every Session:**
- [ ] Read AGENTS.md / GEMINI.md (sections 11-24)
- [ ] Read docs/PROD_GATE_CLOSURE/00_README.md
- [ ] Read docs/ANTI_DRIFT_GUARDRAILS.md
- [ ] Fill out session window (template in guardrails)
- [ ] Confirm guardrails ACTIVE

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
