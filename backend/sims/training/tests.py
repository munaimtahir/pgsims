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
from sims.users.models import ResidentProfile, SupervisorProfile
from sims.supervision.models import ResidentSupervisorAssignment

User = get_user_model()

TODAY = date.today()
NEXT_MONTH = TODAY + timedelta(days=30)
NEXT_YEAR = TODAY + timedelta(days=365)


def make_user(username, role, **kwargs):
    if role in ("RESIDENT", "RESIDENT") and "specialty" not in kwargs:
        kwargs["specialty"] = "medicine"
    if role in ("RESIDENT", "RESIDENT") and "year" not in kwargs:
        kwargs["year"] = "1"
    if role in ("SUPERVISOR", "SUPERVISOR") and "specialty" not in kwargs:
        kwargs["specialty"] = "medicine"
    u = User.objects.create_user(
        username=username, password="Test1234!", role=role,
        email=f"{username}@test.com", first_name=username.capitalize(),
        **kwargs
    )
    if role == "RESIDENT":
        ResidentProfile.objects.get_or_create(user=u)
    elif role == "SUPERVISOR":
        SupervisorProfile.objects.get_or_create(user=u)
    return u


class TrainingProgramModelTest(TestCase):
    def test_str(self):
        p = TrainingProgram(name="Medicine", code="MED", duration_months=36)
        self.assertIn("MED", str(p))


class ResidentTrainingRecordConstraintTest(TestCase):
    def setUp(self):
        self.resident = make_user("res1", "RESIDENT")
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
        self.resident = make_user("res2", "RESIDENT")
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
        self.admin = make_user("admin1", "ADMIN")
        self.utrmc = make_user("utrmc1", "ADMIN")
        self.utrmc_user = make_user("utrmcviewer", "SUPPORT_STAFF")
        self.resident = make_user("res3", "RESIDENT")
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

    def test_utrmc_user_can_read_but_not_update_program_policy(self):
        self._auth(self.utrmc_user)
        get_response = self.client.get(f"/api/programs/{self.prog.id}/policy/")
        self.assertEqual(get_response.status_code, 200)

        put_response = self.client.put(
            f"/api/programs/{self.prog.id}/policy/",
            {"allow_program_change": False},
            format="json",
        )
        self.assertEqual(put_response.status_code, 403)


