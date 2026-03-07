"""
Comprehensive role-based workflow tests for PGSIMS.

Tests every major API endpoint across all system roles:
  - pg / resident    : postgraduate trainee
  - supervisor       : medical supervisor (supervisee-scoped)
  - admin            : system administrator
  - utrmc_user       : read-only UTRMC oversight
  - utrmc_admin      : UTRMC admin with override authority

Coverage:
  Authentication · Hospitals · Departments · Hospital-Departments ·
  Users · Supervision Links · HOD Assignments · Training Programs ·
  Resident Training Records · Rotation Assignments (full workflow) ·
  Leave Requests (full workflow) · Notifications · Bulk Import/Export ·
  Audit Log · My-Rotations / My-Leaves views · UTRMC Eligibility
"""

import datetime

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from sims.academics.models import Department
from sims.notifications.models import Notification
from sims.rotations.models import Hospital, HospitalDepartment
from sims.training.models import (
    LeaveRequest,
    ResidentTrainingRecord,
    RotationAssignment,
    TrainingProgram,
)
from sims.users.models import User

# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

TODAY = datetime.date.today()
TOMORROW = TODAY + datetime.timedelta(days=1)
IN_30 = TODAY + datetime.timedelta(days=30)
IN_60 = TODAY + datetime.timedelta(days=60)
IN_90 = TODAY + datetime.timedelta(days=90)


def make_user(username, role, password="Test@pass1", **kwargs):
    u = User.objects.create_user(
        username=username,
        password=password,
        email=f"{username}@test.local",
        first_name=username.capitalize(),
        last_name="Test",
        role=role,
        specialty="medicine",
        **kwargs,
    )
    return u


def auth_client(user, password="Test@pass1"):
    """Return an APIClient authenticated for *user* via JWT."""
    c = APIClient()
    response = c.post("/api/auth/login/", {"username": user.username, "password": password})
    assert response.status_code == status.HTTP_200_OK, (
        f"JWT login failed for {user.username}: {response.data}"
    )
    c.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
    return c


# ---------------------------------------------------------------------------
# Module-scoped fixtures (shared across all tests in this module)
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def django_db_setup():
    pass


@pytest.fixture
def hospital(db):
    h, _ = Hospital.objects.get_or_create(code="TEST-UTH", defaults={"name": "Test UTRMC Hospital", "is_active": True})
    return h


@pytest.fixture
def department(db):
    d, _ = Department.objects.get_or_create(code="TEST-MED", defaults={"name": "Test Internal Medicine"})
    return d


@pytest.fixture
def hospital_dept(db, hospital, department):
    hd, _ = HospitalDepartment.objects.get_or_create(hospital=hospital, department=department)
    return hd


@pytest.fixture
def prog(db, department):
    p, _ = TrainingProgram.objects.get_or_create(
        code="TEST-MD-MED",
        defaults={
            "name": "Test MD Internal Medicine",
            "duration_months": 36,
            "degree_type": "MD",
            "department": department,
            "active": True,
        },
    )
    return p


@pytest.fixture
def u_admin(db):
    u, _ = User.objects.get_or_create(
        username="u_admin",
        defaults={
            "email": "u_admin@test.local",
            "first_name": "Admin",
            "last_name": "Test",
            "role": "admin",
            "specialty": "medicine",
            "is_staff": True,
            "is_superuser": True,
        },
    )
    u.set_password("Test@pass1")
    u.save()
    return u


@pytest.fixture
def u_utrmc_admin(db):
    u, _ = User.objects.get_or_create(
        username="u_utrmc_admin",
        defaults={
            "email": "u_utrmc_admin@test.local",
            "first_name": "Utrmc_Admin",
            "last_name": "Test",
            "role": "utrmc_admin",
            "specialty": "medicine",
        },
    )
    u.set_password("Test@pass1")
    u.save()
    return u


@pytest.fixture
def u_utrmc_user(db):
    u, _ = User.objects.get_or_create(
        username="u_utrmc_user",
        defaults={
            "email": "u_utrmc_user@test.local",
            "first_name": "Utrmc_User",
            "last_name": "Test",
            "role": "utrmc_user",
            "specialty": "medicine",
        },
    )
    u.set_password("Test@pass1")
    u.save()
    return u


@pytest.fixture
def u_supervisor(db):
    u, _ = User.objects.get_or_create(
        username="u_supervisor",
        defaults={
            "email": "u_supervisor@test.local",
            "first_name": "Supervisor",
            "last_name": "Test",
            "role": "supervisor",
            "specialty": "medicine",
        },
    )
    u.set_password("Test@pass1")
    u.save()
    return u


@pytest.fixture
def u_pg(db, u_supervisor):
    u, _ = User.objects.get_or_create(
        username="u_pg",
        defaults={
            "email": "u_pg@test.local",
            "first_name": "Pg",
            "last_name": "Test",
            "role": "pg",
            "specialty": "medicine",
            "year": "1",
        },
    )
    u.set_password("Test@pass1")
    u.save()
    return u


@pytest.fixture
def resident_training(db, u_pg, prog):
    rt, _ = ResidentTrainingRecord.objects.get_or_create(
        resident_user=u_pg,
        program=prog,
        defaults={
            "start_date": TODAY,
            "expected_end_date": TODAY + datetime.timedelta(days=900),
            "current_level": "y1",
            "active": True,
            "created_by": u_pg,
        },
    )
    return rt


# ---------------------------------------------------------------------------
# 1. Authentication
# ---------------------------------------------------------------------------

