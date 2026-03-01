"""
Canonical migration gate tests for Hospital/Department/Rotation domain logic.
"""
from django.test import TestCase
from rest_framework.test import APIClient

from sims.academics.models import Department
from sims.rotations.models import Hospital, HospitalDepartment
from sims.rotations.services import evaluate_rotation_override_policy
from sims.users.models import User


class CanonicalRotationMigrationGateTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.supervisor = User.objects.create_user(
            username="sup_gate", password="pass", role="supervisor",
            email="sup_gate@example.com", specialty="surgery",
        )
        self.home_hospital = Hospital.objects.create(name="Home Hospital", code="HH")
        self.external_hospital = Hospital.objects.create(name="External Hospital", code="EH")
        self.surgery = Department.objects.create(name="Surgery", code="SURG")
        self.medicine = Department.objects.create(name="Medicine", code="MED")
        HospitalDepartment.objects.create(hospital=self.home_hospital, department=self.surgery)
        self.pg = User.objects.create_user(
            username="pg_gate", password="pass", role="pg",
            email="pg_gate@example.com", specialty="surgery", year="1",
            supervisor=self.supervisor,
            home_hospital=self.home_hospital,
            home_department=self.surgery,
        )

    def test_migration_gate_inter_hospital_same_department_requires_utrmc_approval(self):
        policy = evaluate_rotation_override_policy(self.pg, self.external_hospital, self.surgery)
        self.assertTrue(policy.requires_utrmc_approval)

    def test_migration_gate_deficiency_rule_no_utrmc_approval_required(self):
        policy = evaluate_rotation_override_policy(self.pg, self.external_hospital, self.medicine)
        self.assertFalse(policy.requires_utrmc_approval)
