from celery import shared_task
import logging
from sims.users.models import WorkspaceIdentity
from sims.users.bridge_service import AdminOpsBridgeService

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_identity_to_adminops_task(self, identity_id, actor_id=None):
    """
    Celery task to send a WorkspaceIdentity payload to AdminOps.
    """
    try:
        identity = WorkspaceIdentity.objects.get(id=identity_id)
    except WorkspaceIdentity.DoesNotExist:
        logger.error(f"WorkspaceIdentity {identity_id} not found.")
        return

    # Check if we should send
    if identity.onboarding_status != WorkspaceIdentity.ONBOARDING_STATUS_APPROVED:
        logger.info(f"Identity {identity_id} is not approved. Status: {identity.onboarding_status}")
        return

    actor = None
    if actor_id:
        from sims.users.models import User
        try:
            actor = User.objects.get(id=actor_id)
        except User.DoesNotExist:
            pass

    service = AdminOpsBridgeService()
    success, error = service.send_to_adminops(identity, actor=actor)
    
    if not success and not service.mock_mode:
        # Retry on failure if not in mock mode
        logger.warning(f"Bridge sync failed for identity {identity_id}: {error}. Retrying...")
        raise self.retry(exc=Exception(error))
