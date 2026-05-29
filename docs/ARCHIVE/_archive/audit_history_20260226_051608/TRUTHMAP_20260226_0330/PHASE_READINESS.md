# Phase Readiness (Truth Map)

## Phase Readiness Matrix

| Phase | Requirement | Status | Evidence / Gap |
|-------|-------------|--------|----------------|
| **Phase 1** | Resident logbook submission | ✅ PASS | API and UI exist, flow is functional. |
| **Phase 1** | Supervisor verification | ❌ FAIL | `AttributeError` on `supervisor_comments` in Backend. |
| **Phase 1** | UTRMC dept overview | ⚠️ PARTIAL | Generic Admin dashboard exists, but not "Dept Overview" specific. |
| **Phase 1** | Audit immutability | ✅ PASS | `simple-history` tracks all changes. |
| **Phase 2** | Compliance dashboards | ✅ PASS | `getCompliance` API exists in `analytics.ts`. |
| **Phase 2** | Reminders | ⚠️ PARTIAL | `NotificationService` has logic for deadlines, but needs Celery scheduling. |
| **Phase 2** | Escalation trail | ⚠️ PARTIAL | Audit logs exist, but no explicit "Escalate" action. |
| **Phase 3** | Eligibility calculation | ✅ PASS | `calculate_attendance_summary` in `attendance/services.py` works. |
| **Phase 3** | Config per program | ⚠️ PARTIAL | `LogbookTemplate` handles some config, but rotation rules are hardcoded. |
| **Phase 4** | Research milestones | ⚠️ PARTIAL | `research` template type exists, but no milestone tracking. |

## Concrete Missing Pieces

### For Phase 1 FAIL (Supervisor Verify)
- **Fix**: Rename `supervisor_comments` to `supervisor_feedback` in `backend/sims/logbook/api_views.py`.
- **Fix**: Add `supervisor_feedback` to `PGLogbookEntrySerializer`.

### For Phase 2 PARTIAL (Escalation)
- **Missing**: A field or related model for "Exemption" or "Escalation" in `LogbookEntry`.
- **Location**: `sims.logbook.models.LogbookEntry`.

### For Phase 3 PARTIAL (Config)
- **Missing**: A `ProgramConfig` model to define attendance thresholds per specialty rather than global env var.
- **Location**: `sims.academics.models`.

## Known Unknowns
- Are "Eligibility Gates" purely attendance-based or do they include logbook quota checks? (Database has `MIN_LOGBOOK_ENTRIES_PER_ROTATION` in `settings.py` but logic not yet linked).

## Immediate Next Actions
1. Implement "lock" logic for `LogbookEntry` once status is `approved`.
2. Link `MIN_LOGBOOK_ENTRIES_PER_ROTATION` from settings to a validation service.
