"""Tests for sims.training models, API endpoints, and RBAC."""
from datetime import date, timedelta
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

from sims.academics.models import Department
from sims.rotations.models import Hospital, HospitalDepartment
from .models import (
    TrainingProgram,
    ProgramRotationTemplate,
    ResidentTrainingRecord,
    RotationAssignment,
    LeaveRequest,
    DeputationPosting,
)

User = get_user_model()

TODAY = date.today()
NEXT_MONTH = TODAY + timedelta(days=30)
NEXT_YEAR = TODAY + timedelta(days=365)


def make_user(username, role, **kwargs):
    if role in ("resident", "pg") and "specialty" not in kwargs:
        kwargs["specialty"] = "medicine"
    if role in ("resident", "pg") and "year" not in kwargs:
        kwargs["year"] = "1"
    if role in ("supervisor", "faculty") and "specialty" not in kwargs:
        kwargs["specialty"] = "medicine"
    u = User.objects.create_user(
        username=username, password="Test1234!", role=role,
        email=f"{username}@test.com", first_name=username.capitalize(),
        **kwargs
    )
    return u


class TrainingProgramModelTest(TestCase):
    def test_str(self):
        p = TrainingProgram(name="Medicine", code="MED", duration_months=36)
        self.assertIn("MED", str(p))


class ResidentTrainingRecordConstraintTest(TestCase):
    def setUp(self):
        self.resident = make_user("res1", "resident")
        self.prog = TrainingProgram.objects.create(name="Medicine", code="MED", duration_months=36)

    def test_clean_raises_if_end_before_start(self):
        from django.core.exceptions import ValidationError
        rec = ResidentTrainingRecord(
            resident_user=self.resident, program=self.prog,
            start_date=TODAY, expected_end_date=TODAY - timedelta(days=1)
        )
        with self.assertRaises(ValidationError):
            rec.clean()


class RotationAssignmentOverlapTest(TestCase):
    def setUp(self):
        self.resident = make_user("res2", "resident")
        self.prog = TrainingProgram.objects.create(name="Surgery", code="SURG", duration_months=48)
        self.rec = ResidentTrainingRecord.objects.create(
            resident_user=self.resident, program=self.prog, start_date=TODAY, active=True
        )
        dept = Department.objects.create(name="Surgery Dept", code="SD")
        hosp = Hospital.objects.create(name="Test Hospital", code="TH")
        self.hd = HospitalDepartment.objects.create(hospital=hosp, department=dept)

    def test_no_overlap_allowed(self):
        from django.core.exceptions import ValidationError
        RotationAssignment.objects.create(
            resident_training=self.rec, hospital_department=self.hd,
            start_date=TODAY, end_date=NEXT_MONTH,
            status=RotationAssignment.STATUS_SUBMITTED,
        )
        overlap = RotationAssignment(
            resident_training=self.rec, hospital_department=self.hd,
            start_date=TODAY + timedelta(days=5), end_date=NEXT_MONTH + timedelta(days=10),
            status=RotationAssignment.STATUS_DRAFT,
        )
        with self.assertRaises(ValidationError):
            overlap.clean()

    def test_non_overlapping_is_valid(self):
        RotationAssignment.objects.create(
            resident_training=self.rec, hospital_department=self.hd,
            start_date=TODAY, end_date=NEXT_MONTH,
            status=RotationAssignment.STATUS_SUBMITTED,
        )
        ra = RotationAssignment(
            resident_training=self.rec, hospital_department=self.hd,
            start_date=NEXT_MONTH + timedelta(days=1), end_date=NEXT_MONTH + timedelta(days=30),
        )
        ra.clean()  # should not raise


class TrainingProgramAPITest(APITestCase):
    def setUp(self):
        self.admin = make_user("admin1", "admin")
        self.utrmc = make_user("utrmc1", "utrmc_admin")
        self.resident = make_user("res3", "resident")
        self.prog = TrainingProgram.objects.create(
            name="Pediatrics", code="PED", duration_months=36
        )

    def _auth(self, user):
        self.client.force_authenticate(user=user)

    def test_list_authenticated(self):
        self._auth(self.resident)
        r = self.client.get("/api/programs/")
        self.assertEqual(r.status_code, 200)

    def test_create_utrmc_admin(self):
        self._auth(self.utrmc)
        r = self.client.post("/api/programs/", {"name": "OB/GYN", "code": "OBGYN", "duration_months": 48})
        self.assertEqual(r.status_code, 201)

    def test_create_resident_denied(self):
        self._auth(self.resident)
        r = self.client.post("/api/programs/", {"name": "OB/GYN", "code": "OBGYN2", "duration_months": 48})
        self.assertEqual(r.status_code, 403)

    def test_unauthenticated_denied(self):
        self.client.logout()
        r = self.client.get("/api/programs/")
        self.assertEqual(r.status_code, 401)


