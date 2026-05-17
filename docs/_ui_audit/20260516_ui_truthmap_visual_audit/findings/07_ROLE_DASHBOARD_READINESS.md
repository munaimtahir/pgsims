# Role Dashboard Readiness

| Role | Dashboard exists? | Loads? | Useful data shown? | Main missing UI | Readiness |
| --- | ---: | ---: | ---: | --- | --- |
| UTRMC/Admin | Yes | Yes | Partial | Clear operational “today” summary; import tools should be secondary. | Partial |
| Supervisor | Yes | Yes | Partial | Stronger prioritization of pending work and resident review actions. | Partial |
| Resident | Yes | Broken | Partial | Safe fallback for missing training record and resident data. | Broken |
| HOD | No frontend shell | Unknown | Unknown | No frontend dashboard page exists. | Missing |

## Notes

- The supervisor page is visually cleaner than the UTRMC overview, but it is empty in the current baseline because there are no active residents
- The resident progress page is the best resident-facing screen, but it is not enough to make the resident role ready by itself
- There is a backend HOD dashboard API, but no dedicated frontend route in the current app shell

