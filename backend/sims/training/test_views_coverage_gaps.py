"""
Targeted coverage tests for sims/training/views.py — focused on state-machine
action methods (RotationAssignment, LeaveRequest, DeputationPosting), permission
denial paths, and invalid-status-transition paths that were previously untested.
"""
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from sims.academics.models import Department
from sims.rotations.models import Hospital, HospitalDepartment
from sims.training.models import (
    DeputationPosting,
    LeaveRequest,
    ResidentResearchProject,
    ResidentThesis,
    ResidentTrainingRecord,
    RotationAssignment,
    RotationCompletion,
    SubmissionRequirementTemplate,
    TrainingProgram,
    Workshop,
)

User = get_user_model()

TODAY = date.today()


def make_user(username, role, **kwargs):
    if role == "RESIDENT":
        kwargs.setdefault("specialty", "medicine")
        kwargs.setdefault("year", "1")
    if role == "SUPERVISOR":
        kwargs.setdefault("specialty", "medicine")
    return User.objects.create_user(
        username=username,
        password="Test1234!",
        role=role,
        email=f"{username}@example.com",
        **kwargs,
    )


class RotationAssignmentActionGapsTests(APITestCase):
    """Covers permission-denied and invalid-status-transition branches for
    RotationAssignmentViewSet action methods that lacked direct tests."""

    def setUp(self):
        self.department = Department.objects.create(name="Cardiology", code="CARD-GAP")
        self.hospital = Hospital.objects.create(name="Gap Hospital", code="GH-GAP")
        self.hd = HospitalDepartment.objects.create(hospital=self.hospital, department=self.department)

        self.admin = make_user("gap_admin", "ADMIN")
        self.supervisor = make_user("gap_supervisor", "SUPERVISOR")
        self.other_supervisor = make_user("gap_other_supervisor", "SUPERVISOR")
        self.resident = make_user("gap_resident", "RESIDENT", supervisor=self.supervisor)
        self.other_resident = make_user("gap_other_resident", "RESIDENT")

        self.program = TrainingProgram.objects.create(
            name="Cardiology Program", code="CARD-PROG-GAP", duration_months=48
        )
        self.rtr = ResidentTrainingRecord.objects.create(
            resident_user=self.resident, program=self.program, start_date=TODAY, active=True,
        )

    def _make_rotation(self, status_value=RotationAssignment.STATUS_DRAFT, **extra):
        defaults = dict(
            resident_training=self.rtr,
            hospital_department=self.hd,
            start_date=TODAY,
            end_date=TODAY + timedelta(days=30),
            status=status_value,
        )
        defaults.update(extra)
        return RotationAssignment.objects.create(**defaults)

    # ---- submit ----

    def test_submit_not_found_for_unrelated_user(self):
        # The viewset queryset is scoped by role before the action's own
        # permission check runs, so an unrelated resident gets 404 (object
        # not in their scoped queryset), not 403.
        rotation = self._make_rotation()
        self.client.force_authenticate(self.other_resident)
        r = self.client.post(f"/api/rotations/{rotation.id}/submit/")
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

    def test_submit_invalid_status(self):
        rotation = self._make_rotation(status_value=RotationAssignment.STATUS_ACTIVE)
        self.client.force_authenticate(self.admin)
        r = self.client.post(f"/api/rotations/{rotation.id}/submit/")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    # ---- hod-approve ----

    def test_hod_approve_permission_denied_for_resident(self):
        rotation = self._make_rotation(status_value=RotationAssignment.STATUS_SUBMITTED)
        self.client.force_authenticate(self.resident)
        r = self.client.post(f"/api/rotations/{rotation.id}/hod-approve/")
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_hod_approve_invalid_status(self):
        rotation = self._make_rotation(status_value=RotationAssignment.STATUS_DRAFT)
        self.client.force_authenticate(self.supervisor)
        r = self.client.post(f"/api/rotations/{rotation.id}/hod-approve/")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    # ---- utrmc-approve ----

    def test_utrmc_approve_permission_denied_for_supervisor(self):
        rotation = self._make_rotation(status_value=RotationAssignment.STATUS_SUBMITTED)
        self.client.force_authenticate(self.supervisor)
        r = self.client.post(f"/api/rotations/{rotation.id}/utrmc-approve/")
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_utrmc_approve_invalid_status(self):
        rotation = self._make_rotation(status_value=RotationAssignment.STATUS_DRAFT)
        self.client.force_authenticate(self.admin)
        r = self.client.post(f"/api/rotations/{rotation.id}/utrmc-approve/")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_utrmc_approve_success_from_submitted(self):
        rotation = self._make_rotation(status_value=RotationAssignment.STATUS_SUBMITTED)
        self.client.force_authenticate(self.admin)
        r = self.client.post(f"/api/rotations/{rotation.id}/utrmc-approve/")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["status"], RotationAssignment.STATUS_APPROVED)

    def test_utrmc_approve_success_from_approved_sets_utrmc_only(self):
        rotation = self._make_rotation(
            status_value=RotationAssignment.STATUS_APPROVED,
            approved_by_hod=self.supervisor,
        )
        self.client.force_authenticate(self.admin)
        r = self.client.post(f"/api/rotations/{rotation.id}/utrmc-approve/")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        rotation.refresh_from_db()
        self.assertEqual(rotation.approved_by_utrmc, self.admin)

    # ---- activate ----

    def test_activate_permission_denied_for_supervisor(self):
        rotation = self._make_rotation(status_value=RotationAssignment.STATUS_APPROVED)
        self.client.force_authenticate(self.supervisor)
        r = self.client.post(f"/api/rotations/{rotation.id}/activate/")
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_activate_invalid_status(self):
        rotation = self._make_rotation(status_value=RotationAssignment.STATUS_SUBMITTED)
        self.client.force_authenticate(self.admin)
        r = self.client.post(f"/api/rotations/{rotation.id}/activate/")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_activate_success(self):
        rotation = self._make_rotation(status_value=RotationAssignment.STATUS_APPROVED)
        self.client.force_authenticate(self.admin)
        r = self.client.post(f"/api/rotations/{rotation.id}/activate/")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["status"], RotationAssignment.STATUS_ACTIVE)

    # ---- complete ----

    def test_complete_permission_denied_for_supervisor(self):
        rotation = self._make_rotation(status_value=RotationAssignment.STATUS_ACTIVE)
        self.client.force_authenticate(self.supervisor)
        r = self.client.post(f"/api/rotations/{rotation.id}/complete/")
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_complete_invalid_status(self):
        rotation = self._make_rotation(status_value=RotationAssignment.STATUS_APPROVED)
        self.client.force_authenticate(self.admin)
        r = self.client.post(f"/api/rotations/{rotation.id}/complete/")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_complete_success_creates_pending_completion(self):
        rotation = self._make_rotation(status_value=RotationAssignment.STATUS_ACTIVE)
        self.client.force_authenticate(self.admin)
        r = self.client.post(f"/api/rotations/{rotation.id}/complete/")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["status"], RotationAssignment.STATUS_COMPLETED)
        completion = RotationCompletion.objects.get(rotation=rotation)
        self.assertEqual(completion.status, RotationCompletion.STATUS_PENDING_UTRMC_VERIFICATION)

    # ---- review-application ----

    def test_review_application_permission_denied_for_resident(self):
        rotation = self._make_rotation(status_value=RotationAssignment.STATUS_SUBMITTED)
        self.client.force_authenticate(self.resident)
        r = self.client.post(
            f"/api/rotations/{rotation.id}/review-application/", {"action": "approve"}, format="json"
        )
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_review_application_invalid_status(self):
        rotation = self._make_rotation(status_value=RotationAssignment.STATUS_DRAFT)
        self.client.force_authenticate(self.supervisor)
        r = self.client.post(
            f"/api/rotations/{rotation.id}/review-application/", {"action": "approve"}, format="json"
        )
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_review_application_invalid_action_value(self):
        rotation = self._make_rotation(status_value=RotationAssignment.STATUS_SUBMITTED)
        self.client.force_authenticate(self.supervisor)
        r = self.client.post(
            f"/api/rotations/{rotation.id}/review-application/", {"action": "bogus"}, format="json"
        )
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_review_application_redirect_requires_hospital_department(self):
        rotation = self._make_rotation(status_value=RotationAssignment.STATUS_SUBMITTED)
        self.client.force_authenticate(self.supervisor)
        r = self.client.post(
            f"/api/rotations/{rotation.id}/review-application/", {"action": "redirect"}, format="json"
        )
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_review_application_redirect_success(self):
        other_dept = Department.objects.create(name="Redirect Dept", code="RED-GAP")
        other_hd = HospitalDepartment.objects.create(hospital=self.hospital, department=other_dept)
        rotation = self._make_rotation(status_value=RotationAssignment.STATUS_SUBMITTED)
        self.client.force_authenticate(self.supervisor)
        r = self.client.post(
            f"/api/rotations/{rotation.id}/review-application/",
            {"action": "redirect", "hospital_department": other_hd.id, "reason": "Better fit"},
            format="json",
        )
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["status"], RotationAssignment.STATUS_APPROVED)
        rotation.refresh_from_db()
        self.assertEqual(rotation.hospital_department_id, other_hd.id)
        self.assertIn("Redirected", rotation.notes)

    def test_review_application_defer_returns_with_reason(self):
        rotation = self._make_rotation(status_value=RotationAssignment.STATUS_SUBMITTED)
        self.client.force_authenticate(self.supervisor)
        r = self.client.post(
            f"/api/rotations/{rotation.id}/review-application/",
            {"action": "defer", "reason": "Need more info"},
            format="json",
        )
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["status"], RotationAssignment.STATUS_RETURNED)
        self.assertEqual(r.data["return_reason"], "Need more info")

    def test_review_application_defer_default_reason(self):
        rotation = self._make_rotation(status_value=RotationAssignment.STATUS_SUBMITTED)
        self.client.force_authenticate(self.supervisor)
        r = self.client.post(
            f"/api/rotations/{rotation.id}/review-application/", {"action": "defer"}, format="json"
        )
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["return_reason"], "Deferred by supervisor/HOD.")

    def test_review_application_reject_success(self):
        rotation = self._make_rotation(status_value=RotationAssignment.STATUS_SUBMITTED)
        self.client.force_authenticate(self.supervisor)
        r = self.client.post(
            f"/api/rotations/{rotation.id}/review-application/",
            {"action": "reject", "reason": "Not eligible"},
            format="json",
        )
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["status"], RotationAssignment.STATUS_REJECTED)
        self.assertEqual(r.data["reject_reason"], "Not eligible")

    def test_review_application_approve_with_note(self):
        rotation = self._make_rotation(status_value=RotationAssignment.STATUS_SUBMITTED)
        self.client.force_authenticate(self.supervisor)
        r = self.client.post(
            f"/api/rotations/{rotation.id}/review-application/",
            {"action": "approve", "reason": "Looks good"},
            format="json",
        )
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["status"], RotationAssignment.STATUS_APPROVED)
        self.assertIn("Approval note", r.data["notes"])

    # ---- confirm-completion ----

    def test_confirm_completion_permission_denied_for_resident(self):
        rotation = self._make_rotation(status_value=RotationAssignment.STATUS_ACTIVE)
        self.client.force_authenticate(self.resident)
        r = self.client.post(f"/api/rotations/{rotation.id}/confirm-completion/")
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_confirm_completion_invalid_status(self):
        rotation = self._make_rotation(status_value=RotationAssignment.STATUS_SUBMITTED)
        self.client.force_authenticate(self.supervisor)
        r = self.client.post(f"/api/rotations/{rotation.id}/confirm-completion/")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_confirm_completion_from_approved_transitions_to_completed(self):
        rotation = self._make_rotation(status_value=RotationAssignment.STATUS_APPROVED)
        self.client.force_authenticate(self.admin)
        r = self.client.post(f"/api/rotations/{rotation.id}/confirm-completion/")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["rotation"]["status"], RotationAssignment.STATUS_COMPLETED)
        self.assertIn("completion", r.data)

    def test_confirm_completion_twice_reuses_completion_and_certificate(self):
        rotation = self._make_rotation(status_value=RotationAssignment.STATUS_ACTIVE)
        self.client.force_authenticate(self.admin)
        r1 = self.client.post(f"/api/rotations/{rotation.id}/confirm-completion/", {"notes": "first"}, format="json")
        self.assertEqual(r1.status_code, status.HTTP_200_OK)
        r2 = self.client.post(f"/api/rotations/{rotation.id}/confirm-completion/", {"notes": "second"}, format="json")
        self.assertEqual(r2.status_code, status.HTTP_200_OK)
        self.assertEqual(r1.data["completion"]["id"], r2.data["completion"]["id"])

    # ---- verify-completion ----

    def test_verify_completion_permission_denied_for_supervisor(self):
        rotation = self._make_rotation(status_value=RotationAssignment.STATUS_COMPLETED)
        self.client.force_authenticate(self.supervisor)
        r = self.client.post(f"/api/rotations/{rotation.id}/verify-completion/")
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_verify_completion_not_found(self):
        rotation = self._make_rotation(status_value=RotationAssignment.STATUS_COMPLETED)
        self.client.force_authenticate(self.admin)
        r = self.client.post(f"/api/rotations/{rotation.id}/verify-completion/")
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

    def test_verify_completion_success(self):
        rotation = self._make_rotation(status_value=RotationAssignment.STATUS_ACTIVE)
        self.client.force_authenticate(self.admin)
        confirm = self.client.post(f"/api/rotations/{rotation.id}/confirm-completion/")
        self.assertEqual(confirm.status_code, status.HTTP_200_OK)
        r = self.client.post(f"/api/rotations/{rotation.id}/verify-completion/")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["status"], RotationCompletion.STATUS_VERIFIED)

    # ---- returned ----

    def test_returned_permission_denied_for_resident(self):
        rotation = self._make_rotation(status_value=RotationAssignment.STATUS_SUBMITTED)
        self.client.force_authenticate(self.resident)
        r = self.client.post(f"/api/rotations/{rotation.id}/returned/")
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_returned_invalid_status(self):
        rotation = self._make_rotation(status_value=RotationAssignment.STATUS_DRAFT)
        self.client.force_authenticate(self.supervisor)
        r = self.client.post(f"/api/rotations/{rotation.id}/returned/")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    # ---- reject ----

    def test_reject_permission_denied_for_resident(self):
        rotation = self._make_rotation(status_value=RotationAssignment.STATUS_SUBMITTED)
        self.client.force_authenticate(self.resident)
        r = self.client.post(f"/api/rotations/{rotation.id}/reject/")
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_reject_invalid_status(self):
        rotation = self._make_rotation(status_value=RotationAssignment.STATUS_DRAFT)
        self.client.force_authenticate(self.supervisor)
        r = self.client.post(f"/api/rotations/{rotation.id}/reject/")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reject_success(self):
        rotation = self._make_rotation(status_value=RotationAssignment.STATUS_SUBMITTED)
        self.client.force_authenticate(self.supervisor)
        r = self.client.post(f"/api/rotations/{rotation.id}/reject/", {"reason": "Ineligible"}, format="json")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["status"], RotationAssignment.STATUS_REJECTED)
        self.assertEqual(r.data["reject_reason"], "Ineligible")

    # ---- update / partial_update permission & status gates ----

    def test_update_permission_denied_for_supervisor(self):
        rotation = self._make_rotation(status_value=RotationAssignment.STATUS_DRAFT)
        self.client.force_authenticate(self.supervisor)
        r = self.client.put(
            f"/api/rotations/{rotation.id}/",
            {
                "resident_training": self.rtr.id,
                "hospital_department": self.hd.id,
                "start_date": str(TODAY),
                "end_date": str(TODAY + timedelta(days=30)),
            },
            format="json",
        )
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_blocked_when_not_draft_or_returned(self):
        rotation = self._make_rotation(status_value=RotationAssignment.STATUS_ACTIVE)
        self.client.force_authenticate(self.admin)
        r = self.client.put(
            f"/api/rotations/{rotation.id}/",
            {
                "resident_training": self.rtr.id,
                "hospital_department": self.hd.id,
                "start_date": str(TODAY),
                "end_date": str(TODAY + timedelta(days=30)),
            },
            format="json",
        )
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_partial_update_blocked_when_not_draft_or_returned(self):
        rotation = self._make_rotation(status_value=RotationAssignment.STATUS_SUBMITTED)
        self.client.force_authenticate(self.admin)
        r = self.client.patch(f"/api/rotations/{rotation.id}/", {"notes": "x"}, format="json")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_partial_update_allowed_when_draft(self):
        rotation = self._make_rotation(status_value=RotationAssignment.STATUS_DRAFT)
        self.client.force_authenticate(self.admin)
        r = self.client.patch(f"/api/rotations/{rotation.id}/", {"notes": "updated notes"}, format="json")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["notes"], "updated notes")


