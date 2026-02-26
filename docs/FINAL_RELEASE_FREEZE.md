# PGSIMS/UTRMC — Final Release Freeze

⚠️ **This is a mirror document for convenience.**

**Canonical Source**: `docs/contracts/FINAL_RELEASE_FREEZE.md`

For the complete freeze documentation, verification commands, and governance rules, see:

👉 **[docs/contracts/FINAL_RELEASE_FREEZE.md](contracts/FINAL_RELEASE_FREEZE.md)**

---

## Quick Reference

**Freeze Date**: 2026-02-26  
**Release Tag**: `pgsims-utrmc-freeze-20260226`  
**Status**: LOCKED FOR PRODUCTION ROLLOUT

### What is Frozen

- Authentication & session management (cookie contract)
- Middleware RBAC (5 roles, supervisor scope Option A)
- PG logbook flow (status workflow, edit permissions)
- Supervisor review flow (verify actions, feedback)
- UTRMC roles (read-only + override approval)
- Rotations canonical display (ONE Department, ONE Hospital)
- Option A reference data authority (admin/utrmc_admin CRUD)
- Bulk review endpoint
- Notification preferences and schema
- UI routes and terminology

### Verification Commands

```bash
# Backend (serial)
cd backend
../.venv/bin/python manage.py check
../.venv/bin/python manage.py test

# Frontend (serial)
cd frontend
npm run build
npx playwright test

# Truth-map
grep "Verdict:" docs/contracts/INTEGRATION_TRUTH_MAP.md
```

**Expected**: All PASS, truth-map verdict PASS with 0 unmatched calls.

### Non-Negotiables

- No UI route/terminology changes
- Cookie contract locked (access_token, role, exp)
- Option A master-data authority locked
- Canonical models locked (no duplicate Department/Hospital)
- Serial verification only (no parallel build + Playwright)
- docs/_audit is local-only (never commit)

---

For complete details, drift detection rules, CI gates, and extension guidelines:

📖 **[docs/contracts/FINAL_RELEASE_FREEZE.md](contracts/FINAL_RELEASE_FREEZE.md)**
