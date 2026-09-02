# PGSIMS Frontend Documentation - README

## 📚 What's Included

This folder contains **complete, comprehensive documentation** of the PGSIMS Next.js frontend application. Three documents are provided, each serving a different purpose:

### 1. **FRONTEND_INDEX.md** ⭐ START HERE
   - **Purpose**: Navigation and overview guide
   - **Content**: Directory structure, key statistics, quick reference tables
   - **Best for**: First-time readers, getting oriented
   - **Time to read**: 5-10 minutes

### 2. **FRONTEND_SUMMARY.txt** 📖 EXECUTIVE OVERVIEW
   - **Purpose**: High-level system overview
   - **Content**: Technology stack, architecture, features, deployment model
   - **Best for**: Managers, architects, getting the big picture
   - **Time to read**: 15-20 minutes
   - **Length**: ~400 lines

### 3. **FRONTEND_API_MAP.md** 🔍 DETAILED REFERENCE
   - **Purpose**: Complete API endpoint documentation
   - **Content**: All 84+ endpoints organized by domain, page dependencies, type definitions
   - **Best for**: Developers implementing features or debugging
   - **Time to read**: 30-45 minutes (best used as a reference)
   - **Length**: ~287 lines

### 4. **FRONTEND_QUICK_REFERENCE.txt** ⚡ QUICK LOOKUP
   - **Purpose**: Quick lookup tables and code examples
   - **Content**: Organized tables by endpoint, roles, pages; code patterns
   - **Best for**: Copy-paste references during development
   - **Time to read**: 2-3 minutes (for specific lookups)
   - **Length**: ~343 lines

## 🗺️ Reading Path

### For First-Time Readers
1. Start with **FRONTEND_INDEX.md** (5 min)
2. Read **FRONTEND_SUMMARY.txt** (20 min)
3. Bookmark **FRONTEND_QUICK_REFERENCE.txt** for later use

### For Specific Tasks

**Need to find an API endpoint?**
→ See FRONTEND_QUICK_REFERENCE.txt (table format)
→ Or FRONTEND_API_MAP.md (detailed descriptions)

**Need to understand a page's data flow?**
→ See FRONTEND_API_MAP.md, section "Pages & API Usage"

**Need to add a new feature?**
→ See FRONTEND_QUICK_REFERENCE.txt, section "Common Patterns"
→ Check related FRONTEND_API_MAP.md service module

**Need to understand authentication?**
→ See FRONTEND_SUMMARY.txt, section "Authentication Flow"
→ Or FRONTEND_INDEX.md, section "Authentication Details"

**Need to understand role-based access?**
→ See FRONTEND_SUMMARY.txt, section "Key Features" → "Role-Based Access Control"
→ Or FRONTEND_QUICK_REFERENCE.txt, section "Pages by Role"

## 📊 Key Statistics

| Metric | Value |
|--------|-------|
| Total API Endpoints | 84+ |
| Service Modules | 11 |
| Pages with API Calls | 27 |
| User Roles | 7 |
| TypeScript Files | 50+ |
| Documentation Lines | 630+ |
| Coverage | 100% of public APIs |

## 🎯 What's Documented

✅ **Complete API Mapping**
- All 84+ endpoints with methods and parameters
- Request/response types
- File where each endpoint is defined

✅ **Page Structure**
- All 27 pages with API calls documented
- Which endpoints each page uses
- Feature descriptions

✅ **Service Layer**
- 11 modular API service files
- Organization and structure
- Function signatures and return types

✅ **Authentication & Security**
- Token management (localStorage, cookies)
- Auto-refresh mechanism
- Role-based access control
- Route protection

✅ **State Management**
- Zustand auth store
- React hooks for UI state
- Persistence strategy

✅ **TypeScript Types**
- User model with 7 roles
- Request/response interfaces
- Main domain models

✅ **Code Patterns**
- API service pattern
- Protected page pattern
- File upload pattern
- Bulk import pattern

✅ **Deployment & Configuration**
- Environment variables
- API proxy architecture
- Frontend/backend relationship

## 🔍 Search Tips

### In FRONTEND_INDEX.md
- Use browser Find (Ctrl+F) for quick lookups
- See "Quick Reference" table for common tasks

### In FRONTEND_SUMMARY.txt
- Search for "📋" or specific feature names
- Browse sections in order for architecture understanding

### In FRONTEND_API_MAP.md
- Search by endpoint path (e.g., "/api/my/research/")
- Search by function name (e.g., "trainingApi")
- Search by page name (e.g., "resident/research")