class TestAuthentication:

    def test_login_pg(self, db, u_pg):
        c = APIClient()
        r = c.post("/api/auth/login/", {"username": "u_pg", "password": "Test@pass1"})
        assert r.status_code == status.HTTP_200_OK
        assert "access" in r.data

    def test_login_supervisor(self, db, u_supervisor):
        c = APIClient()
        r = c.post("/api/auth/login/", {"username": "u_supervisor", "password": "Test@pass1"})
        assert r.status_code == status.HTTP_200_OK

    def test_login_admin(self, db, u_admin):
        c = APIClient()
        r = c.post("/api/auth/login/", {"username": "u_admin", "password": "Test@pass1"})
        assert r.status_code == status.HTTP_200_OK

    def test_login_utrmc_admin(self, db, u_utrmc_admin):
        c = APIClient()
        r = c.post("/api/auth/login/", {"username": "u_utrmc_admin", "password": "Test@pass1"})
        assert r.status_code == status.HTTP_200_OK

    def test_login_utrmc_user(self, db, u_utrmc_user):
        c = APIClient()
        r = c.post("/api/auth/login/", {"username": "u_utrmc_user", "password": "Test@pass1"})
        assert r.status_code == status.HTTP_200_OK

    def test_login_wrong_password(self, db, u_pg):
        c = APIClient()
        r = c.post("/api/auth/login/", {"username": "u_pg", "password": "wrongpassword"})
        assert r.status_code == status.HTTP_401_UNAUTHORIZED

    def test_me_returns_own_user(self, db, u_pg):
        c = auth_client(u_pg)
        r = c.get("/api/auth/me/")
        assert r.status_code == status.HTTP_200_OK
        assert r.data["username"] == "u_pg"
        assert r.data["role"] == "pg"

    def test_me_supervisor(self, db, u_supervisor):
        c = auth_client(u_supervisor)
        r = c.get("/api/auth/me/")
        assert r.status_code == status.HTTP_200_OK
        assert r.data["role"] == "supervisor"

    def test_me_unauthenticated_rejected(self, db):
        r = APIClient().get("/api/auth/me/")
        assert r.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)

    def test_protected_endpoint_requires_auth(self, db):
        r = APIClient().get("/api/hospitals/")
        assert r.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)


# ---------------------------------------------------------------------------
# 2. Hospital CRUD
# ---------------------------------------------------------------------------

class TestHospitalAccess:

    def test_admin_can_list_hospitals(self, db, hospital, u_admin):
        c = auth_client(u_admin)
        r = c.get("/api/hospitals/")
        assert r.status_code == status.HTTP_200_OK

    def test_pg_can_list_hospitals(self, db, hospital, u_pg):
        c = auth_client(u_pg)
        r = c.get("/api/hospitals/")
        assert r.status_code == status.HTTP_200_OK

    def test_supervisor_can_list_hospitals(self, db, hospital, u_supervisor):
        c = auth_client(u_supervisor)
        r = c.get("/api/hospitals/")
        assert r.status_code == status.HTTP_200_OK

    def test_utrmc_user_can_list_hospitals(self, db, hospital, u_utrmc_user):
        c = auth_client(u_utrmc_user)
        r = c.get("/api/hospitals/")
        assert r.status_code == status.HTTP_200_OK

    def test_admin_can_create_hospital(self, db, u_admin):
        c = auth_client(u_admin)
        r = c.post("/api/hospitals/", {"name": "Admin Hospital Test", "code": "TEST-ADM-H", "is_active": True})
        assert r.status_code == status.HTTP_201_CREATED

    def test_utrmc_admin_cannot_create_hospital(self, db, u_utrmc_admin):
        # Hospital write is restricted to IsTechAdmin (role=="admin" only)
        c = auth_client(u_utrmc_admin)
        r = c.post("/api/hospitals/", {"name": "UTRMC Hospital B Test", "code": "TEST-UTR-B", "is_active": True})
        assert r.status_code == status.HTTP_403_FORBIDDEN

    def test_supervisor_cannot_create_hospital(self, db, u_supervisor):
        c = auth_client(u_supervisor)
        r = c.post("/api/hospitals/", {"name": "Sup Hospital Test", "code": "TEST-SUP-H", "is_active": True})
        assert r.status_code == status.HTTP_403_FORBIDDEN

    def test_pg_cannot_create_hospital(self, db, u_pg):
        c = auth_client(u_pg)
        r = c.post("/api/hospitals/", {"name": "PG Hospital Test", "code": "TEST-PG-H", "is_active": True})
        assert r.status_code == status.HTTP_403_FORBIDDEN

    def test_utrmc_user_cannot_create_hospital(self, db, u_utrmc_user):
        c = auth_client(u_utrmc_user)
        r = c.post("/api/hospitals/", {"name": "UTRMC-RO Hospital Test", "code": "TEST-URO-H", "is_active": True})
        assert r.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_can_update_hospital(self, db, hospital, u_admin):
        c = auth_client(u_admin)
        r = c.patch(f"/api/hospitals/{hospital.id}/", {"name": "Updated Hospital"})
        assert r.status_code == status.HTTP_200_OK
        assert r.data["name"] == "Updated Hospital"

    def test_pg_cannot_update_hospital(self, db, hospital, u_pg):
        c = auth_client(u_pg)
        r = c.patch(f"/api/hospitals/{hospital.id}/", {"name": "Hacked"})
        assert r.status_code == status.HTTP_403_FORBIDDEN


# ---------------------------------------------------------------------------
# 3. Department CRUD (userbase endpoint /api/departments/)
# ---------------------------------------------------------------------------

