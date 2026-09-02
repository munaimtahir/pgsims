# Encryption Proof

## Requirements
- Raw backup is not uploaded to Drive
- Encrypted backup differs from raw content
- Decrypt restores original content
- Missing encryption key blocks Drive upload

## Status
- File encryption is implemented using Fernet (`backend/sims/backup_center/encryption.py`) and is used by Drive upload/download provider (`backend/sims/backup_center/google_drive.py`).
- Missing `PGSIMS_BACKUP_ENCRYPTION_KEY` blocks token storage and encrypted upload safely (OAuth callback/upload fail with explicit error).
