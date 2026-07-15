import pytest
import io
import csv
from datetime import date
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.test import APIClient

from sims.academics.models import Department, Designation
from sims.rotations.models import Hospital
from sims.users.models import ResidentProfile, SupervisorProfile, AdminProfile
from sims.supervision.models import ResidentSupervisorAssignment
from sims.supervision.services import (
    create_supervisor_assignment,
    change_primary_supervisor,
    end_supervisor_assignment,
    get_supervision_data_quality,
)

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def hospital():
    return Hospital.objects.create(name="Allied Hospital", code="ALLIED", is_active=True)


@pytest.fixture
def department():
    return Department.objects.create(name="Medicine", code="MED", active=True)


@pytest.fixture
def admin_user():
    user = User.objects.create_user(
        username="admin_test",
        password="password123",
        role="ADMIN",
        first_name="Admin",
        last_name="User",
        is_profile_complete=True,
    )
    AdminProfile.objects.update_or_create(
        user=user, defaults={"profile_status": "COMPLETE", "completed_schema_version": 1}
    )
    return user


@pytest.fixture
def resident_user(hospital, department):
    user = User.objects.create_user(
        username="pgr001",
        password="password123",
        role="RESIDENT",
        first_name="Resident",
        last_name="User",
        is_profile_complete=True,
    )
    res_prof, _ = ResidentProfile.objects.update_or_create(
        user=user,
        defaults={
            "profile_status": "COMPLETE",
            "hospital": hospital,
            "department_ref": department,
            "completed_schema_version": 1,
        },
    )
    return user


@pytest.fixture
def supervisor_user(hospital, department):
    user = User.objects.create_user(
        username="sup001",
        password="password123",
        role="SUPERVISOR",
        first_name="Supervisor",
        last_name="User",
        is_profile_complete=True,
    )
    sup_prof, _ = SupervisorProfile.objects.update_or_create(
        user=user,
        defaults={
            "profile_status": "COMPLETE",
            "hospital": hospital,
            "department_ref": department,
            "completed_schema_version": 1,
        },
    )
    return user


