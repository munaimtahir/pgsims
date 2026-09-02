"""Tests for sims/backup_center/management/commands/*.py -- all at 0% coverage previously.

Each command is a thin CLI wrapper around services.py / google_drive.py, which are already
covered elsewhere. These tests mock the underlying service/provider call and assert on the
command's own argument parsing, stdout messaging, exit codes, and error-handling branches --
the part of the code that's actually unique to the command layer.
"""

import io
import os
from unittest import mock

import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command, CommandError

from sims.backup_center.models import BackupCloudConnection, BackupCloudCopy, BackupJob, RestoreJob

User = get_user_model()


def run_command(name, *args, **kwargs):
    out = io.StringIO()
    err = io.StringIO()
    call_command(name, *args, stdout=out, stderr=err, **kwargs)
    return out.getvalue(), err.getvalue()


@pytest.mark.django_db
class TestCreateSystemBackupCommand:
    @mock.patch("sims.backup_center.management.commands.create_system_backup.create_routine_application_data_backup")
    def test_routine_success(self, mock_create):
        mock_create.return_value = BackupJob(id=1, file_name="a.pgsimsbak", file_path="/tmp/a.pgsimsbak")
        out, _ = run_command("create_system_backup", "--routine")
        assert "Routine backup completed" in out
        mock_create.assert_called_once()

    @mock.patch("sims.backup_center.management.commands.create_system_backup.create_routine_application_data_backup")
    def test_routine_failure_reports_error(self, mock_create):
        mock_create.side_effect = RuntimeError("disk full")
        out, _ = run_command("create_system_backup", "--routine")
        assert "Routine backup failed" in out
        assert "disk full" in out

    @mock.patch("sims.backup_center.management.commands.create_system_backup.create_disaster_recovery_backup")
    def test_disaster_success(self, mock_create):
        mock_create.return_value = BackupJob(id=2, file_name="a.pgsimsdr", file_path="/tmp/a.pgsimsdr")
        out, _ = run_command("create_system_backup", "--disaster")
        assert "Disaster backup completed" in out

    @mock.patch("sims.backup_center.management.commands.create_system_backup.create_disaster_recovery_backup")
    def test_disaster_failure_reports_error(self, mock_create):
        mock_create.side_effect = RuntimeError("boom")
        out, _ = run_command("create_system_backup", "--disaster")
        assert "Disaster backup failed" in out

    def test_requires_one_of_routine_or_disaster(self):
        with pytest.raises(CommandError):
            call_command("create_system_backup")

    @mock.patch("sims.backup_center.management.commands.create_system_backup.create_routine_application_data_backup")
    def test_passes_notes_through(self, mock_create):
        mock_create.return_value = BackupJob(id=1, file_name="a.pgsimsbak", file_path="/tmp/a.pgsimsbak")
        run_command("create_system_backup", "--routine", "--notes", "scheduled run")
        _, kwargs = mock_create.call_args
        assert kwargs.get("notes") == "scheduled run"


@pytest.mark.django_db
class TestValidateSystemBackupCommand:
    @mock.patch("sims.backup_center.management.commands.validate_system_backup.validate_backup_file")
    def test_valid_backup_prints_success(self, mock_validate):
        mock_validate.return_value = {
            "valid": True,
            "backup_kind": "routine_application_data",
            "manifest": {"app_name": "PGSIMS"},
            "table_counts": {"users.user": 3},
            "warnings": ["a warning"],
            "errors": [],
        }
        out, _ = run_command("validate_system_backup", "/tmp/fake.pgsimsbak")
        assert "STATUS: VALID" in out
        assert "a warning" in out

    @mock.patch("sims.backup_center.management.commands.validate_system_backup.validate_backup_file")
    def test_invalid_backup_prints_errors(self, mock_validate):
        mock_validate.return_value = {
            "valid": False,
            "backup_kind": "unknown",
            "manifest": {},
            "table_counts": {},
            "warnings": [],
            "errors": ["missing manifest.json"],
        }
        out, _ = run_command("validate_system_backup", "/tmp/fake.pgsimsbak")
        assert "STATUS: INVALID" in out
        assert "missing manifest.json" in out


