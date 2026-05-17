# Recommended UI Architecture

## Proposed Navigation

Dashboard
  - Overview
  - Today’s Work
  - Alerts / Issues

Onboarding & Imports
  - Guided Import
  - Google Sheet Mapping
  - CSV Upload
  - Validation Preview
  - Import History

Residents
  - Resident List
  - Resident Profiles
  - Training Records
  - Logbook Status

Supervisors
  - Supervisor List
  - Assignments
  - Pending Reviews

Programs
  - Training Programs
  - Rotations
  - Eligibility

Hospitals & Departments
  - Hospitals
  - Departments
  - Hospital-Department Matrix
  - HOD Assignments

Reports
  - Progress Reports
  - Eligibility Reports
  - Export Center

Settings
  - Users & Roles
  - Master Data
  - System Health

## Role-Specific Dashboards

### UTRMC/Admin

Should show:

- System setup status
- Data completion status
- Import/onboarding status
- Resident and supervisor counts
- Problems requiring correction

### Supervisor

Should show:

- My residents
- Pending reviews
- Pending approvals
- Recent submissions
- Alerts

### Resident

Should show:

- My training status
- My logbook progress
- My submissions
- My leave/workshop status

## Architecture Principle

The best UI for PGSIMS is not the one with the most visible data. It is the one that makes the next safe action obvious within 30 seconds.

