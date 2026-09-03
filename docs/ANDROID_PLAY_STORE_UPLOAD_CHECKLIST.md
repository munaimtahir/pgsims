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
- [x] Complete the Data Safety declaration — filled and ready to import: `docs/ANDROID_DATA_SAFETY_FILLED.csv`
      (Play Console → App content → Data safety → Import). Human-readable rationale and a
      suggested privacy-policy data paragraph in `docs/ANDROID_DATA_SAFETY_POLICY.md`. **Open
      item within that doc**: the app currently has no self-service data-deletion path — decide
      whether to leave the honest "No" answer or add an admin-contact process before publishing.
- [x] Complete App Access instructions — dedicated reviewer credentials created and verified below.
- [ ] Complete the content rating questionnaire.
- [ ] Declare target audience and age groups (18+ healthcare professionals).
- [ ] Declare whether the app contains ads (No ads).
- [x] Phone screenshots captured: `store_listing_screenshots/01_login.png`, `02_home.png`,
      `03_documents.png` (1080×1920, taken from the actual signed release build against the live
      production backend).
- [ ] Supply remaining store listing assets and descriptions (hi-res icon 512×512, feature graphic 1024×500).
- [ ] Configure internal testing track and upload `app-release.aab`.
- [ ] Complete account-deletion declaration/page URL requirement.
- [ ] Declare declared permissions (`INTERNET`, `ACCESS_NETWORK_STATE`).

## Review-access preparation

A functional login and resident onboarding experience is fully verified against the live production backend (`android.pgsims.alshifalab.pk`).

**Play Console → App content → App access** — select "All or some functionality is restricted"
and paste these details:

- Username: `playstore.reviewer`
- Password: `PlayReview2026!`
- Instructions: "This app requires a residency-program account, provisioned by an institutional
  administrator — there is no self-registration. Use the credentials above at the sign-in screen.
  No further steps or 2FA are required. The account is a fully onboarded and approved resident, so
  all four tabs (Home, Training, Documents, Profile) are immediately accessible after login."

This is a **dedicated reviewer account**, separate from the `android.demo.*` accounts used during
development/testing, created directly in the production DB and independently verified end-to-end
on the actual signed release build (login → approved Home dashboard, `review_status=APPROVED`).
It intentionally has 2 deferred documents outstanding, so the reviewer also sees the
outstanding-document reminder banner. If this account's password ever needs to change, update it
via Django admin/shell on the production backend and update this doc + Console together.

## Signing distinction

The locally retained key is the Google Play **upload key** stored at `/home/munaim/.config/fmu-pg-sims/signing/fmu-pg-sims-upload.jks`. Google Play App Signing manages the distribution **app-signing key** in Google infrastructure.
