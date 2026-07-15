from django.test import TestCase
from django.contrib.auth import get_user_model
from sims.supervision.models import ResidentSupervisorAssignment
from sims.users.models import (
    User, DepartmentMembership, SupervisorProfile, ResidentProfile
)
from sims.academics.models import Department
from datetime import date, timedelta

User = get_user_model()

class UsersModelsTests(TestCase):
    def setUp(self):
        self.dept = Department.objects.create(name="Medicine", code="MED")
        self.user = User.objects.create_user(username="testuser", email="test@test.com", role="RESIDENT")
        self.supervisor = User.objects.create_user(username="sup", role="SUPERVISOR")

    def test_user_display_name(self):
        self.user.first_name = "Test"
        self.user.last_name = "User"
        self.assertEqual(self.user.get_display_name(), "Test User")
        
        self.user.first_name = ""
        self.user.last_name = ""
        self.assertEqual(self.user.get_display_name(), "testuser")

    def test_is_roles(self):
        self.user.role = "RESIDENT"
        self.assertTrue(self.user.is_pg())
        self.assertFalse(self.user.is_supervisor())
        
        self.user.role = "SUPERVISOR"
        self.assertTrue(self.user.is_supervisor())
        
        self.user.role = "ADMIN"
        self.assertTrue(self.user.is_admin())

    def test_department_membership(self):
        # Manually set home_department as it's a separate field in this model
        self.user.home_department = self.dept
        self.user.save()
        
        membership = DepartmentMembership.objects.create(
            user=self.user, department=self.dept,
            member_type=DepartmentMembership.MEMBER_RESIDENT,
            start_date=date.today()
        )
        self.assertEqual(self.user.home_department, self.dept)
        self.assertTrue(membership.active)

    def test_hod_assignment(self):
        assignment = SupervisorProfile.objects.create(
            user=self.supervisor,
            designation_ref="HOD",
            department_ref=self.dept,
        )
        self.assertEqual(assignment.user, self.supervisor)
        self.assertEqual(assignment.designation_ref, "HOD")

    def test_resident_supervisor_assignment(self):
        self.user.supervisor = self.supervisor
        self.user.save()

        resident_profile = ResidentProfile.objects.create(user=self.user, department_ref=self.dept)
        supervisor_profile = SupervisorProfile.objects.create(user=self.supervisor, department_ref=self.dept)
        assignment = ResidentSupervisorAssignment.objects.create(
            supervisor=supervisor_profile,
            resident=resident_profile,
            assignment_type=ResidentSupervisorAssignment.ASSIGNMENT_PRIMARY,
            start_date=date.today(),
            is_active=True,
            status=ResidentSupervisorAssignment.STATUS_ACTIVE,
        )
        self.assertEqual(self.user.supervisor, self.supervisor)
        self.assertEqual(assignment.resident.user, self.user)
        self.assertIn(self.user, self.supervisor.get_assigned_pgs())

    def test_user_archive(self):
        self.user.is_archived = True
        self.user.save()
        self.assertIsNotNone(self.user.archived_date)