class UTRMCEligibilityReadOnlyTests(APITestCase):
    def setUp(self):
        self.utrmc_admin = make_user("eligadmin", "ADMIN")
        self.utrmc_user = make_user("eligviewer", "SUPPORT_STAFF")
        self.resident = make_user("eligresident", "RESIDENT")
        self.program = TrainingProgram.objects.create(name="Medicine", code="MED-ELI", duration_months=36)
        self.record = ResidentTrainingRecord.objects.create(
            resident_user=self.resident,
            program=self.program,
            start_date=TODAY,
            active=True,
        )

    def test_utrmc_user_can_read_eligibility_monitor(self):
        self.client.force_authenticate(self.utrmc_user)
        response = self.client.get("/api/utrmc/eligibility/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("results", response.data)


class RotationAssignmentAPITest(APITestCase):
    def setUp(self):
        self.utrmc = make_user("utrmc2", "ADMIN")
        self.supervisor = make_user("sup1", "SUPERVISOR")
        self.resident_user = make_user("res4", "RESIDENT")
        resident_profile = ResidentProfile.objects.get(user=self.resident_user)
        supervisor_profile = SupervisorProfile.objects.get(user=self.supervisor)
        ResidentSupervisorAssignment.objects.create(
            resident=resident_profile,
            supervisor=supervisor_profile,
            assignment_type=ResidentSupervisorAssignment.ASSIGNMENT_PRIMARY,
            is_active=True,
            status=ResidentSupervisorAssignment.STATUS_ACTIVE,
            start_date=TODAY,
        )

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
        # ADMIN can also perform supervisor approval as an administrative fallback.
        r = self.client.post(f"/api/rotations/{rid}/supervisor-approve/")
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
        self.utrmc = make_user("utrmc3", "ADMIN")
        self.supervisor = make_user("sup2", "SUPERVISOR")
        self.resident_user = make_user("res5", "RESIDENT")

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

    def test_resident_leave_retry_key_is_persisted_and_deduplicated(self):
        self._auth(self.resident_user)
        request_id = "1d294ad4-ceaf-4f34-85ec-12e45dc7b935"
        payload = {
            "resident_training": self.rec.id,
            "leave_type": "annual",
            "start_date": str(TODAY),
            "end_date": str(TODAY + timedelta(days=5)),
            "client_request_id": request_id,
        }

        first = self.client.post("/api/leaves/", payload)
        retry = self.client.post("/api/leaves/", payload)

        self.assertEqual(first.status_code, status.HTTP_201_CREATED)
        self.assertEqual(retry.status_code, status.HTTP_200_OK)
        self.assertEqual(retry.data["id"], first.data["id"])
        self.assertEqual(str(LeaveRequest.objects.get(pk=first.data["id"]).client_request_id), request_id)
        self.assertEqual(LeaveRequest.objects.filter(client_request_id=request_id).count(), 1)

    def test_resident_leave_create_requires_resident_training(self):
        self._auth(self.resident_user)
        r = self.client.post("/api/leaves/", {
            "leave_type": "annual",
            "start_date": str(TODAY),
            "end_date": str(TODAY + timedelta(days=5)),
        })
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("resident_training", r.data)

    def _leave_payload(self, **overrides):
        return {"resident_training": self.rec.pk, "leave_type": "annual",
                "start_date": str(TODAY), "end_date": str(TODAY + timedelta(days=2)),
                "client_request_id": "d804858e-d91b-4cb3-8e8c-c0959133d5f7", **overrides}

    def test_leave_key_persisted_replay_unchanged_and_unfiltered(self):
        for user in (self.resident_user, self.utrmc):
            self._auth(user)
            payload = self._leave_payload()
            first = self.client.post("/api/leaves/", payload, format="json")
            self.assertIn(first.status_code, (200, 201))
            replay = self.client.post("/api/leaves/?status=APPROVED", {**payload, "reason": "changed"}, format="json")
            self.assertEqual(replay.status_code, 200)
            self.assertEqual(first.data, replay.data)
            self.assertEqual(str(LeaveRequest.objects.get(pk=first.data["id"]).client_request_id), payload["client_request_id"])
        self.assertEqual(LeaveRequest.objects.count(), 1)

    def test_leave_invalid_null_and_missing_keys(self):
        self._auth(self.resident_user)
        self.assertEqual(self.client.post("/api/leaves/", self._leave_payload(client_request_id="invalid"), format="json").status_code, 400)
        payload = self._leave_payload(client_request_id=None)
        for _ in range(2):
            self.assertEqual(self.client.post("/api/leaves/", payload, format="json").status_code, 201)
        del payload["client_request_id"]
        self.assertEqual(self.client.post("/api/leaves/", payload, format="json").status_code, 201)
        self.assertEqual(LeaveRequest.objects.count(), 3)

    def test_leave_key_cannot_move_or_change(self):
        self._auth(self.resident_user)
        response = self.client.post("/api/leaves/", self._leave_payload(), format="json")
        for value in (None, "7ed573c2-5659-4e37-baad-de329195d213"):
            self.assertEqual(self.client.patch(f"/api/leaves/{response.data['id']}/", {"client_request_id": value}, format="json").status_code, 400)
        self.assertEqual(self.client.patch(f"/api/leaves/{response.data['id']}/", {"reason": "editable"}, format="json").status_code, 200)

    def test_leave_collision_and_permissions_do_not_leak_existing_record(self):
        self._auth(self.resident_user)
        created = self.client.post("/api/leaves/", self._leave_payload(), format="json")
        other = make_user("leave_other", "RESIDENT")
        other_record = ResidentTrainingRecord.objects.create(resident_user=other, program=self.rec.program, start_date=TODAY)
        self.assertEqual(self.client.post("/api/leaves/", self._leave_payload(resident_training=other_record.pk), format="json").status_code, 403)
        self.assertEqual(self.client.patch(f"/api/leaves/{created.data['id']}/", {"resident_training": other_record.pk}, format="json").status_code, 400)
        for user in (other, self.utrmc):
            self._auth(user)
            collision = self.client.post("/api/leaves/", self._leave_payload(resident_training=other_record.pk), format="json")
            self.assertEqual(collision.status_code, 409)
            self.assertEqual(set(collision.data), {"detail"})
        self._auth(self.supervisor)
        self.assertEqual(self.client.post("/api/leaves/", self._leave_payload(), format="json").status_code, 403)
        self.assertEqual(LeaveRequest.objects.count(), 1)

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


class ResidentDashboardFallbackTest(APITestCase):
    def setUp(self):
        self.resident = make_user("lonely_pg", "RESIDENT")

    def _auth(self):
        self.client.force_authenticate(self.resident)

    def test_resident_summary_returns_empty_state_without_training_record(self):
        self._auth()
        response = self.client.get("/api/residents/me/summary/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.data["training_record"])
        self.assertEqual(response.data["schedule"], [])
        self.assertEqual(response.data["leaves"]["active_count"], 0)
        self.assertEqual(response.data["eligibility"]["IMM"]["status"], None)
        self.assertEqual(response.data["thesis"]["status"], "NOT_STARTED")


from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from unittest import skipUnless
from unittest.mock import patch
from django.db import connection, connections, IntegrityError
from rest_framework.test import APITransactionTestCase, APIClient


@skipUnless(connection.vendor == "postgresql", "PostgreSQL concurrent unique-key gate runs separately")
class LeaveIdempotencyConcurrencyTest(APITransactionTestCase):
    setUp = LeaveRequestAPITest.setUp

    def test_simultaneous_replay_inserts_exactly_once(self):
        from .views import LeaveRequestViewSet
        barrier = Barrier(2)
        original = LeaveRequestViewSet.perform_create
        payload = LeaveRequestAPITest._leave_payload(self)

        def synchronized_create(view, serializer):
            barrier.wait(timeout=15)
            return original(view, serializer)

        def post():
            try:
                client = APIClient()
                client.force_authenticate(User.objects.get(pk=self.resident_user.pk))
                response = client.post("/api/leaves/", payload, format="json")
                return response.status_code, response.data["id"]
            finally:
                connections.close_all()

        with patch.object(LeaveRequestViewSet, "perform_create", synchronized_create):
            with ThreadPoolExecutor(max_workers=2) as pool:
                futures = [pool.submit(post) for _ in range(2)]
                results = [future.result(timeout=30) for future in futures]
        self.assertEqual(sorted(code for code, _ in results), [200, 201])
        self.assertEqual(len({pk for _, pk in results}), 1)
        self.assertEqual(LeaveRequest.objects.count(), 1)


class LeaveIdempotencyRollbackTest(APITestCase):
    setUp = LeaveRequestAPITest.setUp

    def test_unrelated_integrity_failure_rolls_back_and_is_not_a_replay(self):
        from .views import LeaveRequestViewSet
        original = LeaveRequestViewSet.perform_create
        def fail(view, serializer):
            original(view, serializer)
            raise IntegrityError("synthetic post-save failure")
        self.client.force_authenticate(self.resident_user)
        with patch.object(LeaveRequestViewSet, "perform_create", fail):
            with self.assertRaises(IntegrityError):
                self.client.post("/api/leaves/", LeaveRequestAPITest._leave_payload(self), format="json")
        self.assertEqual(LeaveRequest.objects.count(), 0)
