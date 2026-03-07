# Contract Change Policy

## Purpose

This document defines the mandatory process for making any change to the PGSIMS API contract. No endpoint may be added, modified, or removed without following this process.

---

## Change Categories

### Category A — Breaking Changes (require version bump)
- Removing an endpoint
- Renaming an endpoint URL
- Removing a required request field
- Removing a response field
- Changing a field type
- Changing an HTTP method
- Narrowing role permissions (removing access)

### Category B — Additive Changes (no version bump required)
- Adding a new optional request field
- Adding a new response field
- Adding a new endpoint
- Broadening role permissions (adding access)
- Adding a new error code to an existing endpoint

### Category C — Documentation-Only
- Clarifying descriptions
- Adding examples
- Correcting typos in documentation

---

## Mandatory Change Process

### For Category A and B Changes

```
Step 1: Update Contract Document
  → Edit docs/contracts/API_CONTRACT.md
  → Edit docs/contracts/RBAC_MATRIX.md (if permissions change)
  → Update version header in changed document

Step 2: Update Integration Truth Map
  → Edit docs/integration/BACKEND_FRONTEND_TRUTHMAP.md
  → Update the affected feature entry

Step 3: Update Mismatch Report
  → Note in docs/integration/MISMATCH_REPORT.md if a temporary gap exists

Step 4: Implement Backend
  → Update serializer(s)
  → Update view(s)/viewset(s)
  → Update permission class(es) if RBAC changed
  → Write or update test(s)

Step 5: Update Frontend SDK
  → Update TypeScript interface(s) in frontend/lib/api/*.ts
  → Update API client function(s)
  → Update any pages or components consuming the endpoint

Step 6: Update Endpoint Catalog
  → Edit docs/integration/API_ENDPOINT_CATALOG.md

Step 7: Run Tests
  → pytest sims — all must pass
  → npm run lint — no new errors

Step 8: Commit
  → Commit message must reference the contract change
  → Include "contract:" prefix in commit message
```

### For Category C Changes

Directly edit the documentation files and commit with `docs:` prefix.

---

## Emergency Hotfix Process

If a production bug requires an immediate code change that diverges from the contract:

1. Apply the code fix
2. Tag the commit with `hotfix:` prefix
3. **Within 24 hours**, update the contract to reflect the actual behavior
4. File a `MISMATCH_REPORT.md` entry describing the temporary divergence
5. Resolve the documentation debt before next feature release

---

## Contract Freeze Periods

After the pilot deployment begins:
- **Route structure** (`docs/contracts/ROUTES.md`) is frozen — no changes without explicit admin approval
- **Terminology** (`docs/contracts/TERMINOLOGY.md`) is frozen — no changes without explicit admin approval
- Breaking changes to any endpoint used by active users require a migration period

---

## Approval Matrix

| Change Type | Required Approvers |
|-------------|-------------------|
| Category A (breaking) | Tech Lead + Product Owner |
| Category B (additive) | Tech Lead |
| Category C (docs) | Any developer |
| Frozen route/terminology | Admin + Tech Lead |

---

## Audit Log

All contract changes must be documented in `docs/_audit/` as a dated file:

```
docs/_audit/YYYY-MM-DD-<short-description>.md
```

Include: what changed, why, who approved, affected components.
