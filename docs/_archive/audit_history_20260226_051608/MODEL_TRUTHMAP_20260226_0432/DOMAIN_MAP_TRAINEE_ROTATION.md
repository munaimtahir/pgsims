# Domain Map: Trainee & Rotation

## Current Trainee Links (to Department/Hospital)
- A Postgraduate (Trainee) is defined as a `User` with `role="pg"` (`backend/sims/users/models.py`). 
- **Trainee to Supervisor**: `User` contains a direct self-referencing FK `supervisor`.
- **Trainee to Department**: Governed by `academics.StudentProfile` (line 116), referencing `Batch`, which references `academics.Department`. No explicit "Home Hospital" or "Home Department" fields exist on the User profile directly.

## Current Rotation Lifecycle (`backend/sims/rotations/models.py:157`)
- **Linkages**: Points to `pg` (User), `department` (rotations.Department), `hospital` (rotations.Hospital), and `supervisor` (User).
- **Temporal Details**: `start_date`, `end_date`, `status` (planned, ongoing, completed, cancelled, pending).
- **Approvals**: Contains `approved_by` (User) and `approved_at` timestamp. Auto-updates status based on dates during `save()`.

## Identified Missing Domain Elements
To map to real-world complexities (like multi-hospital residency configurations and off-site rotations), the following features are missing:
1. **Explicit Home Affiliation for Trainees**:
   - Needs: `trainee.home_department` (FK canonical Department)
   - Needs: `trainee.home_hospital` (FK canonical Hospital)
2. **From/To Distinct Rotations**:
   - The current `Rotation` record implicitly means "the PG is rotating *to* this hospital/department". It lacks fields capturing *from* (though 'from' could be derived from 'home affiliation', doing so natively provides snapshot isolation during transfers).
3. **Inter-Hospital Exception & Policy Logic**:
   - Real-world rotations that move a Trainee from their "Home Hospital" to a "Host Hospital" typically require explicit approvals.
   - Missing schemas: `is_external_rotation` flag, `override_reason` text field, or structured policy mechanisms for blocking/allowing inter-hospital routing without dean-level approval.
