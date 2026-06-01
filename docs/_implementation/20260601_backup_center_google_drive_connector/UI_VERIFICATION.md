# UI Verification

## Requirements (minimal, additive)
- Add a “Google Drive Backup” panel/card to Backup Center
- Show connection status, connected account email (if available), folder name, last upload/verify timestamps
- Super Admin actions only; no secrets displayed

## Status
- Added “Google Drive Backup” panel to existing Backup Center page (no route changes).
- Super Admin can trigger connect/disconnect/health check/folder/upload/verify/download actions.
- Download action prepares a restore upload and opens the existing Restore Wizard flow.