class LeaveRequestActionGapsTests(APITestCase):
    def setUp(self):
        self.admin = make_user("lg_admin", "ADMIN")
        self.supervisor = make_user("lg_supervisor", "SUPERVISOR")
        self.resident = make_user("lg_resident", "RESIDENT", supervisor=self.supervisor)
        self.other_resident = make_user("lg_other_resident", "RESIDENT")
        self.program = TrainingProgram.objects.create(name="Leave Prog", code="LEAVE-PROG-GAP", duration_months=36)
        self.rtr = ResidentTrainingRecord.objects.create(
            resident_user=self.resident, program=self.program, start_date=TODAY, active=True,
        )

    def _make_leave(self, status_value=LeaveRequest.STATUS_DRAFT):
        return LeaveRequest.objects.create(
            resident_training=self.rtr,
            leave_type=LeaveRequest.TYPE_ANNUAL,
            start_date=TODAY + timedelta(days=5),
            end_date=TODAY + timedelta(days=7),
            status=status_value,
        )

    def test_create_denied_for_supervisor(self):
        self.client.force_authenticate(self.supervisor)
        r = self.client.post("/api/leaves/", {
            "resident_training": self.rtr.id,
            "leave_type": "annual",
            "start_date": str(TODAY),
            "end_date": str(TODAY + timedelta(days=2)),
        })
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_submit_not_found_for_unrelated_resident(self):
        # Same scoping behavior as rotations: an unrelated resident's queryset
        # excludes this leave request entirely, so get_object() 404s before
        # the action's own permission check is reached.
        leave = self._make_leave()
        self.client.force_authenticate(self.other_resident)
        r = self.client.post(f"/api/leaves/{leave.id}/submit/")
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

    def test_submit_invalid_status(self):
        leave = self._make_leave(status_value=LeaveRequest.STATUS_SUBMITTED)
        self.client.force_authenticate(self.resident)
        r = self.client.post(f"/api/leaves/{leave.id}/submit/")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reject_permission_denied_for_resident(self):
        leave = self._make_leave(status_value=LeaveRequest.STATUS_SUBMITTED)
        self.client.force_authenticate(self.resident)
        r = self.client.post(f"/api/leaves/{leave.id}/reject/")
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_reject_invalid_status(self):
        leave = self._make_leave(status_value=LeaveRequest.STATUS_DRAFT)
        self.client.force_authenticate(self.supervisor)
        r = self.client.post(f"/api/leaves/{leave.id}/reject/")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reject_success(self):
        leave = self._make_leave(status_value=LeaveRequest.STATUS_SUBMITTED)
        self.client.force_authenticate(self.supervisor)
        r = self.client.post(f"/api/leaves/{leave.id}/reject/", {"reason": "Overlaps rotation"}, format="json")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["status"], LeaveRequest.STATUS_REJECTED)
        self.assertEqual(r.data["reject_reason"], "Overlaps rotation")

    def test_approve_permission_denied_for_resident(self):
        leave = self._make_leave(status_value=LeaveRequest.STATUS_SUBMITTED)
        self.client.force_authenticate(self.resident)
        r = self.client.post(f"/api/leaves/{leave.id}/approve/")
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_approve_invalid_status(self):
        leave = self._make_leave(status_value=LeaveRequest.STATUS_DRAFT)
        self.client.force_authenticate(self.supervisor)
        r = self.client.post(f"/api/leaves/{leave.id}/approve/")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)


