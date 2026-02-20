"""
Pytest configuration for SIMS tests.
Provides fixtures and configuration for deterministic, reliable testing.
"""

import pytest
import random
from datetime import date, datetime
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import tempfile
import os


@pytest.fixture(scope='session', autouse=True)
def setup_test_environment():
    """Configure test environment for deterministic tests."""
    # Set random seeds for reproducibility
    random.seed(42)
    
    # Configure temporary media storage
    temp_media = tempfile.mkdtemp(prefix='sims_test_media_')
    settings.MEDIA_ROOT = temp_media
    settings.DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
    
    yield
    
    # Cleanup
    import shutil
    try:
        shutil.rmtree(temp_media)
    except Exception:
        pass


@pytest.fixture(autouse=True)
def reset_sequences(db):
    """Reset factory sequences for each test to ensure predictability."""
    from factory import Sequence
    # Factory-boy sequences are automatically reset per test when using pytest-django
    pass


@pytest.fixture
def freeze_time():
    """Fixture to freeze time for tests."""
    from freezegun import freeze_time as freezegun_freeze
    return freezegun_freeze


@pytest.fixture
def pg_user(db):
    """Create a PG user for testing."""
    from sims.tests.factories import PGFactory
    return PGFactory()


@pytest.fixture
def supervisor_user(db):
    """Create a supervisor user for testing."""
    from sims.tests.factories import SupervisorFactory
    return SupervisorFactory()


@pytest.fixture
def admin_user(db):
    """Create an admin user for testing."""
    from sims.tests.factories import AdminFactory
    return AdminFactory()


@pytest.fixture
def clinical_case(db, pg_user):
    """Create a clinical case for testing."""
    from sims.tests.factories import ClinicalCaseFactory
    return ClinicalCaseFactory(pg=pg_user)


@pytest.fixture
def logbook_entry(db, pg_user):
    """Create a logbook entry for testing."""
    from sims.tests.factories import LogbookEntryFactory
    return LogbookEntryFactory(pg=pg_user)


@pytest.fixture
def certificate(db, pg_user):
    """Create a certificate for testing."""
    from sims.tests.factories import CertificateFactory
    return CertificateFactory(pg=pg_user)


@pytest.fixture
def rotation(db, pg_user):
    """Create a rotation for testing."""
    from sims.tests.factories import RotationFactory
    return RotationFactory(pg=pg_user)
