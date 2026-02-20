"""Factories for Certificate models"""

import factory
from factory.django import DjangoModelFactory
from datetime import date, timedelta
from django.core.files.uploadedfile import SimpleUploadedFile
from sims.certificates.models import CertificateType, Certificate
from .user_factories import PGFactory


class CertificateTypeFactory(DjangoModelFactory):
    """Factory for CertificateType model."""

    class Meta:
        model = CertificateType

    name = factory.Sequence(lambda n: f"Certificate Type {n}")
    category = "professional"
    description = factory.Faker("sentence")
    is_required = False
    validity_period_months = 12
    cme_points = 10
    cpd_credits = 5
    is_active = True


class CertificateFactory(DjangoModelFactory):
    """Factory for Certificate model with all required fields."""

    class Meta:
        model = Certificate

    pg = factory.SubFactory(PGFactory)
    certificate_type = factory.SubFactory(CertificateTypeFactory)
    title = factory.Faker("sentence", nb_words=6)
    certificate_number = factory.Sequence(lambda n: f"CERT-{n:05d}")
    issuing_organization = factory.Faker("company")
    issue_date = factory.LazyFunction(lambda: date.today() - timedelta(days=90))
    expiry_date = factory.LazyFunction(lambda: date.today() + timedelta(days=275))
    description = factory.Faker("paragraph")
    skills_acquired = factory.Faker("paragraph")
    cme_points_earned = 10
    cpd_credits_earned = 5
    certificate_file = factory.LazyFunction(
        lambda: SimpleUploadedFile(
            "certificate.pdf", b"fake pdf content", content_type="application/pdf"
        )
    )
    status = "pending"
    is_verified = False
