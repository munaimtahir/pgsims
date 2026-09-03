# PGSIMS Android App — Data Safety Policy

This document is the human-readable basis for the Play Console **Data Safety** section and for
the app's public **privacy policy** page. It reflects the app's actual, verified behavior as of
`versionCode 2` / `versionName 0.2.0` (package `fmu.pg.sims`) — not a generic template. The
machine-readable form matching this policy, ready to import directly into Play Console
(**Play Console → App content → Data safety → Import**), is at
`docs/ANDROID_DATA_SAFETY_FILLED.csv`.

## How this was determined

Not guessed — derived from the actual codebase and a live production audit performed this
session: the Android `ApiService`/repositories (`android/app/src/main/java/fmu/pg/sims/core/`),
the backend's `onboarding_api.py` and `User`/`ResidentProfile` models, the full
`releaseRuntimeClasspath` dependency audit already done for the implementation report (§4.6:
confirmed zero analytics/ads/crash-telemetry SDKs), the Android manifest's permission list
(`INTERNET`, `ACCESS_NETWORK_STATE` only — no location, contacts, camera, storage, etc.), and
direct queries against the live production database and audit log.

## Summary

- **What the app collects**: identity and profile fields needed to onboard a medical resident
  into the training program (name, phone, email, national ID/registration numbers), documents
  the resident uploads to prove eligibility (CNIC copy, PMDC registration certificate, etc.), and
  a server-side audit trail of onboarding actions (submitted, corrected, resubmitted, approved).
- **Who it's shared with**: **nobody**. There is no analytics SDK, no ad SDK, no crash-reporting
  SDK, and no third-party backend. All data goes directly from the app to PGSIMS's own backend
  server over HTTPS and stays there.
- **Why**: exclusively to run the app's core function — verifying and onboarding a resident into
  the postgraduate training program — and for account/security administration by the training
  institution. Never for advertising, and never sold.