@pytest.mark.django_db
class TestSupervisionSpine:
    def test_model_creation_and_constraints(self, resident_user, supervisor_user):
        res_prof = resident_user.resident_profile
        sup_prof = supervisor_user.supervisor_profile

        # Create active primary assignment
        assignment = ResidentSupervisorAssignment.objects.create(
            resident=res_prof,
            supervisor=sup_prof,
            assignment_type=ResidentSupervisorAssignment.ASSIGNMENT_PRIMARY,
            start_date=date.today(),
            is_active=True,
            status=ResidentSupervisorAssignment.STATUS_ACTIVE,
        )
        assert assignment.id is not None
        assert assignment.is_active is True

        # Validation: cannot have active with end date
        assignment.end_date = date.today()
        with pytest.raises(ValidationError):
            assignment.save()

        # Validation: ended must have end date
        assignment.end_date = None
        assignment.status = ResidentSupervisorAssignment.STATUS_ENDED
        with pytest.raises(ValidationError):
            assignment.save()

    def test_business_rules_matching(self, resident_user, supervisor_user, hospital, department):
        res_prof = resident_user.resident_profile
        sup_prof = supervisor_user.supervisor_profile

        # Same hospital & department should succeed
        assignment = create_supervisor_assignment(
            resident=res_prof,
            supervisor=sup_prof,
            assignment_type=ResidentSupervisorAssignment.ASSIGNMENT_PRIMARY,
            start_date=date.today(),
        )
        assert assignment.is_active is True

        # Hospital mismatch
        hosp2 = Hospital.objects.create(name="DHQ Hospital", code="DHQ", is_active=True)
        res_prof.hospital = hosp2
        res_prof.save()

        with pytest.raises(ValidationError) as excinfo:
            create_supervisor_assignment(
                resident=res_prof,
                supervisor=sup_prof,
                assignment_type=ResidentSupervisorAssignment.ASSIGNMENT_CO_SUPERVISOR,
                start_date=date.today(),
            )
        assert "must belong to the same hospital" in str(excinfo.value)

        # Incomplete profile (missing hospital)
        res_prof.hospital = None
        res_prof.save()
        with pytest.raises(ValidationError) as excinfo:
            create_supervisor_assignment(
                resident=res_prof,
                supervisor=sup_prof,
                assignment_type=ResidentSupervisorAssignment.ASSIGNMENT_CO_SUPERVISOR,
                start_date=date.today(),
            )
        assert "Complete Hospital / Training Site first" in str(excinfo.value)

    def test_primary_supervisor_uniqueness(self, resident_user, supervisor_user, hospital, department):
        res_prof = resident_user.resident_profile
        sup_prof = supervisor_user.supervisor_profile

        create_supervisor_assignment(
            resident=res_prof,
            supervisor=sup_prof,
            assignment_type=ResidentSupervisorAssignment.ASSIGNMENT_PRIMARY,
            start_date=date.today(),
        )

        # Try to assign a second active primary
        sup_user2 = User.objects.create_user(username="sup002", role="SUPERVISOR")
        sup_prof2 = SupervisorProfile.objects.create(
            user=sup_user2, hospital=hospital, department_ref=department, profile_status="COMPLETE"
        )

        with pytest.raises(ValidationError) as excinfo:
            create_supervisor_assignment(
                resident=res_prof,
                supervisor=sup_prof2,
                assignment_type=ResidentSupervisorAssignment.ASSIGNMENT_PRIMARY,
                start_date=date.today(),
            )
        assert "already has an active primary supervisor" in str(excinfo.value)

        # Multiple co-supervisors are allowed
        co_assign1 = create_supervisor_assignment(
            resident=res_prof,
            supervisor=sup_prof,
            assignment_type=ResidentSupervisorAssignment.ASSIGNMENT_CO_SUPERVISOR,
            start_date=date.today(),
        )
        co_assign2 = create_supervisor_assignment(
            resident=res_prof,
            supervisor=sup_prof2,
            assignment_type=ResidentSupervisorAssignment.ASSIGNMENT_CO_SUPERVISOR,
            start_date=date.today(),
        )
        assert co_assign1.id is not None
        assert co_assign2.id is not None

    def test_change_primary_supervisor(self, resident_user, supervisor_user, hospital, department):
        res_prof = resident_user.resident_profile
        sup_prof = supervisor_user.supervisor_profile

        # Establish initial primary
        orig_assignment = create_supervisor_assignment(
            resident=res_prof,
            supervisor=sup_prof,
            assignment_type=ResidentSupervisorAssignment.ASSIGNMENT_PRIMARY,
            start_date=date.today(),
        )

        # Rotate primary supervisor
        sup_user2 = User.objects.create_user(username="sup002", role="SUPERVISOR")
        sup_prof2 = SupervisorProfile.objects.create(
            user=sup_user2, hospital=hospital, department_ref=department, profile_status="COMPLETE"
        )

        new_assignment = change_primary_supervisor(
            resident=res_prof,
            new_supervisor=sup_prof2,
            start_date=date.today(),
            reason_for_change="Primary retired",
        )

        # Check orig is deactivated and new is activated
        orig_assignment.refresh_from_db()
        assert orig_assignment.is_active is False
        assert orig_assignment.status == ResidentSupervisorAssignment.STATUS_ENDED
        assert orig_assignment.end_date == date.today()

        assert new_assignment.is_active is True
        assert new_assignment.supervisor == sup_prof2

    def test_api_supervision_endpoints(self, api_client, admin_user, resident_user, supervisor_user):
        res_prof = resident_user.resident_profile
        sup_prof = supervisor_user.supervisor_profile
        api_client.force_authenticate(user=admin_user)

        # 1. Create mapping via API
        url = reverse("supervision:assignment-list")
        payload = {
            "resident_id": res_prof.id,
            "supervisor_id": sup_prof.id,
            "assignment_type": "PRIMARY",
            "start_date": "2026-07-01",
            "notes": "Testing API creation",
        }
        response = api_client.post(url, payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assignment_id = response.data["id"]

        # 2. Get list
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

        # 3. End assignment via API
        end_url = reverse("supervision:assignment-end-assignment", args=[assignment_id])
        end_payload = {"end_date": "2026-12-31", "reason_for_change": "Completed rotation"}
        response = api_client.post(end_url, end_payload, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["status"] == "ENDED"
        assert response.data["is_active"] is False

    def test_supervision_options_api(self, api_client, admin_user, resident_user, supervisor_user):
        api_client.force_authenticate(user=admin_user)
        url = reverse("supervision:options")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert "residents" in response.data
        assert "supervisors" in response.data

    def test_data_quality_endpoint(self, api_client, admin_user):
        api_client.force_authenticate(user=admin_user)
        url = reverse("supervision:data_quality")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert "residents_no_primary" in response.data

    def test_supervision_import_view(self, api_client, admin_user, resident_user, supervisor_user):
        api_client.force_authenticate(user=admin_user)
        url = reverse("supervision:import")

        csv_content = (
            "resident_username,resident_registration_no,resident_email,"
            "supervisor_username,supervisor_pmdc_no,supervisor_email,"
            "assignment_type,start_date,notes\n"
            f"{resident_user.username},,,{supervisor_user.username},,,PRIMARY,2026-07-01,Seeded mapping\n"
        )
        file = io.BytesIO(csv_content.encode("utf-8"))
        file.name = "import_mappings.csv"

        # Dry run mode
        response = api_client.post(url, {"file": file, "dry_run": "true"}, format="multipart")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True
        assert len(response.data["successes"]) == 1

        # Commit mode
        file.seek(0)
        response = api_client.post(url, {"file": file, "dry_run": "false"}, format="multipart")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["success"] is True
        assert ResidentSupervisorAssignment.objects.filter(is_active=True).exists()