@pytest.mark.django_db
class TestRestoreSystemBackupCommand:
    def test_missing_file_exits_nonzero(self, tmp_path):
        missing = tmp_path / "does-not-exist.pgsimsbak"
        with pytest.raises(SystemExit) as excinfo:
            call_command("restore_system_backup", str(missing))
        assert excinfo.value.code != 0

    @mock.patch("sims.backup_center.management.commands.restore_system_backup.validate_backup_file")
    def test_dry_run_valid_prints_success(self, mock_validate, tmp_path):
        f = tmp_path / "backup.pgsimsbak"
        f.write_text("content")
        mock_validate.return_value = {"valid": True, "errors": []}
        out, _ = run_command("restore_system_backup", str(f), "--dry-run")
        assert "Dry-run validation passed" in out

    @mock.patch("sims.backup_center.management.commands.restore_system_backup.validate_backup_file")
    def test_dry_run_invalid_exits_nonzero(self, mock_validate, tmp_path):
        f = tmp_path / "backup.pgsimsbak"
        f.write_text("content")
        mock_validate.return_value = {"valid": False, "errors": ["bad checksum"]}
        with pytest.raises(SystemExit) as excinfo:
            call_command("restore_system_backup", str(f), "--dry-run")
        assert excinfo.value.code != 0

    def test_confirm_without_typed_confirmation_exits(self, tmp_path):
        f = tmp_path / "backup.pgsimsbak"
        f.write_text("content")
        with pytest.raises(SystemExit):
            call_command("restore_system_backup", str(f), "--confirm")

    def test_confirm_with_wrong_typed_confirmation_exits(self, tmp_path):
        f = tmp_path / "backup.pgsimsbak"
        f.write_text("content")
        with pytest.raises(SystemExit):
            call_command(
                "restore_system_backup", str(f), "--confirm", "--typed-confirmation", "NOPE"
            )

    @mock.patch("sims.backup_center.management.commands.restore_system_backup.restore_routine_application_data_backup")
    @mock.patch("sims.backup_center.management.commands.restore_system_backup.getpass.getpass")
    @mock.patch("builtins.input")
    def test_confirm_flow_superadmin_not_found_exits(
        self, mock_input, mock_getpass, mock_restore, tmp_path
    ):
        f = tmp_path / "backup.pgsimsbak"
        f.write_text("content")
        mock_input.return_value = "nobody@example.com"
        mock_getpass.return_value = "whatever"
        with pytest.raises(SystemExit) as excinfo:
            call_command(
                "restore_system_backup", str(f), "--confirm", "--typed-confirmation", "RESTORE"
            )
        assert excinfo.value.code != 0
        mock_restore.assert_not_called()

    @mock.patch("sims.backup_center.management.commands.restore_system_backup.restore_routine_application_data_backup")
    @mock.patch("sims.backup_center.management.commands.restore_system_backup.getpass.getpass")
    @mock.patch("builtins.input")
    def test_confirm_flow_wrong_password_exits(
        self, mock_input, mock_getpass, mock_restore, tmp_path
    ):
        f = tmp_path / "backup.pgsimsbak"
        f.write_text("content")
        superuser = User.objects.create_superuser(
            username="cli_super", email="cli_super@example.com", password="correct-password"
        )
        mock_input.return_value = "cli_super@example.com"
        mock_getpass.return_value = "wrong-password"
        with pytest.raises(SystemExit) as excinfo:
            call_command(
                "restore_system_backup", str(f), "--confirm", "--typed-confirmation", "RESTORE"
            )
        assert excinfo.value.code != 0
        mock_restore.assert_not_called()

    @mock.patch("sims.backup_center.management.commands.restore_system_backup.restore_routine_application_data_backup")
    @mock.patch("sims.backup_center.management.commands.restore_system_backup.getpass.getpass")
    @mock.patch("builtins.input")
    def test_confirm_flow_success_calls_restore(
        self, mock_input, mock_getpass, mock_restore, tmp_path
    ):
        f = tmp_path / "backup.pgsimsbak"
        f.write_text("content")
        superuser = User.objects.create_superuser(
            username="cli_super2", email="cli_super2@example.com", password="correct-password"
        )
        mock_input.return_value = "cli_super2@example.com"
        mock_getpass.return_value = "correct-password"
        restored_job = RestoreJob(id=1, status="restored")
        mock_restore.return_value = restored_job

        out, _ = run_command(
            "restore_system_backup", str(f), "--confirm", "--typed-confirmation", "RESTORE"
        )
        assert "Restore completed successfully" in out
        mock_restore.assert_called_once()
        _, kwargs = mock_restore.call_args
        assert kwargs["restored_by"] == superuser

    @mock.patch("sims.backup_center.management.commands.restore_system_backup.restore_routine_application_data_backup")
    @mock.patch("sims.backup_center.management.commands.restore_system_backup.getpass.getpass")
    @mock.patch("builtins.input")
    def test_confirm_flow_reports_failed_status(
        self, mock_input, mock_getpass, mock_restore, tmp_path
    ):
        f = tmp_path / "backup.pgsimsbak"
        f.write_text("content")
        superuser = User.objects.create_superuser(
            username="cli_super3", email="cli_super3@example.com", password="correct-password"
        )
        mock_input.return_value = "cli_super3@example.com"
        mock_getpass.return_value = "correct-password"
        failed_job = RestoreJob(id=1, status="failed", error_message="dump mismatch")
        mock_restore.return_value = failed_job

        out, _ = run_command(
            "restore_system_backup", str(f), "--confirm", "--typed-confirmation", "RESTORE"
        )
        assert "Restore failed with status" in out
        assert "dump mismatch" in out

    @mock.patch("sims.backup_center.management.commands.restore_system_backup.restore_routine_application_data_backup")
    @mock.patch("sims.backup_center.management.commands.restore_system_backup.getpass.getpass")
    @mock.patch("builtins.input")
    def test_confirm_flow_service_exception_exits(
        self, mock_input, mock_getpass, mock_restore, tmp_path
    ):
        f = tmp_path / "backup.pgsimsbak"
        f.write_text("content")
        User.objects.create_superuser(
            username="cli_super4", email="cli_super4@example.com", password="correct-password"
        )
        mock_input.return_value = "cli_super4@example.com"
        mock_getpass.return_value = "correct-password"
        mock_restore.side_effect = RuntimeError("catastrophic failure")

        with pytest.raises(SystemExit) as excinfo:
            call_command(
                "restore_system_backup", str(f), "--confirm", "--typed-confirmation", "RESTORE"
            )
        assert excinfo.value.code != 0

    @mock.patch("builtins.input")
    def test_interactive_prompt_abort(self, mock_input, tmp_path):
        f = tmp_path / "backup.pgsimsbak"
        f.write_text("content")
        mock_input.return_value = "not restore"
        with pytest.raises(SystemExit):
            call_command("restore_system_backup", str(f))


