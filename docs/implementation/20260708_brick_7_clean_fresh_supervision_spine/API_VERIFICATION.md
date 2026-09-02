# API VERIFICATION — PGMS Brick 7 Clean Fresh Pilot Supervision Spine

This document outlines the REST API contracts, endpoints, and JSON payload shapes for **Brick 7**.

---

## 1. Endpoints List

All endpoints require authentication (JWT Bearer Token).

| Method | Endpoint | Description | Permitted Roles |
| :--- | :--- | :--- | :--- |
| **GET** | `/api/supervision/assignments/` | List assignments (filtered by role) | `ADMIN`, `RESIDENT`, `SUPERVISOR`, `SUPPORT_STAFF` |
| **POST** | `/api/supervision/assignments/` | Create a new active assignment | `ADMIN` |
| **POST** | `/api/supervision/assignments/{id}/end/` | End an active assignment | `ADMIN` |
| **POST** | `/api/supervision/change-primary/` | Atomically change primary supervisor | `ADMIN` |
| **GET** | `/api/supervision/options/` | Fetch list of valid residents & supervisors | `ADMIN`, `RESIDENT`, `SUPERVISOR`, `SUPPORT_STAFF` |
| **GET** | `/api/supervision/data-quality/` | Retrieve supervision data quality anomalies | `ADMIN` |
| **POST** | `/api/supervision/import/` | CSV mapping importer (dry run & commit) | `ADMIN` |

### Legacy Compatibility Surface

- `/api/supervision-links/` remains available for historical compatibility tests and older admin flows.
- Active frontend helpers do not call `/api/supervision-links/`; they use `frontend/lib/api/supervision.ts` and the `/api/supervision/*` endpoints above.

---

## 2. JSON Payload Details

### POST `/api/supervision/assignments/` (Create Assignment)
- **Request Payload**:
  ```json
  {
    "resident_id": 1,
    "supervisor_id": 2,
    "assignment_type": "PRIMARY",
    "start_date": "2026-07-01",
    "notes": "Assigned for clinical year 1"
  }
  ```
- **Response Shape (201 Created)**:
  ```json
  {
    "id": 12,
    "resident": {
      "id": 1,
      "name": "Dr. Ahmad Ali",
      "username": "pgr001",
      "department": "Medicine",
      "training_site": "Allied Hospital"
    },
    "supervisor": {
      "id": 2,
      "name": "Prof. Khalid Mahmood",
      "department": "Medicine",
      "training_site": "Allied Hospital",
      "designation": "Professor"
    },
    "assignment_type": "PRIMARY",
    "status": "ACTIVE",
    "is_active": true,
    "start_date": "2026-07-01",
    "end_date": null,
    "notes": "Assigned for clinical year 1",
    "reason_for_change": "",
    "created_at": "2026-07-08T21:30:00Z",
    "updated_at": "2026-07-08T21:30:00Z"
  }
  ```

### POST `/api/supervision/assignments/{id}/end/` (End Assignment)
- **Request Payload**:
  ```json
  {
    "end_date": "2026-12-31",
    "reason_for_change": "Completed rotation"
  }
  ```
- **Response Shape (200 OK)**:
  ```json
  {
    "id": 12,
    "status": "ENDED",
    "is_active": false,
    "end_date": "2026-12-31",
    "reason_for_change": "Completed rotation"
  }
  ```

### POST `/api/supervision/change-primary/` (Change Primary Supervisor)
- **Request Payload**:
  ```json
  {
    "resident_id": 1,
    "new_supervisor_id": 3,
    "start_date": "2026-08-01",
    "reason_for_change": "Previous primary supervisor retired"
  }
  ```
- **Response Shape (200 OK)**:
  ```json
  {
    "id": 13,
    "resident": { "id": 1, "name": "Dr. Ahmad Ali" },
    "supervisor": { "id": 3, "name": "Dr. Sajid Raza" },
    "assignment_type": "PRIMARY",
    "status": "ACTIVE",
    "is_active": true,
    "start_date": "2026-08-01"
  }
  ```

### GET `/api/supervision/options/` (Options Choices list)
- **Response Shape (200 OK)**:
  ```json
  {
    "residents": [
      {
        "id": 1,
        "name": "Dr. Ahmad Ali",
        "username": "pgr001",
        "training_site": "Allied Hospital",
        "department": "Medicine",
        "program": "FCPS",
        "academic_session": "Session 2026",
        "has_active_primary": true
      }
    ],
    "supervisors": [
      {
        "id": 2,
        "name": "Prof. Khalid Mahmood",
        "training_site": "Allied Hospital",
        "department": "Medicine",
        "designation": "Professor",
        "active_primary_count": 2,
        "active_total_count": 3
      }
  ]
}
```

## 3. Frontend Helper Contract

The current frontend supervision helper exports:

1. `listAssignments()`
2. `getAssignment(id)`
3. `createAssignment(payload)`
4. `endAssignment(id, payload)`
5. `changePrimary(payload)`
6. `getSupervisionOptions(filters)`
7. `getSupervisionDataQuality()`
8. `importSupervisionCsv(payload)`
