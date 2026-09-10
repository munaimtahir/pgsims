from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from sims.users.models import User, ResidentProfile, SupervisorProfile, AdminProfile
from sims.supervision.models import ResidentSupervisorAssignment
from sims.academics.models import Department, Specialty
from django.db.utils import IntegrityError

class AuditRelationshipTests(APITestCase):
    def setUp(self):
        self.dept = Department.objects.create(code="TEST", name="Test Dept", active=True)
        self.specialty = Specialty.objects.create(code="MED", name="Medicine")

        # Resident A
        self.res_a = User.objects.create_user(username="res_a", password="password", role="RESIDENT", specialty=self.specialty)
        self.res_prof_a = ResidentProfile.objects.create(user=self.res_a)

        # Supervisor A
        self.sup_a = User.objects.create_user(username="sup_a", password="password", role="SUPERVISOR", specialty=self.specialty)
        self.sup_prof_a = SupervisorProfile.objects.create(user=self.sup_a)

        self.assignment = ResidentSupervisorAssignment.objects.create(
            resident=self.res_prof_a, supervisor=self.sup_prof_a, assignment_type="PRIMARY",
            start_date="2023-01-01", is_active=True
        )

    def test_duplicate_primary_assignment_fails(self):
        with self.assertRaises(IntegrityError):
            ResidentSupervisorAssignment.objects.create(
                resident=self.res_prof_a, supervisor=self.sup_prof_a, assignment_type="PRIMARY",
                start_date="2023-02-01", is_active=True
            )