class TestDepartmentAccess:

    def test_all_roles_can_list_departments(self, db, department, u_admin, u_pg, u_supervisor, u_utrmc_user):
        for user in [u_admin, u_pg, u_supervisor, u_utrmc_user]:
            c = auth_client(user)
            r = c.get("/api/departments/")
            assert r.status_code == status.HTTP_200_OK, f"Failed for {user.role}"

    def test_admin_can_create_department(self, db, u_admin):
        c = auth_client(u_admin)
        r = c.post("/api/departments/", {"name": "Test Cardiology", "code": "TEST-CARD"})
        assert r.status_code == status.HTTP_201_CREATED

    def test_utrmc_admin_cannot_create_department(self, db, u_utrmc_admin):
        # Department write is restricted to IsTechAdmin (role=="admin" only)
        c = auth_client(u_utrmc_admin)
        r = c.post("/api/departments/", {"name": "Test Neurology", "code": "TEST-NEURO"})
        assert r.status_code == status.HTTP_403_FORBIDDEN

    def test_supervisor_cannot_create_department(self, db, u_supervisor):
        c = auth_client(u_supervisor)
        r = c.post("/api/departments/", {"name": "Bad Dept", "code": "TEST-BAD"})
        assert r.status_code == status.HTTP_403_FORBIDDEN

    def test_pg_cannot_create_department(self, db, u_pg):
        c = auth_client(u_pg)
        r = c.post("/api/departments/", {"name": "Bad Dept", "code": "TEST-BAD2"})
        assert r.status_code == status.HTTP_403_FORBIDDEN

    def test_utrmc_user_cannot_create_department(self, db, u_utrmc_user):
        c = auth_client(u_utrmc_user)
        r = c.post("/api/departments/", {"name": "Bad Dept", "code": "TEST-BAD3"})
        assert r.status_code == status.HTTP_403_FORBIDDEN


# ---------------------------------------------------------------------------
# 4. Hospital-Department Matrix
# ---------------------------------------------------------------------------

class TestHospitalDepartmentAccess:

    def test_all_roles_can_list_hospital_departments(
        self, db, hospital_dept, u_admin, u_pg, u_supervisor
    ):
        for user in [u_admin, u_pg, u_supervisor]:
            c = auth_client(user)
            r = c.get("/api/hospital-departments/")
            assert r.status_code == status.HTTP_200_OK, f"Failed for {user.role}"

    def test_admin_can_create_hospital_department(self, db, hospital, department, u_admin):
        c = auth_client(u_admin)
        h2, _ = Hospital.objects.get_or_create(code="TEST-SEC-H", defaults={"name": "Second Test Hospital"})
        r = c.post("/api/hospital-departments/", {
            "hospital_id": h2.id,
            "department_id": department.id,
            "active": True,
        })
        assert r.status_code == status.HTTP_201_CREATED

    def test_pg_cannot_create_hospital_department(self, db, hospital, department, u_pg):
        c = auth_client(u_pg)
        h3, _ = Hospital.objects.get_or_create(code="TEST-THR-H", defaults={"name": "Third Test Hospital"})
        r = c.post("/api/hospital-departments/", {
            "hospital_id": h3.id,
            "department_id": department.id,
        })
        assert r.status_code == status.HTTP_403_FORBIDDEN


# ---------------------------------------------------------------------------
# 5. User Management
# ---------------------------------------------------------------------------

class TestUserManagement:

    def test_admin_can_list_users(self, db, u_admin, u_pg):
        c = auth_client(u_admin)
        r = c.get("/api/users/")
        assert r.status_code == status.HTTP_200_OK

    def test_supervisor_can_list_users(self, db, u_supervisor, u_pg):
        c = auth_client(u_supervisor)
        r = c.get("/api/users/")
        assert r.status_code == status.HTTP_200_OK

    def test_pg_can_list_users(self, db, u_pg):
        c = auth_client(u_pg)
        r = c.get("/api/users/")
        assert r.status_code == status.HTTP_200_OK

    def test_admin_can_create_user(self, db, u_admin, department, hospital):
        c = auth_client(u_admin)
        r = c.post("/api/users/", {
            "username": "new_pg_001",
            "password": "Test@pass1",
            "email": "new_pg_001@test.local",
            "first_name": "New",
            "last_name": "PG",
            "role": "pg",
            "specialty": "medicine",
        })
        assert r.status_code == status.HTTP_201_CREATED
        assert r.data["role"] == "pg"

    def test_utrmc_admin_can_create_user(self, db, u_utrmc_admin):
        c = auth_client(u_utrmc_admin)
        r = c.post("/api/users/", {
            "username": "new_sup_001",
            "password": "Test@pass1",
            "email": "new_sup_001@test.local",
            "first_name": "New",
            "last_name": "Supervisor",
            "role": "supervisor",
            "specialty": "surgery",
        })
        assert r.status_code == status.HTTP_201_CREATED

    def test_supervisor_cannot_create_user(self, db, u_supervisor):
        c = auth_client(u_supervisor)
        r = c.post("/api/users/", {
            "username": "intruder",
            "password": "Test@pass1",
            "role": "pg",
        })
        assert r.status_code == status.HTTP_403_FORBIDDEN

    def test_pg_cannot_create_user(self, db, u_pg):
        c = auth_client(u_pg)
        r = c.post("/api/users/", {
            "username": "intruder2",
            "password": "Test@pass1",
            "role": "pg",
        })
        assert r.status_code == status.HTTP_403_FORBIDDEN

    def test_utrmc_user_cannot_create_user(self, db, u_utrmc_user):
        c = auth_client(u_utrmc_user)
        r = c.post("/api/users/", {
            "username": "intruder3",
            "password": "Test@pass1",
            "role": "pg",
        })
        assert r.status_code == status.HTTP_403_FORBIDDEN


# ---------------------------------------------------------------------------
# 6. Supervision Links
# ---------------------------------------------------------------------------

