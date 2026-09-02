"""Additional coverage for sims/supervision/views.py and sims/supervision/services.py.

Targets error branches, permission denials, filters, and CSV-import failure paths
that sims/supervision/tests/test_supervision.py does not already exercise.
"""
import io

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from sims.academics.models import Department
from sims.rotations.models import Hospital
from sims.users.models import ResidentProfile, SupervisorProfile, AdminProfile
from sims.supervision.models import ResidentSupervisorAssignment
from sims.supervision.services import (
    create_supervisor_assignment,
    change_primary_supervisor,
    end_supervisor_assignment,
    validate_supervision_match,
)

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def hospital():
    return Hospital.objects.create(name="Push2 Hospital", code="PUSH2H", is_active=True)


@pytest.fixture
def hospital2():
    return Hospital.objects.create(name="Push2 Hospital B", code="PUSH2HB", is_active=True)


@pytest.fixture
def department():
    return Department.objects.create(name="Push2 Dept", code="PUSH2D", active=True)


@pytest.fixture
def department2():
    return Department.objects.create(name="Push2 Dept B", code="PUSH2DB", active=True)


@pytest.fixture
def admin_user():
    user = User.objects.create_user(
        username="push2_admin",
        password="password123",
        role="ADMIN",
        first_name="Admin",
        last_name="Push2",
        is_profile_complete=True,
    )
    AdminProfile.objects.update_or_create(
        user=user, defaults={"profile_status": "COMPLETE", "completed_schema_version": 1}
    )
    return user


def _make_resident(username, hospital, department, reg_no=None):
    user = User.objects.create_user(
        username=username,
        password="password123",
        role="RESIDENT",
        first_name="Res",
        last_name=username,
        is_profile_complete=True,
    )
    ResidentProfile.objects.update_or_create(
        user=user,
        defaults={
            "profile_status": "COMPLETE",
            "hospital": hospital,
            "department_ref": department,
            "completed_schema_version": 1,
            "registration_no": reg_no or f"REG-{username}",
        },
    )
    return user


def _make_supervisor(username, hospital, department, pmdc=None):
    user = User.objects.create_user(
        username=username,
        password="password123",
        role="SUPERVISOR",
        first_name="Sup",
        last_name=username,
        is_profile_complete=True,
    )
    SupervisorProfile.objects.update_or_create(
        user=user,
        defaults={
            "profile_status": "COMPLETE",
            "hospital": hospital,
            "department_ref": department,
            "completed_schema_version": 1,
            "pmdc_no": pmdc or f"PMDC-{username}",
        },
    )
    return user


@pytest.fixture
def resident_user(hospital, department):
    return _make_resident("push2_resident", hospital, department)


@pytest.fixture
def supervisor_user(hospital, department):
    return _make_supervisor("push2_supervisor", hospital, department)


