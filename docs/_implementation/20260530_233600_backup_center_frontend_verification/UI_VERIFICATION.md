# Backup Center Frontend UI Verification and Polish - UI Verification

**Date**: May 30, 2026  
**Status**: VERIFIED  

---

## 1. Screen Flow Mapping

### 1.1. Status Cards Layout
- Displays at `/dashboard/utrmc/backup` for allowed admins:
  - **Last Regular System Backup**: Shows date/time of last Routine backup or "None yet".
  - **Last Full Server Recovery Backup**: Shows date/time of last Disaster backup or "None yet".
  - **Backup Health**: Shows "OK" (green) if last Routine backup exists, else "Needs first backup" (yellow).
  - **Last Restore**: Displays date/time of last restore.
  - **Total Backups**: Integer count of existing backups.

### 1.2. Creation Controls
- **Super Admin (`admin`)**: Sees buttons for "Create Regular System Backup" and "Create Full Server Recovery Backup".
- **UTRMC Admin (`utrmc_admin`)**: Only sees the "Create Regular System Backup" button. The disaster option is fully hidden.
- Description blocks dynamically adjust to show only allowed features.

### 1.3. History Table Actions
- For each backup row:
  - **Download**: Fetches and downloads the `.pgsimsbak`/`.pgsimsdr` zip file.
  - **Check File**: Triggers backend checksum/manifest validation.
  - **View Details**: Toggles an expandable card displaying Backup Contents, File Integrity Details, and Technical Details.
  - **Restore**: Prompts the user with step-by-step instructions to download first, then run the upload wizard.

### 1.4. Restore Wizard Flow
- **Step 1: Upload**: Drag/drop or select file. Safety warning clearly visible.
- **Step 2: Check File**: Validates integrity. Mapped messages shown (e.g. damaged files vs invalid backup formats).
- **Step 3: Review Details**: Displays metadata under group-style accordion panels. Offers "Dry-Run Test".
- **Step 4: Confirm**: Enforces password, typing "RESTORE", and checkbox acknowledgement.
- **Step 5: Result**: Displays final success/failure result inside the wizard.

## 2. Empty States and Error Message Mapping
- **Empty Backups History**: Displays “No backups have been created yet. Create your first Regular System Backup before importing real data.”
- **Checksum Error**: Displays “This backup file may be damaged or changed after creation. Please use another backup file.”
- **Format Error**: Displays “This does not look like a valid PGSIMS backup file.”
- **Restore Failure**: Displays “Restore could not be completed. Your current data has not been replaced. Please contact the technical administrator and keep the automatic protection backup.”
- **Access Denied (Resident/Supervisor/HOD)**: Displays "Access Denied. You do not have permission to access the Backup Center. Only administrative staff may view this page."
