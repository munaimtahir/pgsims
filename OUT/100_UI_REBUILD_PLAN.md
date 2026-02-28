# OUT/100 — UI Rebuild Plan

## What Existed (Pre-Rebuild)
- **Layout**: `DashboardLayout.tsx` with a horizontal topbar containing ALL nav items inline (~200 LOC of role-conditional `<Link>` elements)
- **Duplication issues**: Admin role saw "Dashboard" + UTRMC items + Admin items = 15+ links in one topbar
- **Legacy Quick Actions**: Admin dashboard linked to `/dashboard/admin/bulk-import`, `/dashboard/admin/users` (not UTRMC console)

## What Was Replaced

| Component | Before | After |
|-----------|--------|-------|
| `DashboardLayout.tsx` | 228-line topbar nav | Sidebar shell via `<Sidebar>` component |
| `Sidebar.tsx` | Did not exist | New collapsible sidebar |
| `lib/navRegistry.ts` | Did not exist | Canonical nav config |
| Admin Quick Actions | Pointed to old admin/* | Points to utrmc/* and data-admin/* |

## New Sidebar Shell
- `frontend/components/layout/Sidebar.tsx` — collapsible, role-based, active-link highlight
- `frontend/lib/navRegistry.ts` — single source of truth for nav sections
- `frontend/components/layout/DashboardLayout.tsx` — wrapper using Sidebar

## Deletion Plan
- Old topbar nav code: **DELETED** in place (replaced entirely in `DashboardLayout.tsx`)
- No temporary `/legacy` routes needed — all pages retained; only navigation replaced

## Acceptance Gates
- ✅ Build passes (`npm run build`)
- ✅ No duplicate nav items
- ✅ Role-based rendering (admin sees Admin+UTRMC+DataAdmin; pg sees My Training; supervisor sees Supervisor)
- ✅ All existing routes still accessible
