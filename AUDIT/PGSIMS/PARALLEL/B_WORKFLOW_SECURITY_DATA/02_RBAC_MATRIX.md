# RBAC MATRIX

## ROLES DISCOVERED
* **ADMIN**
* **SUPERVISOR**
* **RESIDENT**
* **SUPPORT_STAFF**

## RESOURCE AUTHORIZATION

This matrix summarizes both statically inspected and dynamically verified authorization rules. Tested scenarios cover both positive path (authorized access) and negative path (unauthorized access attempts).

| Resource/Action | Role | Method | Positive / Negative Scenario | Expected | Actual |
|-----------------|------|--------|------------------------------|----------|--------|
| Resident Profile (Read) | Resident | DYNAMIC_API | Negative: Resident reads other Resident profile | 403 / 404 | 404 Not Found (via Queryset) |
| Resident Profile (Read) | Supervisor | DYNAMIC_API | Negative: Supervisor reads unassigned Resident profile | 403 / 404 | 404 Not Found (via Queryset) |
| Resident Profile (Read) | Supervisor | DYNAMIC_API | Positive: Supervisor reads assigned Resident profile | 200 OK | 200 OK |
| Resident Profile (Read) | Admin | STATIC_CODE_REVIEW | Positive: Admin views any profile | 200 OK | 200 OK (Allowed by IsManager) |
| Resident Profile (Update) | Resident | STATIC_CODE_REVIEW | Negative: Self-update elevates role | 400/403 | Blocked by Serializer |
| Supervision Link (Create) | Admin | STATIC_CODE_REVIEW | Positive: Admin links Resident | 201 Created | 201 Created |
| Supervision Link (Create) | Resident | STATIC_CODE_REVIEW | Negative: Resident links themselves | 403 Forbidden | 403 Forbidden |
| Submissions (Review) | Supervisor | DYNAMIC_API | Positive: Review valid assigned submission | 200 OK | 200 OK |
| Resident Documents (Read) | Supervisor | STATIC_CODE_REVIEW | Negative: Supervisor downloads unassigned doc | 403/404 | Blocked via Queryset |
| Resident Documents (Read) | Resident | STATIC_CODE_REVIEW | Negative: Resident downloads other doc | 403/404 | Blocked via Queryset |
