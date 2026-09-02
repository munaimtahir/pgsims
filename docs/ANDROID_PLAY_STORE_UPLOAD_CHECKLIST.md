# Android Play Store Upload Checklist

## Binary identity

- App name: FMU Postgraduate Residency Portal
- Developer: Vexel Consultants
- Support email: contact@vexel.pk
- Final package/application ID: `fmu.pg.sims`
- Release artifact: locally signed Android App Bundle
- Play App Signing: enroll the new application and retain the local upload key

## Play Console items to complete

- Provide and verify the privacy policy URL; no URL is inferred by this repository.
- Complete the Data Safety declaration from the final data flows and backend policy.
- Complete App Access instructions when the functional login flow exists. Do not use
  production resident credentials in source control.
- Complete the content rating questionnaire.
- Declare the target audience and age groups.
- Declare whether the app contains ads.
- Supply store listing assets and descriptions required by Play Console.
- Configure internal-testing testers and release notes.
- Complete any account-deletion declaration/page requirement applicable to the actual
  account model.
- Review and declare any permission-specific requirements shown by Play Console.

## Review-access preparation

This foundation shell does not yet implement the functional login experience. Before
review or broader testing, create a dedicated non-sensitive review account if App
Access instructions require one, and manage its credentials outside Git.

## Signing distinction

The locally retained key is the Google Play **upload key**. Google Play App Signing
should manage the distribution **app-signing key** for this new application. The
private upload keystore and its passwords are stored outside the repository and are
not recorded here.
