from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from sims.academics.models import Department
from sims.rotations.models import Hospital, HospitalDepartment, Rotation
from sims.rotations.services import validate_rotation_override_requirements

User = get_user_model()


class CanonicalRotationModelTests(TestCase):
    def setUp(self):
        self.supervisor = User.objects.create_user(
            username="sup",
            password="pass",
            role="supervisor",
            email="sup@example.com",
            specialty="medicine",
        )
        self.utrmc_admin = User.objects.create_user(
            username="uadmin",
            password="pass",
            role="utrmc_admin",
            email="uadmin@example.com",
        )
        self.home_hospital = Hospital.objects.create(name="Home", code="HOME")
        self.other_hospital = Hospital.objects.create(name="Other", code="OTHER")
        self.medicine = Department.objects.create(name="Medicine", code="MED")
        self.surgery = Department.objects.create(name="Surgery", code="SURG")
        HospitalDepartment.objects.create(hospital=self.home_hospital, department=self.medicine)
        HospitalDepartment.objects.create(hospital=self.other_hospital, department=self.medicine)
        HospitalDepartment.objects.create(hospital=self.other_hospital, department=self.surgery)

        self.pg = User.objects.create_user(
            username="pg",
            password="pass",
            role="pg",
            email="pg@example.com",
            specialty="medicine",
            year="1",
            supervisor=self.supervisor,
            home_hospital=self.home_hospital,
            home_department=self.medicine,
        )

    def test_rotation_requires_hospital_department_matrix_match(self):
        rotation = Rotation(
            pg=self.pg,
            department=self.surgery,
            hospital=self.home_hospital,
            supervisor=self.supervisor,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30),
        )
        with self.assertRaises(ValidationError):
            rotation.full_clean()

    def test_rotation_allows_hosted_department(self):
        rotation = Rotation.objects.create(
            pg=self.pg,
            department=self.medicine,
            hospital=self.home_hospital,
            supervisor=self.supervisor,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30),
            status="planned",
        )
        self.assertEqual(rotation.department, self.medicine)

    def test_override_policy_validator_requires_utrmc_admin_when_available_at_home(self):
        with self.assertRaisesMessage(ValueError, "override_reason"):
            validate_rotation_override_requirements(
                self.pg, self.other_hospital, self.medicine, "", None
            )
        with self.assertRaisesMessage(ValueError, "utrmc_admin"):
            validate_rotation_override_requirements(
                self.pg, self.other_hospital, self.medicine, "Need exposure", "supervisor"
            )
        decision = validate_rotation_override_requirements(
            self.pg, self.other_hospital, self.medicine, "Need exposure", "utrmc_admin"
        )
        self.assertTrue(decision.requires_utrmc_approval)