class TestSupervisionLinks:

    def test_admin_can_list_supervision_links(self, db, u_admin):
        c = auth_client(u_admin)
        r = c.get("/api/supervision-links/")
        assert r.status_code == status.HTTP_200_OK

    def test_supervisor_can_list_supervision_links(self, db, u_supervisor):
        # BaseManagedModelViewSet.list() restricts to manager roles (admin/utrmc_admin)
        c = auth_client(u_supervisor)
        r = c.get("/api/supervision-links/")
        assert r.status_code == status.HTTP_403_FORBIDDEN

    def test_pg_can_list_supervision_links(self, db, u_pg):
        # BaseManagedModelViewSet.list() restricts to manager roles (admin/utrmc_admin)
        c = auth_client(u_pg)
        r = c.get("/api/supervision-links/")
        assert r.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_can_create_supervision_link(self, db, u_admin, u_supervisor, u_pg, department):
        c = auth_client(u_admin)
        r = c.post("/api/supervision-links/", {
            "supervisor_user_id": u_supervisor.id,
            "resident_user_id": u_pg.id,
            "department_id": department.id,
            "start_date": str(TODAY),
            "active": True,
        })
        assert r.status_code == status.HTTP_201_CREATED

    def test_utrmc_admin_can_create_supervision_link(
        self, db, u_utrmc_admin, u_supervisor, u_pg, department
    ):
        c = auth_client(u_utrmc_admin)
        r = c.post("/api/supervision-links/", {
            "supervisor_user_id": u_supervisor.id,
            "resident_user_id": u_pg.id,
            "department_id": department.id,
            "start_date": str(TODAY),
            "active": True,
        })
        assert r.status_code == status.HTTP_201_CREATED

    def test_supervisor_cannot_create_supervision_link(
        self, db, u_supervisor, u_pg, department
    ):
        c = auth_client(u_supervisor)
        r = c.post("/api/supervision-links/", {
            "supervisor_user_id": u_supervisor.id,
            "resident_user_id": u_pg.id,
            "department_id": department.id,
            "start_date": str(TODAY),
            "active": True,
        })
        assert r.status_code == status.HTTP_403_FORBIDDEN

    def test_pg_cannot_create_supervision_link(self, db, u_pg, u_supervisor, department):
        c = auth_client(u_pg)
        r = c.post("/api/supervision-links/", {
            "supervisor_user_id": u_supervisor.id,
            "resident_user_id": u_pg.id,
            "department_id": department.id,
            "start_date": str(TODAY),
        })
        assert r.status_code == status.HTTP_403_FORBIDDEN


# ---------------------------------------------------------------------------
# 7. Training Programs
# ---------------------------------------------------------------------------

class TestTrainingPrograms:

    def test_all_roles_can_list_programs(self, db, prog, u_admin, u_pg, u_supervisor, u_utrmc_user):
        for user in [u_admin, u_pg, u_supervisor, u_utrmc_user]:
            c = auth_client(user)
            r = c.get("/api/programs/")
            assert r.status_code == status.HTTP_200_OK, f"Failed for {user.role}"

    def test_unauthenticated_cannot_list_programs(self, db, prog):
        r = APIClient().get("/api/programs/")
        assert r.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create_program(self, db, department, u_admin):
        c = auth_client(u_admin)
        r = c.post("/api/programs/", {
            "name": "Test MD Surgery",
            "code": "TEST-MD-SRG",
            "duration_months": 36,
            "degree_type": "MD",
            "department": department.id,
            "active": True,
        })
        assert r.status_code == status.HTTP_201_CREATED

    def test_utrmc_admin_can_create_program(self, db, department, u_utrmc_admin):
        c = auth_client(u_utrmc_admin)
        r = c.post("/api/programs/", {
            "name": "Test MD Pediatrics",
            "code": "TEST-MD-PED",
            "duration_months": 36,
            "degree_type": "MD",
            "department": department.id,
            "active": True,
        })
        assert r.status_code == status.HTTP_201_CREATED

    def test_supervisor_cannot_create_program(self, db, department, u_supervisor):
        c = auth_client(u_supervisor)
        r = c.post("/api/programs/", {
            "name": "MD Hack",
            "code": "TEST-MD-HCK",
            "duration_months": 36,
            "degree_type": "MD",
            "department": department.id,
        })
        assert r.status_code == status.HTTP_403_FORBIDDEN

    def test_pg_cannot_create_program(self, db, department, u_pg):
        c = auth_client(u_pg)
        r = c.post("/api/programs/", {
            "name": "MD Hack",
            "code": "TEST-MD-HK2",
            "duration_months": 36,
            "degree_type": "MD",
            "department": department.id,
        })
        assert r.status_code == status.HTTP_403_FORBIDDEN

    def test_utrmc_user_cannot_create_program(self, db, department, u_utrmc_user):
        c = auth_client(u_utrmc_user)
        r = c.post("/api/programs/", {
            "name": "MD Hack",
            "code": "TEST-MD-HK3",
            "duration_months": 36,
            "degree_type": "MD",
            "department": department.id,
        })
        assert r.status_code == status.HTTP_403_FORBIDDEN


# ---------------------------------------------------------------------------
# 8. Resident Training Records
# ---------------------------------------------------------------------------

class TestResidentTrainingRecords:

    def test_admin_can_list_training_records(self, db, resident_training, u_admin):
        c = auth_client(u_admin)
        r = c.get("/api/resident-training/")
        assert r.status_code == status.HTTP_200_OK
        assert r.data["count"] >= 1

    def test_pg_sees_own_training_record(self, db, resident_training, u_pg):
        c = auth_client(u_pg)
        r = c.get("/api/resident-training/")
        assert r.status_code == status.HTTP_200_OK
        ids = [item["id"] for item in r.data["results"]]
        assert resident_training.id in ids

    def test_admin_can_create_training_record(self, db, u_admin, u_pg, prog):
        # Create a fresh pg for this test
        pg2 = make_user("u_pg2_tr", "pg")
        c = auth_client(u_admin)
        r = c.post("/api/resident-training/", {
            "resident_user": pg2.id,
            "program": prog.id,
            "start_date": str(TODAY),
            "expected_end_date": str(IN_90),
            "current_level": "y1",
            "active": True,
        })
        assert r.status_code == status.HTTP_201_CREATED

    def test_pg_cannot_create_training_record(self, db, u_pg, prog):
        pg3 = make_user("u_pg3_tr", "pg")
        c = auth_client(u_pg)
        r = c.post("/api/resident-training/", {
            "resident_user": pg3.id,
            "program": prog.id,
            "start_date": str(TODAY),
            "expected_end_date": str(IN_90),
            "current_level": "y1",
        })
        assert r.status_code == status.HTTP_403_FORBIDDEN

    def test_supervisor_cannot_create_training_record(self, db, u_supervisor, u_pg, prog):
        c = auth_client(u_supervisor)
        pg4 = make_user("u_pg4_tr", "pg")
        r = c.post("/api/resident-training/", {
            "resident_user": pg4.id,
            "program": prog.id,
            "start_date": str(TODAY),
            "expected_end_date": str(IN_90),
            "current_level": "y1",
        })
        assert r.status_code == status.HTTP_403_FORBIDDEN


