"""
Coverage push for sims/users/management/commands/* that were at 0% coverage:
repair_identity_profiles, create_superadmin, recompute_data_quality,
reset_pilot_data, seed_e2e, import_trainees, preview_trainees.

repair_identity_profiles.py matters most: it is the identity-repair safety
net AGENTS.md tells agents to rerun after touching identity/profile code.
While writing these tests we found (and fixed, separately) a real bug in
that command: its legacy-role remap branch compared a *lowercased* role
string against *uppercase* literals (e.g. `role_lower in ["ADMIN", ...]`),
so it could never match and every legacy-role user was misclassified as
"invalid" instead of being remapped. The fix restores the mapping from
AGENTS.md section 4 (UTRMC_ADMIN/SUPER_ADMIN/SYSTEM_ADMIN -> ADMIN, etc.).
The tests below exercise both the remap path and the now-unreachable
"still invalid" path.
"""
import io
import tempfile

from django.contrib.auth import get_user_model
from django.core.management import call_command, CommandError
from django.test import TestCase

from sims.academics.models import Department
from sims.rotations.models import Hospital, HospitalDepartment
from sims.users.models import (
    AdminProfile,
    ResidentProfile,
    SupervisorProfile,
    SupportStaffProfile,
)

User = get_user_model()


class RepairIdentityProfilesCommandTests(TestCase):
    def _run(self):
        out = io.StringIO()
        call_command("repair_identity_profiles", stdout=out)
        return out.getvalue()

    def test_creates_missing_profile_for_valid_role_user(self):
        user = User.objects.create_user(username="repair_res1", password="x", role="RESIDENT")
        self.assertFalse(hasattr(user, "resident_profile"))
        output = self._run()
        user.refresh_from_db()
        self.assertTrue(ResidentProfile.objects.filter(user=user).exists())
        self.assertIn("Final status: PASS", output)

    def test_deletes_mismatched_profile(self):
        user = User.objects.create_user(username="repair_res2", password="x", role="SUPERVISOR")
        # Create the profile while its role is valid, then make the identity
        # mismatched.  Profile.save() intentionally rejects invalid role links.
        SupervisorProfile.objects.create(user=user)
        User.objects.filter(pk=user.pk).update(role="RESIDENT")
        self._run()
        user.refresh_from_db()
        self.assertFalse(SupervisorProfile.objects.filter(user=user).exists())
        self.assertTrue(ResidentProfile.objects.filter(user=user).exists())

    def test_legacy_role_remap_admin(self):
        user = User.objects.create_user(username="repair_legacy_admin", password="x", role="RESIDENT")
        User.objects.filter(pk=user.pk).update(role="UTRMC_ADMIN")
        self._run()
        user.refresh_from_db()
        self.assertEqual(user.role, "ADMIN")
        self.assertTrue(AdminProfile.objects.filter(user=user).exists())

    def test_legacy_role_remap_supervisor(self):
        user = User.objects.create_user(username="repair_legacy_sup", password="x", role="RESIDENT")
        User.objects.filter(pk=user.pk).update(role="TEACHER")
        self._run()
        user.refresh_from_db()
        self.assertEqual(user.role, "SUPERVISOR")
        self.assertTrue(SupervisorProfile.objects.filter(user=user).exists())

    def test_legacy_role_remap_resident(self):
        user = User.objects.create_user(username="repair_legacy_res", password="x", role="ADMIN")
        User.objects.filter(pk=user.pk).update(role="STUDENT")
        self._run()
        user.refresh_from_db()
        self.assertEqual(user.role, "RESIDENT")
        self.assertTrue(ResidentProfile.objects.filter(user=user).exists())

    def test_legacy_role_remap_support_staff(self):
        user = User.objects.create_user(username="repair_legacy_staff", password="x", role="RESIDENT")
        User.objects.filter(pk=user.pk).update(role="CLERK")
        self._run()
        user.refresh_from_db()
        self.assertEqual(user.role, "SUPPORT_STAFF")
        self.assertTrue(SupportStaffProfile.objects.filter(user=user).exists())

    def test_unrecognized_role_marked_invalid(self):
        user = User.objects.create_user(username="repair_unknown", password="x", role="RESIDENT")
        User.objects.filter(pk=user.pk).update(role="TOTALLY_UNKNOWN_ROLE")
        output = self._run()
        self.assertIn("invalid/unknown role", output)
        self.assertIn("Final status: FAIL", output)

    def test_idempotent_on_already_correct_users(self):
        user = User.objects.create_user(username="repair_ok", password="x", role="ADMIN")
        AdminProfile.objects.create(user=user, profile_status="COMPLETE")
        output = self._run()
        self.assertIn("Final status: PASS", output)
        self.assertEqual(AdminProfile.objects.filter(user=user).count(), 1)


