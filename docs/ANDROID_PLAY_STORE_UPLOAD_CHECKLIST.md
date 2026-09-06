# Android Play Store Upload Checklist

This checklist applies only to the generic Companion product. The historic institutional Portal
listing and reviewer-account details were deliberately removed from this tracked document: Portal
is now a separate development/release track and no passwords or reviewer credentials belong in Git.

## Companion candidate

- App name: PGR Companion: Residency
- Application ID: `pk.vexel.pgrcompanion`
- Version: `1.1.0` (versionCode `2`)
- Artifact: `builds/companion/PGR-Companion-1.1.0.aab`
- SHA-256: `f48ae84b95f0553f6ed983fab0f5036044a07ac99e2b5f64230e2e0421e23e9e`
- Target/min SDK: 36 / 26
- Network/authentication: none required; Companion has no `INTERNET` permission.

## Before upload

- [ ] Confirm the upload-key certificate in Play Console matches the recorded local fingerprint in
      `docs/ANDROID_RELEASE_VERIFICATION.md`.
- [ ] Confirm versionCode `2` has not already been uploaded in the Companion Play Console.
- [ ] Complete the normal store-listing, content-rating, privacy, and Data Safety declarations for
      the generic local-first Companion product.
- [ ] Upload only the frozen AAB above; compare its SHA-256 before selecting it in Play Console.

## Institutional Portal boundary

Portal is not a Companion release variant and must not be uploaded as a replacement artifact.
For a future Portal Play review, create reviewer access through a secure out-of-band channel and
record only the procedure (never credentials) under `docs/play-policy/`.