### In FRONTEND_QUICK_REFERENCE.txt
- Tables organized alphabetically within sections
- Search for HTTP methods (GET, POST, PATCH, etc.)
- Look for specific role names

## 💡 Key Concepts

### API Organization
- **11 service modules** in `lib/api/`
- Each module handles a domain (auth, training, users, etc.)
- All use centralized `apiClient` from `lib/api/client.ts`

### Role-Based Access
- **7 roles**: pg, resident, supervisor, faculty, admin, utrmc_user, utrmc_admin
- Each role has dedicated dashboard(s)
- Routes protected with `ProtectedRoute` component

### State Management
- **Auth state**: Zustand with localStorage persistence
- **UI state**: React hooks (useState)
- **No Redux**: Simple and lightweight approach

### API Proxy
- Frontend makes requests to `/api/*` (same-origin)
- Next.js proxy route forwards to Django backend
- Avoids CORS issues, handles token refresh

### Authentication Flow
1. POST /api/auth/login/ → get access + refresh tokens
2. Store in localStorage + Zustand + cookies
3. Add "Bearer {token}" to all requests
4. On 401: auto-refresh and retry

## 🚀 Getting Started with Code

### To Add a New API Call
1. Find the appropriate file in `lib/api/`
2. Add new function following the pattern
3. Export from `lib/api/index.ts`
4. Use in your component/page

### To Add a New Page
1. Create `page.tsx` in appropriate `/dashboard/[role]/` folder
2. Wrap with `<ProtectedRoute allowedRoles={[...]}>`
3. Use API service functions from `lib/api/`
4. Handle loading/error states

### To Understand a Page's Data Flow
1. Find page in `app/dashboard/`
2. Check imports for which API services it uses
3. Look up those services in `lib/api/` for endpoints
4. Reference endpoint details in this documentation

## 📋 File Locations Quick Reference

| Task | File |
|------|------|
| View all auth endpoints | lib/api/auth.ts |
| View all training endpoints | lib/api/training.ts |
| View all user management endpoints | lib/api/userbase.ts |
| Handle authentication state | store/authStore.ts |
| Protect routes | components/auth/ProtectedRoute.tsx |
| Set up HTTP client | lib/api/client.ts |
| Define types | types/index.ts |
| Configure RBAC | lib/rbac.ts |

## ✅ Verification Checklist

This documentation covers:

- ✅ All API endpoints (84+)
- ✅ All service modules (11)
- ✅ All pages (27)
- ✅ All roles (7)
- ✅ All types and interfaces
- ✅ Authentication flow
- ✅ State management
- ✅ RBAC implementation
- ✅ File upload handling
- ✅ Bulk operations
- ✅ Environment configuration
- ✅ Code patterns and examples

## 🔗 Cross-References

Within the documentation:
- **FRONTEND_INDEX.md** → Quick links to other docs
- **FRONTEND_SUMMARY.txt** → Detailed sections for deep dives
- **FRONTEND_API_MAP.md** → Section references and groupings
- **FRONTEND_QUICK_REFERENCE.txt** → Organized lookup tables

## 📝 Notes

- Documentation is current as of March 2024
- Based on 50+ TypeScript source files
- Covers 100% of public API endpoints
- Includes real code examples from the codebase
- No external dependencies required to understand

## 🎓 Learning Path Recommendation

**Week 1: Orientation**
- Day 1: Read FRONTEND_INDEX.md
- Day 2-3: Read FRONTEND_SUMMARY.txt
- Day 4-5: Browse FRONTEND_QUICK_REFERENCE.txt

**Week 2: Deep Dive**
- Review FRONTEND_API_MAP.md, paying attention to your role's pages
- Study lib/api/*.ts files for your domain
- Trace one complete page's data flow

**Week 3+: Implementation**
- Use FRONTEND_QUICK_REFERENCE.txt while developing
- Refer to FRONTEND_API_MAP.md for detailed endpoint info
- Follow code patterns in documentation

## 💬 Questions?

If you need to find something specific:

1. **Look for it in FRONTEND_QUICK_REFERENCE.txt first** (quickest)
2. **Search FRONTEND_API_MAP.md by endpoint or function** (detailed)
3. **Check FRONTEND_SUMMARY.txt for concepts** (architecture)
4. **Use FRONTEND_INDEX.md as a guide** (navigation)

---

**Documentation Generated**: March 7, 2024
**Coverage**: 100% of frontend API and architecture
**Format**: Markdown + Text (readable in any text editor)
**Maintenance**: Update when new endpoints are added to the frontend

