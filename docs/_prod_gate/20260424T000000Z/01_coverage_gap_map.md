# Coverage Gap Map - 2026-04-24

## Backend Coverage Gaps
| File | Current % | Target % | Missing Test Type | Priority |
|---|---:|---:|---|---|
| `sims/bulk/services.py` | 11.23 | 95.00 | Unit tests for bulk import/export logic | High |
| `sims/users/views.py` | 21.51 | 95.00 | Viewset action and negative path tests | High |
| `sims/bulk/userbase_engine.py` | 56.11 | 95.00 | Complex transformation logic tests | Medium |
| `sims/training/views.py` | 61.20 | 95.00 | State machine and dashboard API tests | High |
| `sims/training/eligibility.py` | 62.50 | 95.00 | Edge case eligibility computation tests | Medium |
| `sims/common_permissions.py` | 66.21 | 95.00 | Missing permission class branches | Medium |
| `sims/users/models.py` | 70.74 | 95.00 | Model property and method tests | Medium |

## Frontend Coverage Gaps
| File | Current % | Target % | Missing Test Type | Priority |
|---|---:|---:|---|---|
| `app/dashboard/utrmc/page.tsx` | 0.00 | 90.00 | UTRMC Dashboard page logic | High |
| `app/dashboard/supervisor/page.tsx` | 0.00 | 90.00 | Supervisor Dashboard page logic | High |
| `app/dashboard/resident/progress/page.tsx` | 0.00 | 90.00 | Resident Logbook/Progress logic | High |
| `components/layout/Sidebar.tsx` | 0.00 | 90.00 | Nav visibility and role-based items | High |
| `components/ui/ImportExportPanel.tsx` | 0.00 | 90.00 | Bulk operation handlers | Medium |
| `lib/api/*.ts` | ~2.50 | 90.00 | API client method tests (mocked) | High |
| `store/authStore.ts` | 0.00 | 90.00 | Zustand state transition tests | Medium |

## Priority Strategy
1. **Backend**: Focus on `sims/users/views.py` and `sims/training/views.py` as they contain the most critical logic for active scope.
2. **Frontend**: Focus on `app/` dashboard pages and `lib/api` methods.
3. **Shared**: Ensure `authStore.ts` and `Sidebar.tsx` are covered as they control the entry points for all roles.
