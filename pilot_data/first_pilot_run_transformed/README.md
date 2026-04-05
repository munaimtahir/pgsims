# First Pilot Source Package - populated

This package is populated from the uploaded Urology trainee roster for the first pilot run.

Source basis:
- Department: Urology
- Total residents: 18
- Total supervisors: 4

Key mapping decisions used in this package:
- hospital_code = UTRMC
- department_code = SURG
- specialty = urology
- program_code values:
  - MS-UROLOGY
  - FCPS-UROLOGY
- Missing resident emails were filled with placeholder addresses in the format:
  - uro###@placeholder.example.com
- Supervisor emails were not present in the source roster, so placeholder supervisor emails were created from supervisor names using:
  - <sanitized-name>@placeholder.example.com

Important notes before import:
- Resident years are preserved exactly from source data, including 5th year records.
- If the application currently validates resident year as 1-4 only, the importer/runtime must handle this explicitly.
- training_start, training_end, start_date, and expected_end_date were left blank because they were not present in the source roster.
- A supplemental file `pilot_source_status_reference.csv` is included to preserve synopsis/thesis status and IMM status from the original roster, even though these fields are not part of the canonical import CSV headers.
