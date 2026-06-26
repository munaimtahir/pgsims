# Frontend / Backend Truth Map

Classification legend:

- `GREEN` = visible frontend action has a working backend endpoint and the payload/response contract matches.
- `BACKEND_ONLY` = backend endpoint exists but is intentionally paused or not surfaced in the active UI.
- `FRONTEND_ONLY` = frontend surface exists without a backend path.
- `PAYLOAD_MISMATCH` = visible UI sends shape that backend does not accept.
- `RESPONSE_MISMATCH` = backend returns shape that UI does not handle.
- `RBAC_MISMATCH` = route exists but the role gate is inconsistent.
- `HIDDEN_PAGE` = route exists but is hidden from current navigation.
- `DUPLICATE_PATHWAY` = legacy duplicate surface still exists but is not active.
- `UX_OVERLOAD` = page mixes monitoring and operations in a way that overwhelms the workflow.

| Feature | Classification | Evidence / status |
| --- | --- | --- |
| Users page filters and row actions | `GREEN` | Filters for role, department, active, supervisor, programme are wired to `/api/users/`; row actions bind to reset/deactivate/delete endpoints. |
| Supervision Links save flow | `GREEN` | Form posts `supervisor_user_id`, `resident_user_id`, `department_id`, `start_date`, `active`; table renders supervisor/resident names with fallbacks. |
| HOD Assignments save flow | `GREEN` | Candidate list excludes admin and uses actual faculty/supervisor candidates; save payload matches serializer shape. |
| Resident Programme Assignment | `GREEN` | Dedicated page `/dashboard/utrmc/resident-training` binds to resident training record CRUD endpoints. |
| Dashboard operational clutter | `GREEN` after cleanup | Dashboard now shows summary KPIs and links instead of the bulk setup form. |
| Resident onboarding wizard | `GREEN` | Active onboarding links are only the simplified path in the sidebar; legacy duplicates are not in nav. |
| Login sheet / imported batches / incomplete profiles | `GREEN` | Sidebar exposes all three pages and the onboarding API surfaces are reachable from the UI. |
| AdminOps bridge callback | `BACKEND_ONLY` | Endpoint exists but is intentionally paused for the pilot workflow. |
| Backup Google Drive connector | `BACKEND_ONLY` | Backend connector endpoints exist; they are not part of the active onboarding workflow. |
| Legacy `rotations/` path shell | `HIDDEN_PAGE` | Route exists as a redirect shell, not a current workflow entrypoint. |
| Legacy duplicate onboarding/supervisor pages | `DUPLICATE_PATHWAY` | Present on disk, hidden from the current sidebar and not part of the active pilot flow. |
| Users / supervision / HOD save failures from live UI | `GREEN` after fixes | Generic save failures now surface backend validation details. |
| Blank supervisor/resident columns on supervision links | `GREEN` after fixes | Table now falls back to nested user fields and raw IDs when needed. |
| HOD candidate list showing admin users | `GREEN` after fixes | Candidate pool is restricted to supervisor/faculty roles. |
| Oversized dashboard with operational forms | `UX_OVERLOAD` before fix, now cleared | The page has been reduced to monitoring cards and route links. |

## Summary

The active pilot workflow is now consistent end-to-end:

`Resident Excel Import -> Column Mapping -> Preview -> Import Residents -> Generate Login IDs -> Export Login Sheet -> First Login -> Complete Profile -> Resident Dashboard`

The remaining backend surfaces are either intentionally paused or hidden legacy paths, not active workflow gaps.
