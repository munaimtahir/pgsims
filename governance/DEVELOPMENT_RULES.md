# Development Rules

## Overview

These rules govern all development in the PGSIMS system. All developers and agents must follow these rules without exception.

---

## Backend Rules

### Route Definition
- All API routes **must** be defined in the relevant app's `urls.py`
- Route paths **must** match the contract in `docs/contracts/API_CONTRACT.md`
- DRF `DefaultRouter` must be used for standard CRUD viewsets
- Custom actions must use `@action` decorator with explicit `methods` and `url_path`
- No route may be registered without a corresponding contract entry

### Request Validation
- All request inputs must be validated by a DRF Serializer
- Serializers must explicitly define allowed fields (no `fields = '__all__'` in write operations)
- Required vs optional fields must match the contract schema
- File upload endpoints must validate MIME type and file size

### Response Payloads
- All responses must use DRF Serializers — no manual `JsonResponse` with ad-hoc dicts
- Response shapes must exactly match the documented contract
- Paginated list responses must use `{ count, results }` format
- Never return internal model field names that differ from the contract (use `source=` if needed)

### Authentication & Authorization
- All protected endpoints must declare a permission class
- Permission classes must align with `docs/contracts/RBAC_MATRIX.md`
- Use documented permission helpers: `IsTechAdmin`, `IsManager`, `_is_admin_or_utrmc_admin()`
- Never grant access based on undocumented role combinations

### Status Codes
- `200 OK` — successful read or state query
- `201 Created` — successful create
- `204 No Content` — successful delete
- `400 Bad Request` — validation failure
- `401 Unauthorized` — missing/invalid token
- `403 Forbidden` — authenticated but unauthorized
- `404 Not Found` — resource does not exist
- `409 Conflict` — workflow state conflict

### Audit Trail
- All state transitions must go through the ORM (never raw SQL `UPDATE`)
- `django-simple-history` must remain active on all models with state
- `NotificationService` must be used for all notification creation
- Never mutate `approved` or `verified` records without explicit workflow action

---

## Frontend Rules

### API Layer
- All HTTP requests must go through `frontend/lib/api/*.ts` client functions
- **No raw `fetch()` or `axios` calls** may appear in page components or UI hooks
- API client functions must be typed with TypeScript interfaces matching the contract
- The two exceptions permitted: `apiClient.get('/api/users/?role=supervisor')` within `training.ts` context (already documented)

### Request Payloads
- Payloads must use the TypeScript types defined in `frontend/lib/api/*.ts`
- Optional fields must be explicitly typed as `field?: type`
- File uploads must use `FormData` and set `Content-Type: multipart/form-data`

### Response Handling
- All API responses must be typed using the interfaces in `frontend/lib/api/*.ts`
- Defensive parsing via `toArray()` helper must be used where backend may return array or paginated object
- Error state must be handled in every async call (try/catch or `.catch()`)
- Never assume a field exists without checking for null/undefined

### Data Flow Architecture
```
UI Component → Feature Service / API Function → apiClient → Backend
```
Never skip the API layer.

### UI State
- Loading state must be shown during all async operations
- Error state must be displayed to the user on failure
- Optimistic updates are allowed only for non-destructive operations

---

## Cross-Cutting Rules

### Naming Consistency
- Backend serializer field names must match frontend TypeScript interface property names
- URL slugs in routes must match between backend URL patterns and frontend route definitions
- Status string values must match exactly (e.g., `"draft"`, `"pending"`, `"approved"`)

### Migration Policy
- No migration may be created that drops a column without a deprecation period
- Schema migrations must be reviewed against the data contract
- No migration may change a nullable field to non-null without a data migration

### Testing
- Every new endpoint must have at least one test in the relevant `test_*.py` file
- Role-based access tests must cover at least: allowed role, denied role, unauthenticated
- Frontend API client functions must have type coverage via TypeScript strict mode

---

## Forbidden Patterns

The following patterns are permanently prohibited:

| Pattern | Reason |
|---------|--------|
| `class RotationDepartment(models.Model)` | Duplicate canonical entity |
| `Notification.objects.create(user=..., message=..., type=...)` | Legacy notification schema |
| `fetch('/api/...')` in page components | Bypasses API governance layer |
| Direct DB `UPDATE` for state transitions | Bypasses audit trail |
| `fields = '__all__'` in write serializers | Exposes internal fields |
| Hard-coded role strings not in RBAC matrix | Undocumented permissions |