class DeputationPostingActionGapsTests(APITestCase):
    def setUp(self):
        self.admin = make_user("dp_admin", "ADMIN")
        self.supervisor = make_user("dp_supervisor", "SUPERVISOR")
        self.resident = make_user("dp_resident", "RESIDENT", supervisor=self.supervisor)
        self.program = TrainingProgram.objects.create(name="Dep Prog", code="DEP-PROG-GAP", duration_months=36)
        self.rtr = ResidentTrainingRecord.objects.create(
            resident_user=self.resident, program=self.program, start_date=TODAY, active=True,
        )

    def _make_posting(self, status_value=DeputationPosting.STATUS_SUBMITTED):
        return DeputationPosting.objects.create(
            resident_training=self.rtr,
            posting_type=DeputationPosting.TYPE_DEPUTATION,
            institution_name="Other Hospital",
            start_date=TODAY + timedelta(days=1),
            end_date=TODAY + timedelta(days=10),
            status=status_value,
        )

    def test_create_denied_for_supervisor(self):
        self.client.force_authenticate(self.supervisor)
        r = self.client.post("/api/postings/", {
            "resident_training": self.rtr.id,
            "posting_type": "deputation",
            "institution_name": "X Hospital",
            "start_date": str(TODAY),
            "end_date": str(TODAY + timedelta(days=5)),
        })
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_allowed_for_resident(self):
        self.client.force_authenticate(self.resident)
        r = self.client.post("/api/postings/", {
            "resident_training": self.rtr.id,
            "posting_type": "deputation",
            "institution_name": "X Hospital",
            "start_date": str(TODAY),
            "end_date": str(TODAY + timedelta(days=5)),
        })
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

    def test_approve_permission_denied_for_resident(self):
        posting = self._make_posting()
        self.client.force_authenticate(self.resident)
        r = self.client.post(f"/api/postings/{posting.id}/approve/")
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_approve_invalid_status(self):
        posting = self._make_posting(status_value=DeputationPosting.STATUS_APPROVED)
        self.client.force_authenticate(self.supervisor)
        r = self.client.post(f"/api/postings/{posting.id}/approve/")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_approve_success(self):
        posting = self._make_posting()
        self.client.force_authenticate(self.supervisor)
        r = self.client.post(f"/api/postings/{posting.id}/approve/")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["status"], DeputationPosting.STATUS_APPROVED)

    def test_reject_permission_denied_for_resident(self):
        posting = self._make_posting()
        self.client.force_authenticate(self.resident)
        r = self.client.post(f"/api/postings/{posting.id}/reject/")
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_reject_invalid_status(self):
        posting = self._make_posting(status_value=DeputationPosting.STATUS_APPROVED)
        self.client.force_authenticate(self.supervisor)
        r = self.client.post(f"/api/postings/{posting.id}/reject/")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reject_success(self):
        posting = self._make_posting()
        self.client.force_authenticate(self.supervisor)
        r = self.client.post(f"/api/postings/{posting.id}/reject/", {"reason": "Denied"}, format="json")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["status"], DeputationPosting.STATUS_REJECTED)
        self.assertEqual(r.data["reject_reason"], "Denied")

    def test_complete_permission_denied_for_supervisor(self):
        posting = self._make_posting(status_value=DeputationPosting.STATUS_APPROVED)
        self.client.force_authenticate(self.supervisor)
        r = self.client.post(f"/api/postings/{posting.id}/complete/")
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_complete_invalid_status(self):
        posting = self._make_posting(status_value=DeputationPosting.STATUS_SUBMITTED)
        self.client.force_authenticate(self.admin)
        r = self.client.post(f"/api/postings/{posting.id}/complete/")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_complete_success(self):
        posting = self._make_posting(status_value=DeputationPosting.STATUS_APPROVED)
        self.client.force_authenticate(self.admin)
        r = self.client.post(f"/api/postings/{posting.id}/complete/")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["status"], DeputationPosting.STATUS_COMPLETED)


