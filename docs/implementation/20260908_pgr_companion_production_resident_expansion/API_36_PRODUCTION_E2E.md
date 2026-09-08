# API-36 production E2E

Device: `AdForge_API_36`, Android 16 / API 36, `x86_64`. The signed release APK was installed from
the source commit under test and used the production release base URL.

| Workflow | Result |
| --- | --- |
| Fresh install and production login | PASS |
| Home and current training summary | PASS |
| Training, server-selected current posting, history and rotation detail | PASS |
| Requirements, assessments/workshops empty state and Documents | PASS |
| Production document replacement | PASS |
| Logbook list, detail and submit | PASS |
| Returned-for-correction feedback, edit and resubmit | PASS — production status returned to `SUBMITTED` |
| Profile display and permitted full-name update | PASS |
| Background/force-stop/relaunch encrypted-session restore | PASS |
| Logout and re-login | PASS |
| Uninstall/reinstall removes local session | PASS |
| App crash buffer | PASS — no fatal application exception |

The only visible emulator issue was one transient System UI startup ANR before app testing; it did
not recur and was not an application crash.