@pytest.mark.django_db
class TestChangePrimaryView:
    def test_non_admin_forbidden(self, api_client, resident_user):
        api_client.force_authenticate(user=resident_user)
        url = reverse("supervision:change_primary")
        response = api_client.post(url, {}, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_missing_fields(self, api_client, admin_user):
        api_client.force_authenticate(user=admin_user)
        url = reverse("supervision:change_primary")
        response = api_client.post(url, {"resident_id": 1}, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_resident_not_found(self, api_client, admin_user, supervisor_user):
        api_client.force_authenticate(user=admin_user)
        url = reverse("supervision:change_primary")
        response = api_client.post(
            url,
            {
                "resident_id": 999999,
                "new_supervisor_id": supervisor_user.supervisor_profile.id,
                "start_date": "2026-08-01",
            },
            format="json",
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_supervisor_not_found(self, api_client, admin_user, resident_user):
        api_client.force_authenticate(user=admin_user)
        url = reverse("supervision:change_primary")
        response = api_client.post(
            url,
            {
                "resident_id": resident_user.resident_profile.id,
                "new_supervisor_id": 999999,
                "start_date": "2026-08-01",
            },
            format="json",
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_invalid_date_format(self, api_client, admin_user, resident_user, supervisor_user):
        api_client.force_authenticate(user=admin_user)
        url = reverse("supervision:change_primary")
        response = api_client.post(
            url,
            {
                "resident_id": resident_user.resident_profile.id,
                "new_supervisor_id": supervisor_user.supervisor_profile.id,
                "start_date": "01-08-2026",
            },
            format="json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_happy_path_ends_existing_and_creates_new(
        self, api_client, admin_user, resident_user, supervisor_user, hospital, department
    ):
        create_supervisor_assignment(
            resident=resident_user.resident_profile,
            supervisor=supervisor_user.supervisor_profile,
            assignment_type=ResidentSupervisorAssignment.ASSIGNMENT_PRIMARY,
            start_date="2026-01-01",
            actor=admin_user,
        )
        new_supervisor = _make_supervisor("push2_supervisor2", hospital, department)
        api_client.force_authenticate(user=admin_user)
        url = reverse("supervision:change_primary")
        response = api_client.post(
            url,
            {
                "resident_id": resident_user.resident_profile.id,
                "new_supervisor_id": new_supervisor.supervisor_profile.id,
                "start_date": "2026-08-01",
                "reason_for_change": "rotation",
            },
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK

    def test_new_supervisor_already_primary_raises_validation_error(
        self, api_client, admin_user, resident_user, supervisor_user
    ):
        create_supervisor_assignment(
            resident=resident_user.resident_profile,
            supervisor=supervisor_user.supervisor_profile,
            assignment_type=ResidentSupervisorAssignment.ASSIGNMENT_PRIMARY,
            start_date="2026-01-01",
            actor=admin_user,
        )
        api_client.force_authenticate(user=admin_user)
        url = reverse("supervision:change_primary")
        response = api_client.post(
            url,
            {
                "resident_id": resident_user.resident_profile.id,
                "new_supervisor_id": supervisor_user.supervisor_profile.id,
                "start_date": "2026-08-01",
            },
            format="json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestDataQualityAndOptionsPermissions:
    def test_data_quality_non_admin_forbidden(self, api_client, resident_user):
        api_client.force_authenticate(user=resident_user)
        url = reverse("supervision:data_quality")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_options_with_filters_and_only_unassigned(
        self, api_client, admin_user, resident_user, supervisor_user, hospital, department
    ):
        api_client.force_authenticate(user=admin_user)
        url = reverse("supervision:options")
        response = api_client.get(
            url,
            {
                "training_site_id": hospital.id,
                "department_id": department.id,
                "only_unassigned_residents": "true",
            },
        )
        assert response.status_code == status.HTTP_200_OK
        assert any(r["username"] == resident_user.username for r in response.data["residents"])

        create_supervisor_assignment(
            resident=resident_user.resident_profile,
            supervisor=supervisor_user.supervisor_profile,
            assignment_type=ResidentSupervisorAssignment.ASSIGNMENT_PRIMARY,
            start_date="2026-01-01",
            actor=admin_user,
        )
        response = api_client.get(
            url,
            {"only_unassigned_residents": "true"},
        )
        assert response.status_code == status.HTTP_200_OK
        assert not any(r["username"] == resident_user.username for r in response.data["residents"])


@pytest.mark.django_db
class TestAssignmentViewSetFiltersAndErrors:
    def test_role_scoped_queryset_resident(
        self, api_client, admin_user, resident_user, supervisor_user
    ):
        create_supervisor_assignment(
            resident=resident_user.resident_profile,
            supervisor=supervisor_user.supervisor_profile,
            assignment_type=ResidentSupervisorAssignment.ASSIGNMENT_PRIMARY,
            start_date="2026-01-01",
            actor=admin_user,
        )
        api_client.force_authenticate(user=resident_user)
        url = reverse("supervision:assignment-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1

    def test_role_scoped_queryset_supervisor(
        self, api_client, admin_user, resident_user, supervisor_user
    ):
        create_supervisor_assignment(
            resident=resident_user.resident_profile,
            supervisor=supervisor_user.supervisor_profile,
            assignment_type=ResidentSupervisorAssignment.ASSIGNMENT_PRIMARY,
            start_date="2026-01-01",
            actor=admin_user,
        )
        api_client.force_authenticate(user=supervisor_user)
        url = reverse("supervision:assignment-list")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 1

    def test_filters_is_active_type_ids_hospital_department(
        self, api_client, admin_user, resident_user, supervisor_user, hospital, department
    ):
        create_supervisor_assignment(
            resident=resident_user.resident_profile,
            supervisor=supervisor_user.supervisor_profile,
            assignment_type=ResidentSupervisorAssignment.ASSIGNMENT_PRIMARY,
            start_date="2026-01-01",
            actor=admin_user,
        )
        api_client.force_authenticate(user=admin_user)
        url = reverse("supervision:assignment-list")

        for params in (
            {"is_active": "true"},
            {"is_active": "false"},
            {"assignment_type": "PRIMARY"},
            {"resident_id": resident_user.resident_profile.id},
            {"supervisor_id": supervisor_user.supervisor_profile.id},
            {"hospital_id": hospital.id},
            {"department_id": department.id},
        ):
            response = api_client.get(url, params)
            assert response.status_code == status.HTTP_200_OK

    def test_create_duplicate_active_assignment_returns_400(
        self, api_client, admin_user, resident_user, supervisor_user
    ):
        create_supervisor_assignment(
            resident=resident_user.resident_profile,
            supervisor=supervisor_user.supervisor_profile,
            assignment_type=ResidentSupervisorAssignment.ASSIGNMENT_CO_SUPERVISOR,
            start_date="2026-01-01",
            actor=admin_user,
        )
        api_client.force_authenticate(user=admin_user)
        url = reverse("supervision:assignment-list")
        payload = {
            "resident_id": resident_user.resident_profile.id,
            "supervisor_id": supervisor_user.supervisor_profile.id,
            "assignment_type": "CO_SUPERVISOR",
            "start_date": "2026-02-01",
        }
        response = api_client.post(url, payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_end_assignment_missing_end_date(
        self, api_client, admin_user, resident_user, supervisor_user
    ):
        assignment = create_supervisor_assignment(
            resident=resident_user.resident_profile,
            supervisor=supervisor_user.supervisor_profile,
            assignment_type=ResidentSupervisorAssignment.ASSIGNMENT_PRIMARY,
            start_date="2026-01-01",
            actor=admin_user,
        )
        api_client.force_authenticate(user=admin_user)
        url = reverse("supervision:assignment-end-assignment", args=[assignment.id])
        response = api_client.post(url, {}, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_end_assignment_invalid_date_format(
        self, api_client, admin_user, resident_user, supervisor_user
    ):
        assignment = create_supervisor_assignment(
            resident=resident_user.resident_profile,
            supervisor=supervisor_user.supervisor_profile,
            assignment_type=ResidentSupervisorAssignment.ASSIGNMENT_PRIMARY,
            start_date="2026-01-01",
            actor=admin_user,
        )
        api_client.force_authenticate(user=admin_user)
        url = reverse("supervision:assignment-end-assignment", args=[assignment.id])
        response = api_client.post(
            url, {"end_date": "31-12-2026", "reason_for_change": "x"}, format="json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_end_assignment_already_ended_returns_400(
        self, api_client, admin_user, resident_user, supervisor_user
    ):
        assignment = create_supervisor_assignment(
            resident=resident_user.resident_profile,
            supervisor=supervisor_user.supervisor_profile,
            assignment_type=ResidentSupervisorAssignment.ASSIGNMENT_PRIMARY,
            start_date="2026-01-01",
            actor=admin_user,
        )
        end_supervisor_assignment(
            assignment=assignment, end_date="2026-06-01", reason_for_change="done", actor=admin_user
        )
        api_client.force_authenticate(user=admin_user)
        url = reverse("supervision:assignment-end-assignment", args=[assignment.id])
        response = api_client.post(
            url, {"end_date": "2026-07-01", "reason_for_change": "again"}, format="json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestSupervisionImportFailurePaths:
    def _post_csv(self, api_client, url, csv_content, dry_run="true"):
        file = io.BytesIO(csv_content.encode("utf-8"))
        file.name = "import.csv"
        return api_client.post(url, {"file": file, "dry_run": dry_run}, format="multipart")

    def test_non_admin_forbidden(self, api_client, resident_user):
        api_client.force_authenticate(user=resident_user)
        url = reverse("supervision:import")
        response = api_client.post(url, {}, format="multipart")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_no_file_uploaded(self, api_client, admin_user):
        api_client.force_authenticate(user=admin_user)
        url = reverse("supervision:import")
        response = api_client.post(url, {}, format="multipart")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_resident_not_found(self, api_client, admin_user, supervisor_user):
        api_client.force_authenticate(user=admin_user)
        url = reverse("supervision:import")
        csv_content = (
            "resident_username,resident_registration_no,resident_email,"
            "supervisor_username,supervisor_pmdc_no,supervisor_email,"
            "assignment_type,start_date,notes\n"
            f"nosuchuser,,,{supervisor_user.username},,,PRIMARY,2026-07-01,\n"
        )
        response = self._post_csv(api_client, url, csv_content)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is False
        assert len(response.data["failures"]) == 1

    def test_supervisor_not_found(self, api_client, admin_user, resident_user):
        api_client.force_authenticate(user=admin_user)
        url = reverse("supervision:import")
        csv_content = (
            "resident_username,resident_registration_no,resident_email,"
            "supervisor_username,supervisor_pmdc_no,supervisor_email,"
            "assignment_type,start_date,notes\n"
            f"{resident_user.username},,,nosuchsup,,,PRIMARY,2026-07-01,\n"
        )
        response = self._post_csv(api_client, url, csv_content)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is False
        assert len(response.data["failures"]) == 1

    def test_hospital_mismatch(
        self, api_client, admin_user, hospital, hospital2, department
    ):
        resident = _make_resident("push2_res_hmis", hospital, department)
        supervisor = _make_supervisor("push2_sup_hmis", hospital2, department)
        api_client.force_authenticate(user=admin_user)
        url = reverse("supervision:import")
        csv_content = (
            "resident_username,resident_registration_no,resident_email,"
            "supervisor_username,supervisor_pmdc_no,supervisor_email,"
            "assignment_type,start_date,notes\n"
            f"{resident.username},,,{supervisor.username},,,PRIMARY,2026-07-01,\n"
        )
        response = self._post_csv(api_client, url, csv_content)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is False
        assert "Hospital mismatch" in response.data["failures"][0]["error"]

    def test_department_mismatch(
        self, api_client, admin_user, hospital, department, department2
    ):
        resident = _make_resident("push2_res_dmis", hospital, department)
        supervisor = _make_supervisor("push2_sup_dmis", hospital, department2)
        api_client.force_authenticate(user=admin_user)
        url = reverse("supervision:import")
        csv_content = (
            "resident_username,resident_registration_no,resident_email,"
            "supervisor_username,supervisor_pmdc_no,supervisor_email,"
            "assignment_type,start_date,notes\n"
            f"{resident.username},,,{supervisor.username},,,PRIMARY,2026-07-01,\n"
        )
        response = self._post_csv(api_client, url, csv_content)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is False
        assert "Department mismatch" in response.data["failures"][0]["error"]

    def test_invalid_assignment_type(
        self, api_client, admin_user, resident_user, supervisor_user
    ):
        api_client.force_authenticate(user=admin_user)
        url = reverse("supervision:import")
        csv_content = (
            "resident_username,resident_registration_no,resident_email,"
            "supervisor_username,supervisor_pmdc_no,supervisor_email,"
            "assignment_type,start_date,notes\n"
            f"{resident_user.username},,,{supervisor_user.username},,,BOGUS,2026-07-01,\n"
        )
        response = self._post_csv(api_client, url, csv_content)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is False
        assert "Invalid assignment_type" in response.data["failures"][0]["error"]

    def test_invalid_start_date(
        self, api_client, admin_user, resident_user, supervisor_user
    ):
        api_client.force_authenticate(user=admin_user)
        url = reverse("supervision:import")
        csv_content = (
            "resident_username,resident_registration_no,resident_email,"
            "supervisor_username,supervisor_pmdc_no,supervisor_email,"
            "assignment_type,start_date,notes\n"
            f"{resident_user.username},,,{supervisor_user.username},,,PRIMARY,bad-date,\n"
        )
        response = self._post_csv(api_client, url, csv_content)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is False
        assert "Invalid start_date" in response.data["failures"][0]["error"]

    def test_already_has_active_primary(
        self, api_client, admin_user, resident_user, supervisor_user, hospital, department
    ):
        create_supervisor_assignment(
            resident=resident_user.resident_profile,
            supervisor=supervisor_user.supervisor_profile,
            assignment_type=ResidentSupervisorAssignment.ASSIGNMENT_PRIMARY,
            start_date="2026-01-01",
            actor=admin_user,
        )
        new_supervisor = _make_supervisor("push2_sup_dup_primary", hospital, department)
        api_client.force_authenticate(user=admin_user)
        url = reverse("supervision:import")
        csv_content = (
            "resident_username,resident_registration_no,resident_email,"
            "supervisor_username,supervisor_pmdc_no,supervisor_email,"
            "assignment_type,start_date,notes\n"
            f"{resident_user.username},,,{new_supervisor.username},,,PRIMARY,2026-07-01,\n"
        )
        response = self._post_csv(api_client, url, csv_content)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is False
        assert "already has an active primary supervisor" in response.data["failures"][0]["error"]

    def test_duplicate_active_assignment(
        self, api_client, admin_user, resident_user, supervisor_user
    ):
        create_supervisor_assignment(
            resident=resident_user.resident_profile,
            supervisor=supervisor_user.supervisor_profile,
            assignment_type=ResidentSupervisorAssignment.ASSIGNMENT_CO_SUPERVISOR,
            start_date="2026-01-01",
            actor=admin_user,
        )
        api_client.force_authenticate(user=admin_user)
        url = reverse("supervision:import")
        csv_content = (
            "resident_username,resident_registration_no,resident_email,"
            "supervisor_username,supervisor_pmdc_no,supervisor_email,"
            "assignment_type,start_date,notes\n"
            f"{resident_user.username},,,{supervisor_user.username},,,CO_SUPERVISOR,2026-07-01,\n"
        )
        response = self._post_csv(api_client, url, csv_content)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is False
        assert "Duplicate active assignment" in response.data["failures"][0]["error"]

    def test_lookup_by_registration_number_and_pmdc(
        self, api_client, admin_user, hospital, department
    ):
        resident = _make_resident("push2_res_reg", hospital, department, reg_no="REGNO-777")
        supervisor = _make_supervisor("push2_sup_pmdc", hospital, department, pmdc="PMDC-777")
        api_client.force_authenticate(user=admin_user)
        url = reverse("supervision:import")
        csv_content = (
            "resident_username,resident_registration_no,resident_email,"
            "supervisor_username,supervisor_pmdc_no,supervisor_email,"
            "assignment_type,start_date,notes\n"
            f",REGNO-777,,,PMDC-777,,PRIMARY,2026-07-01,via lookup\n"
        )
        response = self._post_csv(api_client, url, csv_content)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True
        assert len(response.data["successes"]) == 1

    def test_bad_csv_parse_error(self, api_client, admin_user):
        api_client.force_authenticate(user=admin_user)
        url = reverse("supervision:import")
        # Non-utf8 bytes to trigger decode failure.
        file = io.BytesIO(b"\xff\xfe\x00\x01")
        file.name = "bad.csv"
        response = api_client.post(url, {"file": file, "dry_run": "true"}, format="multipart")
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestValidateSupervisionMatchDirect:
    def test_incomplete_hospital_raises(self, resident_user, supervisor_user):
        resident_user.resident_profile.hospital = None
        resident_user.resident_profile.save()
        with pytest.raises(Exception):
            validate_supervision_match(
                resident=resident_user.resident_profile,
                supervisor=supervisor_user.supervisor_profile,
                assignment_type=ResidentSupervisorAssignment.ASSIGNMENT_PRIMARY,
            )

    def test_incomplete_department_raises(self, resident_user, supervisor_user):
        resident_user.resident_profile.department_ref = None
        resident_user.resident_profile.save()
        with pytest.raises(Exception):
            validate_supervision_match(
                resident=resident_user.resident_profile,
                supervisor=supervisor_user.supervisor_profile,
                assignment_type=ResidentSupervisorAssignment.ASSIGNMENT_PRIMARY,
            )

    def test_hospital_mismatch_raises(self, resident_user, supervisor_user, hospital2):
        supervisor_user.supervisor_profile.hospital = hospital2
        supervisor_user.supervisor_profile.save()
        with pytest.raises(Exception):
            validate_supervision_match(
                resident=resident_user.resident_profile,
                supervisor=supervisor_user.supervisor_profile,
                assignment_type=ResidentSupervisorAssignment.ASSIGNMENT_PRIMARY,
            )

    def test_department_mismatch_raises(self, resident_user, supervisor_user, department2):
        supervisor_user.supervisor_profile.department_ref = department2
        supervisor_user.supervisor_profile.save()
        with pytest.raises(Exception):
            validate_supervision_match(
                resident=resident_user.resident_profile,
                supervisor=supervisor_user.supervisor_profile,
                assignment_type=ResidentSupervisorAssignment.ASSIGNMENT_PRIMARY,
            )
