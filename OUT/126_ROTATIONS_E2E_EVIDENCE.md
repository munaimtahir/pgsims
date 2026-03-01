# OUT/126 — Rotations E2E Evidence

Generated: 2026-03-01

## Method
API smoke test scenario executed against production backend (http://localhost:8014)
with production containers running (`docker compose --env-file .env -f docker/docker-compose.prod.yml`).

## E2E Test Script
Location: `/tmp/e2e_rotations_v2.sh`

## Run Output

```
=== Step 1: Authentication ===
✅ Login as utrmc_admin (HTTP 200)
✅ Login as e2e_pg (resident) (HTTP 200)
✅ Login as supervisor (HTTP 200)
  e2e_pg user ID: 27

=== Step 2: Create Training Program ===
✅ Create Training Program (HTTP 201)
  Program ID: 3

=== Step 3: Get HospitalDepartment ===
✅ HospitalDepartment available (HTTP OK)
  HD_ID=56 DEPT_ID=54

=== Step 4: Create Rotation Template ===
✅ Create Rotation Template (HTTP 201)
  Template ID: 3

=== Step 5: Create Resident Training Record for e2e_pg (user 27) ===
✅ Create Resident Training Record (HTTP 201)
  RTR ID: 3

=== Step 6: Rotation Assignment Workflow ===
✅ Create Rotation draft (HTTP 201)
  Rotation ID: 3
✅ Submit Rotation (HTTP 200)
✅ HOD approve Rotation (HTTP 200)
✅ UTRMC approve Rotation (HTTP 200)
✅ Rotation status APPROVED (HTTP OK)

=== Step 7: Resident views their schedule ===
✅ Resident sees rotations (HTTP OK)

=== Step 8: Leave Request Workflow ===
✅ Resident creates Leave (DRAFT) (HTTP 201)
  Leave ID: 3
✅ Resident submits Leave (HTTP 200)
✅ UTRMC admin approves Leave (HTTP 200)
✅ Leave status APPROVED in resident view (HTTP OK)

=== Step 9: Approval Inboxes ===
✅ UTRMC rotations approval inbox (HTTP 200)
✅ UTRMC leaves approval inbox (HTTP 200)
✅ Supervisor pending rotations inbox (HTTP 200)

=== Step 10: RBAC Guard ===
✅ Resident blocked from creating program (403/401) (HTTP BLOCKED)

=== Step 11: Bulk Import (Dry-run) ===
✅ Bulk import programs dry-run (HTTP 200)

===========================================
RESULTS: 22 PASS, 0 FAIL
STATUS: ALL PASS ✅
===========================================
```

## Scenario Coverage

| Step | Actor | Action | Result |
|------|-------|--------|--------|
| 1 | utrmc_admin | Login | ✅ Token obtained |
| 1 | e2e_pg | Login | ✅ Token obtained |
| 1 | e2e_supervisor | Login | ✅ Token obtained |
| 2 | utrmc_admin | Create Training Program | ✅ 201 Created |
| 3 | utrmc_admin | List HospitalDepartments | ✅ 200 OK |
| 4 | utrmc_admin | Create Rotation Template | ✅ 201 Created |
| 5 | utrmc_admin | Create Resident Training Record | ✅ 201 Created |
| 6a | utrmc_admin | Create Rotation draft | ✅ 201 Created |
| 6b | utrmc_admin | Submit rotation | ✅ 200 OK → status: SUBMITTED |
| 6c | utrmc_admin | HOD approve rotation | ✅ 200 OK → status: APPROVED |
| 6d | utrmc_admin | UTRMC approve rotation | ✅ 200 OK → status: APPROVED |
| 6e | system | Verify final status | ✅ status = APPROVED |
| 7 | e2e_pg | View my rotation schedule | ✅ 200 OK, count ≥ 1 |
| 8a | e2e_pg | Create Leave request (DRAFT) | ✅ 201 Created |
| 8b | e2e_pg | Submit leave | ✅ 200 OK → status: SUBMITTED |
| 8c | utrmc_admin | Approve leave | ✅ 200 OK → status: APPROVED |
| 8d | e2e_pg | Verify leave status | ✅ APPROVED in resident view |
| 9 | utrmc_admin | Check approval inboxes | ✅ 3 endpoints return 200 |
| 10 | e2e_pg | Attempt to create program (blocked) | ✅ 403/401 |
| 11 | utrmc_admin | Bulk import programs dry-run | ✅ 200 OK |

## Container State During Test
```
NAME                   STATUS
pgsims_backend_prod    Up (healthy)
pgsims_beat            Up
pgsims_db_prod         Up (healthy)
pgsims_frontend_prod   Up (healthy)
pgsims_redis_prod      Up (healthy)
pgsims_worker          Up
```

## Verdict: PASS ✅ (22/22 checks passed)
