"""Factories for User models"""
import factory
from factory.django import DjangoModelFactory
from faker import Faker
from django.contrib.auth import get_user_model

User = get_user_model()
fake = Faker()


class UserFactory(DjangoModelFactory):
    """Base factory for User model"""

    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@sims.test")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    is_active = True
    is_archived = False


class AdminFactory(UserFactory):
    """Factory for admin users"""

    username = factory.Sequence(lambda n: f"admin{n}")
    role = "admin"
    is_staff = True


class SupervisorFactory(UserFactory):
    """Factory for supervisor users"""

    username = factory.Sequence(lambda n: f"supervisor{n}")
    role = "supervisor"
    specialty = "medicine"


class PGFactory(UserFactory):
    """Factory for PG (postgraduate) users"""

    username = factory.Sequence(lambda n: f"pg{n}")
    role = "pg"
    specialty = "medicine"
    year = "1"
    supervisor = factory.LazyAttribute(lambda o: o.supervisor if o.supervisor else SupervisorFactory())
