# Backend Truth Map (Executive)

## Scope and Verification Basis
This map is built from runtime checks, Django introspection, router/schema inspection, and code-path references captured in `OUT/28_VERIFICATION_EVIDENCE_LOG.md`.

## Module Overview
Core backend modules discovered (`OUT/installed_apps.txt`):
- Users/Auth (`users`)
- Academics (`academics`)
- Rotations (`rotations`)
- Logbook (`logbook`)
- Cases (`cases`)
- Certificates (`certificates`)
- Attendance (`attendance`)
- Results (`results`)
- Reports (`reports`)
- Notifications (`notifications`)
- Analytics (`analytics`)
- Search (`search`)
- Audit (`audit`)
- Bulk operations (`bulk`)

## Core Entity Truth
- Complete model catalog: `OUT/21_MODELS_CATALOG.md`
- Raw introspection inventory: `OUT/models_inventory.json`
- Relationship graph: `OUT/models_graph.dot`

Highlights:
- Canonical Department: `academics.Department`
- Canonical Hospital: `rotations.Hospital`
- Hospital↔Department matrix: `rotations.HospitalDepartment`
- User role model: `users.User.role` with `admin/supervisor/pg/utrmc_user/utrmc_admin`

## Workflow / State Machine Truth
See `OUT/22_WORKFLOWS_STATE_MACHINES.md`.

High-value workflows verified:
- **Logbook**: draft → pending → approved/returned/rejected with object-level supervisor scope checks.
- **Cases**: draft/needs_revision → submitted → approved/needs_revision/rejected.
- **Rotations**: planned → ongoing → completed + UTRMC override approval policy.
- **Certificates**: review model drives pending/under_review/approved/rejected + expiry transition.
- **Student profile**: controlled status update endpoint.

## RBAC Truth
See `OUT/23_RBAC_PERMISSIONS_MAP.md`.

Key enforcement surfaces:
- DRF global `IsAuthenticated` default + JWT/Session auth.
- Shared permission classes in `sims/common_permissions.py`.
- Role decorators/mixins in `sims/users/decorators.py`.
- Queryset/object scoping at view level for supervisor↔assigned-PG boundaries.

## API Surface Truth
- Endpoint catalog: `OUT/24_API_ENDPOINTS_CATALOG.md` (151 normalized endpoints)
- Machine-readable endpoint dump: `OUT/api_endpoints.json`
- Synthetic OpenAPI export (introspected): `OUT/openapi.json`
- Serializer field/payload map: `OUT/25_SERIALIZERS_PAYLOAD_SHAPES.md`
- Serializer inventory JSON: `OUT/serializers_inventory.json`

## Import/Export + Jobs + Notifications Truth
See `OUT/26_IMPORT_EXPORT_AND_JOBS.md`.

- Bulk import/export is centralized in `BulkService` + `BulkOperation` audit model.
- Scheduled reports implemented via `ScheduledReportRunner` + management command.
- Notification canonical schema and delivery service are present.

## Production Readiness Snapshot (from this verification)
- ✅ Django checks pass.
- ✅ Migrations applied.
- ✅ Full backend test command passed (`286` tests).
- ✅ `/admin/` reachable externally (redirect to login).
- ⚠️ Compose service alias mismatch (`backend` vs `web`) for operational commands.
- ⚠️ Celery beat entries reference task modules not present in repository.
- ⚠️ OpenAPI generation tooling incomplete in runtime image.

## Frontend Navigation Build Next Steps (contract-driven)
1. Use `OUT/24_API_ENDPOINTS_CATALOG.md` to map route→API dependencies by module.
2. Prioritize nav modules with complete API + workflow coverage:
   - Logbook, Cases, Rotations, Users/Auth, Notifications.
3. For certificates/reports, align frontend actions to current backend capabilities:
   - Certificates: list/download + model/admin review flow.
   - Reports: scheduled report CRUD and export.
4. Resolve gaps in `OUT/27_GAPS_AND_FIX_RECOMMENDATIONS.md` before expanding advanced admin/operations UI.

## Linked Artifacts
- `OUT/21_MODELS_CATALOG.md`
- `OUT/22_WORKFLOWS_STATE_MACHINES.md`
- `OUT/23_RBAC_PERMISSIONS_MAP.md`
- `OUT/24_API_ENDPOINTS_CATALOG.md`
- `OUT/25_SERIALIZERS_PAYLOAD_SHAPES.md`
- `OUT/26_IMPORT_EXPORT_AND_JOBS.md`
- `OUT/27_GAPS_AND_FIX_RECOMMENDATIONS.md`
- `OUT/28_VERIFICATION_EVIDENCE_LOG.md`