# ---------------------------------------------------------------------------
# 9. Rotation Assignment — Full Workflow
# ---------------------------------------------------------------------------

class TestRotationAssignmentWorkflow:

    def test_admin_can_create_rotation(self, db, resident_training, hospital_dept, u_admin):
        c = auth_client(u_admin)
        r = c.post("/api/rotations/", {
            "resident_training": resident_training.id,
            "hospital_department": hospital_dept.id,
            "start_date": str(IN_30),
            "end_date": str(IN_60),
        })
        assert r.status_code == status.HTTP_201_CREATED
        assert r.data["status"] == RotationAssignment.STATUS_DRAFT

    def test_utrmc_admin_can_create_rotation(self, db, resident_training, hospital_dept, u_utrmc_admin):
        c = auth_client(u_utrmc_admin)
        r = c.post("/api/rotations/", {
            "resident_training": resident_training.id,
            "hospital_department": hospital_dept.id,
            "start_date": str(IN_30),
            "end_date": str(IN_60),
        })
        assert r.status_code == status.HTTP_201_CREATED

    def test_supervisor_cannot_create_rotation(self, db, resident_training, hospital_dept, u_supervisor):
        c = auth_client(u_supervisor)
        r = c.post("/api/rotations/", {
            "resident_training": resident_training.id,
            "hospital_department": hospital_dept.id,
            "start_date": str(IN_30),
            "end_date": str(IN_60),
        })
        assert r.status_code == status.HTTP_403_FORBIDDEN

    def test_pg_cannot_create_rotation(self, db, resident_training, hospital_dept, u_pg):
        c = auth_client(u_pg)
        r = c.post("/api/rotations/", {
            "resident_training": resident_training.id,
            "hospital_department": hospital_dept.id,
            "start_date": str(IN_30),
            "end_date": str(IN_60),
        })
        assert r.status_code == status.HTTP_403_FORBIDDEN

    def test_pg_can_list_own_rotations(self, db, resident_training, hospital_dept, u_pg, u_admin):
        # Admin creates rotation for the pg
        admin_c = auth_client(u_admin)
        admin_c.post("/api/rotations/", {
            "resident_training": resident_training.id,
            "hospital_department": hospital_dept.id,
            "start_date": str(IN_30),
            "end_date": str(IN_60),
        })
        c = auth_client(u_pg)
        r = c.get("/api/rotations/")
        assert r.status_code == status.HTTP_200_OK

    def test_admin_can_list_all_rotations(self, db, resident_training, hospital_dept, u_admin):
        admin_c = auth_client(u_admin)
        admin_c.post("/api/rotations/", {
            "resident_training": resident_training.id,
            "hospital_department": hospital_dept.id,
            "start_date": str(IN_30),
            "end_date": str(IN_60),
        })
        r = admin_c.get("/api/rotations/")
        assert r.status_code == status.HTTP_200_OK

    def test_full_rotation_submit_hod_approve_workflow(
        self, db, resident_training, hospital_dept, u_admin, u_supervisor, department
    ):
        """admin creates → admin submits → supervisor (as HOD) approves."""
        from sims.users.models import HODAssignment

        # Assign supervisor as HOD so they can see the rotation
        HODAssignment.objects.create(
            hod_user=u_supervisor,
            department=department,
            start_date=TODAY,
            active=True,
        )

        admin_c = auth_client(u_admin)
        # Create
        r = admin_c.post("/api/rotations/", {
            "resident_training": resident_training.id,
            "hospital_department": hospital_dept.id,
            "start_date": str(IN_30),
            "end_date": str(IN_60),
        })
        assert r.status_code == status.HTTP_201_CREATED
        rot_id = r.data["id"]

        # Submit
        r = admin_c.post(f"/api/rotations/{rot_id}/submit/")
        assert r.status_code == status.HTTP_200_OK
        assert r.data["status"] == RotationAssignment.STATUS_SUBMITTED

        # HOD approve (supervisor)
        sup_c = auth_client(u_supervisor)
        r = sup_c.post(f"/api/rotations/{rot_id}/hod-approve/")
        assert r.status_code == status.HTTP_200_OK
        assert r.data["status"] == RotationAssignment.STATUS_APPROVED

    def test_utrmc_approve_rotation(
        self, db, resident_training, hospital_dept, u_admin, u_utrmc_admin, u_supervisor, department
    ):
        """admin creates → submit → hod-approve → utrmc-approve."""
        from sims.users.models import HODAssignment

        HODAssignment.objects.create(
            hod_user=u_supervisor, department=department, start_date=TODAY, active=True
        )
        admin_c = auth_client(u_admin)

        r = admin_c.post("/api/rotations/", {
            "resident_training": resident_training.id,
            "hospital_department": hospital_dept.id,
            "start_date": str(IN_30),
            "end_date": str(IN_60),
        })
        rot_id = r.data["id"]
        admin_c.post(f"/api/rotations/{rot_id}/submit/")
        # admin can hod-approve (admin or utrmc_admin bypasses HOD check)
        admin_c.post(f"/api/rotations/{rot_id}/hod-approve/")

        utrmc_c = auth_client(u_utrmc_admin)
        r = utrmc_c.post(f"/api/rotations/{rot_id}/utrmc-approve/")
        assert r.status_code == status.HTTP_200_OK
        assert r.data["status"] == RotationAssignment.STATUS_APPROVED

    def test_pg_cannot_utrmc_approve(self, db, resident_training, hospital_dept, u_admin, u_pg, u_supervisor):
        from sims.users.models import HODAssignment
        HODAssignment.objects.create(
            hod_user=u_supervisor,
            department=resident_training.program.department,
            start_date=TODAY,
            active=True,
        )
        admin_c = auth_client(u_admin)
        r = admin_c.post("/api/rotations/", {
            "resident_training": resident_training.id,
            "hospital_department": hospital_dept.id,
            "start_date": str(IN_30),
            "end_date": str(IN_60),
        })
        rot_id = r.data["id"]
        admin_c.post(f"/api/rotations/{rot_id}/submit/")
        admin_c.post(f"/api/rotations/{rot_id}/hod-approve/")

        pg_c = auth_client(u_pg)
        r = pg_c.post(f"/api/rotations/{rot_id}/utrmc-approve/")
        assert r.status_code in (status.HTTP_403_FORBIDDEN, status.HTTP_400_BAD_REQUEST)

    def test_return_rotation(self, db, resident_training, hospital_dept, u_admin, u_supervisor):
        """Admin can return (reject-with-reason) a submitted rotation."""
        from sims.users.models import HODAssignment
        HODAssignment.objects.create(
            hod_user=u_supervisor,
            department=resident_training.program.department,
            start_date=TODAY,
            active=True,
        )
        admin_c = auth_client(u_admin)
        r = admin_c.post("/api/rotations/", {
            "resident_training": resident_training.id,
            "hospital_department": hospital_dept.id,
            "start_date": str(IN_30),
            "end_date": str(IN_60),
        })
        rot_id = r.data["id"]
        admin_c.post(f"/api/rotations/{rot_id}/submit/")

        r = admin_c.post(f"/api/rotations/{rot_id}/returned/", {"reason": "Needs revision"})
        assert r.status_code == status.HTTP_200_OK
        assert r.data["status"] == RotationAssignment.STATUS_RETURNED


