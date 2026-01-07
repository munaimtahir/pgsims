# Quick Import Instructions

## Step 1: Run Migration
```bash
cd /home/munaim/srv/apps/pgsims
python manage.py migrate users
```

## Step 2: Import Trainee Data

### Option A: Dry Run First (Recommended)
```bash
python manage.py import_trainees /home/munaim/Downloads/Trainee_Data_Department_of_Urology.xlsx --dry-run --allow-partial
```

### Option B: Direct Import
```bash
python manage.py import_trainees /home/munaim/Downloads/Trainee_Data_Department_of_Urology.xlsx --allow-partial
```

## Step 3: Verify Import
```bash
python manage.py shell
```

Then in the shell:
```python
from sims.users.models import User
trainees = User.objects.filter(role='pg', specialty='urology')
print(f"Total trainees imported: {trainees.count()}")
for t in trainees[:5]:
    print(f"{t.username} - {t.get_full_name()} - Year {t.year}")
```

Or use the verification script:
```bash
python verify_import.py
```

## What to Expect

- All trainees will have username format: `firstname.lastname`
- Email format: `username.pgr@pmc.edu.pk`
- Training year automatically calculated from joining date
- Supervisors created automatically if not found
- Default password: `changeme123` (should be changed)

## Troubleshooting

If you get "ModuleNotFoundError: No module named 'django'":
- Activate your virtual environment first
- Or install dependencies: `pip install -r requirements.txt`
