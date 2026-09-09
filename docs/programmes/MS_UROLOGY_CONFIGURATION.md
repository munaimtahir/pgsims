# MS Urology programme configuration

## Source and scope

The approved source workbook is `urology_pgsims_institutional_demo_ready.xlsx`. The requested
FMU curriculum PDF/title was not present in this checkout on 2026-09-10, so the configuration
records the curriculum decisions supplied in the implementation brief and preserves the source
limitations. FCPS Urology is only a minimal association programme; no MS rules are applied to it.

## Canonical mapping

| Capability | Existing PGSIMS model | Configuration |
|---|---|---|
| Institution | `academics.Institution` | FMU / `FMU` |
| Hospital | `rotations.Hospital` | Allied Hospital-I Faisalabad / `AHF-I` |
| Department | `academics.Department` + `rotations.HospitalDepartment` | Urology / `UROLOGY` |
| Programme | `training.TrainingProgram` | MS Urology / `MS-URO`, 60 months |
| Phases/rotations | `training.ProgramRotationTemplate` | Part I, General Surgery, Part III, Renal Transplantation, Nephrology |
| Policy | `training.ProgramPolicy` | 24-month IMM and 60-month final gates |
| Milestones | `training.ProgramMilestone` | Intermediate at month 24; Final at month 60 |
| Workshop requirements | `ProgramMilestoneWorkshopRequirement` | Six requirements, first three by IMM and three throughout |
| Research requirements | `ProgramMilestoneResearchRequirement` | Synopsis/submission and thesis gates |
| Logbook | `ProgramMilestoneLogbookRequirement` + existing logbook APIs | Required at both milestones |
| Resident | `users.ResidentProfile` + `training.ResidentTrainingRecord` | 28 approved rows |
| Supervision | `supervision.ResidentSupervisorAssignment` | One active primary assignment per resident |

## Training structure

- Part I — Initial Urology: months 1–6, 26 weeks.
- Part II — General Surgery: months 7–24, 78 weeks; synopsis submission milestone at month 24.
- Part III — Advanced Urology: months 25–60, 156 weeks.
- Part III mandatory specialty templates: Renal Transplantation (2 months) and Nephrology (1 month).

Templates are programme-relative. They do not create global calendar dates; resident-specific
`RotationAssignment` records remain the scheduling mechanism.

## Workshops

The six MS requirements are Communication Skills, Research Synopsis & Thesis Writing Skills,
Basic Surgical Skills, Basic Biostatistics & Research Methodology, Information Technology Skills,
and Initial Life Support (ILS). Basic Surgical Skills is a requirement only; no resident completion
is assumed without evidence.

## Assessment/portfolio limitations

The current canonical architecture exposes milestone records and a legacy standalone `Exam`, but
does not provide a programme-linked structured exam blueprint for marks/components or a generic
programme-linked portfolio model. The configuration therefore does not invent those models. CIA,
Intermediate and Final are represented as programme milestones/policy text, while detailed marks,
portfolio domains, and the full specialty procedure catalogue remain follow-up work.

## Curriculum ambiguities

1. The intermediate eligibility wording mentions three mandatory rotations, while the detailed
   programme structure places Renal Transplantation and Nephrology in Part III. PGSIMS follows the
   detailed structure and does not require either rotation before month 24.
2. One continuous-assessment passage says four years, conflicting with the title, statutes and
   programme structure. PGSIMS uses five years / 60 months.

## FCPS boundary

`FCPS Urology` is retained only as the minimal active programme association needed by the seven
approved residents. Its duration, rotations, examinations, workshops, research and assessment
configuration are pending a verified FCPS source.
