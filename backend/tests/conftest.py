import pytest
from django.contrib.auth.hashers import make_password
from sims.users.models import User

@pytest.fixture
def admin_user(db):
    return User.objects.create(
        username="admin_test",
        email="admin@sims.test",
        password=make_password("testpass123"),
        role="admin",
        first_name="Admin",
        last_name="User",
        is_staff=True,
        is_superuser=True,
        is_active=True,
    )

@pytest.fixture
def supervisor_user(db):
    return User.objects.create(
        username="supervisor_test",
        email="supervisor@sims.test",
        password=make_password("testpass123"),
        role="supervisor",
        specialty="medicine",
        first_name="Super",
        last_name="Visor",
        is_staff=True,
        is_active=True,
    )

@pytest.fixture
def pg_user(db, supervisor_user):
    return User.objects.create(
        username="pg_test",
        email="pg@sims.test",
        password=make_password("testpass123"),
        role="pg",
        specialty="medicine",
        year="1",
        supervisor=supervisor_user,
        first_name="Post",
        last_name="Graduate",
        is_active=True,
    )
