from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from rest_framework.test import APIClient

from sims.academics.models import Department
from sims.rotations.models import Hospital, HospitalDepartment
from sims.users.models import HODAssignment, SupervisorResidentLink, User


class UserbasePermissionAndConstraintTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(
            username="admin_userbase",
            password="pass12345",
            role="admin",
            email="admin_userbase@example.com",
        )
        self.utrmc_admin = User.objects.create_user(
            username="utrmc_admin_userbase",
            password="pass12345",
            role="utrmc_admin",
            email="utrmc_admin_userbase@example.com",
        )
        self.supervisor = User.objects.create_user(
            username="supervisor_userbase",
            password="pass12345",
            role="supervisor",
            specialty="medicine",
            email="supervisor_userbase@example.com",
        )
        self.faculty = User.objects.create_user(
            username="faculty_userbase",
            password="pass12345",
            role="faculty",
            specialty="medicine",
            email="faculty_userbase@example.com",
        )
        self.resident = User.objects.create_user(
            username="resident_userbase",
            password="pass12345",
            role="resident",
            specialty="medicine",
            year="1",
            email="resident_userbase@example.com",
        )
        self.department = Department.objects.create(name="Medicine Userbase", code="MED-UB")
        self.hospital = Hospital.objects.create(name="Hospital Userbase", code="HOSP-UB")
        self.hospital_department = HospitalDepartment.objects.create(
            hospital=self.hospital,
            department=self.department,
        )

    def test_resident_cannot_create_departments(self):
        self.client.force_authenticate(self.resident)
        response = self.client.post(
            "/api/departments/",
            {"name": "Blocked Department", "code": "BLK", "active": True},
            format="json",
        )
        self.assertEqual(response.status_code, 403)

    def test_supervisor_cannot_create_users(self):
        self.client.force_authenticate(self.supervisor)
        response = self.client.post(
            "/api/users/",
            {
                "username": "blocked_user_create",
                "email": "blocked_user_create@example.com",
                "password": "Pass123456!",
                "first_name": "Blocked",
                "last_name": "User",
                "role": "resident",
                "specialty": "medicine",
                "year": "1",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 403)

    def test_utrmc_admin_can_create_supervision_link(self):
        self.client.force_authenticate(self.utrmc_admin)
        response = self.client.post(
            "/api/supervision-links/",
            {
                "supervisor_user_id": self.faculty.id,
                "resident_user_id": self.resident.id,
                "department_id": self.department.id,
                "start_date": date.today().isoformat(),
                "active": True,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["supervisor_user"]["id"], self.faculty.id)
        self.assertEqual(response.data["resident_user"]["id"], self.resident.id)

    def test_hod_assignment_allows_only_one_active_per_department(self):
        HODAssignment.objects.create(
            department=self.department,
            hod_user=self.faculty,
            start_date=date.today(),
            active=True,
            created_by=self.admin,
            updated_by=self.admin,
        )
        with self.assertRaises(ValidationError):
            HODAssignment.objects.create(
                department=self.department,
                hod_user=self.supervisor,
                start_date=date.today() + timedelta(days=1),
                active=True,
                created_by=self.admin,
                updated_by=self.admin,
            )

    def test_hospital_department_pair_is_unique(self):
        with self.assertRaises(IntegrityError):
            HospitalDepartment.objects.create(hospital=self.hospital, department=self.department)

    def test_supervision_link_role_constraints(self):
        with self.assertRaises(ValidationError):
            SupervisorResidentLink.objects.create(
                supervisor_user=self.resident,
                resident_user=self.supervisor,
                department=self.department,
                start_date=date.today(),
                active=True,
                created_by=self.admin,
                updated_by=self.admin,
            )
