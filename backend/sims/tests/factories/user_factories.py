"""
Comprehensive user factories for SIMS testing.
All factories ensure valid model creation with required fields.
"""

import factory
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from factory.django import DjangoModelFactory

User = get_user_model()


class UserFactory(DjangoModelFactory):
    """Base factory for User model."""

    class Meta:
        model = User
        skip_postgeneration_save = True

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@sims.test")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    password = factory.LazyFunction(lambda: make_password("testpass123"))
    is_active = True
    is_archived = False
    role = "admin"


class AdminFactory(UserFactory):
    """Factory for admin users."""

    username = factory.Sequence(lambda n: f"admin{n}")
    role = "admin"
    is_staff = True
    is_superuser = True


class SupervisorFactory(UserFactory):
    """Factory for supervisor users with required specialty."""

    username = factory.Sequence(lambda n: f"supervisor{n}")
    role = "supervisor"
    specialty = "medicine"


class PGFactory(UserFactory):
    """Factory for PG users with all required fields."""

    username = factory.Sequence(lambda n: f"pg{n}")
    role = "pg"
    specialty = "medicine"
    year = "1"
    supervisor = factory.SubFactory(SupervisorFactory)
