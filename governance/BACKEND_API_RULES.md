# Backend API Rules

## Architecture

```
HTTP Request
    ↓
URL Router (urls.py)
    ↓
ViewSet / APIView (views.py)
    ↓
Permission Checks (permissions.py)
    ↓
Serializer (serializers.py) — validation
    ↓
Business Logic / Service Layer (services.py or domain/)
    ↓
ORM (models.py)
    ↓
Database (PostgreSQL)
```

---

## URL Routing Rules

### Router Registration
- All standard CRUD resources must use `DefaultRouter` with `ViewSet`
- Custom actions must use `@action(methods=[...], detail=True/False, url_path='...')`
- Route names must be consistent with the contract (use `basename=` in `register()`)

### URL Prefix Policy
| App | URL Prefix | File |
|-----|-----------|------|
| Auth | `/api/auth/` | `sims/users/api_urls.py` |
| Org Graph (userbase) | `/api/` | `sims/users/userbase_urls.py` |
| User CRUD | `/api/users/` | `sims/users/api_user_urls.py` |
| Training | `/api/` | `sims/training/urls.py` |
| Notifications | `/api/notifications/` | `sims/notifications/urls.py` |
| Audit | `/api/audit/` | `sims/audit/urls.py` |
| Bulk | `/api/bulk/` | `sims/bulk/urls.py` |

### Naming Conflicts
- Both `userbase_urls.py` and `training/urls.py` mount at `/api/` — ensure no path conflicts
- If a new endpoint might conflict, consult `docs/integration/API_ENDPOINT_CATALOG.md` first

---

## ViewSet Rules

### Standard ViewSet
```python
class XViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsManager]
    serializer_class = XSerializer
    queryset = X.objects.all()

    def get_queryset(self):
        # Always scope queryset based on requesting user's role
        ...
```

### Action Definition
```python
@action(methods=["post"], detail=True, url_path="submit")
def submit(self, request, pk=None):
    instance = self.get_object()
    # validate state
    # transition state
    # send notification via NotificationService
    return Response(self.get_serializer(instance).data)
```

---

## Serializer Rules

### Read vs Write Serializers
- Use `read_only=True` for fields that should never be written
- Use `write_only=True` for fields that should never be read (e.g., passwords)
- Never use `fields = '__all__'` in create/update serializers
- Explicitly list fields in `Meta.fields`

### Nested Serializers
- Use read-only nested serializers for display (e.g., `hospital_name`)
- Use FK id fields for write operations (e.g., `hospital` takes an integer ID)

### Validation
```python
def validate(self, data):
    # Cross-field validation
    if data['end_date'] < data['start_date']:
        raise serializers.ValidationError("end_date must be after start_date")
    return data

def validate_field_name(self, value):
    # Single-field validation
    if value not in ALLOWED_VALUES:
        raise serializers.ValidationError("Invalid value")
    return value
```

---

## Permission Rules

### Always Declare Permissions
Every view must explicitly declare `permission_classes`. Never rely on global defaults for business-sensitive endpoints.

### Scope Filtering
Supervisors must only see data for their assigned residents:
```python
def get_queryset(self):
    user = self.request.user
    if user.role == 'supervisor':
        return Rotation.objects.filter(pg__supervisionlink__supervisor=user)
    return Rotation.objects.all()
```

### Permission Hierarchy
```
IsTechAdmin > IsManager > IsAuthenticated
```

---

## Model Rules

### Required Fields for Key Models
| Model | Required Fields |
|-------|----------------|
| `HODAssignment` | `start_date` (NOT NULL) |
| `SupervisorResidentLink` (SupervisionLink) | `start_date` (NOT NULL) |
| `RotationAssignment` | `pg`, `department`, `hospital`, `start_date`, `end_date` |
| `ResidentTrainingRecord` | `resident`, `program`, `current_level` |

### Status Constants
Use the model's class-level constants, not raw strings:
```python
rotation.status = RotationAssignment.STATUS_APPROVED  # ✓
rotation.status = "approved"  # ✗
```

### Notification Pattern
Always use `NotificationService`:
```python
from sims.notifications.services import NotificationService

service = NotificationService(actor=request.user)
service.send(
    recipient=pg,
    verb="rotation_returned",
    title="Rotation Returned for Revision",
    template="notifications/rotation_returned.html",
    context={"rotation": rotation},
    channels=[Notification.CHANNEL_IN_APP]
)
```

Never use `Notification.objects.create(user=..., message=..., type=...)`.

---

## Audit Trail Rules

- All state-changing views must go through Django ORM (never raw SQL)
- `django-simple-history` is active on key models and must NOT be removed
- Never directly set `updated_at` or `created_at` — use `auto_now`/`auto_now_add`
- Approved/verified records may only be mutated through explicit workflow actions

---

## Response Rules

### Pagination
All list endpoints using `ModelViewSet` automatically paginate via `DEFAULT_PAGINATION_CLASS`.
Response shape:
```json
{
  "count": 42,
  "next": "http://...",
  "previous": null,
  "results": [...]
}
```

### Action Responses
Custom actions must return the updated serialized object:
```python
return Response(self.get_serializer(instance).data, status=status.HTTP_200_OK)
```

### Delete
Always return `204 No Content` on successful delete.

---

## Test Requirements

Every ViewSet must have tests covering:
1. Authenticated access by an allowed role → success
2. Authenticated access by a disallowed role → 403
3. Unauthenticated access → 401
4. Invalid payload → 400
5. State machine violations → 409 (for workflow endpoints)
