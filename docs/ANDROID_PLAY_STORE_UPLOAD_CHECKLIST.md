# Android Play Store Upload Checklist

## Binary identity

- App name: FMU Postgraduate Residency Portal
- Developer: Vexel Consultants
- Support email: contact@vexel.pk
- Final package/application ID: `fmu.pg.sims`
- Version Code: 2
- Version Name: `0.2.0`
- Target SDK: 36 (Android 16)
- Min SDK: 26 (Android 8.0)
- Release artifact: locally signed Android App Bundle (`android/app/build/outputs/bundle/release/app-release.aab`)
- AAB SHA-256: `d336461153a0e06707598a25cb05ff5d0e6117297d255a3634d81aa7a936c20d`
- APK SHA-256: `4d3934b7bebf44b9dc32ef9e4848f4545cc9a108a100bced20fb282d71702bc1`
- Upload Key Fingerprint (SHA-256): `35:16:7F:22:5F:FF:61:55:54:80:07:07:EA:F1:54:F1:E6:55:B4:8F:0A:FE:0E:0A:68:48:E4:CC:EB:DD:44:B9`
- Upload Certificate: `/home/munaim/.config/fmu-pg-sims/signing/fmu-pg-sims-upload-certificate.pem`
- Play App Signing: enroll the application and retain the local upload key

## Play Console items to complete

- [ ] Provide and verify the privacy policy URL (external web host required).
- [ ] Complete the Data Safety declaration (Network calls to `android.pgsims.alshifalab.pk`, personal info, documents uploaded).
- [ ] Complete App Access instructions (Dedicated demo account credentials provided to Play Reviewers).
- [ ] Complete the content rating questionnaire.
- [ ] Declare target audience and age groups (18+ healthcare professionals).
- [ ] Declare whether the app contains ads (No ads).
- [ ] Supply store listing assets and descriptions (Hi-res icon 512x512, feature graphic 1024x500, phone screenshots).
- [ ] Configure internal testing track and upload `app-release.aab`.
- [ ] Complete account-deletion declaration/page URL requirement.
- [ ] Declare declared permissions (`INTERNET`, `ACCESS_NETWORK_STATE`).

## Review-access preparation

A functional login and resident onboarding experience is fully verified against the live production backend (`android.pgsims.alshifalab.pk`). For Play Console App Access review:
- Create a dedicated non-sensitive review resident account using `seed_android_e2e_demo` or universal user creation (`/users/new`).
- Provide instructions explaining the 4-role residency model, credential format, and temporary-to-new password change requirement on initial login.

## Signing distinction

The locally retained key is the Google Play **upload key** stored at `/home/munaim/.config/fmu-pg-sims/signing/fmu-pg-sims-upload.jks`. Google Play App Signing manages the distribution **app-signing key** in Google infrastructure.
