# Blocker 1 Handoff: Schema Gate

## Session Goal

Attempted to close production blocker #1, the OpenAPI schema gate.

## Current Status

- Blocker not resolved.
- `drf-spectacular` still reports APIView serializer inference errors and warnings.
- The schema command also reports warning-level failures that would still trip `--fail-on-warn`.

## Files Touched In This Attempt

- `backend/sims/training/views.py`
- `backend/sims/bulk/views.py`
- `backend/sims/notifications/views.py`
- `backend/sims/users/userbase_views.py`
- `backend/sims/users/api_views.py`

## What Was Tried

### Retry 1

- Added `@extend_schema(responses={200: None})` at class level for the training, bulk, notification, and userbase APIViews.
- Result: schema errors remained unchanged.

### Retry 2

- Added method-level `@extend_schema(responses={200: None})` to representative training inbox endpoints.
- Result: schema errors remained unchanged.

### Retry 3

- Ran the schema gate against the containerized backend after the decorators were in place.
- Result: `drf-spectacular` still emitted the same serializer inference errors for the active APIViews.

## Commands Run

```bash
cd backend && SECRET_KEY=test-secret python3 manage.py spectacular --file /tmp/schema.yaml --validate --fail-on-warn
docker compose -f docker/docker-compose.yml exec -T backend python manage.py spectacular --file /tmp/schema.yaml --validate --fail-on-warn
```

## Key Logs

### Local runtime attempt

- `RuntimeError: SECRET_KEY environment variable is required`
- `sqlite3.OperationalError: no such table: users_user`

### Container schema run

- APIView errors still present for:
  - `backend/sims/users/userbase_views.py`
  - `backend/sims/users/api_views.py`
  - `backend/sims/bulk/views.py`
  - `backend/sims/training/views.py`
  - `backend/sims/notifications/views.py`
- Warnings still present for:
  - serializer type-hint warnings in `backend/sims/training/serializers.py`
  - `NotificationListView` queryset evaluation
  - `ProgramMilestoneViewSet` path/queryset introspection
  - DRF field max/min warnings

### Representative schema output

```text
Error [RotationApprovalInboxView]: unable to guess serializer
Error [LeaveApprovalInboxView]: unable to guess serializer
Error [MyRotationsView]: unable to guess serializer
Error [MyLeavesView]: unable to guess serializer
Error [ResidentSummaryView]: unable to guess serializer
Error [SupervisorSummaryView]: unable to guess serializer
Error [LogbookReviewQueueView]: unable to guess serializer
Error [ResidentOperationalDashboardView]: unable to guess serializer
Error [SupervisorOperationalDashboardView]: unable to guess serializer
Error [UTRMCOperationalDashboardView]: unable to guess serializer
Error [NotificationMarkReadView]: unable to guess serializer
Error [NotificationPreferenceView]: unable to guess serializer
Error [NotificationUnreadCountView]: unable to guess serializer
Error [BulkReviewView]: unable to guess serializer
Error [BulkImportView]: unable to guess serializer
Error [BulkExportView]: unable to guess serializer
Error [AuthMeView]: unable to guess serializer
Error [DataQualitySummaryView]: unable to guess serializer
Error [DataQualityUsersView]: unable to guess serializer
Error [DataQualityRecomputeView]: unable to guess serializer
Error [DataCorrectionAuditView]: unable to guess serializer
Error [SupervisorAssignedPGsView]: unable to guess serializer
Error [ProgramPolicyView]: unable to guess serializer
Error [MyEligibilityView]: unable to guess serializer
Error [ResidentResearchProjectView]: unable to guess serializer
Error [ResearchProjectActionView]: unable to guess serializer
Error [ResidentThesisView]: unable to guess serializer
Error [ThesisSubmitView]: unable to guess serializer
Error [MyWorkshopCompletionsView]: unable to guess serializer
Error [MyWorkshopCompletionDetailView]: unable to guess serializer
Error [SubmissionCertificatesView]: unable to guess serializer
Error [RotationCompletionsView]: unable to guess serializer
Error [RotationCompletionVerifyView]: unable to guess serializer
```

## Why This Blocker Is Still Open

- The current annotations did not satisfy `drf-spectacular` for these `APIView` and function-based view surfaces.
- The remaining path is likely to require a different schema strategy:
  - explicit serializers for response payloads, or
  - converting some endpoints to `GenericAPIView`/serializer-backed views, or
  - a more precise `extend_schema` pattern per method.
- That is larger than the safe retry budget for this session.

## Recommended Next Agent Handoff

1. Start from `backend/sims/training/views.py` and `backend/sims/users/api_views.py`.
2. Replace the broad `responses={200: None}` approach with explicit response serializers for the active dashboard and workflow endpoints first.
3. Add `swagger_fake_view` guards to schema-sensitive querysets:
   - `ProgramMilestoneViewSet.get_queryset`
   - `NotificationListView.get_queryset`
4. Re-run containerized schema validation after each small batch.
5. Stop and document if the schema count does not move after the next two batches.
