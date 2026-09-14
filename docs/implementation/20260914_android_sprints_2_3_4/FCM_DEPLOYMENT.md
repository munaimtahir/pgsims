# FCM Deployment

1. Register `pk.vexel.pgrcompanion` in the owner-controlled Firebase project.
2. Provision `google-services.json` through the secure Android build path; never commit it.
3. Mount the Firebase service-account JSON outside the VPS repository and configure
   `GOOGLE_APPLICATION_CREDENTIALS` for backend/worker containers.
4. Set `FCM_ENABLED=true`, deploy only PGSIMS services, authenticate an emulator, and verify a
   notification reaches only its recipient's registered device.

PGSIMS remains the event, permissions, and preference authority; Firebase is transport only.
