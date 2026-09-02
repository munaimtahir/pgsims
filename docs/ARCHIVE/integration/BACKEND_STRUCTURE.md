# PGSIMS Backend Structure & API Organization

## 📁 Project Directory Structure

```
/home/munaim/srv/apps/pgsims/backend/
├── sims_project/
│   ├── urls.py                 # Main URL router (entry point)
│   ├── settings.py             # Django settings
│   ├── wsgi.py                 # WSGI config
│   └── health.py               # Health check views
│
├── sims/                       # Main Django app
│   ├── __init__.py
│   ├── users/
│   │   ├── urls.py                    # HTML template routes
│   │   ├── api_urls.py                # JWT auth endpoints
│   │   ├── api_user_urls.py           # User CRUD endpoints
│   │   ├── userbase_urls.py           # Org graph endpoints
│   │   ├── api_views.py               # Auth view functions
│   │   ├── userbase_views.py          # ViewSets: Hospital, Dept, Users, etc.
│   │   ├── views.py                   # HTML template views
│   │   ├── models.py                  # User, Hospital, Department models
│   │   └── serializers.py
│   │
│   ├── training/
│   │   ├── urls.py                    # Training & rotation routes
│   │   ├── views.py                   # ViewSets + APIViews
│   │   │   ├── TrainingProgramViewSet
│   │   │   ├── ProgramRotationTemplateViewSet
│   │   │   ├── RotationAssignmentViewSet (+ 7 @action endpoints)
│   │   │   ├── LeaveRequestViewSet (+ 3 @action endpoints)
│   │   │   ├── DeputationPostingViewSet (+ 3 @action endpoints)
│   │   │   ├── ProgramMilestoneViewSet
│   │   │   ├── WorkshopViewSet (read-only)
│   │   │   └── Custom APIView endpoints (research, thesis, eligibility, etc.)
│   │   ├── models.py
│   │   └── serializers.py
│   │
│   ├── audit/
│   │   ├── urls.py                    # Audit routes
│   │   ├── views.py                   # ActivityLogViewSet, AuditReportViewSet
│   │   ├── models.py
│   │   └── serializers.py
│   │
│   ├── bulk/
│   │   ├── urls.py                    # Bulk operations routes
│   │   ├── views.py                   # 8 bulk APIView classes
│   │   └── models.py
│   │
│   ├── notifications/
│   │   ├── urls.py                    # Notification routes
│   │   ├── views.py                   # 4 notification APIView classes
│   │   ├── models.py
│   │   └── serializers.py
│   │
│   ├── academics/
│   │   ├── urls.py                    # Academic routes
│   │   ├── views.py                   # DepartmentViewSet, BatchViewSet, StudentViewSet
│   │   ├── models.py
│   │   └── serializers.py
│   │
│   ├── rotations/
│   │   ├── urls.py                    # Rotation utility routes
│   │   ├── views.py                   # department_by_hospital_api
│   │   └── models.py                  # Hospital, HospitalDepartment
│   │
│   └── _legacy/                       # Legacy/deprecated apps
│       ├── cases/
│       │   ├── urls.py
│       │   ├── api_urls.py            # Case API routes
│       │   ├── views.py               # HTML views
│       │   ├── api_views.py           # Case API classes
│       │   ├── models.py
│       │   └── serializers.py
│       │
│       ├── logbook/
│       │   ├── urls.py
│       │   ├── api_urls.py            # Logbook API routes
│       │   ├── views.py               # HTML views
│       │   ├── api_views.py           # Logbook API classes
│       │   ├── models.py
│       │   └── serializers.py
│       │
│       ├── certificates/
│       │   ├── urls.py
│       │   ├── api_urls.py            # Certificate API routes
│       │   ├── views.py               # HTML views
│       │   ├── api_views.py           # Certificate API classes
│       │   └── models.py
│       │
│       ├── analytics/
│       │   ├── urls.py                # Analytics routes (13 endpoints)
│       │   ├── views.py               # Dashboard & analytics views
│       │   ├── models.py
│       │   └── serializers.py
│       │
│       ├── attendance/
│       │   ├── urls.py                # Attendance API routes
│       │   ├── api_views.py           # Attendance API classes
│       │   └── models.py
│       │
│       ├── reports/
│       │   ├── urls.py                # Reports API routes
│       │   ├── views.py               # Report view classes
│       │   └── models.py
│       │
│       ├── results/
│       │   ├── urls.py                # Results routes
│       │   ├── views.py               # ExamViewSet, ScoreViewSet
│       │   └── models.py
│       │
│       └── search/
│           ├── urls.py                # Search routes
│           ├── views.py               # GlobalSearchView, etc.
│           └── models.py
│
├── manage.py                   # Django management
├── conftest.py                 # Pytest config
├── pytest.ini
└── requirements.txt            # Python dependencies
```

