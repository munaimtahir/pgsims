"""Factories for Logbook models"""

import factory
from factory.django import DjangoModelFactory

from sims.logbook.models import Diagnosis, Procedure


class DiagnosisFactory(DjangoModelFactory):
    """Factory for Diagnosis model."""

    class Meta:
        model = Diagnosis

    name = factory.Sequence(lambda n: f"Diagnosis {n}")
    category = "other"
    is_active = True


class ProcedureFactory(DjangoModelFactory):
    """Factory for Procedure model."""

    class Meta:
        model = Procedure

    name = factory.Sequence(lambda n: f"Procedure {n}")
    category = "diagnostic"
    is_active = True
