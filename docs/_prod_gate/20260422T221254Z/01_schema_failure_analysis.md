# Schema Failure Analysis

**Timestamp (UTC):** 20260422T221254Z

## Status

Current command fails with warnings/errors:
```bash
cd backend && SECRET_KEY=test-secret python3 manage.py spectacular --file ../OUT/prod_gate_artifacts/20260422T211654Z/schema/openapi.yaml --validate --fail-on-warn
```

Output contains ~50 schema generation issues.

## Issue Classification and Root Causes

### Issue Class 1: APIViews Without Schema Annotations (25+ views)

**Root Cause:** APIViews that don't inherit from ViewSets or use `@extend_schema` decorators lack serializer information for schema generation.

**Affected Views:**
- `sims/users/userbase_views.py`: DataQualitySummaryView, DataQualityUsersView, DataQualityRecomputeView, DataCorrectionAuditView, AuthMeView
- `sims/users/api_views.py`: change_password_view, logout_view, password_reset_request_view, password_reset_confirm_view, user_profile_view, update_profile_view, register_view
- `sims/bulk/views.py`: BulkAssignmentView, BulkReviewView, BulkImportView, BulkTraineeImportView, BulkSupervisorImportView, BulkResidentImportView, BulkDepartmentImportView, BulkExportView, BulkImportEntityView, BulkTemplateView
- `sims/training/views.py`: ResidentOperationalDashboardView, SupervisorOperationalDashboardView, HODOperationalDashboardView, UTRMCOperationalDashboardView, MyRotationsView, MyLeavesView, LogbookReviewQueueView, LogbookMyThresholdView, ResidentResearchProjectView, ResearchProjectActionView, ResidentThesisView, ThesisSubmitView, MyWorkshopCompletionsView, MyWorkshopCompletionDetailView, MilestoneResearchRequirementView, MyEligibilityView
- `sims/notifications/views.py`: NotificationMarkReadView, NotificationPreferenceView, NotificationUnreadCountView

**Fix Strategy:**
- For each view, add `@extend_schema` decorator with appropriate `request` and `responses` parameters
- Example:
  ```python
  from drf_spectacular.utils import extend_schema
  from drf_spectacular.openapi import OpenApiResponse
  
  class MyAPIView(APIView):
      @extend_schema(
          request=MyRequestSerializer,
          responses=MyResponseSerializer,
          description="Do something"
      )
      def post(self, request):
          # ...
  ```

### Issue Class 2: Duplicate Department Serializers (4 warnings)

**Root Cause:** Two different Department serializers exist:
- `sims.academics.serializers.DepartmentSerializer` (canonical)
- `sims.users.userbase_serializers.DepartmentSerializer` (duplicate/wrapper)

**Error Messages:**
```
Warning [DepartmentViewSet > DepartmentSerializer]: Encountered 2 components with identical names "Department" and different identities
```

**Affected Files:**
- `sims/users/userbase_serializers.py:43` defines `DepartmentSerializer`
- `sims/academics/serializers.py` defines the canonical `DepartmentSerializer`
- `sims/users/userbase_views.py:112` uses DepartmentViewSet with the userbase serializer

**Fix Strategy:**
Option A (Recommended - Contract-First): Remove `sims.users.userbase_serializers.DepartmentSerializer` and use `sims.academics.serializers.DepartmentSerializer` throughout.

Option B (If userbase version differs intentionally): Rename to `DepartmentUserbaseSerializer` or similar to avoid collision.

Check which fields differ and use the canonical Department model from `sims.academics.models` per `AGENTS.md` governance rules.

### Issue Class 3: Missing @extend_schema_field on SerializerMethodFields (7 warnings)

**Root Cause:** SerializerMethodFields without return type hints or `@extend_schema_field` can't be introspected.

**Affected Serializers and Fields:**
- `sims/training/serializers.py:139` LeaveRequestSerializer.get_resident_name
- `sims/training/serializers.py:161` DeputationPostingSerializer.get_resident_name
- `sims/training/serializers.py:429` LogbookEntrySerializer.get_resident_name
- `sims/training/serializers.py:429` LogbookEntrySerializer.get_reviewed_by_name
- `sims/training/serializers.py:415` LogbookReviewSerializer.get_reviewer_name
- `sims/training/serializers.py:384` LogbookThresholdConfigSerializer.get_configured_by_name
- `sims/training/serializers.py:52` ProgramRotationTemplateSerializer.get_allowed_hospital_names

