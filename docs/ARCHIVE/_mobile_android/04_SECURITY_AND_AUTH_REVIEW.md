# Security and Auth Review for Mobile Integration

## 1. Authentication Protocol
- **Method**: JWT (JSON Web Token) via `rest_framework_simplejwt`.
- **Flow**:
  1. `POST /api/auth/login/` -> Obtain `access` and `refresh` tokens.
  2. Header: `Authorization: Bearer <access_token>`.
  3. Expiry: Access token (60 min), Refresh token (7 days).
- **Mobile Security**: Refresh tokens MUST be stored in the Android **EncryptedSharedPreferences** or **Keystore**.

## 2. Authorization (RBAC)
- The backend enforces Role-Based Access Control (RBAC) at the viewset/endpoint level.
- **Permissions**:
  - `IsResident`: Scopes logbook and summary to own data.
  - `IsSupervisor`: Allows access to `review-queue` and supervised residents' progress.
- **Security Check**: Mobile app must NOT rely on client-side role checks for security; the backend is the source of truth and enforces these.

## 3. Data Integrity & Safety
- **HTTPS**: Required for all production API traffic.
- **CORS**: `corsheaders` is active. For the mobile app, `CORS_ALLOWED_ORIGINS` may need to include `null` or specific app schemas if running in a WebView, but for native Retrofit calls, CORS is typically not enforced by the backend against non-browser clients.
- **CSRF**: `CsrfViewMiddleware` is active. However, DRF's `SessionAuthentication` uses CSRF, while `JWTAuthentication` does not. Native mobile apps using JWT are exempt from CSRF tokens.

## 4. Input Validation & Throttling
- **Throttling**: Anon (100/hr) and User (1000/hr) rates are active. Login is further limited to 5/min.
- **SQL Injection**: Prevented by Django ORM.
- **Mass Assignment**: Prevented by explicit Serializer `fields` definitions.

## 5. Potential Risks
- **Token Leakage**: If the device is compromised, a 7-day refresh token allows persistent access.
- **Mitigation**: Implement "Logout from all devices" on the backend by blacklisting refresh tokens (requires enabling `token_blacklist` app in Django).
- **Certificate Forgery**: Residents might upload fake certificates. The backend should ideally hash or sign files, but currently, it relies on Supervisor manual verification.
