from datetime import date, timedelta

import factory
from factory.django import DjangoModelFactory

from sims.academics.models import Department
from sims.rotations.models import Hospital, Rotation

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
    code = factory.Sequence(lambda n: f"DEPT{n:03d}")
    description = factory.Faker("paragraph")
    active = True


class CanonicalDepartmentFactory(DepartmentFactory):
    pass


class RotationHospitalFactory(HospitalFactory):
    pass


class HospitalDepartmentMatrixFactory(DjangoModelFactory):
    class Meta:
        model = "rotations.HospitalDepartment"

    hospital = factory.SubFactory(HospitalFactory)
    department = factory.SubFactory(DepartmentFactory)
    is_active = True


class RotationFactory(DjangoModelFactory):
    """Factory for Rotation model with all required fields."""

    class Meta:
        model = Rotation

    pg = factory.SubFactory(PGFactory)
    supervisor = factory.LazyAttribute(lambda obj: obj.pg.supervisor)
    department = factory.SubFactory(DepartmentFactory)
    hospital = factory.SubFactory(HospitalFactory)
    start_date = factory.LazyFunction(lambda: date.today() - timedelta(days=30))
    end_date = factory.LazyFunction(lambda: date.today() + timedelta(days=60))
    objectives = factory.Faker("paragraph")
    status = "ongoing"
