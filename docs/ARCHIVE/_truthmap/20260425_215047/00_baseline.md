# Stage 0: Baseline Audit Environment

**Timestamp**: 2026-04-25 21:50:28 UTC
**Audit Type**: Runtime Truthmap Verification (Observational Only)
**Evidence Folder**: `docs/_truthmap/20260425_215047/`

## Git Baseline

```
Branch:        main
Commit:        45bc653 (ahead of origin/main by 13 commits)
Commit Date:   2026-04-25
Commit Msg:    Add quick start guide for anti-drift guardrails
Status:        Working directory CLEAN (uncommitted changes stashed)
Stash ID:      audit-stash-baseline
```

**Working Tree Before Audit**: 
- Modified files: 21 tracked files (stashed)
- Untracked files: 40+ test files (kept, non-interfering)
- Status: CLEAN for audit purposes

**Audit Constraint**: No changes will be made during this audit. All code remains as-is.

## Project Structure

### Backend
```
backend/
├── sims_project/          Django settings & URL routing
│   ├── settings.py        Configuration
│   ├── urls.py            URL dispatch
│   └── celery.py          Background task config
├── sims/                  Core app modules
│   ├── users/             User auth & profiles
│   ├── training/          Training programs, rotations, leaves
│   ├── rotations/         Rotation assignments
│   ├── academics/         Departments, hospitals
│   ├── logbook/           Logbook entries (if exists)
│   ├── workshops/         Workshops (if exists)
│   ├── notifications/     Notifications
│   ├── bulk/              Bulk import/export
│   ├── audit/             Audit logs
│   └── search/            Search functionality
└── manage.py              Django CLI

Database: PostgreSQL (Docker)
ORM: Django ORM
API Framework: Django REST Framework
```

### Frontend
```
frontend/
├── app/                   Next.js App Router pages
│   ├── dashboard/         Role-based dashboards
│   │   ├── resident/
│   │   ├── supervisor/
│   │   └── utrmc/
│   ├── login/
│   ├── register/
│   └── [other pages]
├── components/            React components
├── lib/                   Utilities & API client
│   └── api/              API client SDK
└── e2e/                  Playwright tests
    └── feature-layer/    E2E test suite

Framework: Next.js 14
Language: TypeScript
CSS: Tailwind CSS
API Client: Axios (wrapped in lib/api/)
```

### Testing
```
Frontend E2E:
  Command: cd frontend && npm run test:e2e:feature-layer:local
  Config:  frontend/playwright.config.ts
  Seed:    ./scripts/e2e_seed.sh

Backend Tests:
  Command: cd backend && SECRET_KEY=test-secret pytest sims -q
  Config:  backend/sims_project/settings_test.py
```

### Docker Compose
```
Services:
  - db (PostgreSQL)
  - redis (cache/message broker)
  - backend (Django Gunicorn)
  - frontend (Next.js)
  - worker (Celery)
  - beat (Celery scheduler)

Compose File: docker/docker-compose.yml

Start: make up (or docker compose -f docker/docker-compose.yml up -d)
Logs:  make logs (or docker compose logs -f)
Stop:  make down (or docker compose -f docker/docker-compose.yml down)
```

## Environment Configuration

### Backend (.env)
```
DJANGO_SETTINGS_MODULE=sims_project.settings
SECRET_KEY=(from .env)
DEBUG=True (development) or False (production)
DATABASE_URL=postgresql://...
REDIS_URL=redis://localhost:6379/0
CORS_ALLOWED_ORIGINS=http://localhost:3000
JWT_SECRET_KEY=(from .env)
```

### Frontend (.env.local or .env.localhost)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_API_BASE=/api
```

## Test Environment Setup

### Database State
```
Seed command: cd backend && python manage.py sims_seed_demo
Creates: Demo trainees, supervisors, departments, hospitals, rotations, etc.
```

### Seeded Test Users (Estimated)
```
Resident:      pg_user@example.com or similar
Supervisor:    supervisor@example.com or similar
UTRMC Admin:   utrmc@example.com or similar
System Admin:  admin@example.com or similar
(Exact credentials from seed script)
```

### Docker Setup for Audit
```
Database: Fresh PostgreSQL container
Status: Running (verified by docker ps)
Migrations: Applied (via docker compose up)
Seed data: Can be applied via management command inside container
```

## Audit Execution Method

### Approach
1. **Backend Route Inventory** (Stage 1): Django URL resolver inspection
2. **Frontend Static Inventory** (Stage 2): Source code grep/scan
3. **Playwright Runtime Discovery** (Stage 3): Browser automation + network capture
4. **Direct Route Testing** (Stage 4): Test each frontend route directly
5. **Backend Runtime Tests** (Stage 5): API endpoint validation
6. **Linkage Matrix** (Stage 6): Combine all evidence
7. **Module Verdicts** (Stage 7): Specific feature status
8. **Gap Register** (Stage 8): Verified gaps only
9. **GO/NO-GO Verdicts** (Stage 9): By readiness stage
10. **Executive Report** (Stage 10): Final summary

### Tools Used
- **Django Shell**: Backend route inspection
- **Playwright**: Browser automation & network capture
- **cURL/Axios**: Direct API testing
- **grep/ripgrep**: Source code scanning
- **Docker Compose**: Environment management

### Constraints
- ✅ OBSERVATIONAL ONLY (no code changes)
- ✅ Evidence-based only (no assumptions)
- ✅ Runtime verified (not static analysis alone)
- ✅ Role-based testing (all 4-5 roles)
- ✅ Network captured (API calls recorded)
- ✅ Screenshots taken (visual evidence)

## Key Investigation Targets

Based on previous analysis, these areas require runtime verification:

1. **Programs Module**
   - Does frontend page exist?
   - Is create/edit button visible?
   - Does backend endpoint work?

2. **Training Programs Module**
   - Is it exposed in UTRMC admin?
   - Can programs be created/edited?
   - Can policy/milestones be configured?

3. **Workshops Module**
   - Is there a resident page?
   - Is there admin management?
   - Can completions be recorded?

4. **Logbook Module**
   - Is it visible in resident dashboard?
   - Can entries be created/submitted?
   - Can supervisors review?
   - Is backend-only or full frontend?

5. **Supervision Links**
   - Can UTRMC manage supervisor-resident links?
   - Is API working?
   - Is UI visible?

6. **Role-Based Navigation**
   - Is nav different per role?
   - Are hidden routes accessible directly?
   - Are permissions enforced?

## Next Steps

- Proceed to **Stage 1**: Backend Route Inventory
- Document all findings in `01_backend_route_inventory.md`
- Generate CSV for import to database

---

**Audit Status**: ✅ BASELINE ESTABLISHED
**Ready to Proceed**: YES
**Working Tree**: CLEAN
**Database**: Ready (seed manually if needed)
