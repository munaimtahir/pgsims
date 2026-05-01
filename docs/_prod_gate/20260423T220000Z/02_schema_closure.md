# Schema Closure - 2026-04-23

## Status
- **Strict Schema Gate**: PASS (0 errors, 53 warnings).
- **Errors Resolved**: 315 errors (65 unique) reduced to 0.

## Actions Taken
1. **Auth Endpoints**: Decorated `register_view`, `logout_view`, `user_profile_view`, `update_profile_view`, `password_reset_request_view`, `password_reset_confirm_view`, `change_password_view` with `@extend_schema`.
2. **Userbase Endpoints**: Decorated `AuthMeView`, `DataQualitySummaryView`, `DataQualityUsersView`, `DataQualityRecomputeView`, `DataCorrectionAuditView`.
3. **Bulk Endpoints**: Decorated all bulk import/export views.
4. **Training Endpoints**: Decorated all operational dashboard views, summary views, and base submission views.
5. **Serializers**:
   - Added auth request/response serializers to `sims/users/serializers.py`.
   - Added data quality and audit serializers to `sims/users/userbase_serializers.py`.
   - Added dashboard serializers to `sims/training/dashboard_serializers.py`.
   - Added type hints to `UserManagementSerializer.get_departments`.
6. **Class-level Serializers**: Added `serializer_class` to various `APIView` subclasses to provide `drf-spectacular` with default schema metadata.

## Remaining Warnings
- 53 warnings remain, mostly "unable to resolve type hint for function".
- These do not block the strict gate if only errors are prohibited, but they should be cleaned up for high-quality documentation.
- "enum naming collision" warning for `status` field.
- "operationId collision" warnings for bulk and workshop endpoints.

## Next Steps
- Resolve remaining type hint warnings using `@extend_schema_field`.
- Fix enum naming collisions.
- Address operationId collisions.
