# Frontend Integration Rules

## Architecture

The frontend follows a strict layered architecture:

```
UI Components (app/**/*.tsx)
        ↓
Feature/API Functions (lib/api/*.ts)
        ↓
apiClient (lib/api/client.ts)
        ↓
Backend REST API
```

**No layer may be skipped.** UI components must never call `fetch()` or `axios` directly.

---

## API Client Layer (`lib/api/client.ts`)

The base Axios client handles:
- Base URL resolution (browser vs server-side rendering)
- Authorization header injection from stored JWT token
- Token refresh on 401 responses via interceptor
- Cookie clearing on authentication failure

**Rules:**
- Do not modify `client.ts` without updating `API_SOURCE_OF_TRUTH.md`
- The base URL is determined by `NEXT_PUBLIC_API_URL` (browser) or `SERVER_API_URL` (SSR)
- All requests automatically include the `Authorization: Bearer <token>` header

---

## Feature API Modules (`lib/api/*.ts`)

Each module handles one feature domain:

| Module | Domain | Backend Prefix |
|--------|--------|---------------|
| `auth.ts` | Authentication, profile | `/api/auth/` |
| `userbase.ts` | Org graph (hospitals, departments, users, links) | `/api/` |
| `hospitals.ts` | Simple hospital CRUD | `/api/hospitals/` |
| `departments.ts` | Simple dept CRUD + hospital-departments, supervision links | `/api/` |
| `users.ts` | User management | `/api/users/` |
| `training.ts` | Programs, rotations, leaves, research, thesis, workshops, eligibility, summaries | `/api/` |
| `notifications.ts` | Notifications | `/api/notifications/` |
| `audit.ts` | Audit logs and reports | `/api/audit/` |
| `bulk.ts` | Bulk import/export | `/api/bulk/` |

**Rules for each module:**
1. Export named functions or an object with named methods (e.g., `trainingApi`, `userbaseApi`)
2. All functions must be async and return typed promises
3. TypeScript interfaces must be defined at the top of each file
4. Use `toArray<T>(data)` helper for responses that may be paginated or direct arrays
5. Never expose `apiClient` directly from a module — wrap all calls in named functions

---

## TypeScript Typing Rules

- Every API request payload must have a TypeScript interface: `interface CreateXPayload { ... }`
- Every API response must have a TypeScript interface: `interface XResponse { ... }` or `interface X { ... }`
- Optional fields must use `field?: type` syntax
- Nullable fields must use `field: type | null` syntax
- Paginated responses must use `{ count: number; results: T[] }`
- Never use `any` in API function signatures

---

## Frontend Data Flow Examples

### Resident viewing their rotations
```typescript
// Page: app/dashboard/pg/page.tsx
import { trainingApi } from '@/lib/api';

const rotations = await trainingApi.getMyRotations();
```

### Admin creating a hospital
```typescript
// Page: app/dashboard/utrmc/hospitals/page.tsx
import { userbaseApi } from '@/lib/api';

await userbaseApi.createHospital({ name: '...', code: '...' });
```

### Supervisor approving research
```typescript
import { trainingApi } from '@/lib/api';

await trainingApi.approveResearch({ residentId, feedback });
```

---

## Pages and Their API Dependencies

Each page must declare its API dependencies at the top level comment block:
```typescript
/**
 * Page: /dashboard/pg
 * API Dependencies:
 *   - trainingApi.getResidentSummary() → GET /api/residents/me/summary/
 *   - trainingApi.getMyRotations() → GET /api/my/rotations/
 */
```

---

## Error Handling in Pages

All API calls in pages must handle errors. Minimum required:
```typescript
const [error, setError] = useState<string | null>(null);
const [loading, setLoading] = useState(false);

try {
  setLoading(true);
  const data = await trainingApi.getMyRotations();
  setData(data);
} catch (e) {
  setError('Failed to load rotations. Please try again.');
} finally {
  setLoading(false);
}
```

---

## Pagination

When consuming paginated endpoints, use the `count` + `results` pattern:
```typescript
const response = await apiClient.get<{ count: number; results: Item[] }>('/api/items/');
const items = response.data.results;
const total = response.data.count;
```

---

## File Upload

For multipart file uploads:
```typescript
const fd = new FormData();
fd.append('synopsis_file', file);
await apiClient.patch('/api/my/research/', fd, {
  headers: { 'Content-Type': 'multipart/form-data' }
});
```

Never use `JSON.stringify()` for FormData payloads.

---

## Known Exceptions

| Location | Pattern | Reason |
|----------|---------|--------|
| `app/dashboard/resident/research/page.tsx:54` | `apiClient.get('/api/users/?role=supervisor')` | Supervisor dropdown — no dedicated endpoint exists; acceptable until userbase API adds filtered query |
| `app/dashboard/resident/research/page.tsx:83` | `apiClient.patch('/api/my/research/', fd, ...)` | Multipart file upload — cannot go through trainingApi wrapper without FormData support |

Both exceptions are tracked in `docs/integration/MISMATCH_REPORT.md`.
