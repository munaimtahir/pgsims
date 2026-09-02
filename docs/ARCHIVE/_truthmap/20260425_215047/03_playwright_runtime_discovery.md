# Stage 3: Playwright Runtime Discovery Audit

**Date**: 2026-04-25 21:50:47 UTC
**Environment**: Local Docker (http://localhost:8082)
**Audit Type**: Observational - No data modification

## Executive Summary

| Role | Landing Page | Sidebar Items | Visible Pages | Broken Pages | Errors |
|------|---|---|---|---|---|
| resident | ✓ | 3 | 0 | 3 | 1 |
| supervisor | ✓ | 1 | 0 | 1 | 1 |
| utrmc_admin | ✓ | 9 | 0 | 9 | 1 |
| admin | ✓ | 9 | 0 | 9 | 1 |

## Findings by Role

### RESIDENT
**Landing Page**: http://localhost:8082/dashboard/resident

**Sidebar Items** (3):
- [ ] My Dashboard → `/dashboard/resident`
- [ ] My Schedule → `/dashboard/resident/schedule`
- [ ] Logbook → `/dashboard/resident/progress`

**Visible Pages** (0):
- None navigated

**Broken/Error Pages** (3):
- ✗ `/dashboard/resident` (404 or error)
- ✗ `/dashboard/resident/schedule` (404 or error)
- ✗ `/dashboard/resident/progress` (404 or error)

**Errors/Issues** (1):
- `Login error: `

**CTAs by Page**:
- **/dashboard/resident**: Sign out, Open Logbook, View Schedule, Logbook & Readiness
- **/dashboard/resident/schedule**: Sign out, Save Draft
- **/dashboard/resident/progress**: Sign out, Save Logbook Draft

### SUPERVISOR
**Landing Page**: http://localhost:8082/dashboard/supervisor

**Sidebar Items** (1):
- [ ] Overview → `/dashboard/supervisor`

**Visible Pages** (0):
- None navigated

**Broken/Error Pages** (1):
- ✗ `/dashboard/supervisor` (404 or error)

**Errors/Issues** (1):
- `Login error: `

**CTAs by Page**:
- **/dashboard/supervisor**: Sign out

### UTRMC_ADMIN
**Landing Page**: http://localhost:8082/dashboard/utrmc

**Sidebar Items** (9):
- [ ] Overview → `/dashboard/utrmc`
- [ ] Hospitals → `/dashboard/utrmc/hospitals`
- [ ] Departments → `/dashboard/utrmc/departments`
- [ ] H-D Matrix → `/dashboard/utrmc/matrix`
- [ ] Users → `/dashboard/utrmc/users`
- [ ] Supervision Links → `/dashboard/utrmc/supervision`
- [ ] HOD Assignments → `/dashboard/utrmc/hod`
- [ ] Programmes → `/dashboard/utrmc/programs`
- [ ] Eligibility Monitor → `/dashboard/utrmc/eligibility-monitoring`

**Visible Pages** (0):
- None navigated

**Broken/Error Pages** (9):
- ✗ `/dashboard/utrmc` (404 or error)
- ✗ `/dashboard/utrmc/hospitals` (404 or error)
- ✗ `/dashboard/utrmc/departments` (404 or error)
- ✗ `/dashboard/utrmc/matrix` (404 or error)
- ✗ `/dashboard/utrmc/users` (404 or error)
- ✗ `/dashboard/utrmc/supervision` (404 or error)
- ✗ `/dashboard/utrmc/hod` (404 or error)
- ✗ `/dashboard/utrmc/programs` (404 or error)
- ✗ `/dashboard/utrmc/eligibility-monitoring` (404 or error)

**Errors/Issues** (1):
- `Login error: `

**CTAs by Page**:
- **/dashboard/utrmc**: Sign out, Open Data Quality, 🔍 Dry Run (validate only), ✅ Apply Import, ⬇ Download Template, ⬇ Export CSV, ⬇ Export Excel, 🔍 Dry Run (validate only), ✅ Apply Import, ⬇ Download Template
- **/dashboard/utrmc/hospitals**: Sign out, + Add Hospital, Edit, Edit, Edit, Edit
- **/dashboard/utrmc/departments**: Sign out, + Add Department, Edit, Edit, Edit, Edit, Edit, Edit, Edit, Edit
- **/dashboard/utrmc/matrix**: Sign out, ✓, ✓, ✓, ✓, ✓, ✓, ✓, ✓, ✓
- **/dashboard/utrmc/users**: Sign out, + Add User, Edit, Edit, Edit, Edit, Edit, Edit, Edit, Edit
- **/dashboard/utrmc/supervision**: Sign out, + Add Link
- **/dashboard/utrmc/hod**: Sign out, + Add HOD
- **/dashboard/utrmc/programs**: Sign out, ACTIVE-BASELINEActive Surface Baseline Programme, E2E-FCPSE2E Baseline FCPS Program, PILOT-BASELINEPilot Baseline Program
- **/dashboard/utrmc/eligibility-monitoring**: Sign out, Filter

### ADMIN
**Landing Page**: http://localhost:8082/dashboard/utrmc

**Sidebar Items** (9):
- [ ] Overview → `/dashboard/utrmc`
- [ ] Hospitals → `/dashboard/utrmc/hospitals`
- [ ] Departments → `/dashboard/utrmc/departments`
- [ ] H-D Matrix → `/dashboard/utrmc/matrix`
- [ ] Users → `/dashboard/utrmc/users`
- [ ] Supervision Links → `/dashboard/utrmc/supervision`
- [ ] HOD Assignments → `/dashboard/utrmc/hod`
- [ ] Programmes → `/dashboard/utrmc/programs`
- [ ] Eligibility Monitor → `/dashboard/utrmc/eligibility-monitoring`

**Visible Pages** (0):
- None navigated

**Broken/Error Pages** (9):
- ✗ `/dashboard/utrmc` (404 or error)
- ✗ `/dashboard/utrmc/hospitals` (404 or error)
- ✗ `/dashboard/utrmc/departments` (404 or error)
- ✗ `/dashboard/utrmc/matrix` (404 or error)
- ✗ `/dashboard/utrmc/users` (404 or error)
- ✗ `/dashboard/utrmc/supervision` (404 or error)
- ✗ `/dashboard/utrmc/hod` (404 or error)
- ✗ `/dashboard/utrmc/programs` (404 or error)
- ✗ `/dashboard/utrmc/eligibility-monitoring` (404 or error)

**Errors/Issues** (1):
- `Login error: `

**CTAs by Page**:
- **/dashboard/utrmc**: Sign out, Open Data Quality, 🔍 Dry Run (validate only), ✅ Apply Import, ⬇ Download Template, ⬇ Export CSV, ⬇ Export Excel, 🔍 Dry Run (validate only), ✅ Apply Import, ⬇ Download Template
- **/dashboard/utrmc/hospitals**: Sign out, + Add Hospital, Edit, Edit, Edit, Edit
- **/dashboard/utrmc/departments**: Sign out, + Add Department, Edit, Edit, Edit, Edit, Edit, Edit, Edit, Edit
- **/dashboard/utrmc/matrix**: Sign out, ✓, ✓, ✓, ✓, ✓, ✓, ✓, ✓, ✓
- **/dashboard/utrmc/users**: Sign out, + Add User, Edit, Edit, Edit, Edit, Edit, Edit, Edit, Edit
- **/dashboard/utrmc/supervision**: Sign out, + Add Link
- **/dashboard/utrmc/hod**: Sign out, + Add HOD
- **/dashboard/utrmc/programs**: Sign out, ACTIVE-BASELINEActive Surface Baseline Programme, E2E-FCPSE2E Baseline FCPS Program, PILOT-BASELINEPilot Baseline Program
- **/dashboard/utrmc/eligibility-monitoring**: Sign out, Filter

## Answers to Key Questions

### 1. Does Resident see Logbook in sidebar?
✅ **YES** - Found: "Logbook"

### 2. Does Resident see Workshops in sidebar?
❌ **NO**

### 3. Does UTRMC Admin see Programs in sidebar?
✅ **YES** - Found: "Programmes"

### 4. Does UTRMC Admin see Training Programs in sidebar?
❌ **NO**

### 5. Does Supervisor see Logbook Review in sidebar?
❌ **NO**

### 6. Can any role create a new entity (programs, workshops, etc.)?
❌ **NO** - No create buttons observed

### 7. What pages 404 or error?
- `/dashboard/resident`
- `/dashboard/resident/schedule`
- `/dashboard/resident/progress`
- `/dashboard/supervisor`
- `/dashboard/utrmc`
- `/dashboard/utrmc/hospitals`
- `/dashboard/utrmc/departments`
- `/dashboard/utrmc/matrix`
- `/dashboard/utrmc/users`
- `/dashboard/utrmc/supervision`
- `/dashboard/utrmc/hod`
- `/dashboard/utrmc/programs`
- `/dashboard/utrmc/eligibility-monitoring`

### 8. What API calls are 5xx or fail?
- None detected

## Artifacts
- Screenshots: `docs/_truthmap/20260425_215047/screenshots/`
- Playwright traces: `docs/_truthmap/20260425_215047/traces/`
- CSV matrices: `docs/_truthmap/20260425_215047/*.csv`
