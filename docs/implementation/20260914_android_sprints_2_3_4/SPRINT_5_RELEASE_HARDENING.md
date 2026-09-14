# Android Sprint 5 — Release Hardening

## Implemented safeguards

- The mobile client routes unsupported ADMIN and SUPPORT_STAFF accounts to an explicit restricted
  view; it does not attempt resident API calls for those roles.
- Network operations use bounded HTTP timeouts and turn transport failures into user-safe messages.
- Session refresh retries one request after a 401; an unusable refresh token clears the local session.
- Notification targets are typed and backend-validated. Arbitrary notification metadata never
  becomes a mobile navigation route.
- Offline drafts and uploads are encrypted at rest, constrained to authenticated retry work, and
  purged on logout. Queued material is retained after a failure instead of being silently lost.
- FCM is disabled by default in both client and server configuration.

## Required evidence still outstanding

The current checkout has no Android emulator interaction or VPS deployment evidence for this
change set. The release remains **CONDITIONAL GO** until the role/session/offline matrix, backend
migrations/tests, signed release build, artifact verification, and scoped VPS rollout are recorded.

Do not enable `FCM_ENABLED` as part of this release. It requires a separately reviewed deployment
configuration and an authenticated device-token delivery test.
