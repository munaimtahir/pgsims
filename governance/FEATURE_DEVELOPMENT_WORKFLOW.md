# Feature Development Workflow

## Overview

Every new feature in PGSIMS follows this contract-first workflow. Skipping any step is prohibited.

---

## Phase 1: Contract Definition

Before writing a single line of implementation code:

### 1.1 Define the API Contract
Edit `docs/contracts/API_CONTRACT.md` and add:
```markdown
### Feature: <Name>

**Endpoint:** `POST /api/feature-name/`
**Method:** POST
**Auth:** Required
**Roles:** pg, supervisor

**Request Body:**
{
  "field1": "string",
  "field2": 123
}

**Response (201):**
{
  "id": 1,
  "field1": "string",
  "field2": 123,
  "created_at": "2026-01-01T00:00:00Z"
}

**Errors:**
- 400: Validation failure
- 403: Role not allowed
```

### 1.2 Define RBAC
Edit `docs/contracts/RBAC_MATRIX.md` to add the new endpoint's permission row.

### 1.3 Define Data Model (if new entity)
Edit `docs/contracts/DATA_MODEL.md` to document the new entity and its relationships.

### 1.4 Update Integration Catalog
Add a pending entry to `docs/integration/API_ENDPOINT_CATALOG.md`:
```
| POST /api/feature-name/ | PENDING | - | - | pg, supervisor |
```

### 1.5 Update Missing Implementations
Add an entry to `docs/integration/MISSING_IMPLEMENTATIONS.md`:
```
| Feature Name | Contract: ✓ | Backend: ✗ | Frontend: ✗ |
```

---

## Phase 2: Backend Implementation

### 2.1 Create/Update Model
- Add model to appropriate app (`sims/<app>/models.py`)
- Run `python manage.py makemigrations`
- Verify migration
- Run `python manage.py migrate`

### 2.2 Create Serializer
- Add serializer to `sims/<app>/serializers.py`
- Explicitly list all fields (no `__all__`)
- Add validation logic

### 2.3 Create ViewSet/View
- Add view to `sims/<app>/views.py`
- Set `permission_classes` to match contract RBAC
- Scope queryset by role

### 2.4 Register URL
- Add to `sims/<app>/urls.py`
- Verify path matches contract exactly

### 2.5 Write Tests
- Add to `sims/<app>/test_<feature>.py` or extend existing test file
- Minimum: 3 tests (allowed role, denied role, unauthenticated)

### 2.6 Verify
```bash
cd backend && pytest sims/<app>/test_<feature>.py -v
```

---

## Phase 3: Frontend Implementation

### 3.1 Define TypeScript Types
In the appropriate `frontend/lib/api/<module>.ts`:
```typescript
export interface FeatureName {
  id: number;
  field1: string;
  field2: number;
  created_at: string;
}

export interface CreateFeaturePayload {
  field1: string;
  field2: number;
}
```

### 3.2 Create API Function
```typescript
export const featureApi = {
  async createFeature(payload: CreateFeaturePayload): Promise<FeatureName> {
    const r = await apiClient.post<FeatureName>('/api/feature-name/', payload);
    return r.data;
  }
};
```

### 3.3 Create/Update Page
- Create page under correct route per `docs/contracts/ROUTES.md`
- Import API function from `lib/api`
- Add loading and error states
- Handle all documented error codes

### 3.4 Lint
```bash
cd frontend && npm run lint
```

---

## Phase 4: Integration Verification

### 4.1 Update Truth Map
Edit `docs/integration/BACKEND_FRONTEND_TRUTHMAP.md` and add/update the feature entry.

### 4.2 Update Endpoint Catalog
Mark the entry in `docs/integration/API_ENDPOINT_CATALOG.md` as `IMPLEMENTED`.

### 4.3 Update Missing Implementations
Mark the entry in `docs/integration/MISSING_IMPLEMENTATIONS.md` as complete.

### 4.4 Run Full Test Suite
```bash
cd backend && pytest sims -v
cd frontend && npm run lint
```

### 4.5 Scan for Forbidden Patterns
```bash
# Check for duplicate Department models
grep -r "class.*Department.*models.Model" backend/sims --include="*.py"

# Check for legacy notification keys
grep -rn "Notification.objects.create" backend/sims --include="*.py" | grep "user=\|message=\|type="

# Check for raw fetch in frontend pages
grep -rn "fetch(" frontend/app --include="*.tsx" | grep -v "// "
```

---

## Phase 5: Audit Documentation

Create an audit entry in `docs/_audit/`:
```
docs/_audit/YYYY-MM-DD-<feature-name>.md
```

Include:
- Feature name and description
- Contract changes made
- Backend files changed
- Frontend files changed
- Test results
- Any known limitations

---

## Phase 6: Commit

Use the `feat:` prefix and reference the contract:
```
feat: add <feature name>

- Contract defined in docs/contracts/API_CONTRACT.md
- Backend: sims/<app>/views.py + serializers.py + urls.py
- Frontend: lib/api/<module>.ts + app/dashboard/...
- Tests: sims/<app>/test_<feature>.py — all pass
- Truth map updated

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>
```

---

## Quick Reference Checklist

```
□ Contract defined in docs/contracts/API_CONTRACT.md
□ RBAC entry added to docs/contracts/RBAC_MATRIX.md
□ Model created/migrated
□ Serializer with explicit fields
□ View with permission_classes
□ URL registered matching contract
□ Tests written and passing
□ TypeScript types defined
□ API client function created
□ Page implemented
□ Truth map updated
□ Endpoint catalog updated
□ Audit entry created
□ Forbidden pattern scan clean
□ Full test suite passes
```
