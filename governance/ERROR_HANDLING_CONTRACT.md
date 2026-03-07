# Error Handling Contract

## Standard Error Response Shape

All API errors must return a JSON body following one of these shapes:

### Validation Error (400)
```json
{
  "field_name": ["Error message for this field."],
  "non_field_errors": ["Non-field error message."]
}
```
Or for nested objects:
```json
{
  "nested_object": {
    "field_name": ["Error message."]
  }
}
```

### Authentication Error (401)
```json
{
  "detail": "Authentication credentials were not provided."
}
```
Or for expired token:
```json
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid",
  "messages": [{"token_class": "AccessToken", "token_type": "access", "message": "Token is expired"}]
}
```

### Authorization Error (403)
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### Not Found (404)
```json
{
  "detail": "Not found."
}
```

### Workflow Conflict (409)
```json
{
  "detail": "Cannot perform this action in the current state.",
  "current_status": "approved",
  "allowed_statuses": ["draft", "returned"]
}
```

### Server Error (500)
```json
{
  "detail": "A server error occurred. Please try again later."
}
```

---

## Frontend Error Handling Rules

### Display Logic

| HTTP Status | User Display | Action |
|-------------|-------------|--------|
| 400 | Show field-level validation messages inline | Highlight offending form fields |
| 401 | Redirect to login page | Clear stored tokens |
| 403 | Show "Access denied" message | Do not redirect |
| 404 | Show "Not found" message | Optionally navigate back |
| 409 | Show workflow conflict message with current state | Refresh page state |
| 422 | Treat as 400 (unprocessable entity) | Show validation errors |
| 500 | Show generic "Something went wrong" message | Offer retry button |
| Network error | Show "Cannot connect to server" | Offer retry button |

### Token Expiry Handling
- Axios interceptor in `frontend/lib/api/client.ts` handles automatic token refresh on 401
- If refresh fails, user is redirected to `/login`
- Tokens are cleared from cookies on redirect

### API Client Error Pattern
```typescript
try {
  const result = await apiFunction(payload);
  // handle success
} catch (error) {
  if (axios.isAxiosError(error)) {
    const status = error.response?.status;
    const data = error.response?.data;
    // display appropriate error to user
  }
}
```

---

## Workflow State Errors

For state machine violations, backends must return 409 with the current state and valid transitions.

### Rotation Workflow
```
draft → submitted → approved → active → completed
                 ↘ returned → draft (re-editable)
                 ↘ rejected (terminal)
```

### Leave Workflow
```
draft → submitted → approved (terminal)
                 ↘ rejected (terminal)
```

### Research Workflow
```
draft → submitted_to_supervisor → synopsis_approved → submitted_to_university → accepted
                               ↘ supervisor_returned → draft (re-editable)
```

---

## Throttle Errors

When rate limit is exceeded (login endpoint):
```json
{
  "detail": "Request was throttled. Expected available in X seconds."
}
```
HTTP Status: `429 Too Many Requests`

---

## Bulk Operation Errors

For bulk import endpoints, partial success is reported as:
```json
{
  "success_count": 45,
  "error_count": 5,
  "errors": [
    {"row": 3, "field": "email", "message": "Invalid email format"},
    {"row": 7, "field": "role", "message": "Unknown role value"}
  ]
}
```
HTTP Status: `200 OK` (partial success is not an error at the HTTP level)