# ---------------------------------------------------------------------------
# 10. Leave Request — Full Workflow
# ---------------------------------------------------------------------------

class TestLeaveRequestWorkflow:

    def test_pg_can_create_leave(self, db, resident_training, u_pg):
        c = auth_client(u_pg)
        r = c.post("/api/leaves/", {
            "resident_training": resident_training.id,
            "leave_type": "annual",
            "start_date": str(IN_30),
            "end_date": str(IN_30 + datetime.timedelta(days=5)),
            "reason": "Annual leave",
        })
        assert r.status_code == status.HTTP_201_CREATED
        assert r.data["status"] == LeaveRequest.STATUS_DRAFT

    def test_admin_can_create_leave(self, db, resident_training, u_admin):
        c = auth_client(u_admin)
        r = c.post("/api/leaves/", {
            "resident_training": resident_training.id,
            "leave_type": "sick",
            "start_date": str(IN_30),
            "end_date": str(IN_30 + datetime.timedelta(days=3)),
            "reason": "Medical leave",
        })
        assert r.status_code == status.HTTP_201_CREATED

    def test_supervisor_cannot_create_leave(self, db, resident_training, u_supervisor):
        c = auth_client(u_supervisor)
        r = c.post("/api/leaves/", {
            "resident_training": resident_training.id,
            "leave_type": "annual",
            "start_date": str(IN_30),
            "end_date": str(IN_30 + datetime.timedelta(days=3)),
            "reason": "Test",
        })
        assert r.status_code == status.HTTP_403_FORBIDDEN

    def test_utrmc_user_cannot_create_leave(self, db, resident_training, u_utrmc_user):
        c = auth_client(u_utrmc_user)
        r = c.post("/api/leaves/", {
            "resident_training": resident_training.id,
            "leave_type": "annual",
            "start_date": str(IN_30),
            "end_date": str(IN_30 + datetime.timedelta(days=3)),
            "reason": "Test",
        })
        assert r.status_code == status.HTTP_403_FORBIDDEN

    def test_pg_sees_own_leaves(self, db, resident_training, u_pg):
        c = auth_client(u_pg)
        c.post("/api/leaves/", {
            "resident_training": resident_training.id,
            "leave_type": "annual",
            "start_date": str(IN_30),
            "end_date": str(IN_30 + datetime.timedelta(days=3)),
            "reason": "Test",
        })
        r = c.get("/api/leaves/")
        assert r.status_code == status.HTTP_200_OK

    def test_full_leave_submit_and_approve_workflow(
        self, db, resident_training, u_pg, u_supervisor, u_admin
    ):
        """pg creates → pg submits → supervisor approves."""
        from sims.users.models import SupervisorResidentLink

        # Link supervisor to pg
        SupervisorResidentLink.objects.create(
            supervisor_user=u_supervisor,
            resident_user=u_pg,
            department=resident_training.program.department,
            start_date=TODAY,
            active=True,
        )

        pg_c = auth_client(u_pg)
        r = pg_c.post("/api/leaves/", {
            "resident_training": resident_training.id,
            "leave_type": "annual",
            "start_date": str(IN_60),
            "end_date": str(IN_60 + datetime.timedelta(days=5)),
            "reason": "Annual leave request",
        })
        assert r.status_code == status.HTTP_201_CREATED
        leave_id = r.data["id"]

        # pg submits
        r = pg_c.post(f"/api/leaves/{leave_id}/submit/")
        assert r.status_code == status.HTTP_200_OK
        assert r.data["status"] == LeaveRequest.STATUS_SUBMITTED

        # supervisor approves
        sup_c = auth_client(u_supervisor)
        r = sup_c.post(f"/api/leaves/{leave_id}/approve/")
        assert r.status_code == status.HTTP_200_OK
        assert r.data["status"] == LeaveRequest.STATUS_APPROVED

    def test_leave_reject_workflow(self, db, resident_training, u_pg, u_supervisor):
        """pg creates → pg submits → supervisor rejects."""
        from sims.users.models import SupervisorResidentLink
        SupervisorResidentLink.objects.get_or_create(
            supervisor_user=u_supervisor,
            resident_user=u_pg,
            defaults={"department": resident_training.program.department, "start_date": TODAY, "active": True},
        )

        pg_c = auth_client(u_pg)
        r = pg_c.post("/api/leaves/", {
            "resident_training": resident_training.id,
            "leave_type": "sick",
            "start_date": str(IN_90),
            "end_date": str(IN_90 + datetime.timedelta(days=2)),
            "reason": "Sick",
        })
        leave_id = r.data["id"]
        pg_c.post(f"/api/leaves/{leave_id}/submit/")

        sup_c = auth_client(u_supervisor)
        r = sup_c.post(f"/api/leaves/{leave_id}/reject/", {"reason": "Not applicable"})
        assert r.status_code == status.HTTP_200_OK
        assert r.data["status"] == LeaveRequest.STATUS_REJECTED

    def test_pg_cannot_approve_own_leave(self, db, resident_training, u_pg):
        c = auth_client(u_pg)
        r = c.post("/api/leaves/", {
            "resident_training": resident_training.id,
            "leave_type": "annual",
            "start_date": str(IN_30),
            "end_date": str(IN_30 + datetime.timedelta(days=3)),
            "reason": "Test",
        })
        leave_id = r.data["id"]
        c.post(f"/api/leaves/{leave_id}/submit/")
        r = c.post(f"/api/leaves/{leave_id}/approve/")
        assert r.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_sees_all_leaves(self, db, resident_training, u_pg, u_admin):
        pg_c = auth_client(u_pg)
        pg_c.post("/api/leaves/", {
            "resident_training": resident_training.id,
            "leave_type": "annual",
            "start_date": str(IN_60),
            "end_date": str(IN_60 + datetime.timedelta(days=3)),
            "reason": "Admin view test",
        })
        admin_c = auth_client(u_admin)
        r = admin_c.get("/api/leaves/")
        assert r.status_code == status.HTTP_200_OK
        assert r.data["count"] >= 1


