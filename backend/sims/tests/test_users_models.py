from django.test import TestCase
from django.contrib.auth import get_user_model
from sims.users.models import (
    User, DepartmentMembership, SupervisorResidentLink, SupervisorProfile
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

    def test_supervisor_resident_link(self):
        self.user.supervisor = self.supervisor
        self.user.save()
        
        link = SupervisorResidentLink.objects.create(
            supervisor_user=self.supervisor, resident_user=self.user,
            start_date=date.today()
        )
        self.assertEqual(self.user.supervisor, self.supervisor)
        self.assertIn(self.user, self.supervisor.get_assigned_pgs())

    def test_user_archive(self):
        self.user.is_archived = True
        self.user.save()
        self.assertIsNotNone(self.user.archived_date)
