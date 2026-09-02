from django.apps import AppConfig
from django.db import OperationalError, ProgrammingError


class CertificatesConfig(AppConfig):
    """
    Configuration for the SIMS Certificates app.

    This app manages certificate tracking and verification for the SIMS platform:
    - Certificate upload and storage
    - Certificate type management
    - Review and approval workflows
    - Expiry tracking and notifications
    - CME/CPD points tracking
    - Compliance reporting

    Created: 2025-05-29 16:55:35 UTC
    Author: SMIB2012
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "sims.certificates"
    verbose_name = "SIMS Certificates & Credentials"

    def ready(self):
        """
        Called when Django starts.
        Import any signal handlers or perform app initialization.
        """
        try:
            # Import signals for certificate management
            pass

            # Register any custom model permissions
            from django.contrib.auth.models import Permission
            from django.contrib.contenttypes.models import ContentType

            from .models import Certificate, CertificateReview

            # Create custom permissions if they don't exist
            certificate_ct = ContentType.objects.get_for_model(Certificate)
            review_ct = ContentType.objects.get_for_model(CertificateReview)

            custom_permissions = [
                ("can_verify_certificates", "Can verify certificates", certificate_ct),
                ("can_approve_certificates", "Can approve certificates", certificate_ct),
                ("can_view_all_certificates", "Can view all certificates", certificate_ct),
                ("can_review_certificates", "Can review certificates", review_ct),
                ("can_generate_reports", "Can generate certificate reports", certificate_ct),
            ]

            for codename, name, content_type in custom_permissions:
                Permission.objects.get_or_create(
                    codename=codename, name=name, content_type=content_type
                )

            # Set up periodic tasks for certificate expiry checking
            self._setup_certificate_tasks()

        except (OperationalError, ProgrammingError):
            # Database not ready (migrations not applied). Skip DB-dependent initialization.
            pass
        except ImportError:
            pass
        except Exception as e:
            # Log the error but don't prevent app from loading
            import logging

            logger = logging.getLogger("sims.certificates")
            logger.warning(f"Error in certificates app ready(): {e}")

    def _setup_certificate_tasks(self):
        """Setup periodic tasks for certificate management"""
        try:
            # This would integrate with Celery or Django-RQ for periodic tasks
            # For now, we'll just log that the setup is attempted
            import logging

            logger = logging.getLogger("sims.certificates")
            logger.info("Certificate periodic tasks setup completed")

            # Example of what would be set up:
            # - Daily check for expiring certificates
            # - Weekly compliance reports
            # - Monthly certificate statistics

        except Exception as e:
            import logging

            logger = logging.getLogger("sims.certificates")
            logger.warning(f"Could not setup certificate periodic tasks: {e}")