---

## 🔗 URL Routing Flow

### Main Router (`sims_project/urls.py`)

```python
urlpatterns = [
    # Admin & Utils
    path("", home_view),
    path("admin/", admin.site.urls),
    
    # HTML/Template routes
    path("users/", include("sims.users.urls")),
    path("rotations/", include("sims.rotations.urls")),
    
    # REST API routes
    path("api/auth/", include("sims.users.api_urls")),           # JWT auth
    path("api/", include("sims.users.userbase_urls")),           # Org graph
    path("api/users/", include("sims.users.api_user_urls")),     # User CRUD
    path("api/", include("sims.training.urls")),                 # Training/rotations
    path("api/audit/", include("sims.audit.urls")),              # Audit
    path("api/bulk/", include("sims.bulk.urls")),                # Bulk ops
    path("api/notifications/", include("sims.notifications.urls")), # Notifications
    path("academics/", include("sims.academics.urls")),          # Academics
    
    # Legacy APIs (separate includes)
    # Via middleware/settings routing
]
```

---

## 📊 API Endpoint Statistics by App

| App | Active | Legacy | ViewSets | APIViews | @actions | Total |
|-----|--------|--------|----------|----------|----------|-------|
| users | ✓ | - | 8 | 2 | 2 | 25 |
| training | ✓ | - | 7 | 17 | 13 | 50+ |
| audit | ✓ | - | 2 | 0 | 2 | 3 |
| bulk | ✓ | - | 0 | 8 | 0 | 8 |
| notifications | ✓ | - | 0 | 4 | 0 | 4 |
| academics | ✓ | - | 3 | 0 | 0 | 3 |
| rotations | ✓ | - | 0 | 1 | 0 | 1 |
| **Subtotal Active** | - | - | **20** | **32** | **17** | **94** |
| cases | - | ✓ | 0 | 7 | 0 | 7 |
| logbook | - | ✓ | 0 | 5 | 0 | 5 |
| certificates | - | ✓ | 0 | 2 | 0 | 2 |
| analytics | - | ✓ | 0 | 8 | 0 | 8 |
| attendance | - | ✓ | 0 | 2 | 0 | 2 |
| reports | - | ✓ | 0 | 6 | 0 | 6 |
| results | - | ✓ | 2 | 0 | 0 | 2 |
| search | - | ✓ | 0 | 3 | 0 | 3 |
| **Subtotal Legacy** | - | - | **2** | **33** | **0** | **35** |
| **TOTAL** | - | - | **22** | **65** | **17** | **129** |

---

## 🔐 Custom Permission Classes

Location: Various app files (check imports)

```python
# Common permission checks
IsAuthenticated          # Built-in DRF
IsAdminUser            # Built-in DRF
AllowAny               # Built-in DRF

# Custom implementations (check files for import location)
IsSupervisor           # Supervisor/Faculty role
IsPGUser               # PG/Resident role
IsUTRMCAdmin           # UTRMC admin role
IsTechAdmin            # Tech admin role
ReadAnyWriteAdminOnly  # Read for all, write for admin
CanViewPendingLogbookQueue    # Custom logbook permission
CanVerifyLogbookEntry         # Custom logbook permission
AnalyticsAccessPermission      # Custom analytics permission
```

---

## 🏗️ ViewSet Details

### Standard CRUD Operations (per ViewSet)
- `GET /resource/` → `list()`
- `POST /resource/` → `create()`
- `GET /resource/{id}/` → `retrieve()`
- `PUT /resource/{id}/` → `update()`
- `PATCH /resource/{id}/` → `partial_update()`
- `DELETE /resource/{id}/` → `destroy()`

### ViewSets with Custom @action Endpoints

**RotationAssignmentViewSet** (7 actions):
```
submit          POST /api/rotations/{id}/submit/
hod-approve     POST /api/rotations/{id}/hod-approve/
utrmc-approve   POST /api/rotations/{id}/utrmc-approve/
activate        POST /api/rotations/{id}/activate/
complete        POST /api/rotations/{id}/complete/
returned        POST /api/rotations/{id}/returned/
reject          POST /api/rotations/{id}/reject/
```

