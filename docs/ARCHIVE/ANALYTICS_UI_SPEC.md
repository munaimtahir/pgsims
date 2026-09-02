# Admin Analytics UI Spec

Route: `/dashboard/admin/analytics`  
Navigation: existing Admin nav item **Analytics** (unchanged/frozen route policy).

## Global Filter Bar
- Date range (`start_date`, `end_date`), default last 14 days
- Department filter (`department_id`)
- Role filter (`role`)
- CSV export button for current tab table (`GET /api/analytics/v1/tabs/{tab}/export/`)

Loading state: table skeleton  
Empty state: `No data yet for the selected filters.`

## Tabs
1. Overview
2. Adoption
3. Logbook
4. Review/SLA
5. Departments
6. Rotations
7. Research
8. Data Ops
9. System
10. Security
11. Live

## Widget/Chart/Table Definitions

| Tab | Widget | Metric definition | Query | Endpoint | Empty/Loading |
|---|---|---|---|---|---|
| Overview | Total Events card | Sum of tracked events in filter range | Count all tab events | `/v1/tabs/overview/` | 0 shown / skeleton |
| Overview | Login Success card | Count `auth.login.succeeded` | Group by event_type | `/v1/tabs/overview/` | 0 shown / skeleton |
| Adoption | Feature Usage card | Count `ui.feature.used` | Group by event_type + day series | `/v1/tabs/adoption/` | 0 shown / skeleton |
| Logbook | Status events table | Counts by logbook workflow events | Group by logbook event_type | `/v1/tabs/logbook/` | empty table / skeleton |
| Review/SLA | Avg Review Time card | Avg hours from submit/resubmit to first review action | entity pair timing calculation | `/v1/tabs/review-sla/` | 0 shown / skeleton |
| Departments | Department activity table | Events by department | Group by `department_id` | `/v1/tabs/departments/` | empty table / skeleton |
| Rotations | Hospital activity table | Events by hospital | Group by `hospital_id` | `/v1/tabs/rotations/` | empty table / skeleton |
| Research | Research events table | Count research event types (reserved) | Group by event_type | `/v1/tabs/research/` | empty table / skeleton |
| Data Ops | Import/Export status table | Counts for started/completed/failed | Group by event_type | `/v1/tabs/data-ops/` | empty table / skeleton |
| System | API/system errors table | Counts for `system.*` types | Group by event_type + day | `/v1/tabs/system/` | empty table / skeleton |
| Security | RBAC/Login failure table | Counts for denied/failure | Group by event_type + day | `/v1/tabs/security/` | empty table / skeleton |
| Live | Live feed table | Last up to 200 events | Desc by occurred_at | `/v1/tabs/live/` (poll 7s) | empty table / skeleton |

## Live Feed Behavior
- Poll interval: 7 seconds
- Max events shown: 200
- Uses global filters
- No websockets/SSE

## Widget → Source Mapping Matrix

| Widget | Analytics category | Required events | Aggregation | Endpoint | Frontend component |
|---|---|---|---|---|---|
| Total Events | overview | all tab events | sum | `/v1/tabs/overview/` | KPI card |
| Login Success | security/auth | `auth.login.succeeded` | count | `/v1/tabs/overview/` | KPI card |
| Login Failure | security/auth | `auth.login.failed` | count/day | `/v1/tabs/security/` | table + series |
| Logbook Created | logbook | `logbook.case.created` | count | `/v1/tabs/logbook/` | table |
| Logbook Submitted | logbook | `logbook.case.submitted`,`logbook.case.resubmitted` | count/day | `/v1/tabs/logbook/` | table + series |
| Logbook Verified | review | `logbook.case.verified` | count | `/v1/tabs/logbook/` | table |
| Sent Back/Rejections | review | `logbook.case.sent_back`,`logbook.case.rejected` | count | `/v1/tabs/logbook/` | table |
| Review SLA | review | submit/resubmit + review events | avg duration | `/v1/tabs/review-sla/` | KPI + table |
| Department Distribution | departments | all events with department_id | group count | `/v1/tabs/departments/` | table |
| Hospital Distribution | rotations | all events with hospital_id | group count | `/v1/tabs/rotations/` | table |
| Import Pipeline | data ops | `data.import.*` | count | `/v1/tabs/data-ops/` | table |
| Export Pipeline | data ops | `data.export.*` | count | `/v1/tabs/data-ops/` | table |
| API Error Monitor | system | `system.api.error` | count/day | `/v1/tabs/system/` | table + series |
| RBAC Denials | security | `auth.rbac.denied` | count/day | `/v1/tabs/security/` | table + series |
| Live Feed | live | all recent events | latest N | `/v1/tabs/live/` | table (polling) |
