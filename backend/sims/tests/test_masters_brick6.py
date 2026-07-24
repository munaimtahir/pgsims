import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.management import call_command
from rest_framework import status
from rest_framework.test import APIClient

from sims.academics.models import Institution, Department, Specialty, Designation, AcademicSession
from sims.rotations.models import Hospital
from sims.training.models import TrainingProgram

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


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
    # Ensure AdminProfile exists
    from sims.users.models import AdminProfile
    AdminProfile.objects.update_or_create(user=user, defaults={"profile_status": "COMPLETE"})
    return user


@pytest.fixture
def resident_user():
    user = User.objects.create_user(
        username="pgr_test",
        password="password123",
        role="RESIDENT",
        first_name="Resident",
        last_name="User",
        is_profile_complete=False,
    )
    # Ensure ResidentProfile exists
    from sims.users.models import ResidentProfile
    ResidentProfile.objects.update_or_create(user=user, defaults={"profile_status": "INCOMPLETE"})
    return user


@pytest.mark.django_db
def test_seed_pilot_masters_command():
    """Test that the seed_pilot_masters command runs successfully and is idempotent."""
    call_command("seed_pilot_masters")
    
    assert Institution.objects.filter(code="FMU").exists()
    assert Hospital.objects.filter(code="ALLIED").exists()
    assert Department.objects.filter(code="MED").exists()
    assert Designation.objects.filter(code="HOD").exists()
    assert AcademicSession.objects.filter(code="2026").exists()
    assert Specialty.objects.filter(code="GI_SURG").exists()

    # Run again to ensure idempotency
    call_command("seed_pilot_masters")


@pytest.mark.django_db
def test_identity_options_endpoint(api_client, resident_user):
    """Test that /api/identity/options/ returns all master option lists."""
    call_command("seed_pilot_masters")
    api_client.force_authenticate(user=resident_user)

    url = reverse("identity_options")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert "institutions" in data
    assert "training_sites" in data
    assert "departments" in data
    assert "programs" in data
    assert "academic_sessions" in data
    assert "designations" in data
    assert "specialties" in data

    # Check correct format (id matches code for string refs)
    session_option = data["academic_sessions"][0]
    assert session_option["id"] == session_option["code"]


@pytest.mark.django_db
def test_onboarding_profile_completion_resolves_master_foreign_keys(api_client, resident_user):
    """Test that complete-profile resolves ForeignKey fields from codes."""
    call_command("seed_pilot_masters")
    api_client.force_authenticate(user=resident_user)

    # Prepare payload with string codes
    hosp = Hospital.objects.filter(code="ALLIED").first()
    dept = Department.objects.filter(code="MED").first()
    prog = TrainingProgram.objects.filter(code="FCPS").first()

    payload = {
        "full_name": "Resident Updated Name",
        "phone": "+923001234567",
        "email": "resident.updated@example.com",
        "hospital": hosp.id,
        "department_ref": dept.id,
        "program_ref": prog.id,
        "academic_session_ref": "2026",
    }

    url = "/api/auth/complete-profile/"
    response = api_client.post(url, payload, format="json")
    assert response.status_code == status.HTTP_200_OK

    # Verify model fields are correctly saved as ForeignKeys
    resident_user.refresh_from_db()
    profile = resident_user.resident_profile
    assert profile.hospital == hosp
    assert profile.department_ref == dept
    assert profile.program_ref == prog
    assert profile.academic_session_ref.code == "2026"
    assert resident_user.is_profile_complete is True


@pytest.mark.django_db
def test_data_quality_endpoint(api_client, admin_user, resident_user):
    """Test the detailed /api/data-quality/ endpoint."""
    call_command("seed_pilot_masters")
    
    # Ensure there's a resident missing critical fields
    resident_user.resident_profile.hospital = None
    resident_user.resident_profile.department_ref = None
    resident_user.resident_profile.save()

    api_client.force_authenticate(user=admin_user)
    response = api_client.get("/api/data-quality/")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert "summary" in data
    assert "sections" in data

    summary = data["summary"]
    assert summary["residents_missing_hospital"] >= 1
    assert summary["residents_missing_department"] >= 1

    # Check structure of items in sections
    section = [s for s in data["sections"] if s["key"] == "residents_missing_hospital"][0]
    assert len(section["items"]) >= 1
    item = section["items"][0]
    assert "user_id" in item
    assert "name" in item
    assert "link" in item
