# Baseline Initialization

## Command

```bash
docker exec pgsims_backend python manage.py initialize_pgsims_baseline
```

## Result

The baseline initialization command completed successfully and is idempotent.

## Created or Ensured

### Groups

- `admin`
- `utrmc_admin`
- `supervisor`
- `resident`
- `pg`
- `hod`

### Canonical Hospitals

- `AH` - Allied Hospital
- `DHQ` - DHQ Hospital
- `GGH` - Govt General Hospital Ghulam Muhammadabad
- `UTRMC` - UTRMC Teaching Hospital

### Canonical Departments

- `ANAES` - Anaesthesia
- `CARD` - Cardiology
- `DERM` - Dermatology
- `ENT` - Ear, Nose & Throat
- `EMERG` - Emergency Medicine
- `GASTRO` - Gastroenterology
- `OBG` - Gynecology & Obstetrics
- `ICU` - Intensive Care Unit
- `MED` - Medicine
- `NEPH` - Nephrology
- `NEURO` - Neurology
- `ONCO` - Oncology
- `OPTH` - Ophthalmology
- `ORTH` - Orthopedics
- `PATH` - Pathology
- `PED` - Pediatrics
- `PSY` - Psychiatry
- `PULM` - Pulmonology
- `RADIO` - Radiology
- `SURG` - Surgery

### Admin Access

- Username: `admin`
- Email: `admin@pgsims.local`
- Password in live container: `admin123`
- Role: `admin`
- Flags: `is_staff=True`, `is_superuser=True`

## Intentional Non-Creation

- No fake residents were created.
- No fake supervisors were created.
- No fake HODs were assigned.
- No fake hospital-department matrix rows were generated.