class RotationAssignmentAPITest(APITestCase):
    def setUp(self):
        self.utrmc = make_user("utrmc2", "utrmc_admin")
        self.supervisor = make_user("sup1", "supervisor")
        self.resident_user = make_user("res4", "resident")
        self.resident_user.supervisor = self.supervisor
        self.resident_user.save(update_fields=["supervisor"])

        prog = TrainingProgram.objects.create(name="Medicine", code="MED2", duration_months=36)
        self.rec = ResidentTrainingRecord.objects.create(
            resident_user=self.resident_user, program=prog,
            start_date=TODAY, active=True,
        )
        dept = Department.objects.create(name="Medicine Dept", code="MD")
        hosp = Hospital.objects.create(name="Allied Hospital", code="AH")
        self.hd = HospitalDepartment.objects.create(hospital=hosp, department=dept)

    def _auth(self, user):
        self.client.force_authenticate(user=user)

    def _create_rotation(self):
        self._auth(self.utrmc)
        r = self.client.post("/api/rotations/", {
            "resident_training": self.rec.id,
            "hospital_department": self.hd.id,
            "start_date": str(TODAY),
            "end_date": str(NEXT_MONTH),
        })
        self.assertEqual(r.status_code, 201)
        return r.data["id"]

    def test_create_and_submit_flow(self):
        rid = self._create_rotation()
        # submit
        r = self.client.post(f"/api/rotations/{rid}/submit/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["status"], "SUBMITTED")

    def test_hod_approve_after_submit(self):
        rid = self._create_rotation()
        self.client.post(f"/api/rotations/{rid}/submit/")
        # utrmc_admin can also do hod-approve
        r = self.client.post(f"/api/rotations/{rid}/hod-approve/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["status"], "APPROVED")

    def test_resident_cannot_create(self):
        self._auth(self.resident_user)
        r = self.client.post("/api/rotations/", {
            "resident_training": self.rec.id,
            "hospital_department": self.hd.id,
            "start_date": str(TODAY),
            "end_date": str(NEXT_MONTH),
        })
        self.assertEqual(r.status_code, 403)

    def test_resident_sees_own_rotations(self):
        self._create_rotation()
        self._auth(self.resident_user)
        r = self.client.get("/api/rotations/")
        self.assertEqual(r.status_code, 200)

    def test_supervisor_sees_supervised_resident_rotation_without_department_membership(self):
        self._create_rotation()
        self._auth(self.supervisor)
        r = self.client.get("/api/rotations/")
        self.assertEqual(r.status_code, 200)
        rows = r.data if isinstance(r.data, list) else r.data.get("results", [])
        self.assertEqual(len(rows), 1)

    def test_supervisor_pending_rotations_includes_direct_supervisor_assignment(self):
        rid = self._create_rotation()
        self.client.post(f"/api/rotations/{rid}/submit/")
        self._auth(self.supervisor)
        r = self.client.get("/api/supervisor/rotations/pending/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["count"], 1)

    def test_returned_rotation_can_be_resubmitted_by_resident(self):
        rid = self._create_rotation()
        self.client.post(f"/api/rotations/{rid}/submit/")
        self._auth(self.supervisor)
        returned = self.client.post(
            f"/api/rotations/{rid}/returned/",
            {"reason": "Please adjust dates."},
        )
        self.assertEqual(returned.status_code, 200)
        self.assertEqual(returned.data["status"], "RETURNED")

        self._auth(self.resident_user)
        resubmitted = self.client.post(f"/api/rotations/{rid}/submit/")
        self.assertEqual(resubmitted.status_code, 200)
        self.assertEqual(resubmitted.data["status"], "SUBMITTED")
        self.assertEqual(resubmitted.data["return_reason"], "")


class LeaveRequestAPITest(APITestCase):
    def setUp(self):
        self.utrmc = make_user("utrmc3", "utrmc_admin")
        self.supervisor = make_user("sup2", "supervisor")
        self.resident_user = make_user("res5", "resident")

        prog = TrainingProgram.objects.create(name="Medicine", code="MED3", duration_months=36)
        self.rec = ResidentTrainingRecord.objects.create(
            resident_user=self.resident_user, program=prog, start_date=TODAY, active=True,
        )

    def _auth(self, user):
        self.client.force_authenticate(user=user)

    def test_resident_creates_leave(self):
        self._auth(self.resident_user)
        r = self.client.post("/api/leaves/", {
            "resident_training": self.rec.id,
            "leave_type": "annual",
            "start_date": str(TODAY),
            "end_date": str(TODAY + timedelta(days=5)),
        })
        self.assertEqual(r.status_code, 201)

    def test_full_leave_approval_flow(self):
        self._auth(self.resident_user)
        r = self.client.post("/api/leaves/", {
            "resident_training": self.rec.id,
            "leave_type": "sick",
            "start_date": str(TODAY),
            "end_date": str(TODAY + timedelta(days=3)),
        })
        lid = r.data["id"]
        # submit
        r = self.client.post(f"/api/leaves/{lid}/submit/")
        self.assertEqual(r.data["status"], "SUBMITTED")
        # approve
        self._auth(self.utrmc)
        r = self.client.post(f"/api/leaves/{lid}/approve/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["status"], "APPROVED")
