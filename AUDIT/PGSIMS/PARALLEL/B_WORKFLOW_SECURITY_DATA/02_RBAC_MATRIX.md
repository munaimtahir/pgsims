# RBAC MATRIX

## ROLES DISCOVERED
* **ADMIN**
* **SUPERVISOR**
* **RESIDENT**
* **SUPPORT_STAFF**

## RESOURCE AUTHORIZATION

| Resource/Action | Role | UI Visible | API Allowed | Object Scope | Expected | Actual |
|-----------------|------|------------|-------------|--------------|----------|--------|
| Resident Profile (Read) | Resident | Yes | Yes | Self Only | Self Only | Self Only |
| Resident Profile (Read) | Supervisor | Yes | Yes | Assigned Only | Assigned Only | Assigned Only |
| Resident Profile (Read) | Admin | Yes | Yes | All | All | All |
| Supervision Link (Create) | Admin | Yes | Yes | All | All | All |
| Logbook (Submit) | Resident | Yes | Yes | Self Only | Self Only | Self Only |
| Submissions (Review) | Supervisor | Yes | Yes | Assigned Only | Assigned Only | Assigned Only |
| Resident Documents (Read) | Supervisor | Yes | Yes | Assigned Only | Assigned Only | Assigned Only |
| Resident Documents (Read) | Resident | Yes | Yes | Self Only | Self Only | Self Only |
