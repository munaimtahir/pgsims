# Missing API Gaps for Android Integration

This document identifies required backend enhancements to support a high-quality native Android mobile experience.

## 1. High Priority (Blockers for MVP)

### 1.1 Mobile Bootstrap Endpoint
Currently, the app must make 3-4 calls on startup (Login -> Profile -> Summary -> Unread Notifications). 
- **Recommendation**: Create `GET /api/mobile/bootstrap/` which returns:
  - User profile summary.
  - Active role-specific summary (Resident or Supervisor dashboard).
  - Unread notification count.
  - Basic system settings (version, maintenance flags).

### 1.2 Push Notification Registration
There is currently no way for a mobile device to register its push token (FCM).
- **Recommendation**: Create `POST /api/notifications/register-device/`
  - Payload: `{ "token": "fcm_token_string", "platform": "android", "device_id": "unique_id" }`.

### 1.3 Logbook Clinical Evidence Attachments
The `LogbookEntry` model lacks a field for clinical evidence (e.g., photo of redacted prescription or procedure record).
- **Recommendation**: Add an optional `image` or `document` field to `LogbookEntry` or create a generic `Media` attachment system similar to `SubmissionDocument`.

## 2. Medium Priority (UX Improvements)

### 2.1 Consistent Error Schema
While DRF provides standard error responses, a more structured mobile-friendly schema is preferred for easier parsing.
- **Goal**: `{ "code": "VALIDATION_ERROR", "message": "Short description", "fields": { "username": ["Required"] } }`.

### 2.2 Offline Sync Support
The mobile app should ideally support saving logbooks while offline.
- **Requirement**: The backend should support `idempotency-keys` or handle client-generated UUIDs to prevent duplicates if a resident submits the same draft twice during sync.

### 2.3 Search Throttling Information
The app should know the current rate limits to avoid getting blocked silently.
- **Recommendation**: Include `Rate-Limit` headers in responses.

## 3. Low Priority (Future Proofing)

### 3.1 App Version Enforcement
- **Recommendation**: Add a minimum supported version check in the bootstrap endpoint to force updates if the API contract changes breakingly.

### 3.2 Bio-metric Auth Verification
- **Recommendation**: The backend is already set up with JWT, which is fine for biometric auth (the app stores the token in a secure keystore). No backend change needed unless we want dedicated biometric session binding.
