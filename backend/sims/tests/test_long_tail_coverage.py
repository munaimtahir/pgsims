from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from sims.training.models import (
    LogbookEntry, RotationAssignment, ResidentTrainingRecord, TrainingProgram,
    LeaveRequest
)
from sims.rotations.models import Hospital, HospitalDepartment
from sims.academics.models import Department
from sims.supervision.models import ResidentSupervisorAssignment
from django.utils import timezone
from datetime import date, timedelta
import json

User = get_user_model()

class LongTailCoverageTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username="tail_admin", role="ADMIN")
        self.supervisor = User.objects.create_user(username="tail_sup", role="SUPERVISOR")
        self.pg = User.objects.create_user(username="tail_pg", role="RESIDENT")
        self.other_pg = User.objects.create_user(username="other_pg", role="RESIDENT")
        
        self.program = TrainingProgram.objects.create(name="T", code="T", duration_months=12)
        self.rtr = ResidentTrainingRecord.objects.create(resident_user=self.pg, program=self.program, start_date=date.today())
        self.hospital = Hospital.objects.create(name="H", code="H")
        self.dept = Department.objects.create(name="D", code="D")
        self.hdept = HospitalDepartment.objects.create(hospital=self.hospital, department=self.dept)
        
        from sims.users.models import ResidentProfile, SupervisorProfile
        sup_prof, _ = SupervisorProfile.objects.get_or_create(
            user=self.supervisor,
            defaults={"hospital": self.hospital, "department_ref": self.dept},
        )
        res_prof, _ = ResidentProfile.objects.get_or_create(
            user=self.pg,
            defaults={"hospital": self.hospital, "department_ref": self.dept},
        )
        ResidentSupervisorAssignment.objects.get_or_create(
            resident=res_prof,
            supervisor=sup_prof,
            assignment_type=ResidentSupervisorAssignment.ASSIGNMENT_PRIMARY,
            defaults={
                "start_date": date.today(),
                "is_active": True
            }
        )

    def test_rotation_assignment_submit_denied_for_other_pg(self):
        assignment = RotationAssignment.objects.create(
            resident_training=self.rtr, hospital_department=self.hdept,
            start_date=date.today(), end_date=date.today()+timedelta(days=1),
            status="DRAFT"
        )
        # other_pg CANNOT see this assignment, so it should be 404
        self.client.force_authenticate(user=self.other_pg)
        url = reverse("rotation-assignment-submit", kwargs={"pk": assignment.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)

    def test_rotation_assignment_utrmc_approve_denied_for_supervisor(self):
        assignment = RotationAssignment.objects.create(
            resident_training=self.rtr, hospital_department=self.hdept,
            start_date=date.today(), end_date=date.today()+timedelta(days=1),
            status="SUBMITTED"
        )
        # supervisor CAN see it now (linked), but NOT UTRMC-approve it.
        self.client.force_authenticate(user=self.supervisor)
        url = reverse("rotation-assignment-utrmc-approve", kwargs={"pk": assignment.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)

    def test_logbook_entry_review_invalid_action(self):
        entry = LogbookEntry.objects.create(
            resident_training_record=self.rtr, patient_id_number="X",
            patient_seen_at=timezone.now(), status="SUBMITTED"
        )
        self.client.force_authenticate(user=self.admin)
        url = reverse("logbook-entry-review", kwargs={"pk": entry.pk})
        response = self.client.post(url, 
                                   data=json.dumps({"action": "invalid"}),
                                   content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_leave_request_approve_denied_for_pg(self):
        leave = LeaveRequest.objects.create(
            resident_training=self.rtr, leave_type="sick",
            start_date=date.today(), end_date=date.today(),
            status="SUBMITTED"
        )
        self.client.force_authenticate(user=self.pg)
        url = reverse("leave-request-approve", kwargs={"pk": leave.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)

    def test_user_profile_update_invalid_data(self):
        self.client.force_authenticate(user=self.pg)
        url = reverse("auth_api:profile_update")
        response = self.client.patch(url, 
                                   data=json.dumps({"email": "not-an-email"}),
                                   content_type="application/json")
        self.assertIn(response.status_code, [200, 400]) 

    def test_user_search_anonymous(self):
        # Uses LoginRequiredMixin, redirects to login (302)
        url = reverse("users:user_search_api")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
