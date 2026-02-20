"""Factories for Rotation models"""

import factory
from factory.django import DjangoModelFactory
from datetime import date, timedelta
from sims.rotations.models import Hospital, Department, Rotation
from .user_factories import PGFactory


class HospitalFactory(DjangoModelFactory):
    """Factory for Hospital model."""

    class Meta:
        model = Hospital

    name = factory.Sequence(lambda n: f"Hospital {n}")
    code = factory.Sequence(lambda n: f"HOSP{n:03d}")
    address = factory.Faker("address")
    phone = factory.Faker("phone_number")
    email = factory.Faker("email")
    website = factory.Faker("url")
    description = factory.Faker("paragraph")
    facilities = factory.Faker("paragraph")
    is_active = True


class DepartmentFactory(DjangoModelFactory):
    """Factory for Department model."""

    class Meta:
        model = Department

    name = factory.Sequence(lambda n: f"Department {n}")
    hospital = factory.SubFactory(HospitalFactory)
    head_of_department = factory.Faker("name")
    contact_email = factory.Faker("email")
    contact_phone = factory.Faker("phone_number")
    description = factory.Faker("paragraph")
    is_active = True


class RotationFactory(DjangoModelFactory):
    """Factory for Rotation model with all required fields."""

    class Meta:
        model = Rotation

    pg = factory.SubFactory(PGFactory)
    supervisor = factory.LazyAttribute(lambda obj: obj.pg.supervisor)
    department = factory.SubFactory(DepartmentFactory)
    hospital = factory.LazyAttribute(lambda obj: obj.department.hospital)
    start_date = factory.LazyFunction(lambda: date.today() - timedelta(days=30))
    end_date = factory.LazyFunction(lambda: date.today() + timedelta(days=60))
    objectives = factory.Faker("paragraph")
    status = "active"
