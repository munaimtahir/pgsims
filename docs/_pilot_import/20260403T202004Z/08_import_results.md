# 08 Import Results

## Dry-Run (Canonical Direct) Key Outcomes

- training-programs: success
- faculty-supervisors: failed initially on blank password in one row (dry-run strict validation path)
- residents: failed (`training_start is required`)
- supervision-links: failed (`start_date is required`)
- resident-training-records: failed (`Missing resident_email, program_code, or start_date`)

## Apply (Transformed Compatibility Package) Results

Final apply results after deterministic transformations:

```json
{
  "training-programs": {
    "successes": 2,
    "failures": 0,
    "created": 0,
    "updated": 2,
    "skipped": 0
  },
  "faculty-supervisors": {
    "successes": 4,
    "failures": 0,
    "created": 0,
    "updated": 4,
    "skipped": 0
  },
  "residents": {
    "successes": 18,
    "failures": 0,
    "created": 18,
    "updated": 0,
    "skipped": 0
  },
  "supervision-links": {
    "successes": 18,
    "failures": 0,
    "created": 18,
    "updated": 0,
    "skipped": 0
  },
  "resident-training-records": {
    "successes": 18,
    "failures": 0,
    "created": 18,
    "updated": 0,
    "skipped": 0
  }
}
```

## Traceability Notes

- Placeholder emails from canonical source were preserved.
- Year=5 residents imported and linked successfully.
- No duplicate demo/test users were introduced by the import.