class WorkshopViewSetTests(APITestCase):
    def test_list_workshops(self):
        Workshop.objects.create(name="Active Workshop", code="AW-GAP", is_active=True)
        Workshop.objects.create(name="Inactive Workshop", code="IW-GAP", is_active=False)
        user = make_user("wsv_user", "RESIDENT")
        self.client.force_authenticate(user)
        r = self.client.get("/api/workshops/")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        names = [item["name"] for item in r.data.get("results", r.data)]
        self.assertIn("Active Workshop", names)
        self.assertNotIn("Inactive Workshop", names)


class ResearchProjectActionViewGapsTests(APITestCase):
    def setUp(self):
        self.admin = make_user("rpa_admin", "ADMIN")
        self.supervisor = make_user("rpa_supervisor", "SUPERVISOR")
        self.other_supervisor = make_user("rpa_other_supervisor", "SUPERVISOR")
        self.resident = make_user("rpa_resident", "RESIDENT", supervisor=self.supervisor)
        self.program = TrainingProgram.objects.create(name="RPA Prog", code="RPA-PROG-GAP", duration_months=36)
        self.rtr = ResidentTrainingRecord.objects.create(
            resident_user=self.resident, program=self.program, start_date=TODAY, active=True,
        )
        self.project = ResidentResearchProject.objects.create(
            resident_training_record=self.rtr, title="Gap Study",
        )

    def test_unknown_action(self):
        self.client.force_authenticate(self.resident)
        r = self.client.post("/api/my/research/action/bogus-action/")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_supervisor_approve_requires_role(self):
        self.project.status = ResidentResearchProject.STATUS_SUBMITTED_SUPERVISOR
        self.project.save()
        self.client.force_authenticate(self.resident)
        r = self.client.post(
            "/api/my/research/action/supervisor-approve/", {"project_id": self.project.id}, format="json"
        )
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_supervisor_approve_requires_project_id(self):
        self.project.status = ResidentResearchProject.STATUS_SUBMITTED_SUPERVISOR
        self.project.save()
        self.client.force_authenticate(self.supervisor)
        r = self.client.post("/api/my/research/action/supervisor-approve/", {}, format="json")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_full_transition_chain_via_actions(self):
        self.client.force_authenticate(self.resident)
        r = self.client.post("/api/my/research/action/submit-to-supervisor/")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["status"], ResidentResearchProject.STATUS_SUBMITTED_SUPERVISOR)

        self.client.force_authenticate(self.supervisor)
        r = self.client.post(
            "/api/my/research/action/supervisor-approve/",
            {"project_id": self.project.id, "feedback": "Good work"},
            format="json",
        )
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["status"], ResidentResearchProject.STATUS_APPROVED_SUPERVISOR)

        self.client.force_authenticate(self.resident)
        r = self.client.post("/api/my/research/action/submit-to-university/")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["status"], ResidentResearchProject.STATUS_SUBMITTED_UNIVERSITY)

        self.client.force_authenticate(self.resident)
        denied = self.client.post(
            "/api/my/research/action/accept-by-university/", {"project_id": self.project.id}, format="json"
        )
        self.assertEqual(denied.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(self.admin)
        r = self.client.post(
            "/api/my/research/action/accept-by-university/",
            {"project_id": self.project.id, "university_submission_ref": "REF-1"},
            format="json",
        )
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["status"], ResidentResearchProject.STATUS_ACCEPTED_UNIVERSITY)
        self.project.refresh_from_db()
        self.assertEqual(self.project.university_submission_ref, "REF-1")

    def test_supervisor_return_transitions_to_draft(self):
        self.project.status = ResidentResearchProject.STATUS_SUBMITTED_SUPERVISOR
        self.project.save()
        self.client.force_authenticate(self.supervisor)
        r = self.client.post(
            "/api/my/research/action/supervisor-return/",
            {"project_id": self.project.id, "feedback": "Needs revision"},
            format="json",
        )
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["status"], ResidentResearchProject.STATUS_DRAFT)

    def test_invalid_transition_returns_400(self):
        # project is in DRAFT status; submit-to-university is invalid from DRAFT
        self.client.force_authenticate(self.admin)
        r = self.client.post(
            "/api/my/research/action/accept-by-university/",
            {"project_id": self.project.id},
            format="json",
        )
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)


