# PGSIMS User Roles and Permissions

This document outlines the Role-Based Access Control (RBAC) matrix for PGSIMS.

## Roles
1. **Super Admin / Admin**: Complete access to create/update configuration masters, onboard staff/residents, assign supervisors, and execute bulk setup data imports.
2. **UTRMC Admin**: Clinical governance admin with oversight, setup access, and override approval rights for inter-hospital assignments.
3. **UTRMC User / Viewer**: Read-only oversight access to programs, eligibility statistics, and matrix layouts. Cannot mutate data.
4. **HOD (Head of Department)**: Manages and approves rotation placements and logbook configurations at the department level.
5. **Supervisor / Faculty**: Reviews and verifies logbook entries, leaves, and documents for assigned residents.
6. **Resident / Postgraduate (PG)**: Submits logbook entries, leaves, and academic documents. Views personal dashboard and scheduling timelines.
7. **Data Entry / Clerk**: Limited administrative access for trainee registration and data entry.

## Permissions & Scope Matrix

| Action | Admin / UTRMC Admin | HOD | Supervisor | Resident |
| :--- | :---: | :---: | :---: | :---: |
| **Manage Hospitals/Depts** | Yes | No | No | No |
| **Manage Matrix Setup** | Yes | No | No | No |
| **Onboard Users / Bulk Import** | Yes | No | No | No |
| **Assign Supervisors** | Yes | Yes (Dept) | No | No |
| **Create Rotation Placements** | Yes | Yes (Dept) | No | No (View only) |
| **Submit Leaves** | No | No | No | Yes (Own) |
| **Approve Leaves / Rotations** | Yes | Yes (Dept) | Yes (Assigned) | No |
| **Submit Logbook** | No | No | No | Yes (Own) |
| **Approve/Return Logbook** | No | Yes (Dept) | Yes (Assigned) | No |
| **View Eligibility Monitors** | Yes | Yes (Dept) | Yes (Assigned) | Yes (Own) |