**LeaveRequestViewSet** (3 actions):
```
submit    POST /api/leaves/{id}/submit/
approve   POST /api/leaves/{id}/approve/
reject    POST /api/leaves/{id}/reject/
```

**DeputationPostingViewSet** (3 actions):
```
approve   POST /api/postings/{id}/approve/
reject    POST /api/postings/{id}/reject/
complete  POST /api/postings/{id}/complete/
```

**HospitalViewSet** (1 action):
```
departments  GET /api/hospitals/{id}/departments/
```

**DepartmentViewSet** (1 action):
```
roster  GET /api/departments/{id}/roster/
```

**ActivityLogViewSet** (1 action):
```
export  GET /api/audit/activity/export/
```

**AuditReportViewSet** (1 action):
```
latest  GET /api/audit/reports/latest/
```

---

## 🔄 Request/Response Flow

```
HTTP Request
    ↓
Main Router (sims_project/urls.py)
    ↓
App-specific URLs (e.g., sims/training/urls.py)
    ↓
ViewSet or APIView
    ↓
Serializer (validation/transformation)
    ↓
Model
    ↓
Database
    ↓
Response (JSON)
```

---

## 🚀 How to Add a New Endpoint

1. **Create view** in `sims/<app>/views.py`:
```python
from rest_framework import viewsets
from rest_framework.decorators import action

class MyViewSet(viewsets.ModelViewSet):
    queryset = MyModel.objects.all()
    serializer_class = MySerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def my_action(self, request, pk=None):
        # Custom logic
        pass
```

2. **Register in router** (`sims/<app>/urls.py`):
```python
router = DefaultRouter()
router.register(r'myresource', MyViewSet, basename='myresource')

urlpatterns = [
    path('', include(router.urls)),
]
```

3. **Include in main router** (`sims_project/urls.py`):
```python
path('api/', include('sims.<app>.urls')),
```

4. **Create serializer** (`sims/<app>/serializers.py`):
```python
class MySerializer(serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = ['id', 'name', ...]
```

5. **Add model** (`sims/<app>/models.py`):
```python
class MyModel(models.Model):
    name = models.CharField(max_length=100)
    # fields...
```

---

## 📚 Key Files to Review

### Must-Read Files:
1. `/home/munaim/srv/apps/pgsims/backend/sims_project/urls.py` - Main router
2. `/home/munaim/srv/apps/pgsims/backend/sims/training/views.py` - Largest app with complex logic
3. `/home/munaim/srv/apps/pgsims/backend/sims/users/userbase_views.py` - Org graph ViewSets
4. `/home/munaim/srv/apps/pgsims/backend/sims/users/api_views.py` - Auth endpoints

### Configuration:
- `/home/munaim/srv/apps/pgsims/backend/sims_project/settings.py` - Django settings
- `/home/munaim/srv/apps/pgsims/backend/requirements.txt` - Dependencies

### Testing:
- `/home/munaim/srv/apps/pgsims/backend/conftest.py` - Pytest fixtures
- `/home/munaim/srv/apps/pgsims/backend/pytest.ini` - Pytest config

---

## 🔍 Finding Specific Endpoints

### By Feature:
- **Authentication**: `sims/users/api_urls.py`
- **Training Management**: `sims/training/urls.py`
- **Approvals**: `sims/training/views.py` (custom @actions)
- **Bulk Operations**: `sims/bulk/urls.py`
- **Analytics**: `sims/_legacy/analytics/urls.py`
- **User Management**: `sims/users/userbase_urls.py`

### By HTTP Method:
- **GET endpoints**: List/retrieve data
- **POST endpoints**: Create or action endpoints (custom logic)
- **PUT/PATCH**: Update data
- **DELETE**: Remove data

---

## 📞 API Documentation URLs

- **Auto-generated DRF Browsable API**: `http://localhost:8000/api/`
- **Admin Panel**: `http://localhost:8000/admin/`
- **Swagger/OpenAPI**: (if installed) Check settings.py for drf-spectacular

---

## 🎯 Key Patterns Used

1. **ViewSets + DefaultRouter** - Standard CRUD endpoints
2. **@action decorators** - Custom endpoints on ViewSets
3. **APIView** - Non-standard endpoints
4. **State Machine** - Rotation status workflow (DRAFT → SUBMITTED → ... → COMPLETED)
5. **Role-Based Access** - Permission classes for user roles
6. **Pagination** - ListCreateAPIView uses PageNumberPagination
7. **Filtering** - filterset_fields on ViewSets
8. **Serializers** - Data validation and transformation