class ThesisSubmitViewTests(APITestCase):
    def setUp(self):
        self.resident = make_user("tsv_resident", "RESIDENT")
        self.program = TrainingProgram.objects.create(name="TSV Prog", code="TSV-PROG-GAP", duration_months=36)
        self.rtr = ResidentTrainingRecord.objects.create(
            resident_user=self.resident, program=self.program, start_date=TODAY, active=True,
        )

    def test_no_thesis_record(self):
        self.client.force_authenticate(self.resident)
        r = self.client.post("/api/my/thesis/submit/")
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

    def test_missing_thesis_file(self):
        ResidentThesis.objects.create(
            resident_training_record=self.rtr, status=ResidentThesis.STATUS_IN_PROGRESS,
        )
        self.client.force_authenticate(self.resident)
        r = self.client.post("/api/my/thesis/submit/")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_already_submitted(self):
        from django.core.files.uploadedfile import SimpleUploadedFile
        thesis = ResidentThesis.objects.create(
            resident_training_record=self.rtr,
            status=ResidentThesis.STATUS_SUBMITTED,
            thesis_file=SimpleUploadedFile("thesis.pdf", b"data"),
        )
        self.client.force_authenticate(self.resident)
        r = self.client.post("/api/my/thesis/submit/")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_successful_submit(self):
        from django.core.files.uploadedfile import SimpleUploadedFile
        ResidentThesis.objects.create(
            resident_training_record=self.rtr,
            status=ResidentThesis.STATUS_IN_PROGRESS,
            thesis_file=SimpleUploadedFile("thesis.pdf", b"data"),
        )
        self.client.force_authenticate(self.resident)
        r = self.client.post("/api/my/thesis/submit/", {"final_submission_ref": "FIN-1"}, format="json")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data["status"], ResidentThesis.STATUS_SUBMITTED)
        self.assertEqual(r.data["final_submission_ref"], "FIN-1")