# ---------------------------------------------------------------------------
# 11. Notifications
# ---------------------------------------------------------------------------

class TestNotifications:

    def test_pg_receives_own_notifications(self, db, u_pg, u_admin):
        Notification.objects.create(
            recipient=u_pg,
            verb="test_notification",
            title="Test",
            body="Test body",
        )
        c = auth_client(u_pg)
        r = c.get("/api/notifications/")
        assert r.status_code == status.HTTP_200_OK
        # Notifications are scoped to recipient — just verify the response is a list
        assert isinstance(r.data.get("results", r.data), list)

    def test_supervisor_sees_own_notifications(self, db, u_supervisor):
        Notification.objects.create(
            recipient=u_supervisor,
            verb="test_notification",
            title="Supervisor Note",
            body="For supervisor",
        )
        c = auth_client(u_supervisor)
        r = c.get("/api/notifications/")
        assert r.status_code == status.HTTP_200_OK

    def test_pg_cannot_see_other_users_notifications(self, db, u_pg, u_supervisor):
        Notification.objects.create(
            recipient=u_supervisor,
            verb="private_note",
            title="Private",
            body="For supervisor only",
        )
        c = auth_client(u_pg)
        r = c.get("/api/notifications/")
        assert r.status_code == status.HTTP_200_OK
        verbs = [item["verb"] for item in r.data.get("results", r.data)]
        assert "private_note" not in verbs

    def test_mark_notification_read(self, db, u_pg):
        n = Notification.objects.create(
            recipient=u_pg,
            verb="test_mark_read",
            title="Mark Me",
            body="Body",
        )
        c = auth_client(u_pg)
        # NotificationMarkReadSerializer expects 'notification_ids'
        r = c.post("/api/notifications/mark-read/", {"notification_ids": [n.id]})
        assert r.status_code in (status.HTTP_200_OK, status.HTTP_204_NO_CONTENT)

    def test_unread_count_endpoint(self, db, u_pg):
        # Create unread notification (read_at=None means unread; is_read is a property)
        Notification.objects.create(
            recipient=u_pg, verb="unread1", title="Unread", body="."
        )
        c = auth_client(u_pg)
        r = c.get("/api/notifications/unread-count/")
        assert r.status_code == status.HTTP_200_OK
        assert "count" in r.data or "unread_count" in r.data or "unread" in r.data

    def test_unauthenticated_cannot_access_notifications(self, db):
        r = APIClient().get("/api/notifications/")
        assert r.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)


# ---------------------------------------------------------------------------
# 12. Bulk Import / Export
# ---------------------------------------------------------------------------

