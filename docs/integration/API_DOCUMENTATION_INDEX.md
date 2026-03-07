# PGSIMS Backend API Documentation Index

This index helps you navigate all backend API documentation files created for the PGSIMS project.

---

## 📚 Documentation Files

### 1. **API_CATALOG.md** (35KB, 693 lines)
**Comprehensive Complete Reference**

The most detailed documentation of ALL backend endpoints organized by:
- URL prefix and file location
- HTTP methods for each endpoint
- View class/function names
- Permission classes
- Brief descriptions

**Contains:**
- 19 sections covering all API areas
- 120+ individual endpoints cataloged
- Custom @action decorators with parameters
- ViewSet CRUD operation mappings
- Permission patterns and role-based access
- Statistics by app

**When to use:** Full endpoint reference, understanding permissions, finding specific endpoints by functionality

**Location:** `/home/munaim/srv/apps/pgsims/API_CATALOG.md`

---

### 2. **API_QUICK_REFERENCE.md** (9.7KB, 299 lines)
**Developer Quick Start Guide**

Fast lookup guide organized by API groups with:
- Code examples (curl/JSON)
- State machine diagrams
- Common workflows
- Query parameters

**Contains:**
- Authentication examples
- Grouped endpoints by functionality
- Common patterns and workflows
- Response format examples
- Permission levels quick matrix
- Practical usage examples

**When to use:** Quick lookups during development, understanding workflows, finding endpoint examples

**Location:** `/home/munaim/srv/apps/pgsims/API_QUICK_REFERENCE.md`

---

### 3. **BACKEND_STRUCTURE.md** (13KB, 390 lines)
**Architecture & Project Organization**

Deep dive into project structure with:
- Complete directory tree
- File organization by app
- ViewSet details and custom actions
- How to add new endpoints
- Key files to review

**Contains:**
- Full directory structure
- URL routing flow diagram
- Statistics table by app
- Custom permission classes
- ViewSet conventions
- How-to add new endpoint guide
- Finding endpoints by feature or method

**When to use:** Understanding project structure, adding new features, understanding routing, setting up development

**Location:** `/home/munaim/srv/apps/pgsims/BACKEND_STRUCTURE.md`

---

## 🎯 Quick Navigation by Use Case

### "I need to find a specific endpoint"
→ Start with **API_QUICK_REFERENCE.md** for quick lookup, then check **API_CATALOG.md** for full details

### "I need to understand rotation workflow"
→ **API_QUICK_REFERENCE.md** - State Machine section + Common Workflows section

### "I need to implement a new feature"
→ **BACKEND_STRUCTURE.md** - How to Add New Endpoint section + understand existing patterns

### "I need to understand permissions"
→ **API_CATALOG.md** - KEY PERMISSION PATTERNS section

### "I need to understand project structure"
→ **BACKEND_STRUCTURE.md** - Full documentation with directory tree

### "I need all training endpoints"
→ **API_CATALOG.md** - Section 4: TRAINING & ROTATIONS API

### "I need bulk import details"
→ **API_CATALOG.md** - Section 6: BULK OPERATIONS API

### "I need legacy API details"
→ **API_CATALOG.md** - Sections 9-16: LEGACY APIs

---

## 📊 API Statistics Summary

| Metric | Count |
|--------|-------|
| **Total Active Endpoints** | 94 |
| **Total Legacy Endpoints** | 35 |
| **Total Endpoints** | 129+ |
| **ViewSets** | 22 |
| **APIView Classes** | 65 |
| **@action Decorators** | 17+ |
| **HTML Template Views** | 30+ |
| **Utility/Health Endpoints** | 7 |

---

## 🔑 Key API Areas

### Core APIs (Active)
1. **Authentication** - JWT token management
2. **Organizational Graph** - Hospitals, departments, users
3. **Training & Rotations** - Main business logic (50+ endpoints)
4. **Audit & Logging** - Activity tracking
5. **Bulk Operations** - Batch import/export
6. **Notifications** - User notifications

### Supporting APIs (Active)
7. **Academics** - Departments, batches, students
8. **System** - Health checks, settings

### Legacy APIs (Deprecated but Active)
9. **Cases** - Case management
10. **Logbook** - Logbook entries
11. **Certificates** - Training certificates
12. **Analytics** - Dashboard analytics
13. **Reports** - Report generation
14. **Search** - Global search
15. **Attendance** - Attendance tracking
16. **Results** - Exam results

---

## 🔐 Authentication

All endpoints (except login/register) require:
- **JWT Token** via `Authorization: Bearer <token>`
- Obtained from `POST /api/auth/login/`
- Refreshable via `POST /api/auth/refresh/`

---

## 🗂️ File Organization

```
Backend:
├── sims_project/
│   └── urls.py              # Main router
├── sims/
│   ├── users/               # Auth + org graph
│   ├── training/            # Main business logic
│   ├── audit/               # Activity tracking
│   ├── bulk/                # Batch operations
│   ├── notifications/       # Notifications
│   ├── academics/           # Academic data
│   ├── rotations/           # Hospital rotation utils
│   └── _legacy/             # Deprecated apps
└── Documentation (Created):
    ├── API_CATALOG.md                  # Complete reference
    ├── API_QUICK_REFERENCE.md          # Quick guide
    ├── BACKEND_STRUCTURE.md            # Architecture
    └── API_DOCUMENTATION_INDEX.md      # This file
```

---

## 📝 Content Organization in API_CATALOG.md

The complete catalog is organized in 19 sections:

1. **Authentication API** - Login, profile, password reset
2. **User Management API** - Org graph (hospitals, depts, users)
3. **Users Extended API** - User CRUD, supervisor endpoints
4. **Training & Rotations API** - Main app (programs, rotations, leaves, research)
5. **Audit API** - Activity logs, audit reports
6. **Bulk Operations API** - Import/export
7. **Notifications API** - User notifications
8. **Academics API** - Departments, batches, students
9. **Legacy - Analytics API** - Dashboard analytics
10. **Legacy - Cases API** - Case management
11. **Legacy - Logbook API** - Logbook entries
12. **Legacy - Certificates API** - Training certificates
13. **Legacy - Reports API** - Report generation
14. **Legacy - Results API** - Exam results
15. **Legacy - Search API** - Global search
16. **Legacy - Attendance API** - Attendance management
17. **Utility Endpoints** - Health checks, home page
18. **HTML/Template Endpoints** - Non-REST views
19. **Rotations Utility** - Department lookup

---

## 🚀 Getting Started

### Step 1: Understand Authentication
- Read: **API_QUICK_REFERENCE.md** - Authentication section
- Endpoint: `POST /api/auth/login/`

### Step 2: Explore Main Features
- **Training/Rotations**: API_QUICK_REFERENCE.md - Section 4
- **Users**: API_CATALOG.md - Sections 2-3
- **Bulk Ops**: API_QUICK_REFERENCE.md - Section 6

### Step 3: Understand Project Structure
- Read: **BACKEND_STRUCTURE.md** - Full documentation

### Step 4: Reference as Needed
- API_CATALOG.md for comprehensive details
- API_QUICK_REFERENCE.md for examples and workflows

---

## 💡 Key Concepts

### State Machine (Rotations)
Rotations follow this workflow:
```
DRAFT → SUBMITTED → APPROVED → ACTIVE → COMPLETED
                ↓                  ↓
              RETURNED           REJECTED
```
See: API_QUICK_REFERENCE.md - Rotation Approval Flow section

### Role-Based Access
- **Admin/UTRMC Admin**: Full access
- **Supervisor/Faculty**: Approve workflows, view supervisees
- **Resident/PG**: Submit, view own records
- **Authenticated User**: Read org data

See: API_CATALOG.md - KEY PERMISSION PATTERNS section

### ViewSet Pattern
Standard endpoints generated from ViewSets:
- `GET /resource/` - List
- `POST /resource/` - Create
- `GET /resource/{id}/` - Retrieve
- `PUT /resource/{id}/` - Update
- `PATCH /resource/{id}/` - Partial update
- `DELETE /resource/{id}/` - Delete
- `POST /resource/{id}/{action}/` - Custom action

See: BACKEND_STRUCTURE.md - ViewSet Details section

---

## 🔍 Finding Information

### By Endpoint Type
- **CRUD Operations**: BACKEND_STRUCTURE.md - Standard CRUD section
- **State Machines**: API_QUICK_REFERENCE.md - Common Workflows
- **Custom Actions**: API_CATALOG.md - Search "@action"
- **Permissions**: API_CATALOG.md - KEY PERMISSION PATTERNS

### By Feature
- **Authentication**: API_CATALOG.md - Section 1
- **User Management**: API_CATALOG.md - Sections 2-3
- **Rotations**: API_CATALOG.md - Section 4 (main)
- **Approvals**: API_QUICK_REFERENCE.md - Rotation Approval Flow
- **Bulk Import**: API_CATALOG.md - Section 6
- **Analytics**: API_CATALOG.md - Section 9

### By App
- **sims.users**: API_CATALOG.md - Sections 1-3
- **sims.training**: API_CATALOG.md - Section 4
- **sims.audit**: API_CATALOG.md - Section 5
- **sims.bulk**: API_CATALOG.md - Section 6
- **sims.notifications**: API_CATALOG.md - Section 7
- **sims.academics**: API_CATALOG.md - Section 8
- **Legacy**: API_CATALOG.md - Sections 9-16

---

## 📞 Support & References

### Documentation Files
- **API_CATALOG.md** - `/home/munaim/srv/apps/pgsims/API_CATALOG.md`
- **API_QUICK_REFERENCE.md** - `/home/munaim/srv/apps/pgsims/API_QUICK_REFERENCE.md`
- **BACKEND_STRUCTURE.md** - `/home/munaim/srv/apps/pgsims/BACKEND_STRUCTURE.md`
- **This Index** - `/home/munaim/srv/apps/pgsims/API_DOCUMENTATION_INDEX.md`

### Source Code
- **Main Router** - `/home/munaim/srv/apps/pgsims/backend/sims_project/urls.py`
- **Training Views** - `/home/munaim/srv/apps/pgsims/backend/sims/training/views.py`
- **User Views** - `/home/munaim/srv/apps/pgsims/backend/sims/users/userbase_views.py`
- **Settings** - `/home/munaim/srv/apps/pgsims/backend/sims_project/settings.py`

---

## ✅ Documentation Completeness

- ✅ All 129+ endpoints documented
- ✅ All ViewSets with custom actions listed
- ✅ All permission classes documented
- ✅ All URL patterns mapped
- ✅ File paths for every endpoint
- ✅ HTTP methods for every endpoint
- ✅ Brief descriptions for every endpoint
- ✅ Example workflows provided
- ✅ Quick reference guide created
- ✅ Architecture documentation provided

---

## 📄 Last Updated

**Generated:** March 7, 2025
**Coverage:** All files in `/home/munaim/srv/apps/pgsims/backend/`
**Total Endpoints Cataloged:** 129+
**Sections:** 19 major sections + utilities

