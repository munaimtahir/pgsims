"""Test factories for SIMS models"""

from .user_factories import AdminFactory, SupervisorFactory, PGFactory, UserFactory
from .logbook_factories import (
    DiagnosisFactory,
    ProcedureFactory,
)
from .case_factories import CaseCategoryFactory, ClinicalCaseFactory
from .certificate_factories import CertificateTypeFactory, CertificateFactory
from .rotation_factories import (
    HospitalFactory,
    DepartmentFactory,
    RotationFactory,
)

__all__ = [
    # User factories
    "AdminFactory",
    "SupervisorFactory",
    "PGFactory",
    "UserFactory",
    # Logbook factories
    "DiagnosisFactory",
    "ProcedureFactory",
    # Case factories
    "CaseCategoryFactory",
    "ClinicalCaseFactory",
    # Certificate factories
    "CertificateTypeFactory",
    "CertificateFactory",
    # Rotation factories
    "HospitalFactory",
    "DepartmentFactory",
    "RotationFactory",
]