@pytest.mark.django_db
class TestGoogleDriveBackupStatusCommand:
    def test_no_connection_row(self):
        out, _ = run_command("google_drive_backup_status")
        assert "not_connected" in out

    def test_reports_existing_connection(self):
        BackupCloudConnection.objects.create(
            provider="google_drive", status="connected", account_email="ops@example.com"
        )
        out, _ = run_command("google_drive_backup_status")
        assert "status=connected" in out
        assert "ops@example.com" in out


@pytest.mark.django_db
class TestGoogleDriveBackupHealthCheckCommand:
    def test_raises_when_not_connected(self):
        with pytest.raises(CommandError, match="not connected"):
            call_command("google_drive_backup_health_check")

    @mock.patch("sims.backup_center.management.commands.google_drive_backup_health_check.GoogleDriveBackupProvider")
    def test_success_prints_result(self, mock_provider_cls):
        BackupCloudConnection.objects.create(provider="google_drive", status="connected")
        mock_provider_cls.return_value.health_check.return_value = {"status": "healthy"}
        out, _ = run_command("google_drive_backup_health_check")
        assert "healthy" in out


@pytest.mark.django_db
class TestUploadBackupToGoogleDriveCommand:
    def test_backup_not_found_raises(self):
        with pytest.raises(CommandError, match="not found"):
            call_command("upload_backup_to_google_drive", "--backup-id", "99999")

    @mock.patch("sims.backup_center.management.commands.upload_backup_to_google_drive.GoogleDriveBackupProvider")
    def test_success_prints_result(self, mock_provider_cls):
        job = BackupJob.objects.create(backup_kind="routine_application_data", status="completed")
        cloud_copy = mock.MagicMock(id=5, remote_file_id="drive-id-1")
        mock_provider_cls.return_value.upload_backup.return_value = cloud_copy
        out, _ = run_command("upload_backup_to_google_drive", "--backup-id", str(job.id))
        assert "uploaded cloud_copy_id=5" in out
        assert "drive-id-1" in out


