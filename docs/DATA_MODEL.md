# PGSIMS Canonical Data Model

The data model for PGSIMS is strictly structured to support postgraduate medical training programs and placements.

## Core Structural Masters

### 1. Hospital (`rotations.Hospital`)
- Represents medical institutions where training rotations take place.
- Key fields: `name`, `code` (unique), `address`, `is_active`.

### 2. Department (`academics.Department`)
- The single canonical list of medical specialties and departments (e.g., Urology, Pathology, Internal Medicine).
- Key fields: `name`, `code` (unique), `description`, `active`.
- **Note**: No secondary or duplicate department models exist in active workflows.

### 3. Hospital-Department Matrix (`rotations.HospitalDepartment`)
- Connects a Hospital and a Department, establishing that a specific department exists and is active inside that hospital site.
- Key fields: `hospital` (FK Hospital), `department` (FK Department), `is_active`.
- Constraint: `UniqueConstraint(fields=["hospital", "department"])`.

## Trainee & Placement Records

### 1. Resident Training Record (`training.ResidentTrainingRecord`)
- Represents a postgraduate resident's enrollment in a specific program.
- Key fields: `resident_user` (FK User), `program` (FK TrainingProgram), `start_date`, `current_level`, `status` (ACTIVE/COMPLETED).

### 2. Resident Rotation Assignment (`training.RotationAssignment`)
- Represents a clinical placement of a resident inside the Hospital-Department matrix.
- Key fields: `resident_training` (FK ResidentTrainingRecord), `hospital_department` (FK HospitalDepartment), `start_date`, `end_date`, `status` (DRAFT/SUBMITTED/APPROVED/COMPLETED).
- **Rule**: Rotations point directly to `HospitalDepartment` matrix rows, not separately to Hospital or Department.

## Users & Assignments

### 1. User (`users.User`)
- Extended Django AbstractUser model with role attributes: `admin`, `supervisor`, `resident`, `utrmc_admin`, `utrmc_user`.

### 2. Department Membership (`users.DepartmentMembership`)
- Connects users to canonical departments with roles (`supervisor`, `resident`, `faculty`).

### 3. Hospital Assignment (`users.HospitalAssignment`)
- Connects users to `HospitalDepartment` sites.

### 4. Supervisor Resident Link (`users.SupervisorResidentLink`)
- Establishes supervision lines between a supervisor and a resident.
