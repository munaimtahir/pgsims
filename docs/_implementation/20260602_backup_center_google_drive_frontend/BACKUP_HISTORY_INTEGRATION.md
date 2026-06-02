# Backup History Integration (2026-06-02 UTC)

## Display
Backup History table adds a compact “Google Drive” column with labels:
- Not uploaded
- Uploaded
- Verified
- Failed
- Restore-ready

## Actions
Drive actions are placed inside “View Details” expanded section to avoid clutter:
- Upload to Drive (only when local backup exists)
- Verify Drive Copy (only when uploaded and not verified)
- Download from Drive (only when verified; download prepares a Restore Wizard upload)