- **Encryption in transit**: yes. All API traffic goes over HTTPS to `android.pgsims.alshifalab.pk`
  (Let's Encrypt certificate, verified live this session).
- **Encryption at rest (on-device)**: auth tokens are stored using
  `androidx.security.crypto.EncryptedSharedPreferences` (Tink-backed), not plain SharedPreferences.

## Data types collected (maps to Play Console categories)

| Play Console category | Collected? | What specifically | Source in code |
|---|---|---|---|
| Personal info → Name | Yes | Full name | `User.first_name`/`last_name`, set via onboarding "Personal Information" step |
| Personal info → Email address | Yes | Email address | `User.email` / `ResidentProfile.email` |
| Personal info → User IDs | Yes | Username (institutional login ID) | `User.username` |
| Personal info → Phone number | Yes | Contact number | `User.phone_number` / `ResidentProfile.phone` |
| Personal info → Other info | Yes | National ID (CNIC) number, registration number, and training/program enrollment details (hospital, department, specialty, session, level) | `ResidentProfile.cnic`, `.registration_no`, and training fields |
| Personal info → Address, Race/ethnicity, Political/religious beliefs, Sexual orientation | **No** | Not collected anywhere in the app | — |
| Financial info (all) | **No** | The app has no payment/purchase flow | — |
| Location (approximate or precise) | **No** | No location permission requested; not in the manifest | — |
| Web browsing history | **No** | Not collected | — |
| Messages (email content, SMS, other) | **No** | Not collected | — |
| Photos and videos (standalone) | **No** | See "Files and docs" below instead | — |
| Audio files | **No** | Not collected | — |
| Health and fitness | **No** | The app manages professional training records, not the resident's personal health/fitness data | — |
| Contacts | **No** | No contacts permission requested | — |
| Calendar | **No** | Not collected | — |
| App info and performance (crash logs, diagnostics) | **No** | No crash-reporting or analytics SDK is bundled (verified against the full release dependency tree) | — |
| Files and docs | Yes | Identity/eligibility documents the resident uploads (e.g. CNIC copy, PMDC registration certificate), via the system file/photo picker | `ResidentDocument`, `OnboardingDocumentsScreen` |
| App activity → App interactions | Yes | Server-side audit log of onboarding actions (draft saved, submitted, correction requested, resubmitted, approved) — used for accountability, not analytics or ads | `sims.audit.models.ActivityLog` (`verb` field, e.g. `ONBOARDING_SUBMITTED`) |
| App activity → search history, installed apps, other | **No** | Not collected | — |
| Device or other IDs | **No** | No advertising ID or device-fingerprinting library is used | — |

## Purpose of collection

For every data type marked "Yes" above, the declared purposes are:

- **App functionality** — the core reason: the resident onboarding workflow cannot function
  without this data (identity verification, contact info, eligibility documents).
- **Account management** — administering the resident's account within the institution's
  system.
- **Fraud prevention, security, and compliance** — applies specifically to the ID/registration
  numbers, uploaded documents, and the audit log, which exist to verify a real resident's
  identity/eligibility and to maintain an accountable record of who did what and when.
- **Developer communications** — applies only to email address, which the institution may use to
  reach a resident about their account or onboarding status.

**Never selected for any data type**: Analytics, Advertising or marketing, Personalization. The
app does not do any of these things.

## Sharing

**Nothing is shared with third parties.** Every data type above is marked "Collected" only (not
"Shared") in the filled form. All requests go from the Android app directly to the PGSIMS
production backend (`android.pgsims.alshifalab.pk`, operated by the institution itself) — there is
no third-party analytics platform, ad network, crash reporter, or external processor in the data
path.

## Data deletion — a real gap you should decide on before publishing

The template this was based on had a **pre-filled but factually incorrect** answer claiming user
data is "automatically deleted within 90 days." That is not true of this app: resident training
and onboarding records are retained for the duration of the residency program (multi-year) and
for institutional/accreditation record-keeping — there is no 90-day auto-deletion anywhere in the
codebase, and claiming there is would misrepresent the app to Google and to users. I corrected the
filled form to the honest answer: **"No, the app does not currently provide a way for users to
request that their data is deleted."**

This is accurate today, but it's worth deciding deliberately rather than leaving as a permanent
gap, since Play policy expects apps to eventually offer *some* path (even a manual/administrative
one) for a data-deletion request. Two reasonable options, your call:

1. **Do nothing further right now** — "No" is a truthful, policy-compliant answer as long as it
   stays true. Revisit if Google flags it during review.
2. **Add a lightweight path**: a documented process where a resident (or ex-resident) can email
   the program administrator to request account closure, subject to the institution's legitimate
   retention obligations for training/accreditation records — then change the answer to "Yes" with
   that contact process described. This doesn't require new app code, just an institutional
   policy + a line in the privacy policy page.

## Account creation

The app does **not** let a user create their own account (no self-registration/sign-up screen
exists anywhere in the Android app). Every account — resident, supervisor, support staff, or
admin — is provisioned by an institutional administrator through the PGSIMS web console
(`/users/new`), outside the mobile app, matching the platform's universal-identity-creation model
(see `CLAUDE.md`). A resident's first action in the app is always signing in with credentials
already issued to them, then setting their own password on first login. This is declared as:

- Account creation methods supported: **None** (app does not allow in-app account creation)
- Can users log in with accounts created outside the app: **Yes**, via employment/enterprise
  (institutional) provisioning

## Privacy policy page — suggested data-handling paragraph

If you don't already have this on the hosted privacy policy page Play Console needs a URL for,
here's ready-to-use text reflecting the above:

> **What we collect.** When you sign in to the FMU Postgraduate Residency Portal app, we collect
> the identity and training-program information you provide during onboarding — your name, phone
> number, email address, national ID (CNIC) and registration numbers, training program/department
> details, and any identity or eligibility documents you upload (such as a CNIC copy or PMDC
> registration certificate). We also keep an internal audit record of onboarding actions on your
> account (submitted, corrected, resubmitted, approved) for accountability and security purposes.
>
> **How we use it.** This information is used only to verify your identity, onboard you into the
> postgraduate residency training program, and administer your account. We do not use it for
> advertising or marketing, and we do not build behavioral profiles from it.
>
> **Who we share it with.** Nobody outside the institution. We do not use third-party analytics,
> advertising, or crash-reporting services in this app, and we do not sell or share your data with
> external companies.
>
> **How we protect it.** All communication between the app and our servers is encrypted in transit
> (HTTPS). Your session credentials are stored on your device using Android's encrypted storage.
>
> **How long we keep it.** Training and onboarding records are retained for the duration of your
> residency program and as required for institutional accreditation record-keeping. [Add your
> institution's specific retention period here if you have one, or note that deletion requests can
> be sent to `[program admin contact]`.]

## Files delivered

- `docs/ANDROID_DATA_SAFETY_FILLED.csv` — the corrected, filled Data Safety form in Google's own
  import/export CSV schema. Import it directly: **Play Console → your app → App content → Data
  safety → Import data safety details** (Play Console does support importing this exact format).
  Review the imported answers on-screen before publishing — Google's UI may re-validate a couple
  of conditionally-required fields depending on other answers already set in your Console.
- `docs/ANDROID_DATA_SAFETY_POLICY.md` — this document.