class CreateSuperadminCommandTests(TestCase):
    def test_creates_new_superadmin(self):
        out = io.StringIO()
        call_command("create_superadmin", stdout=out)
        user = User.objects.get(username="admin")
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertEqual(user.role, "ADMIN")
        self.assertTrue(user.check_password("admin123"))
        self.assertTrue(AdminProfile.objects.filter(user=user).exists())
        self.assertIn("Superadmin created", out.getvalue())

    def test_ensures_existing_user_promoted(self):
        User.objects.create_user(username="admin", password="whatever", role="RESIDENT")
        out = io.StringIO()
        call_command("create_superadmin", stdout=out)
        user = User.objects.get(username="admin")
        self.assertEqual(user.role, "ADMIN")
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertIn("Superadmin ensured", out.getvalue())

    def test_reset_password_flag(self):
        call_command("create_superadmin")
        out = io.StringIO()
        call_command("create_superadmin", "--reset-password", stdout=out)
        user = User.objects.get(username="admin")
        self.assertTrue(user.check_password("admin123"))
        self.assertIn("admin123", out.getvalue())

    def test_custom_username_and_password(self):
        out = io.StringIO()
        call_command(
            "create_superadmin",
            "--username=customadmin",
            "--password=custompass123",
            stdout=out,
        )
        user = User.objects.get(username="customadmin")
        self.assertTrue(user.check_password("custompass123"))


class RecomputeDataQualityCommandTests(TestCase):
    def test_recompute_all_users(self):
        User.objects.create_user(username="rdq_res1", password="x", role="RESIDENT", email="")
        out = io.StringIO()
        call_command("recompute_data_quality", stdout=out)
        output = out.getvalue()
        self.assertIn("Recompute complete", output)
        self.assertIn("Total users processed", output)

    def test_recompute_specific_user(self):
        user = User.objects.create_user(username="rdq_res2", password="x", role="RESIDENT")
        out = io.StringIO()
        call_command("recompute_data_quality", f"--user-id={user.id}", stdout=out)
        self.assertIn(f"Recomputing flags for user {user.id}", out.getvalue())

    def test_recompute_user_not_found(self):
        out = io.StringIO()
        call_command("recompute_data_quality", "--user-id=999999", stdout=out)
        self.assertIn("not found", out.getvalue())


class ResetPilotDataCommandTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="ADMIN", password="x", email="a@a.com", role="ADMIN"
        )
        self.resident = User.objects.create_user(
            username="pilot_resident", password="x", role="RESIDENT"
        )

    def test_dry_run_makes_no_changes(self):
        out = io.StringIO()
        call_command("reset_pilot_data", stdout=out)
        self.assertIn("DRY-RUN", out.getvalue())
        self.assertTrue(User.objects.filter(username="pilot_resident").exists())

    def test_confirm_deletes_non_preserved_users(self):
        out = io.StringIO()
        call_command("reset_pilot_data", "--confirm", stdout=out)
        self.assertIn("reset completed successfully", out.getvalue())
        self.assertFalse(User.objects.filter(username="pilot_resident").exists())
        self.assertTrue(User.objects.filter(username="ADMIN").exists())