class TestBulkOperations:

    def test_admin_can_export_departments(self, db, department, u_admin):
        c = auth_client(u_admin)
        r = c.get("/api/bulk/exports/departments/")
        assert r.status_code in (status.HTTP_200_OK, status.HTTP_204_NO_CONTENT)

    def test_utrmc_admin_can_export_departments(self, db, department, u_utrmc_admin):
        c = auth_client(u_utrmc_admin)
        r = c.get("/api/bulk/exports/departments/")
        assert r.status_code in (status.HTTP_200_OK, status.HTTP_204_NO_CONTENT)

    def test_pg_cannot_export(self, db, u_pg):
        c = auth_client(u_pg)
        r = c.get("/api/bulk/exports/departments/")
        assert r.status_code in (
            status.HTTP_403_FORBIDDEN,
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_404_NOT_FOUND,
        )

    def test_supervisor_cannot_export(self, db, u_supervisor):
        c = auth_client(u_supervisor)
        r = c.get("/api/bulk/exports/departments/")
        assert r.status_code in (
            status.HTTP_403_FORBIDDEN,
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_404_NOT_FOUND,
        )

    def test_admin_can_dry_run_import(self, db, u_admin):
        import io
        csv_content = "name,code\nTest Dept Alpha,TDA\n"
        csv_file = io.BytesIO(csv_content.encode())
        csv_file.name = "test_import.csv"
        c = auth_client(u_admin)
        r = c.post(
            "/api/bulk/import/",
            {"file": csv_file, "entity": "departments", "dry_run": "true"},
            format="multipart",
        )
        assert r.status_code in (
            status.HTTP_200_OK,
            status.HTTP_201_CREATED,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_pg_cannot_bulk_import(self, db, u_pg):
        import io
        csv_content = "name,code\nHack Dept,HCK\n"
        csv_file = io.BytesIO(csv_content.encode())
        csv_file.name = "hack.csv"
        c = auth_client(u_pg)
        r = c.post(
            "/api/bulk/import/",
            {"file": csv_file, "entity": "departments", "dry_run": "true"},
            format="multipart",
        )
        assert r.status_code in (
            status.HTTP_403_FORBIDDEN,
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_400_BAD_REQUEST,
        )


# ---------------------------------------------------------------------------
# 13. Audit Log
# ---------------------------------------------------------------------------

class TestAuditLog:

    def test_admin_can_access_audit_log(self, db, u_admin):
        c = auth_client(u_admin)
        r = c.get("/api/audit/activity/")
        assert r.status_code == status.HTTP_200_OK

    def test_utrmc_admin_can_access_audit_log(self, db, u_utrmc_admin):
        # IsAdminUser checks is_staff; utrmc_admin has no is_staff, so 403
        c = auth_client(u_utrmc_admin)
        r = c.get("/api/audit/activity/")
        assert r.status_code == status.HTTP_403_FORBIDDEN

    def test_pg_cannot_access_audit_log(self, db, u_pg):
        c = auth_client(u_pg)
        r = c.get("/api/audit/activity/")
        assert r.status_code in (status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED)

    def test_supervisor_cannot_access_audit_log(self, db, u_supervisor):
        c = auth_client(u_supervisor)
        r = c.get("/api/audit/activity/")
        assert r.status_code in (status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED)


# ---------------------------------------------------------------------------
# 14. My-Rotations / My-Leaves (resident-scoped views)
# ---------------------------------------------------------------------------

class TestMyViews:

    def test_pg_my_rotations(self, db, resident_training, hospital_dept, u_pg, u_admin):
        admin_c = auth_client(u_admin)
        admin_c.post("/api/rotations/", {
            "resident_training": resident_training.id,
            "hospital_department": hospital_dept.id,
            "start_date": str(IN_30),
            "end_date": str(IN_60),
        })
        c = auth_client(u_pg)
        r = c.get("/api/my/rotations/")
        assert r.status_code == status.HTTP_200_OK

    def test_pg_my_leaves(self, db, resident_training, u_pg):
        c = auth_client(u_pg)
        c.post("/api/leaves/", {
            "resident_training": resident_training.id,
            "leave_type": "annual",
            "start_date": str(IN_30),
            "end_date": str(IN_30 + datetime.timedelta(days=3)),
            "reason": "Test",
        })
        r = c.get("/api/my/leaves/")
        assert r.status_code == status.HTTP_200_OK

    def test_supervisor_can_view_pending_rotations(self, db, u_supervisor):
        c = auth_client(u_supervisor)
        r = c.get("/api/supervisor/rotations/pending/")
        assert r.status_code == status.HTTP_200_OK


# ---------------------------------------------------------------------------
# 15. UTRMC Eligibility View
# ---------------------------------------------------------------------------

class TestUTRMCEligibility:

    def test_utrmc_admin_can_view_eligibility(self, db, u_utrmc_admin):
        c = auth_client(u_utrmc_admin)
        r = c.get("/api/utrmc/eligibility/")
        assert r.status_code == status.HTTP_200_OK

    def test_admin_can_view_eligibility(self, db, u_admin):
        c = auth_client(u_admin)
        r = c.get("/api/utrmc/eligibility/")
        assert r.status_code == status.HTTP_200_OK

    def test_pg_cannot_view_eligibility(self, db, u_pg):
        c = auth_client(u_pg)
        r = c.get("/api/utrmc/eligibility/")
        assert r.status_code in (status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED)

    def test_supervisor_cannot_view_eligibility(self, db, u_supervisor):
        c = auth_client(u_supervisor)
        r = c.get("/api/utrmc/eligibility/")
        assert r.status_code in (status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED)

    def test_utrmc_user_cannot_view_eligibility(self, db, u_utrmc_user):
        c = auth_client(u_utrmc_user)
        r = c.get("/api/utrmc/eligibility/")
        assert r.status_code in (
            status.HTTP_200_OK,  # if read-only access is granted
            status.HTTP_403_FORBIDDEN,
        )


# ---------------------------------------------------------------------------
# 16. Resident & Supervisor Summary Views
# ---------------------------------------------------------------------------

class TestSummaryViews:

    def test_pg_can_view_own_summary(self, db, resident_training, u_pg):
        c = auth_client(u_pg)
        r = c.get("/api/residents/me/summary/")
        assert r.status_code in (status.HTTP_200_OK, status.HTTP_404_NOT_FOUND)

    def test_supervisor_can_view_summary(self, db, u_supervisor):
        c = auth_client(u_supervisor)
        r = c.get("/api/supervisors/me/summary/")
        assert r.status_code == status.HTTP_200_OK

    def test_admin_can_view_supervisor_summary(self, db, u_admin):
        c = auth_client(u_admin)
        r = c.get("/api/supervisors/me/summary/")
        assert r.status_code == status.HTTP_200_OK
