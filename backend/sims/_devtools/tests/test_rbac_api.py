from datetime import date, timedelta

from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from sims.academics.models import Department
from sims.logbook.models import LogbookEntry
from sims.rotations.models import Hospital, HospitalDepartment, Rotation
from sims.users.models import User


class RBACAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.admin = User.objects.create_user(
            username="admin_rbac",
            password="pass",
            role="admin",
            email="admin_rbac@example.com",
        )
        self.utrmc_user = User.objects.create_user(
            username="utrmc_reader_rbac",
            password="pass",
            role="utrmc_user",
            email="utrmc_reader_rbac@example.com",
        )
        self.utrmc_admin = User.objects.create_user(
            username="utrmc_admin_rbac",
            password="pass",
            role="utrmc_admin",
            email="utrmc_admin_rbac@example.com",
        )
        self.supervisor = User.objects.create_user(
            username="sup_rbac",
            password="pass",
            role="supervisor",
            email="sup_rbac@example.com",
            specialty="surgery",
        )
        self.other_supervisor = User.objects.create_user(
            username="sup_other_rbac",
            password="pass",
            role="supervisor",
            email="sup_other_rbac@example.com",
            specialty="medicine",
        )

        self.home_hospital = Hospital.objects.create(name="Home Hospital", code="HOME")
        self.other_hospital = Hospital.objects.create(name="External Hospital", code="EXT")
        self.surgery = Department.objects.create(name="Surgery", code="SURG")
        self.medicine = Department.objects.create(name="Medicine", code="MED")
        self.pathology = Department.objects.create(name="Pathology", code="PATH")

        HospitalDepartment.objects.create(hospital=self.home_hospital, department=self.surgery)
        HospitalDepartment.objects.create(hospital=self.other_hospital, department=self.surgery)
        HospitalDepartment.objects.create(hospital=self.other_hospital, department=self.medicine)

        self.pg = User.objects.create_user(
            username="pg_rbac",
            password="pass",
            role="pg",
            email="pg_rbac@example.com",
            specialty="surgery",
            year="1",
            supervisor=self.supervisor,
            home_hospital=self.home_hospital,
            home_department=self.surgery,
        )
        self.other_pg = User.objects.create_user(
            username="pg_other_rbac",
            password="pass",
            role="pg",
            email="pg_other_rbac@example.com",
            specialty="medicine",
            year="1",
            supervisor=self.other_supervisor,
            home_hospital=self.other_hospital,
            home_department=self.medicine,
        )

        self.own_rotation = Rotation.objects.create(
            pg=self.pg,
            department=self.surgery,
            hospital=self.home_hospital,
            supervisor=self.supervisor,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30),
            status="planned",
        )
        self.other_rotation = Rotation.objects.create(
            pg=self.other_pg,
            department=self.medicine,
            hospital=self.other_hospital,
            supervisor=self.other_supervisor,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30),
            status="planned",
        )
        self.override_rotation = Rotation.objects.create(
            pg=self.pg,
            department=self.surgery,
            hospital=self.other_hospital,
            supervisor=self.supervisor,
            start_date=date.today() + timedelta(days=40),
            end_date=date.today() + timedelta(days=70),
            status="planned",
            override_reason="Need exposure to tertiary caseload",
        )

        self.pending_entry = LogbookEntry.objects.create(
            pg=self.pg,
            supervisor=self.supervisor,
            rotation=self.own_rotation,
            case_title="RBAC test case",
            date=date.today(),
            location_of_activity="Ward",
            patient_history_summary="History",
            management_action="Action",
            topic_subtopic="Topic",
            status="pending",
            submitted_to_supervisor_at=timezone.now(),
        )

    def test_logbook_pending_queue_supervisor_scope_and_out_of_scope_verify_denied(self):
        self.client.force_authenticate(self.supervisor)
        pending_resp = self.client.get("/api/logbook/pending/")
        self.assertEqual(pending_resp.status_code, 200)
        self.assertEqual(pending_resp.data["count"], 1)
        self.assertEqual(pending_resp.data["results"][0]["id"], self.pending_entry.id)

        self.client.force_authenticate(self.other_supervisor)
        verify_resp = self.client.patch(
            f"/api/logbook/{self.pending_entry.id}/verify/",
            {"action": "approved", "feedback": "Not my trainee"},
            format="json",
        )
        self.assertEqual(verify_resp.status_code, 403)

    def test_logbook_utrmc_read_only_access(self):
        self.client.force_authenticate(self.utrmc_user)
        self.assertEqual(self.client.get("/api/logbook/pending/").status_code, 200)
        deny = self.client.patch(
            f"/api/logbook/{self.pending_entry.id}/verify/",
            {"action": "approved"},
            format="json",
        )
        self.assertEqual(deny.status_code, 403)

    def test_rotations_pg_only_sees_own_detail(self):
        self.client.force_authenticate(self.pg)
        own = self.client.get(f"/api/rotations/my/{self.own_rotation.id}/")
        self.assertEqual(own.status_code, 200)
        other = self.client.get(f"/api/rotations/my/{self.other_rotation.id}/")
        self.assertEqual(other.status_code, 404)

    def test_rotation_override_approval_requires_utrmc_admin(self):
        self.client.force_authenticate(self.utrmc_user)
        denied = self.client.patch(
            f"/api/rotations/{self.override_rotation.id}/utrmc-approve/",
            {},
            format="json",
        )
        self.assertEqual(denied.status_code, 403)

        self.client.force_authenticate(self.utrmc_admin)
        approved = self.client.patch(
            f"/api/rotations/{self.override_rotation.id}/utrmc-approve/",
            {},
            format="json",
        )
        self.assertEqual(approved.status_code, 200)
        self.override_rotation.refresh_from_db()
        self.assertEqual(self.override_rotation.utrmc_approved_by, self.utrmc_admin)
        self.assertIsNotNone(self.override_rotation.utrmc_approved_at)

    def test_department_reference_data_write_restricted(self):
        self.client.force_authenticate(self.pg)
        list_resp = self.client.get("/academics/api/departments/")
        self.assertEqual(list_resp.status_code, 200)
        pg_create = self.client.post(
            "/academics/api/departments/",
            {"name": "Dermatology", "code": "DERM", "active": True},
            format="json",
        )
        self.assertEqual(pg_create.status_code, 403)

        self.client.force_authenticate(self.admin)
        admin_create = self.client.post(
            "/academics/api/departments/",
            {"name": "Dermatology", "code": "DERM", "active": True},
            format="json",
        )
        self.assertEqual(admin_create.status_code, 201)

        self.client.force_authenticate(self.utrmc_admin)
        uadmin_create = self.client.post(
            "/academics/api/departments/",
            {"name": "Radiology", "code": "RAD", "active": True},
            format="json",
        )
        self.assertEqual(uadmin_create.status_code, 403)
        uadmin_patch = self.client.patch(
            f"/academics/api/departments/{self.surgery.id}/",
            {"description": "Nope"},
            format="json",
        )
        self.assertEqual(uadmin_patch.status_code, 403)
        uadmin_put = self.client.put(
            f"/academics/api/departments/{self.surgery.id}/",
            {"name": self.surgery.name, "code": self.surgery.code, "active": True},
            format="json",
        )
        self.assertEqual(uadmin_put.status_code, 403)
        uadmin_delete = self.client.delete(f"/academics/api/departments/{self.surgery.id}/")
        self.assertEqual(uadmin_delete.status_code, 403)

    def test_hospital_reference_data_write_restricted(self):
        self.client.force_authenticate(self.supervisor)
        list_resp = self.client.get("/api/rotations/hospitals/")
        self.assertEqual(list_resp.status_code, 200)
        sup_create = self.client.post(
            "/api/rotations/hospitals/",
            {"name": "New Hospital", "code": "NH"},
            format="json",
        )
        self.assertEqual(sup_create.status_code, 403)

        self.client.force_authenticate(self.admin)
        admin_create = self.client.post(
            "/api/rotations/hospitals/",
            {"name": "New Hospital", "code": "NH"},
            format="json",
        )
        self.assertEqual(admin_create.status_code, 201)

        self.client.force_authenticate(self.utrmc_admin)
        uadmin_create = self.client.post(
            "/api/rotations/hospitals/",
            {"name": "UTRMC Attempt", "code": "UA"},
            format="json",
        )
        self.assertEqual(uadmin_create.status_code, 403)
        uadmin_patch = self.client.patch(
            f"/api/rotations/hospitals/{self.home_hospital.id}/",
            {"description": "Nope"},
            format="json",
        )
        self.assertEqual(uadmin_patch.status_code, 403)
        uadmin_put = self.client.put(
            f"/api/rotations/hospitals/{self.home_hospital.id}/",
            {"name": self.home_hospital.name, "code": self.home_hospital.code, "is_active": True},
            format="json",
        )
        self.assertEqual(uadmin_put.status_code, 403)
        uadmin_delete = self.client.delete(f"/api/rotations/hospitals/{self.home_hospital.id}/")
        self.assertEqual(uadmin_delete.status_code, 403)

    def test_hospital_department_write_utrmc_admin_primary_with_admin_recovery(self):
        self.client.force_authenticate(self.admin)
        admin_create = self.client.post(
            "/api/rotations/hospital-departments/",
            {
                "hospital_id": self.home_hospital.id,
                "department_id": self.medicine.id,
                "is_active": True,
            },
            format="json",
        )
        self.assertEqual(admin_create.status_code, 201)

        self.client.force_authenticate(self.utrmc_admin)
        uadmin_create = self.client.post(
            "/api/rotations/hospital-departments/",
            {
                "hospital_id": self.other_hospital.id,
                "department_id": self.pathology.id,
                "is_active": True,
            },
            format="json",
        )
        self.assertEqual(uadmin_create.status_code, 201)