class SeedE2ECommandTests(TestCase):
    def test_seed_e2e_creates_deterministic_fixtures(self):
        out = io.StringIO()
        call_command("seed_e2e", stdout=out)
        self.assertIn("seed_e2e completed successfully", out.getvalue())
        self.assertTrue(User.objects.filter(username="e2e_admin").exists())
        self.assertTrue(User.objects.filter(username="e2e_pg").exists())
        self.assertTrue(Hospital.objects.filter(code="UTRMC", is_active=True).exists())

    def test_seed_e2e_is_idempotent(self):
        call_command("seed_e2e")
        out = io.StringIO()
        call_command("seed_e2e", stdout=out)
        self.assertIn("seed_e2e completed successfully", out.getvalue())
        self.assertEqual(User.objects.filter(username="e2e_admin").count(), 1)


def _write_trainee_csv(rows):
    header = "Sr. No.,Name of Trainee,Date of Joining,MS/FCPS,Supervisor Name\n"
    body = "\n".join(rows)
    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".csv", delete=False, newline=""
    )
    tmp.write(header + body + "\n")
    tmp.flush()
    tmp.close()
    return tmp.name


class PreviewTraineesCommandTests(TestCase):
    def test_file_not_found(self):
        out = io.StringIO()
        call_command("preview_trainees", "/no/such/file.csv", stdout=out)
        self.assertIn("File not found", out.getvalue())

    def test_preview_valid_csv(self):
        path = _write_trainee_csv(
            ["1,John Doe,2024-01-01,FCPS,Dr Smith", "2,,2024-01-02,FCPS,Dr Smith"]
        )
        out = io.StringIO()
        call_command("preview_trainees", path, stdout=out)
        output = out.getvalue()
        self.assertIn("TRAINEE DATA PREVIEW", output)
        self.assertIn("Valid trainees: 1", output)
        self.assertIn("Warnings/Errors: 1", output)


class ImportTraineesCommandTests(TestCase):
    def test_file_not_found(self):
        out = io.StringIO()
        call_command("import_trainees", "/no/such/file.csv", "--dry-run", stdout=out)
        self.assertIn("File not found", out.getvalue())

    def test_creates_admin_user_and_imports_dry_run(self):
        path = _write_trainee_csv(["1,Jane Roe,2024-01-01,FCPS,Dr Jones"])
        out = io.StringIO()
        call_command("import_trainees", path, "--dry-run", stdout=out)
        output = out.getvalue()
        self.assertIn("Importing trainees from", output)
        self.assertTrue(User.objects.filter(username="import_admin", role="ADMIN").exists())
        self.assertIn("IMPORT RESULTS", output)


class RemainingUserCommandSmokeTests(TestCase):
    """Exercise the command entry branches that do not require pilot input files."""

    def test_cleanup_runtime_defaults_to_dry_run(self):
        out = io.StringIO()
        call_command("cleanup_pilot_runtime", stdout=out)
        self.assertIn("Mode: DRY-RUN", out.getvalue())

    def test_seed_org_data_dry_run(self):
        out = io.StringIO()
        call_command("seed_org_data", "--dry-run", stdout=out)
        self.assertIn("DRY RUN", out.getvalue())
        self.assertEqual(Department.objects.count(), 0)

    def test_seed_pilot_masters_is_idempotent(self):
        out = io.StringIO()
        call_command("seed_pilot_masters", stdout=out)
        call_command("seed_pilot_masters", stdout=io.StringIO())
        self.assertIn("Institutions:", out.getvalue())

    def test_active_surface_requires_org_data(self):
        err = io.StringIO()
        call_command("seed_active_surface_baseline", stderr=err)
        self.assertIn("seed_org_data must run", err.getvalue())

    def test_pilot_bundle_requires_admin_actor(self):
        with self.assertRaises(CommandError):
            call_command("import_pilot_bundle")