class MyWorkshopCompletionDetailViewTests(APITestCase):
    def setUp(self):
        self.resident = make_user("wcd_resident", "RESIDENT")
        self.program = TrainingProgram.objects.create(name="WCD Prog", code="WCD-PROG-GAP", duration_months=36)
        self.rtr = ResidentTrainingRecord.objects.create(
            resident_user=self.resident, program=self.program, start_date=TODAY, active=True,
        )
        self.workshop = Workshop.objects.create(name="WCD Workshop", code="WCD-WS-GAP")

    def test_get_and_delete_completion(self):
        from django.utils import timezone
        from sims.training.models import ResidentWorkshopCompletion

        completion = ResidentWorkshopCompletion.objects.create(
            resident_training_record=self.rtr,
            workshop=self.workshop,
            completed_at=timezone.now(),
        )
        self.client.force_authenticate(self.resident)
        get_r = self.client.get(f"/api/my/workshops/{completion.id}/")
        self.assertEqual(get_r.status_code, status.HTTP_200_OK)

        delete_r = self.client.delete(f"/api/my/workshops/{completion.id}/")
        self.assertEqual(delete_r.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ResidentWorkshopCompletion.objects.filter(id=completion.id).exists())

    def test_get_completion_not_found_for_other_resident(self):
        from django.utils import timezone
        from sims.training.models import ResidentWorkshopCompletion

        completion = ResidentWorkshopCompletion.objects.create(
            resident_training_record=self.rtr,
            workshop=self.workshop,
            completed_at=timezone.now(),
        )
        other = make_user("wcd_other", "RESIDENT")
        other_program = TrainingProgram.objects.create(name="Other Prog", code="WCD-OTHER-GAP", duration_months=36)
        ResidentTrainingRecord.objects.create(
            resident_user=other, program=other_program, start_date=TODAY, active=True,
        )
        self.client.force_authenticate(other)
        r = self.client.get(f"/api/my/workshops/{completion.id}/")
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)


