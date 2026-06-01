# Token Storage Proof

## Requirements
- Access token and refresh token are encrypted at rest
- No plaintext tokens in DB
- No token fields leaked via API

## Status
- Tokens are stored encrypted via Fernet (`backend/sims/backup_center/encryption.py`).
- Test asserts stored DB fields are not plaintext and decrypt back to expected values (`backend/sims/backup_center/tests.py`).