@pytest.mark.django_db
class TestVerifyGoogleDriveBackupCommand:
    def test_backup_not_found_raises(self):
        with pytest.raises(CommandError, match="not found"):
            call_command("verify_google_drive_backup", "--backup-id", "99999")

    def test_no_cloud_copy_raises(self):
        job = BackupJob.objects.create(backup_kind="routine_application_data", status="completed")
        with pytest.raises(CommandError, match="No Google Drive cloud copy found"):
            call_command("verify_google_drive_backup", "--backup-id", str(job.id))

    @mock.patch("sims.backup_center.management.commands.verify_google_drive_backup.GoogleDriveBackupProvider")
    def test_success_marks_verified(self, mock_provider_cls):
        job = BackupJob.objects.create(backup_kind="routine_application_data", status="completed")
        connection = BackupCloudConnection.objects.create(provider="google_drive", status="connected")
        cloud_copy = BackupCloudCopy.objects.create(
            backup_record=job,
            provider="google_drive",
            connection=connection,
            remote_file_id="drive-id-1",
        )
        out, _ = run_command("verify_google_drive_backup", "--backup-id", str(job.id))
        assert f"verified cloud_copy_id={cloud_copy.id}" in out
        cloud_copy.refresh_from_db()
        assert cloud_copy.verification_status == "verified"
        assert cloud_copy.verified_at is not None


@pytest.mark.django_db
class TestDownloadGoogleDriveBackupCommand:
    def test_cloud_copy_not_found_raises(self):
        with pytest.raises(CommandError, match="not found"):
            call_command("download_google_drive_backup", "--cloud-copy-id", "99999")

    def test_unverified_copy_raises(self):
        job = BackupJob.objects.create(backup_kind="routine_application_data", status="completed")
        connection = BackupCloudConnection.objects.create(provider="google_drive", status="connected")
        cloud_copy = BackupCloudCopy.objects.create(
            backup_record=job,
            provider="google_drive",
            connection=connection,
            remote_file_id="drive-id-1",
            verification_status="not_uploaded",
        )
        with pytest.raises(CommandError, match="not verified"):
            call_command("download_google_drive_backup", "--cloud-copy-id", str(cloud_copy.id))

    @mock.patch("sims.backup_center.management.commands.download_google_drive_backup.GoogleDriveBackupProvider")
    def test_success_creates_restore_job(self, mock_provider_cls, tmp_path):
        job = BackupJob.objects.create(backup_kind="routine_application_data", status="completed")
        connection = BackupCloudConnection.objects.create(provider="google_drive", status="connected")
        cloud_copy = BackupCloudCopy.objects.create(
            backup_record=job,
            provider="google_drive",
            connection=connection,
            remote_file_id="drive-id-1",
            remote_file_name="backup.pgsimsbak.enc",
            verification_status="verified",
        )

        def fake_download(*, cloud_copy, destination_path):
            with open(destination_path, "wb") as f:
                f.write(b"restored content")
            return destination_path

        mock_provider_cls.return_value.download_backup.side_effect = fake_download

        out, _ = run_command(
            "download_google_drive_backup", "--cloud-copy-id", str(cloud_copy.id)
        )
        assert "restore_ready" in out
        cloud_copy.refresh_from_db()
        assert cloud_copy.download_status == "restore_ready"
        restore_job = RestoreJob.objects.get()
        assert restore_job.uploaded_file
