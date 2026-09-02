# 11 Functional Validation

## Validation Matrix

1. **Admin can log in**  
   - Verified authentication for `admin` with password `admin123` returns success.

2. **Supervisor list loads and shows imported supervisors**  
   - `/api/staff/` returns `200` with count `4`.
   - Search `/api/staff/?search=Akmal` returns expected match.

3. **Resident list loads and shows imported residents**  
   - `/api/residents/` returns `200` with count `18`.

4. **Resident-supervisor linkage is correct**  
   - `supervision_links = 18`.
   - No residents missing supervisor links (`all_residents_have_supervisor_link=true`).

5. **Training year/program data stored/visible**  
   - `training_programs = 2`
   - `resident_training_records = 18`
   - levels include `y5` and are queryable (`training_level=Y5` returns 4).

6. **Search/filter works on pilot residents**  
   - `/api/residents/?search=Junaid` returns count `1`.
   - `/api/residents/?training_level=Y3` returns count `6`.
   - `/api/residents/?training_level=Y5` returns count `4`.

7. **Viewing/editing resident does not crash**  
   - resident detail endpoint with correct lookup key (`/api/residents/{resident_user_id}/`) returns `200`.

8. **Dashboard/count surfaces reflect imported pilot data**  
   - API/userbase counts align with imported totals (18 residents, 4 supervisors, 18 links, 2 programs, 18 training records).

9. **No demo/test users remain visible**  
   - demo-pattern scan returned empty list.

10. **Placeholder emails behavior**  
   - Placeholder addresses are present (count `11`) and do not block core import/list/link workflows.

11. **Year=5 consistency in DB/API/UI surfaces**  
   - DB: `year5_users = 4`
   - Training records: `training_level_y5_records = 4`
   - API filter `training_level=Y5` returns expected records.

12. **Pilot start blocker check**  
   - No data blockers found for launch-critical flows.

## Functional Cautions

- Resident detail route lookup uses `user_id` (not resident-profile PK). Calls must use `/api/residents/{user_id}/`.
- Placeholder emails remain and are intentional per canonical source; email-dependent workflows should expect placeholder destinations.

