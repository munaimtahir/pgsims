# Data safety facts

The app stores resident-entered profile information, training records, reminder records, and user-selected PDF/image copies in app-private storage. No data is transmitted off-device by the shipped app source or declared runtime permissions. There are no ads, analytics, location collection, contacts, phone/SMS access, microphone access, or patient-record fields. The product is not intended for patient information.

The document picker is Android's system picker. Selected files are copied into the app's private `files/documents` directory; broad storage permissions are not requested.
