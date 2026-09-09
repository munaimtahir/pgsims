import pytest
from datetime import date
from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command

from sims.academics.models import Department
from sims.rotations.models import Hospital
from sims.training.models import TrainingProgram, ResidentTrainingRecord
from sims.users.models import ResidentProfile, SupervisorProfile
from sims.supervision.models import ResidentSupervisorAssignment

User = get_user_model()

COMMAND = "reconcile_urology_supervisor_profiles"


@pytest.fixture
def hospital():
    return Hospital.objects.create(name="Allied Hospital-I Faisalabad", code="AH1", is_active=True)


@pytest.fixture
def department():
    return Department.objects.create(name="Urology Department", code="UROLOGY", active=True)


@pytest.fixture
def program(department):
    return TrainingProgram.objects.create(
        name="MS Urology", code="MS-URO", duration_months=48, department=department
    )


@pytest.fixture
def wired_identities(hospital, department, program):
    """Reproduces the pre-repair production shape: canonical demo logins each with their own
    empty profile, plus separately-named real accounts holding the real Urology data."""
    login_supervisor = User.objects.create_user(
        username="supervisor", password="x", role="SUPERVISOR", first_name="Supervisor", last_name="User",
    )
    login_resident = User.objects.create_user(
        username="resident", password="x", role="RESIDENT", first_name="Resident", last_name="User",
    )
    SupervisorProfile.objects.create(user=login_supervisor)
    ResidentProfile.objects.create(user=login_resident)

    real_supervisor = User.objects.create_user(
        username="supmtahirbashirmalik", password="x", role="SUPERVISOR",
        first_name="M.", last_name="Tahir Bashir Malik", email="tahir@example.com",
    )
    real_sup_profile = SupervisorProfile.objects.create(
        user=real_supervisor, hospital=hospital, department_ref=department,
    )

    real_resident = User.objects.create_user(
        username="pgrdrjawadsaifullah", password="x", role="RESIDENT",
        first_name="Dr. Jawad", last_name="Saifullah", email="jawad@example.com",
    )
    real_res_profile = ResidentProfile.objects.create(
        user=real_resident, hospital=hospital, department_ref=department,
    )
    ResidentTrainingRecord.objects.create(
        resident_user=real_resident, program=program, start_date=date(2022, 1, 1), current_level="y5",
    )
    ResidentSupervisorAssignment.objects.create(
        resident=real_res_profile, supervisor=real_sup_profile,
        assignment_type=ResidentSupervisorAssignment.ASSIGNMENT_PRIMARY, start_date=date(2022, 1, 1),
    )

    return {
        "login_supervisor": login_supervisor,
        "login_resident": login_resident,
        "real_supervisor": real_supervisor,
        "real_resident": real_resident,
        "real_sup_profile": real_sup_profile,
        "real_res_profile": real_res_profile,
    }


@pytest.mark.django_db
class TestReconcileUrologySupervisorProfiles:
    def test_supervisor_login_resolves_to_tahir(self, wired_identities):
        call_command(COMMAND)
        u = User.objects.get(username="supervisor")
        assert u.get_full_name() == "M. Tahir Bashir Malik"
        assert u.role == "SUPERVISOR"
        assert u.supervisor_profile.pk == wired_identities["real_sup_profile"].pk
        assert u.supervisor_profile.department_ref.code == "UROLOGY"

    def test_resident_login_resolves_to_jawad(self, wired_identities):
        call_command(COMMAND)
        u = User.objects.get(username="resident")
        assert u.get_full_name() == "Dr. Jawad Saifullah"
        assert u.resident_profile.pk == wired_identities["real_res_profile"].pk

    def test_resident_training_record_follows_login_user(self, wired_identities):
        call_command(COMMAND)
        u = User.objects.get(username="resident")
        tr = ResidentTrainingRecord.objects.get(resident_user=u)
        assert tr.program.code == "MS-URO"

    def test_supervisor_sees_only_own_resident(self, wired_identities):
        call_command(COMMAND)
        supervisor = User.objects.get(username="supervisor")
        assignments = ResidentSupervisorAssignment.objects.filter(
            supervisor=supervisor.supervisor_profile, is_active=True
        )
        assert assignments.count() == 1
        assert assignments.first().resident.user.username == "resident"

    def test_resident_supervisor_traversal(self, wired_identities):
        call_command(COMMAND)
        resident = User.objects.get(username="resident")
        assignment = ResidentSupervisorAssignment.objects.get(resident=resident.resident_profile, is_active=True)
        assert assignment.supervisor.user.username == "supervisor"

    def test_no_duplicate_profiles_or_assignments(self, wired_identities):
        call_command(COMMAND)
        assert SupervisorProfile.objects.filter(user__username="supervisor").count() == 1
        assert ResidentProfile.objects.filter(user__username="resident").count() == 1
        assert ResidentSupervisorAssignment.objects.filter(is_active=True).count() == 1

    def test_real_identity_logins_retired_not_deleted(self, wired_identities):
        call_command(COMMAND)
        real_sup = User.objects.get(username="supmtahirbashirmalik")
        real_res = User.objects.get(username="pgrdrjawadsaifullah")
        assert real_sup.is_active is False
        assert real_res.is_active is False
        # data preserved, not deleted
        assert SupervisorProfile.objects.filter(user=real_sup).exists()
        assert ResidentProfile.objects.filter(user=real_res).exists()

    def test_idempotent_second_run(self, wired_identities):
        call_command(COMMAND)
        before_sup = SupervisorProfile.objects.count()
        before_res = ResidentProfile.objects.count()
        before_asg = ResidentSupervisorAssignment.objects.count()

        out = StringIO()
        call_command(COMMAND, stdout=out)

        assert SupervisorProfile.objects.count() == before_sup
        assert ResidentProfile.objects.count() == before_res
        assert ResidentSupervisorAssignment.objects.count() == before_asg
        assert "already correct: 2" in out.getvalue() or "already linked and reconciled" in out.getvalue()

    def test_dry_run_makes_no_changes(self, wired_identities):
        call_command(COMMAND, "--dry-run")
        # login accounts still have their own original empty profiles, nothing moved
        login_sup = User.objects.get(username="supervisor")
        assert login_sup.supervisor_profile.pk != wired_identities["real_sup_profile"].pk
        assert User.objects.get(username="supmtahirbashirmalik").is_active is True