class SubmissionReviewActionStartReviewReturnTests(APITestCase):
    """Covers the start-review and return branches of _SubmissionReviewActionBaseView
    that the existing verify-focused flow test doesn't exercise."""

    def setUp(self):
        self.admin = make_user("srar_admin", "ADMIN")
        self.support = make_user("srar_support", "SUPPORT_STAFF")
        self.resident = make_user("srar_resident", "RESIDENT")
        self.program = TrainingProgram.objects.create(name="SRAR Prog", code="SRAR-PROG-GAP", duration_months=36)
        self.rtr = ResidentTrainingRecord.objects.create(
            resident_user=self.resident, program=self.program, start_date=TODAY, active=True,
        )
        from sims.training.models import ResidentSubmission
        self.submission = ResidentSubmission.objects.create(
            resident_training_record=self.rtr,
            submission_type=ResidentSubmission.TYPE_SYNOPSIS,
            status=ResidentSubmission.STATUS_SUBMITTED,
        )

    def test_support_staff_denied(self):
        self.client.force_authenticate(self.support)
        r = self.client.post(
            f"/api/submissions/synopsis/{self.submission.id}/review/",
            {"action": "start-review"},
            format="json",
        )
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_submission_not_found(self):
        self.client.force_authenticate(self.admin)
        r = self.client.post(
            "/api/submissions/synopsis/999999/review/", {"action": "start-review"}, format="json"
        )
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_action(self):
        self.client.force_authenticate(self.admin)
        r = self.client.post(
            f"/api/submissions/synopsis/{self.submission.id}/review/", {"action": "bogus"}, format="json"
        )
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_start_review_success(self):
        self.client.force_authenticate(self.admin)
        r = self.client.post(
            f"/api/submissions/synopsis/{self.submission.id}/review/",
            {"action": "start-review"},
            format="json",
        )
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        from sims.training.models import ResidentSubmission
        self.assertEqual(r.data["status"], ResidentSubmission.STATUS_UNDER_REVIEW)

    def test_return_success(self):
        self.client.force_authenticate(self.admin)
        r = self.client.post(
            f"/api/submissions/synopsis/{self.submission.id}/review/",
            {"action": "return", "comments": "Missing signature"},
            format="json",
        )
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        from sims.training.models import ResidentSubmission
        self.assertEqual(r.data["status"], ResidentSubmission.STATUS_RETURNED)

    def test_start_review_invalid_status(self):
        from sims.training.models import ResidentSubmission
        self.submission.status = ResidentSubmission.STATUS_DRAFT
        self.submission.save()
        self.client.force_authenticate(self.admin)
        r = self.client.post(
            f"/api/submissions/synopsis/{self.submission.id}/review/",
            {"action": "start-review"},
            format="json",
        )
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)


