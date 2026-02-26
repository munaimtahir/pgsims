# PGSIMS/UTRMC — Release Notes (2026-02-26)

**Release Tag**: `pgsims-utrmc-freeze-20260226`  
**Freeze Date**: 2026-02-26  
**Status**: Production-Ready Baseline

---

## Overview

This release establishes the **frozen baseline** for PGSIMS/UTRMC production rollout. All core features are verified and locked with repeatable drift gates.

---

## Included Features

### Core Authentication & Authorization
✅ JWT-based authentication with cookie-only session storage  
✅ Role-based access control (RBAC) for 5 roles: `pg`, `supervisor`, `admin`, `utrmc_user`, `utrmc_admin`  
✅ Middleware auth contract with automatic invalid/expired token handling  
✅ Supervisor scope enforcement (Option A: supervisees-only)

### Postgraduate (PG) Features
✅ Digital logbook with draft/submit/review workflow  
✅ Status progression: draft → submitted → returned/rejected/approved  
✅ Edit permissions: PG can edit only draft/returned entries  
✅ Rotation display with canonical Department/Hospital models  
✅ Personal dashboard with analytics

### Supervisor Features
✅ Pending queue filtered to assigned supervisees only  
✅ Review workflow with approve/return/reject actions  
✅ Feedback mechanism for returned/rejected entries  
✅ Bulk review capability for multiple entries  
✅ Supervisor dashboard with supervisee statistics

### UTRMC Oversight
✅ **utrmc_user**: Read-only access to oversight dashboards, logs, reports, statistics  
✅ **utrmc_admin**: Configuration and override approval powers  
✅ Inter-hospital rotation policy enforcement with override approval  

### Reference Data Management (Option A)
✅ Canonical `Department` model (university-wide, `admin` CRUD only)  
✅ Canonical `Hospital` model (`admin` CRUD only)  
✅ `HospitalDepartment` matrix (`utrmc_admin` primary CRUD; `admin` recovery)  
✅ Master-data authority locked per role

### Notifications
✅ Notification system with canonical schema (`recipient`, `verb`, `body`, `metadata`)  
✅ `NotificationService` helper for consistent delivery  
✅ Notification preferences with `PATCH /api/notifications/preferences/`

### Integration & APIs
✅ Contract-first integration with specs in `docs/contracts/`  
✅ API payload contracts locked in `docs/contracts/API_CONTRACT.md`  
✅ RBAC matrix locked in `docs/contracts/RBAC_MATRIX.md`  
✅ Integration truth-map verified with verdict PASS (0 unmatched frontend calls)

---

## Key Governance Rules

### Frozen Elements (Cannot Change Without Re-Freeze)
- **Routes**: UI route structure locked (`docs/contracts/ROUTES.md`)
- **Terminology**: User-facing terms locked (`docs/contracts/TERMINOLOGY.md`)
- **Cookie Contract**: `access_token`, `role`, `exp` in cookies; refresh token in `localStorage`
- **Option A Authority**: Department/Hospital CRUD roles locked
- **Canonical Models**: ONE Department, ONE Hospital (no duplicates)
- **RBAC Matrix**: Authorization rules locked per role

### Allowed Changes (No Re-Freeze Required)
- Bug fixes that don't change behavior contracts
- Performance improvements
- Helper text and small visual cues
- Internal refactoring that preserves external contracts

### Contract-First Integration
- All backend ↔ frontend integration changes require contract updates
- Contracts in `docs/contracts/` are authoritative
- No "quick fixes" that silently change payload shapes

### Audit Integrity
- All state transitions auditable via `django-simple-history`
- No direct DB edits for state changes
- `docs/_audit/**` is local-only (not committed)

---

## Technical Stack

### Backend
- **Framework**: Django 4.2
- **Python**: 3.11+
- **Database**: PostgreSQL
- **Cache/Broker**: Redis
- **Background Tasks**: Celery + Celery Beat
- **Authentication**: JWT via `djangorestframework-simplejwt`
- **Testing**: pytest with pytest-django

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript (strict mode)
- **Styling**: Tailwind CSS
- **State Management**: React Query (server state) + Zustand (client state)
- **HTTP Client**: Axios
- **E2E Testing**: Playwright

### Infrastructure
- **Deployment**: Docker Compose (Coolify/Traefik recommended)
- **Reverse Proxy**: Nginx or Traefik
- **Services**: web, worker, beat, db, redis, nginx

