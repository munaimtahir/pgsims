from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from sims.users.models import User, ResidentProfile, SupervisorProfile, AdminProfile
from sims.supervision.models import ResidentSupervisorAssignment
from sims.academics.models import Department, Specialty

class AuditRBACTests(APITestCase):
    def setUp(self):
        self.dept = Department.objects.create(code="TEST", name="Test Dept", active=True)
        self.specialty = Specialty.objects.create(code="MED", name="Medicine")

        # Admin
        self.admin = User.objects.create_user(username="admin_a", password="password", role="ADMIN", specialty=self.specialty)
        AdminProfile.objects.create(user=self.admin)

        # Resident A
        self.res_a = User.objects.create_user(username="res_a", password="password", role="RESIDENT", specialty=self.specialty)
        self.res_prof_a = ResidentProfile.objects.create(user=self.res_a)

        # Resident B
        self.res_b = User.objects.create_user(username="res_b", password="password", role="RESIDENT", specialty=self.specialty)
        self.res_prof_b = ResidentProfile.objects.create(user=self.res_b)

        # Supervisor A
        self.sup_a = User.objects.create_user(username="sup_a", password="password", role="SUPERVISOR", specialty=self.specialty)
        self.sup_prof_a = SupervisorProfile.objects.create(user=self.sup_a)

        # Supervisor B
        self.sup_b = User.objects.create_user(username="sup_b", password="password", role="SUPERVISOR", specialty=self.specialty)
        self.sup_prof_b = SupervisorProfile.objects.create(user=self.sup_b)

        # Assignment: Sup A -> Res A
        ResidentSupervisorAssignment.objects.create(
            resident=self.res_prof_a, supervisor=self.sup_prof_a, assignment_type="PRIMARY",
            start_date="2023-01-01", is_active=True
        )

    def test_resident_cannot_access_other_resident_profile(self):
        self.client.force_authenticate(user=self.res_a)
        url = f"/api/residents/{self.res_prof_b.user_id}/"
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_supervisor_cannot_access_unassigned_resident_profile(self):
        self.client.force_authenticate(user=self.sup_a)
        url = f"/api/residents/{self.res_prof_b.user_id}/"
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_supervisor_can_access_assigned_resident_profile(self):
        self.client.force_authenticate(user=self.sup_a)
        url = f"/api/residents/{self.res_prof_a.user_id}/"
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
