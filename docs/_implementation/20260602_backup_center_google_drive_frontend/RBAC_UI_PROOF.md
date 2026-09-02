# RBAC UI Proof (2026-06-02 UTC)

## Super Admin (`admin`)
- Sees Google Drive Backup panel and all action buttons.
- Sees per-backup Google Drive state and drive actions in Backup History details.

## UTRMC Admin (`utrmc_admin`)
- Sees Backup Center page but does not see restore/disaster recovery controls.
- Sees Google Drive Backup panel label but no unsafe Drive action buttons (“Super Admin only”).

## Restricted roles
- Blocked from Backup Center entirely (existing behavior preserved).