---

## Verification Status

All verification gates passed with serial execution:

| Gate | Status | Details |
|------|--------|---------|
| Backend Tests | ✅ PASS | Full test suite passed |
| Frontend Build | ✅ PASS | Production build succeeded |
| Playwright E2E | ✅ PASS | All E2E tests passed |
| Integration Truth-Map | ✅ PASS | 0 unmatched frontend calls |
| RBAC Matrix | ✅ VERIFIED | All roles and permissions defined |
| Contract Docs | ✅ COMPLETE | All integration contracts documented |

---

## Known Operational Notes

### Serial Verification Requirement
⚠️ **Important**: Verification must run serially (not in parallel):
1. Backend tests first
2. Frontend build second
3. Playwright E2E third
4. Truth-map regeneration fourth

**Reason**: Parallel execution of `npm build` + Playwright can intermittently hit Next.js `/_document` endpoint, causing flaky test failures. Serial execution avoids this race condition.

**CI Implementation**: GitHub Actions workflow enforces serial execution with job dependencies.

### docs/_audit Local-Only
⚠️ **Important**: `docs/_audit/**` contains local-only run reports and must NOT be committed to git. Only `docs/_archive/**` evidence summaries should be committed.

---

## Deployment

### Recommended: Coolify/Traefik
See `docs/DEPLOY_COOLIFY_TRAEFIK.md` for production deployment guide.

**Features**:
- Automatic HTTPS with Let's Encrypt
- No nginx configuration needed
- WhiteNoise serves static files
- Zero port 80/443 conflicts
- Built-in health checks

### Environment Configuration
- Backend: `.env` at project root (see `.env.example`)
- Frontend: `.env.local` in `frontend/` (see `.env.local.example`)
- Templates: `.env.localhost`, `.env.vps`, `frontend/.env.localhost`, `frontend/.env.vps`

---

## Drift Detection

CI gates enforce these forbidden patterns:

❌ Duplicate Department models (e.g., `RotationDepartment`)  
❌ Legacy notification keys (`user=`, `message=`, `type=`)  
❌ Breaking API payloads without contract updates  
❌ Direct DB edits bypassing audit trail  
❌ Route/terminology changes without contract updates  
❌ Truth-map verdict != PASS

**CI Workflow**: `.github/workflows/pgsims_drift_gates.yml` runs on every push.

---

## Documentation

### Authoritative Contracts
- `docs/contracts/FINAL_RELEASE_FREEZE.md` — This frozen baseline
- `docs/contracts/API_CONTRACT.md` — API payload shapes
- `docs/contracts/DATA_MODEL.md` — Canonical entity definitions
- `docs/contracts/RBAC_MATRIX.md` — Authorization rules
- `docs/contracts/ROUTES.md` — Frontend route structure
- `docs/contracts/TERMINOLOGY.md` — User-facing terms
- `docs/contracts/TRUTH_TESTS.md` — Gate tests

### Development Guides
- `docs/PROJECT_STRUCTURE.md` — Directory layout
- `docs/FEATURES_STATUS.md` — Feature completeness
- `docs/SYSTEM_STATUS.md` — System health tracking
- `docs/TROUBLESHOOTING.md` — Common issues
- `.github/copilot-instructions.md` — Copilot development guide

---

## Git Tag

**Tag**: `pgsims-utrmc-freeze-20260226`  
**Type**: Annotated  
**Message**: "RBAC+E2E+TruthMap PASS, Option A locked"

```bash
# View tag details
git show pgsims-utrmc-freeze-20260226

# Checkout frozen baseline
git checkout pgsims-utrmc-freeze-20260226
```

---

## Next Steps

1. **Production Deployment**: Follow `docs/DEPLOY_COOLIFY_TRAEFIK.md`
2. **Pilot Rollout**: Deploy to production environment for UTRMC pilot
3. **Monitoring**: Track user feedback and system health
4. **Post-Freeze Changes**: Follow `docs/contracts/FINAL_RELEASE_FREEZE.md` extension guidelines

---

## Support

For questions or issues:
- **Documentation**: Start with `docs/README.md`
- **Governance**: Review `AGENTS.md`
- **Contracts**: Check `docs/contracts/`

---

**Release Team**: PGSIMS Development Team  
**Approved By**: UTRMC Project Governance  
**Next Review**: After first production deployment feedback
