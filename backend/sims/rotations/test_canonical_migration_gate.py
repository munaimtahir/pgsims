from datetime import date, timedelta

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from sims.academics.models import Department
from sims.rotations.models import Hospital, HospitalDepartment, Rotation
from sims.rotations.services import evaluate_rotation_override_policy
from sims.users.models import User


class CanonicalRotationMigrationGateTests(TestCase):
    """Migration gate tests for Hospital/Department/Rotation canonical model."""

    def setUp(self):
        self.client = APIClient()

        self.supervisor = User.objects.create_user(
            username="sup_gate",
            password="pass",
            role="supervisor",
            email="sup_gate@example.com",
            specialty="surgery",
        )
        self.utrmc_user = User.objects.create_user(
            username="utrmc_reader_gate",
            password="pass",
            role="utrmc_user",
            email="utrmc_reader_gate@example.com",
        )
        self.utrmc_admin = User.objects.create_user(
            username="utrmc_admin_gate",
            password="pass",
            role="utrmc_admin",
            email="utrmc_admin_gate@example.com",
        )

        self.home_hospital = Hospital.objects.create(name="Home Hospital", code="HH")
        self.external_hospital = Hospital.objects.create(name="External Hospital", code="EH")

        self.surgery = Department.objects.create(name="Surgery", code="SURG")
        self.medicine = Department.objects.create(name="Medicine", code="MED")

        HospitalDepartment.objects.create(hospital=self.home_hospital, department=self.surgery)

        self.pg = User.objects.create_user(
            username="pg_gate",
            password="pass",
            role="pg",
            email="pg_gate@example.com",
            specialty="surgery",
            year="1",
            supervisor=self.supervisor,
            home_hospital=self.home_hospital,
            home_department=self.surgery,
        )

    def _make_rotation(self, *, department, hospital, override_reason=None):
        return Rotation.objects.create(
            pg=self.pg,
            department=department,
            hospital=hospital,
            supervisor=self.supervisor,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30),
            status="planned",
            override_reason=override_reason,
        )

    def test_migration_gate_inter_hospital_same_department_requires_override_and_utrmc_approval(self):
        rotation = self._make_rotation(department=self.surgery, hospital=self.external_hospital)

        policy = evaluate_rotation_override_policy(rotation.pg, rotation.hospital, rotation.department)
        self.assertTrue(policy.requires_utrmc_approval)

        self.client.force_authenticate(self.utrmc_user)
        url = reverse("rotations_api:utrmc_approve", kwargs={"pk": rotation.id})
        denied = self.client.patch(url, {"override_reason": "Read-only cannot approve"}, format="json")
        self.assertEqual(denied.status_code, 403)

        self.client.force_authenticate(self.utrmc_admin)
        response = self.client.patch(
            url,
            {"override_reason": "Home department exception approved by UTRMC"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["requires_utrmc_approval"])

        rotation.refresh_from_db()
        self.assertEqual(rotation.utrmc_approved_by, self.utrmc_admin)
        self.assertIsNotNone(rotation.utrmc_approved_at)

    def test_migration_gate_deficiency_rule_no_utrmc_approval_required(self):
        rotation = self._make_rotation(
            department=self.medicine,
            hospital=self.external_hospital,
            override_reason=None,
        )

        policy = evaluate_rotation_override_policy(rotation.pg, rotation.hospital, rotation.department)
        self.assertFalse(policy.requires_utrmc_approval)

    def test_rotation_summary_api_returns_contract_shape(self):
        rotation = self._make_rotation(
            department=self.surgery,
            hospital=self.external_hospital,
            override_reason="Awaiting approval",
        )
        self.client.force_authenticate(self.pg)
        response = self.client.get(reverse("rotations_api:my_rotation_detail", kwargs={"pk": rotation.id}))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data["department"], dict)
        self.assertIn("name", response.data["department"])
        self.assertIsInstance(response.data["hospital"], dict)
        self.assertIn("requires_utrmc_approval", response.data)
