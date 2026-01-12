# Seed Demo Data Guide

This guide explains how to load comprehensive demo data into the SIMS application for testing various functions.

## Quick Start

### Option 1: Using the Shell Script (Recommended)

```bash
cd /home/munaim/srv/apps/pgsims
./scripts/seed_demo_data.sh
```

### Option 2: Using Python Directly

```bash
cd /home/munaim/srv/apps/pgsims
python3 scripts/preload_demo_data.py
```

### Option 3: Using Django Management Command (if available)

```bash
python3 manage.py shell < scripts/preload_demo_data.py
```

## What Gets Created

The seed script creates comprehensive test data including:

### Users
- **1 Admin user**
- **4 Supervisor users** (different specialties)
- **5 PG Student users** (different years and specialties)

### Organizational Structure
- **2 Hospitals** (FMU Teaching Hospital, Allied Hospital)
- **8 Rotation Departments** (across both hospitals)
- **4 Academic Departments**
- **4 Batches** (student cohorts)

### Training Records
- **10 Rotations** (2 per student: 1 completed, 1 ongoing)
- **Rotation Evaluations** (supervisor evaluations for completed rotations)
- **10 Certificates** (2 per student: BLS, ACLS, etc.)
- **9+ Logbook Entries** (4-5 per student with diagnoses and procedures)
- **5 Clinical Cases** (2-3 per student with detailed case information)

### Academic Data
- **Student Profiles** (linked to users with academic information)
- **Exams** (midterm, final, theory, practical)
- **Scores** (exam results for all students)

### Attendance Data
- **20+ Attendance Sessions** (lectures, clinical rotations, tutorials, seminars)
- **100+ Attendance Records** (tracking student attendance)
- **Eligibility Summaries** (monthly summaries with 80-95% attendance)

## Demo Credentials

After running the seed script, you can login with these credentials:

### Admin
- **Username:** `admin`
- **Password:** `admin123`

### Supervisors
- **Username:** `dr_smith` | **Password:** `supervisor123` (Surgery)
- **Username:** `dr_jones` | **Password:** `supervisor123` (Medicine)
- **Username:** `dr_ahmed` | **Password:** `supervisor123` (Cardiology)
- **Username:** `dr_ali` | **Password:** `supervisor123` (Orthopedics)

### PG Students
- **Username:** `pg_ahmed` | **Password:** `student123` (Surgery, Year 1)
- **Username:** `pg_fatima` | **Password:** `student123` (Medicine, Year 2)
- **Username:** `pg_ali` | **Password:** `student123` (Surgery, Year 2)
- **Username:** `pg_sara` | **Password:** `student123` (Medicine, Year 1)
- **Username:** `pg_omar` | **Password:** `student123` (Cardiology, Year 3)

## Testing Different Functions

With this seed data, you can test:

1. **User Management**
   - Login as different user roles
   - View user profiles and assignments
   - Test role-based permissions

2. **Rotation Management**
   - View ongoing and completed rotations
   - Create new rotations
   - View rotation evaluations
   - Test rotation status workflows

3. **Academic Management**
   - View student profiles and batches
   - Check academic performance (CGPA)
   - View exam results and scores

4. **Logbook Functions**
   - View logbook entries with diagnoses and procedures
   - Submit new logbook entries
   - Review and approve entries (as supervisor)

5. **Clinical Cases**
   - View detailed clinical cases
   - Submit new cases
   - Review and approve cases

6. **Certificates**
   - View certificate types and student certificates
   - Track certificate validity
   - Verify certificates

7. **Attendance Tracking**
   - View attendance sessions
   - Check attendance records
   - Review eligibility summaries
   - Test exam eligibility based on attendance

8. **Reports and Analytics**
   - Generate various reports
   - View statistics and dashboards
   - Test data export functions

## Notes

- The script uses `get_or_create()` to avoid duplicates, so it's safe to run multiple times
- All dates are set relative to today (past dates for historical data, future dates for upcoming events)
- Attendance percentages are set to 80-95% to ensure students are eligible for exams
- The script runs in a database transaction, so if it fails, no data is saved

## Troubleshooting

If you encounter errors:

1. **Make sure migrations are up to date:**
   ```bash
   python3 manage.py migrate
   ```

2. **Check database connection:**
   - For SQLite: Ensure `db.sqlite3` is writable
   - For PostgreSQL: Check `.env` file and database credentials

3. **Check Python environment:**
   ```bash
   source venv/bin/activate  # if using virtual environment
   ```

4. **View detailed error messages:**
   The script will print detailed error messages if something fails.

## Customization

You can modify `scripts/preload_demo_data.py` to:
- Add more users
- Change specialties and years
- Adjust dates and quantities
- Add more test scenarios
