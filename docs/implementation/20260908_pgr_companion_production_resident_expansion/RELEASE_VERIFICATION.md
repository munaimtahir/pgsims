# Release verification

Source commit: `26e0a214a93397873a44f9a4bbb28999191230b7`.

| Item | Value |
| --- | --- |
| Application ID | `pk.vexel.pgrcompanion` |
| Version | `1.1.4` / code `4` |
| Production API | `https://android.pgsims.alshifalab.pk/` |
| APK SHA-256 | `4ec6125343fc72e0a45fb844394f5fda4bc3af47725d339585505183c3c9fa49` |
| AAB SHA-256 | `4f9fcd0b38005e8aecda4c0508d26f6f8abd6b3c1fba2e374cf0dfa95d44d708` |
| Upload certificate SHA-256 | `a858f42c4460feab688e3e9fce28b3e9e0d5af03a555133e5e134f890b61f010` |

`assembleRelease` and `bundleRelease` passed with the established owner-controlled signing
properties. APK signature verification passed with v2 signing and the expected certificate. Play
Console sequencing was not accessed; the owner confirmed code 3 is used, so this candidate uses
the required next code 4. Upload still requires the normal external console availability check.
