# API Verification — Update 0

## Endpoints Verified
1. **`/api/users/` (POST)**:
   - Acceptable payload format: `{"username": "...", "full_name": "...", "role": "...", ...}`
   - Action: Atomically creates `User` + correct Profile + AuditLog inside an atomic transaction.
   - Status: Verified OK.

2. **`/api/auth/me/` (GET)**:
   - Payload shape:
     ```json
     {
       "id": 1,
       "username": "...",
       "role": "...",
       "must_change_password": true,
       "is_profile_complete": false,
       "profile_type": "...",
       "profile_id": 1,
       "profile_status": "INCOMPLETE",
       "profile_schema_version": 1,
       "completed_schema_version": 0,
       "missing_required_fields": ["phone"],
       "allowed_next_route": "/complete-profile"
     }
     ```
   - Status: Verified OK.

3. **`/api/auth/complete-profile/` (GET / POST)**:
   - GET: Fetches missing fields dynamically from the profile completion registry.
   - POST: Submits values, updates user and profile objects, and triggers a state recalculation.
   - Status: Verified OK.
