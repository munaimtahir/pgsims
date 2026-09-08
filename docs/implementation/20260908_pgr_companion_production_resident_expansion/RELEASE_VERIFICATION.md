# Release verification

Source commit: `e2996f2b7f9ef5651a8d0abf0d66a2026cd75ea6`.

| Item | Value |
| --- | --- |
| Application ID | `pk.vexel.pgrcompanion` |
| Version | `1.1.3` / code `3` |
| Production API | `https://android.pgsims.alshifalab.pk/` |
| APK SHA-256 | `610ed965be06997ce8c465e9e049191f07a760197c74f98dfc431f6285b7f612` |
| AAB SHA-256 | `737ed84a32bf5c2d85ac7737ee79cf91ad633cd9de2615d711c053bd27f2d5e3` |
| Upload certificate SHA-256 | `a858f42c4460feab688e3e9fce28b3e9e0d5af03a555133e5e134f890b61f010` |

`assembleRelease` and `bundleRelease` passed with the established owner-controlled signing
properties. APK signature verification passed with v2 signing and the expected certificate. Play
Console sequencing was not accessed; code 3 must not be uploaded unless its availability is
confirmed there, and the next upload must use a strictly higher unused versionCode if code 3 is
already consumed.
