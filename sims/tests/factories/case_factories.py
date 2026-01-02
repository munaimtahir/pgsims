"""Factories for Cases models"""

from datetime import date

import factory
from factory.django import DjangoModelFactory

from sims.cases.models import CaseCategory, ClinicalCase

from .logbook_factories import DiagnosisFactory
from .user_factories import PGFactory


class CaseCategoryFactory(DjangoModelFactory):
    """Factory for CaseCategory model."""

    class Meta:
        model = CaseCategory

    name = factory.Sequence(lambda n: f"Category {n}")
    description = factory.Faker("sentence")
    color_code = "#007bff"
    is_active = True
    sort_order = 0


class ClinicalCaseFactory(DjangoModelFactory):
    """Factory for ClinicalCase model with all required fields."""

    class Meta:
        model = ClinicalCase

    pg = factory.SubFactory(PGFactory)
    supervisor = factory.LazyAttribute(lambda obj: obj.pg.supervisor)
    case_title = factory.Faker("sentence", nb_words=6)
    category = factory.SubFactory(CaseCategoryFactory)
    date_encountered = factory.LazyFunction(date.today)
    patient_age = 45
    patient_gender = "M"
    complexity = "moderate"
    chief_complaint = factory.Faker("sentence")
    history_of_present_illness = factory.Faker("paragraph")
    physical_examination = factory.Faker("paragraph")
    primary_diagnosis = factory.SubFactory(DiagnosisFactory)
    management_plan = factory.Faker("paragraph")
    clinical_reasoning = factory.Faker("paragraph")
    learning_points = factory.Faker("paragraph")
    status = "draft"
    is_active = True
    is_featured = False
