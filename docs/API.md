# SIMS API Documentation

## Overview

SIMS provides a comprehensive RESTful API for all system operations. All API endpoints are accessible under `/api/` and use JWT authentication.

## Base URL

- Development: `http://localhost:8000`
- Production: `https://your-domain.com`

## Authentication

### JWT Authentication

All authenticated endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <access_token>
```

### Authentication Endpoints

#### Login
```http
POST /api/auth/login/
Content-Type: application/json

{
  "username": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "access": "jwt_access_token",
  "refresh": "jwt_refresh_token",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "full_name": "John Doe",
    "role": "pg"
  }
}
```

#### Register
```http
POST /api/auth/register/
Content-Type: application/json

{
  "username": "string",
  "email": "string",
  "password": "string",
  "password2": "string",
  "first_name": "string",
  "last_name": "string",
  "role": "pg|supervisor|admin"
}
```

#### Refresh Token
```http
POST /api/auth/refresh/
Content-Type: application/json

{
  "refresh": "jwt_refresh_token"
}
```

**Response:**
```json
{
  "access": "new_jwt_access_token"
}
```

## Core API Endpoints

### Academics Module

#### Departments

```http
GET    /academics/api/departments/          # List all departments
POST   /academics/api/departments/          # Create department (admin)
GET    /academics/api/departments/{id}/     # Get department details
PUT    /academics/api/departments/{id}/     # Update department (admin)
DELETE /academics/api/departments/{id}/     # Delete department (admin)
```

#### Batches

```http
GET    /academics/api/batches/              # List all batches
POST   /academics/api/batches/              # Create batch (admin)
GET    /academics/api/batches/{id}/         # Get batch details
PUT    /academics/api/batches/{id}/         # Update batch (admin)
DELETE /academics/api/batches/{id}/         # Delete batch (admin)
GET    /academics/api/batches/{id}/students/ # List students in batch
```

#### Student Profiles

```http
GET    /academics/api/students/                  # List students (role-based)
POST   /academics/api/students/                  # Create student profile (admin)
GET    /academics/api/students/{id}/             # Get student details
PUT    /academics/api/students/{id}/             # Update student (admin/self)
DELETE /academics/api/students/{id}/             # Delete student (admin)
POST   /academics/api/students/{id}/update_status/ # Update student status
```

### Results Module

#### Exams

```http
GET    /results/api/exams/              # List all exams
POST   /results/api/exams/              # Create exam (admin/supervisor)
GET    /results/api/exams/{id}/         # Get exam details
PUT    /results/api/exams/{id}/         # Update exam
DELETE /results/api/exams/{id}/         # Delete exam
GET    /results/api/exams/{id}/scores/  # Get all scores for exam
GET    /results/api/exams/{id}/statistics/ # Get exam statistics
```

#### Scores

```http
GET    /results/api/scores/              # List scores (role-based)
POST   /results/api/scores/              # Create score (admin/supervisor)
GET    /results/api/scores/{id}/         # Get score details
PUT    /results/api/scores/{id}/         # Update score
DELETE /results/api/scores/{id}/         # Delete score
GET    /results/api/scores/my_scores/    # Get current user's scores (students)
```

### Attendance Module

```http
GET    /api/attendance/summary/          # Get attendance summary
POST   /api/attendance/bulk-upload/      # Bulk upload attendance (CSV)
GET    /api/attendance/eligibility/      # Check eligibility status
```

### Logbook Module

```http
GET    /api/logbook/entries/             # List logbook entries
POST   /api/logbook/entries/             # Create entry
GET    /api/logbook/entries/{id}/        # Get entry details
PUT    /api/logbook/entries/{id}/        # Update entry
DELETE /api/logbook/entries/{id}/        # Delete entry
POST   /api/logbook/verify/{id}/         # Verify entry (supervisor)
GET    /api/logbook/pending/             # Get pending verifications
```

### Rotations Module

```http
GET    /rotations/api/list/              # List rotations
POST   /rotations/api/create/            # Create rotation
GET    /rotations/api/{id}/               # Get rotation details
PUT    /rotations/api/{id}/update/       # Update rotation
DELETE /rotations/api/{id}/delete/       # Delete rotation
GET    /rotations/api/calendar/          # Get rotation calendar
GET    /rotations/api/stats/             # Get rotation statistics
```

### Analytics Module

```http
GET    /api/analytics/dashboard/overview/    # Dashboard overview
GET    /api/analytics/dashboard/trends/      # Trends data
GET    /api/analytics/dashboard/compliance/  # Compliance metrics
GET    /api/analytics/performance/           # Performance metrics
```

### Reports Module

```http
GET    /api/reports/generate/            # Generate report
POST   /api/reports/schedule/            # Schedule report
GET    /api/reports/list/                # List available reports
```

### Notifications Module

```http
GET    /api/notifications/                # List notifications
GET    /api/notifications/unread/         # Get unread notifications
POST   /api/notifications/{id}/mark-read/ # Mark as read
GET    /api/notifications/preferences/   # Get preferences
PUT    /api/notifications/preferences/   # Update preferences
```

## Query Parameters

### Pagination

All list endpoints support pagination:

```
?page=1&page_size=25
```

### Filtering

Use query parameters to filter results:

```
?status=active&role=pg
```

### Searching

Use the `search` parameter:

```
?search=john
```

### Ordering

Use the `ordering` parameter:

```
?ordering=-created_at     # Descending
?ordering=name            # Ascending
```

## Response Format

### Success Response

```json
{
  "count": 100,
  "next": "http://api/endpoint/?page=2",
  "previous": null,
  "results": [...]
}
```

### Error Response

```json
{
  "error": "Error message",
  "detail": "Detailed error description"
}
```

## Status Codes

- `200 OK`: Successful GET, PUT, PATCH
- `201 Created`: Successful POST
- `204 No Content`: Successful DELETE
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

## Rate Limiting

- Anonymous users: 100 requests/hour
- Authenticated users: 1000 requests/hour
- Search endpoints: 30 requests/minute

## Best Practices

1. **Always include authentication token** for protected endpoints
2. **Handle token refresh** when access token expires
3. **Use pagination** for large datasets
4. **Implement error handling** for all API calls
5. **Cache responses** when appropriate
6. **Use query parameters** for filtering and searching

## Examples

### Python (using requests)

```python
import requests

# Login
response = requests.post(
    'http://localhost:8000/api/auth/login/',
    json={'username': 'john', 'password': 'password123'}
)
tokens = response.json()

# Make authenticated request
headers = {'Authorization': f'Bearer {tokens["access"]}'}
response = requests.get(
    'http://localhost:8000/academics/api/students/',
    headers=headers
)
students = response.json()
```

### JavaScript (using axios)

```javascript
import axios from 'axios';

// Login
const loginResponse = await axios.post(
  'http://localhost:8000/api/auth/login/',
  { username: 'john', password: 'password123' }
);

const { access } = loginResponse.data;

// Make authenticated request
const studentsResponse = await axios.get(
  'http://localhost:8000/academics/api/students/',
  { headers: { Authorization: `Bearer ${access}` } }
);
```

## Additional Resources

- OpenAPI/Swagger documentation: `/api/docs/` (when configured)
- Postman collection: [Link to collection]
- Frontend TypeScript types: See `frontend/types/index.ts`
