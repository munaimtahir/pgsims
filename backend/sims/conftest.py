"""
Pytest configuration and shared fixtures for SIMS tests.
Provides reusable fixtures for all test modules.
"""

import pytest
from django.test import Client


@pytest.fixture
def client_auth_admin(admin_user):
    """Authenticated client for admin user."""
    client = Client()
    client.force_login(admin_user)
    return client


@pytest.fixture
def client_auth_supervisor(supervisor):
    """Authenticated client for supervisor user."""
    client = Client()
    client.force_login(supervisor)
    return client


@pytest.fixture
def client_auth_pg(pg_user):
    """Authenticated client for PG user."""
    client = Client()
    client.force_login(pg_user)
    return client


@pytest.fixture
def unauthenticated_client():
    """Unauthenticated client for testing login redirects."""
    return Client()
