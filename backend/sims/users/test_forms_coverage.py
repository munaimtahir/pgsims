from django.core.files.uploadedfile import SimpleUploadedFile

import pytest

from sims.academics.models import Specialty
from sims.users.forms import (
    BulkUserUploadForm,
    CustomLoginForm,
    CustomUserChangeForm,
    CustomUserCreationForm,
    SupervisorAssignmentForm,
)
from sims.users.models import User


@pytest.fixture
def specialty():
    return Specialty.objects.create(name="Form Medicine", code="FORM-MED", active=True)


@pytest.fixture
def supervisor(specialty):
    return User.objects.create_user(
        username="form-supervisor", password="Test1234!", role="SUPERVISOR", specialty=specialty.code
    )


@pytest.mark.django_db
def test_creation_form_validates_role_specific_fields_and_saves(specialty, supervisor):
    base = {
        "username": "form-resident", "email": "resident@example.test", "first_name": "Form",
        "last_name": "Resident", "password1": "Test1234!", "password2": "Test1234!",
        "role": "RESIDENT", "specialty": specialty.pk, "year": "1", "supervisor": supervisor.pk,
    }
    form = CustomUserCreationForm(data=base)
    assert form.is_valid(), form.errors
    user = form.save()
    assert user.email == base["email"]

    missing = base | {"username": "missing-specialty", "specialty": "", "supervisor": ""}
    assert not CustomUserCreationForm(data=missing).is_valid()
    assert not CustomUserCreationForm(data=base | {"username": "bad-supervisor", "role": "SUPERVISOR", "supervisor": "", "specialty": ""}).is_valid()


@pytest.mark.django_db
def test_assignment_and_change_forms_filter_by_specialty(specialty, supervisor):
    resident = User.objects.create_user(
        username="form-resident-existing", password="Test1234!", role="RESIDENT", specialty=specialty.code, year="1"
    )
    assignment = SupervisorAssignmentForm(specialty=specialty.code)
    assert list(assignment.fields["pgs"].queryset) == [resident]
    assert list(assignment.fields["supervisor"].queryset) == [supervisor]

    changed = CustomUserChangeForm(instance=resident)
    assert "password" not in changed.fields
    assert supervisor in changed.fields["supervisor"].queryset


@pytest.mark.django_db
def test_upload_and_login_forms_cover_invalid_and_valid_inputs():
    assert not BulkUserUploadForm(files={"file": SimpleUploadedFile("users.txt", b"x")}).is_valid()
    assert not BulkUserUploadForm(files={"file": SimpleUploadedFile("users.csv", b"x" * (5 * 1024 * 1024 + 1))}).is_valid()
    assert BulkUserUploadForm(files={"file": SimpleUploadedFile("users.csv", b"name\n")}).is_valid()

    user = User.objects.create_user(username="form-login", password="Test1234!", role="ADMIN")
    good = CustomLoginForm(data={"username": user.username, "password": "Test1234!"})
    assert good.is_valid()
    assert good.get_user() == user
    assert not CustomLoginForm(data={"username": user.username, "password": "wrong"}).is_valid()