class RotationCompletionVerifyViewTests(APITestCase):
    def setUp(self):
        self.admin = make_user("rcv_admin", "ADMIN")
        self.supervisor = make_user("rcv_supervisor", "SUPERVISOR")

    def test_permission_denied_for_supervisor(self):
        self.client.force_authenticate(self.supervisor)
        r = self.client.post("/api/rotations/completions/1/verify/")
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_completion_not_found(self):
        self.client.force_authenticate(self.admin)
        r = self.client.post("/api/rotations/completions/999999/verify/")
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)


class SubmissionRequirementTemplateWritePermissionTests(APITestCase):
    def setUp(self):
        self.admin = make_user("srt_admin", "ADMIN")
        self.resident = make_user("srt_resident", "RESIDENT")

    def test_create_denied_for_resident(self):
        self.client.force_authenticate(self.resident)
        r = self.client.post("/api/submissions/requirements/", {
            "submission_type": "SYNOPSIS",
            "code": "REQ-1",
            "title": "Requirement 1",
        })
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_allowed_for_admin(self):
        self.client.force_authenticate(self.admin)
        r = self.client.post("/api/submissions/requirements/", {
            "submission_type": "SYNOPSIS",
            "code": "REQ-2",
            "title": "Requirement 2",
        })
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

    def test_destroy_denied_for_resident(self):
        template = SubmissionRequirementTemplate.objects.create(
            submission_type=SubmissionRequirementTemplate.TYPE_SYNOPSIS,
            code="REQ-3",
            title="Requirement 3",
        )
        self.client.force_authenticate(self.resident)
        r = self.client.delete(f"/api/submissions/requirements/{template.id}/")
        self.assertEqual(r.status_code, status.HTTP_403_FORBIDDEN)