**Fix Strategy:**
For each SerializerMethodField, add return type hint and/or `@extend_schema_field` decorator:
```python
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

class MySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    
    @extend_schema_field(serializers.CharField())
    def get_name(self, obj):
        return str(obj.name)
```

### Issue Class 4: Max/Min Value Type Warnings

**Root Cause:** Some numeric fields have max/min values that aren't proper integers.

**Fix Strategy:**
Ensure all IntegerField, DecimalField, etc. have proper integer/decimal constraints:
```python
# Check any field like:
field = serializers.IntegerField(max_value="123")  # Wrong
# Should be:
field = serializers.IntegerField(max_value=123)  # Correct
```

### Issue Class 5: Queryset Inspection Failures on Parameterized ViewSets

**Root Cause:** Views like ProgramMilestoneViewSet use nested routes (e.g., `/programs/{id}/milestones/`) where queryset depends on URL parameters. Drf-spectacular can't introspect the filtered queryset without context.

**Error Message:**
```
Warning [ProgramMilestoneViewSet]: Failed to obtain model through view's queryset due to raised exception. (Exception: 'program_id')
```

**Affected Views:**
- `sims/training/views.py:931` ProgramMilestoneViewSet
- Others with nested routes

**Fix Strategy:**
Add `@extend_schema` with custom `responses` or ensure queryset inspection gracefully handles missing kwargs:
```python
def get_queryset(self):
    if not self.kwargs.get('program_id'):
        return self.queryset.none()  # Schema generation fallback
    return self.queryset.filter(program_id=self.kwargs['program_id'])
```

### Issue Class 6: NotificationListView Queryset Inspection

**Root Cause:** View tries to filter by `request.user.id` but during swagger fake view generation, request.user is AnonymousUser.

**Fix Strategy:**
Add check in get_queryset():
```python
def get_queryset(self):
    if getattr(self, "swagger_fake_view", False):
        return self.queryset.none()
    return self.queryset.filter(recipient=self.request.user)
```

## Execution Plan

### Priority 1: Fix Duplicate Department Serializers (Quick Win)
- Identify differences between the two DepartmentSerializers
- Remove or rename `sims.users.userbase_serializers.DepartmentSerializer`
- Update `sims/users/userbase_views.py::DepartmentViewSet` to use canonical serializer
- Verify no business logic is lost

**Files to change:**
- `sims/users/userbase_serializers.py` (delete or rename class)
- `sims/users/userbase_views.py` (import canonical serializer)
- `sims/users/urls.py` (if needed)

### Priority 2: Fix High-Traffic APIViews with @extend_schema
Start with views that are:
1. Active in mounted routes (from closure_map.md)
2. Hit during E2E tests
3. Used in phase gates

**Recommended order:**
1. ResidentOperationalDashboardView (E2E resident dashboard depends on this)
2. SupervisorOperationalDashboardView (E2E supervisor tests)
3. UTRMCOperationalDashboardView (E2E UTRMC admin tests)
4. DataQualitySummaryView, DataQualityRecomputeView (UTRMC actions)
5. NotificationListView, NotificationMarkReadView (active in all roles)
6. BulkImportView, BulkExportView (UTRMC bulk operations)
7. AuthMeView, change_password_view, logout_view (auth critical paths)

### Priority 3: Add @extend_schema_field to SerializerMethodFields
- Quick to fix: add decorator with serializers.CharField() / serializers.IntegerField() / etc.
- All 7 affected fields in `sims/training/serializers.py`

### Priority 4: Fix Queryset Inspection Failures
- Add .none() fallbacks or @extend_schema overrides for nested viewsets

### Priority 5: Fix Max/Min Value Types
- Audit any numeric fields with non-integer constraints

## Success Criteria

After fixes, the command should produce no errors and ≤5 acceptable warnings:
```bash
cd backend && SECRET_KEY=test-secret python3 manage.py spectacular --file ../OUT/prod_gate_artifacts/20260422T221254Z/schema/openapi.yaml --validate --fail-on-warn
```

Expected output:
- 0 errors for active APIViews
- Warnings only for deferred/non-active features or framework quirks

## Implementation Notes

- All fixes should preserve existing API behavior
- No breaking changes to request/response contracts
- If contract changes are needed, update `docs/contracts/API_CONTRACT.md` in the same PR
- Test each fix: `pytest sims/<module>/tests.py -k <view_name> -xvs`
- Run full schema generation after each major fix to verify progress
