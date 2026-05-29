# Frontend Map (Truth Map)

## Router & Architecture
- **Router Type**: Next.js **App Router** (`app/` directory).
- **Language**: TypeScript (**TSX**).
- **State Management**: **Zustand** (specifically for Auth in `store/authStore.ts`).
- **Styling**: **Tailwind CSS** with **PostCSS**.
- **Icons**: (Likely Lucide/Radix based on standard shadcn setups, though not explicitly verified).

## Discovered Routes
| Route | Role Area | Protection |
|-------|-----------|------------|
| `/` | Public | None |
| `/login` | Public | Redirect if Auth |
| `/dashboard` | Shared | Auth (Zustand state check) |
| `/dashboard/pg/*` | Resident/PG | Role: `pg` |
| `/dashboard/supervisor/*` | Supervisor | Role: `supervisor` |
| `/dashboard/admin/*` | Admin | Role: `admin` |
| `/dashboard/search` | Shared | Auth |

## Auth Protection Mechanism
Protection is primarily handled via client-side state in the `useAuthStore` and layouts. No top-level `middleware.ts` was found, implying routing logic is embedded in `./app` layouts or individual pages.
- **Tokens**: JWT (stored in `localStorage`).
- **Interceptor**: Axios interceptor in `lib/api/client.ts` attaches `Authorization: Bearer <token>` and handles 401 refreshes.

## UI Tech Stack Evidence
- **File**: `frontend/package.json` (implied)
- **File**: `frontend/tailwind.config.ts` (Tailwind detected)
- **File**: `frontend/app/layout.tsx` (App Router structure)
- **File**: `frontend/lib/api/client.ts` (Axios for API calling)

## Discovered API Integration
Frontend uses a manual SDK-style layer in `frontend/lib/api/`:
- `auth.ts`: Authentication flows.
- `logbook.ts`: Logbook CRUD and verification.
- `rotations.ts`: Rotation management.
- `analytics.ts`: Dashboard metrics.

## Known Unknowns
- Exact implementation of role-based route guards (if not using `middleware.ts`).
- Presence of server-side data fetching vs 100% client-side `useEffect` fetching.

## Immediate Next Actions
1. Map each `page.tsx` to its corresponding API calls.
2. Verify if RBAC is enforced on the client-side beyond simple UI hiding.
