# Accessibility Review

| Page/Component | Issue | Accessibility impact | Suggested fix | Priority |
| --- | --- | --- | --- | --- |
| `/dashboard/utrmc/matrix` | Toggle targets are tiny 20px squares with no textual affordance. | Hard to use with keyboard/touch; low discoverability. | Replace with larger labeled toggles or a grouped matrix editor with row/column headers. | High |
| `/dashboard/utrmc/departments` and `/dashboard/utrmc/hospitals` tables | Dense tables rely on small text and low-contrast gray metadata. | Hard to scan for older or busy users. | Increase default table font size and reduce secondary text density. | Medium |
| `/dashboard/resident/page.tsx` | The page assumes `summary.training_record` is always present. | Screen users hit a crash instead of a usable fallback. | Guard null training record and render a guided empty state. | P0 |
| `/dashboard/resident/schedule` | Uses placeholder-driven inputs and no helper summary for leave request fields. | Field purpose is easy to miss; form completion is error-prone. | Add persistent labels, helper text, and required-field hints. | Medium |
| `/dashboard/resident/progress` | The draft logbook form is mostly placeholder-driven and sparse on labels. | Placeholder text is not a reliable label replacement. | Add visible labels for all fields, especially ID, date/time, and notes. | High |
| `/dashboard/utrmc/data-quality` | Filter chips and secondary labels use low-contrast gray text. | Weaker readability for older users and low-vision users. | Increase contrast and use stronger hierarchy for filter states. | Medium |
| `/dashboard/utrmc/eligibility-monitoring` | Status cards rely on color and compact chips without much structural guidance. | Harder to parse for non-technical users and color-blind users. | Add short explanatory text and visible section summaries. | Medium |
| `/dashboard/supervisor` | Empty-state panels are readable, but there is little prioritization of the most important actions. | Users must infer what matters today. | Add a top "today" summary with pending work first. | Medium |
| `frontend/components/ui/ErrorBanner.tsx` | Close button is icon-only and unlabeled. | Screen-reader users get less context. | Add `aria-label` and a visible text dismiss affordance. | Low |
| `frontend/components/ui/LoadingSkeleton.tsx` | Skeletons have no accessible status text. | Loading state is visually obvious but not explained to assistive tech. | Pair skeletons with `aria-busy` and a short loading label. | Low |

## Accessibility Notes

- The sidebar toggle has an `aria-label`, which is good
- Most major page headers are readable, but the app still depends too much on dense tables and small labels
- The biggest accessibility issue in the live baseline is not a contrast problem; it is the lack of a safe fallback on the resident landing route

