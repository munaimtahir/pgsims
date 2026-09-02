"""Tests for the backup/restore orchestration flows in sims/backup_center/services.py.

Unlike test_services_utils.py (which covers small deterministic helpers), this file
exercises create_routine_application_data_backup / create_disaster_recovery_backup /
validate_backup_file / restore_routine_application_data_backup against real files on disk
(sqlite backend, real zip archives, real checksums) rather than mocking away the core logic.

The destructive-restore code path calls `connection.close()` before wiping and reloading
tables. Under the test's sqlite ":memory:" database that would destroy the schema itself
(the whole point of `:memory:` is that it only exists for the lifetime of one connection),
which is a test-environment limitation rather than anything wrong with the production code
(which targets a real on-disk sqlite/postgres database). We patch only that no-op-in-tests
`connection.close()` infra call for the one full end-to-end restore test, and let every other
part of the restore (row deletion, dumpdata/loaddata round-trip, file/zip handling) run for
real.
"""

import os
import shutil
import tempfile
import zipfile
from pathlib import Path
from unittest import mock

from django.conf import settings
from django.test import TestCase, override_settings

from django.contrib.auth import get_user_model

from sims.backup_center.models import BackupJob, RestoreJob, BackupAuditLog
from sims.backup_center.services import (
    create_routine_application_data_backup,
    create_disaster_recovery_backup,
    validate_backup_file,
    restore_routine_application_data_backup,
)

User = get_user_model()


class BackupCenterOrchestrationTestBase(TestCase):
    def setUp(self):
        self.tmp_backup_dir = Path(tempfile.mkdtemp(prefix="pgsims_backup_test_"))
        self.addCleanup(shutil.rmtree, self.tmp_backup_dir, ignore_errors=True)
        self._settings_patch = mock.patch.dict(
            settings.SIMS_SETTINGS, {"BACKUP_LOCATION": self.tmp_backup_dir}
        )
        self._settings_patch.start()
        self.addCleanup(self._settings_patch.stop)

        # NOTE: create_routine_application_data_backup() sets media_included=True purely
        # from `media_root.exists()` (services.py ~L241), even when that directory is
        # empty. validate_backup_file() then requires at least one "media/" zip entry
        # whenever manifest.media_included is true (services.py ~L527-530), so an empty
        # (but existing) MEDIA_ROOT makes every real backup fail validation. See bug note
        # in the test module docstring / final report. Point MEDIA_ROOT at a path that does
        # not exist by default so unrelated tests get the (correct) media_included=False
        # behavior; tests that want to exercise the media-included path create this
        # directory explicitly.
        self.media_root = self.tmp_backup_dir / "media_root"
        self._media_root_patch = mock.patch.object(settings, "MEDIA_ROOT", str(self.media_root))
        self._media_root_patch.start()
        self.addCleanup(self._media_root_patch.stop)

        self.admin = User.objects.create_user(
            username="backup_admin",
            password="pass12345",
            role="ADMIN",
            is_staff=True,
            is_superuser=True,
        )
        self.non_admin = User.objects.create_user(
            username="backup_regular",
            password="pass12345",
            role="ADMIN",
            is_superuser=False,
        )


class CreateRoutineApplicationDataBackupTests(BackupCenterOrchestrationTestBase):
    def test_creates_completed_job_with_real_zip_file(self):
        job = create_routine_application_data_backup(user=self.admin, notes="unit test backup")

        self.assertEqual(job.status, "completed")
        self.assertTrue(job.file_path)
        self.assertTrue(os.path.exists(job.file_path))
        self.assertTrue(job.file_name.endswith(".pgsimsbak"))
        self.assertGreater(job.file_size, 0)
        self.assertTrue(job.checksum)
        self.assertEqual(job.manifest_json["app_name"], "PGSIMS")
        self.assertEqual(job.manifest_json["backup_format_version"], "1.2")
        self.assertIn("users.user", job.table_counts_json)

        with zipfile.ZipFile(job.file_path) as zf:
            names = zf.namelist()
            self.assertIn("manifest.json", names)
            self.assertIn("backup_report.json", names)
            self.assertIn("checksum.sha256", names)
            self.assertIn("database_dump.json", names)

        self.assertTrue(
            BackupAuditLog.objects.filter(
                backup_job=job, action="routine_backup_completed"
            ).exists()
        )
        self.assertTrue(
            BackupAuditLog.objects.filter(
                backup_job=job, action="routine_backup_started"
            ).exists()
        )

    def test_includes_media_when_media_root_has_files(self):
        self.media_root.mkdir(parents=True, exist_ok=True)
        marker = self.media_root / "backup_center_test_marker.txt"
        marker.write_text("hello media")

        job = create_routine_application_data_backup(user=self.admin)

        self.assertTrue(job.media_included)
        self.assertIn("tree_sha256", job.media_summary_json)
        with zipfile.ZipFile(job.file_path) as zf:
            names = zf.namelist()
            self.assertTrue(any(n.startswith("media/") for n in names))

    def test_unsupported_database_engine_marks_job_failed_and_raises(self):
        with mock.patch(
            "sims.backup_center.services.detect_database_engine",
            return_value="django.db.backends.oracle",
        ):
            with self.assertRaises(Exception):
                create_routine_application_data_backup(user=self.admin)

        job = BackupJob.objects.filter(created_by=self.admin).latest("created_at")
        self.assertEqual(job.status, "failed")
        self.assertIn("Unsupported database engine", job.error_message)
        self.assertTrue(
            BackupAuditLog.objects.filter(
                backup_job=job, action="routine_backup_failed"
            ).exists()
        )


class CreateDisasterRecoveryBackupTests(BackupCenterOrchestrationTestBase):
    def test_creates_completed_disaster_bundle_containing_routine_backup(self):
        job = create_disaster_recovery_backup(user=self.admin, notes="dr test")

        self.assertEqual(job.status, "completed")
        self.assertTrue(job.file_name.endswith(".pgsimsdr"))
        self.assertTrue(os.path.exists(job.file_path))

        with zipfile.ZipFile(job.file_path) as zf:
            names = zf.namelist()
            self.assertIn("deployment_metadata.json", names)
            self.assertIn("env.template", names)
            self.assertIn("restore_instructions.md", names)
            self.assertTrue(any(n.endswith(".pgsimsbak") for n in names))

        # An internal routine backup job should also have been created.
        self.assertTrue(
            BackupJob.objects.filter(
                backup_kind="routine_application_data", backup_type="automatic"
            ).exists()
        )
        self.assertTrue(
            BackupAuditLog.objects.filter(
                backup_job=job, action="disaster_backup_completed"
            ).exists()
        )


class ValidateBackupFileTests(BackupCenterOrchestrationTestBase):
    def test_missing_file_reports_error(self):
        result = validate_backup_file(str(self.tmp_backup_dir / "does-not-exist.pgsimsbak"))
        self.assertFalse(result["valid"])
        self.assertIn("File does not exist.", result["errors"])

    def test_non_zip_file_reports_error(self):
        bogus = self.tmp_backup_dir / "bogus.pgsimsbak"
        bogus.write_text("not a zip")
        result = validate_backup_file(str(bogus))
        self.assertFalse(result["valid"])
        self.assertIn("File is not a valid ZIP archive.", result["errors"])

    def test_real_routine_backup_validates_successfully(self):
        job = create_routine_application_data_backup(user=self.admin)
        result = validate_backup_file(job.file_path)
        self.assertTrue(result["valid"])
        self.assertTrue(result["can_restore"])
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["backup_kind"], "routine_application_data")

    def test_real_disaster_backup_validates_successfully(self):
        job = create_disaster_recovery_backup(user=self.admin)
        result = validate_backup_file(job.file_path)
        self.assertTrue(result["valid"], result["errors"])
        self.assertEqual(result["backup_kind"], "disaster_recovery")

    def test_tampered_database_dump_fails_checksum_integrity_check(self):
        job = create_routine_application_data_backup(user=self.admin)

        tampered_path = self.tmp_backup_dir / "tampered.pgsimsbak"
        with zipfile.ZipFile(job.file_path, "r") as src:
            with zipfile.ZipFile(tampered_path, "w") as dst:
                for item in src.infolist():
                    data = src.read(item.filename)
                    if item.filename == "database_dump.json":
                        data = data + b"tampered"
                    dst.writestr(item, data)

        result = validate_backup_file(str(tampered_path))
        self.assertFalse(result["valid"])
        self.assertTrue(
            any("integrity check failed" in e.lower() for e in result["errors"])
        )

    def test_missing_manifest_reports_error(self):
        job = create_routine_application_data_backup(user=self.admin)
        stripped_path = self.tmp_backup_dir / "no_manifest.pgsimsbak"
        with zipfile.ZipFile(job.file_path, "r") as src:
            with zipfile.ZipFile(stripped_path, "w") as dst:
                for item in src.infolist():
                    if item.filename == "manifest.json":
                        continue
                    dst.writestr(item, src.read(item.filename))

        result = validate_backup_file(str(stripped_path))
        self.assertFalse(result["valid"])
        self.assertIn("manifest.json is missing.", result["errors"])

    def test_wrong_app_name_in_manifest_reports_error(self):
        job = create_routine_application_data_backup(user=self.admin)
        bad_path = self.tmp_backup_dir / "bad_app_name.pgsimsbak"
        with zipfile.ZipFile(job.file_path, "r") as src:
            with zipfile.ZipFile(bad_path, "w") as dst:
                for item in src.infolist():
                    data = src.read(item.filename)
                    if item.filename == "manifest.json":
                        import json

                        manifest = json.loads(data)
                        manifest["app_name"] = "NOT_PGSIMS"
                        data = json.dumps(manifest).encode("utf-8")
                    dst.writestr(item, data)

        result = validate_backup_file(str(bad_path))
        self.assertFalse(result["valid"])
        self.assertIn("Not a PGSIMS backup file.", result["errors"])

    def test_unsupported_extension_reports_error(self):
        path = self.tmp_backup_dir / "weird.zip"
        with zipfile.ZipFile(path, "w") as zf:
            zf.writestr("hello.txt", "hi")
        result = validate_backup_file(str(path))
        self.assertFalse(result["valid"])
        self.assertTrue(any("Unsupported file extension" in e for e in result["errors"]))

    def test_disaster_bundle_missing_internal_backup_reports_error(self):
        job = create_disaster_recovery_backup(user=self.admin)
        stripped_path = self.tmp_backup_dir / "no_internal.pgsimsdr"
        with zipfile.ZipFile(job.file_path, "r") as src:
            with zipfile.ZipFile(stripped_path, "w") as dst:
                for item in src.infolist():
                    if item.filename.endswith(".pgsimsbak"):
                        continue
                    dst.writestr(item, src.read(item.filename))

        result = validate_backup_file(str(stripped_path))
        self.assertFalse(result["valid"])
        self.assertIn(
            "Internal .pgsimsbak file missing from disaster bundle.", result["errors"]
        )


class RestoreRoutineApplicationDataBackupTests(BackupCenterOrchestrationTestBase):
    def test_non_superuser_denied(self):
        job = create_routine_application_data_backup(user=self.admin)
        with self.assertRaisesMessage(Exception, "Access Denied"):
            restore_routine_application_data_backup(
                file_path=job.file_path,
                restored_by=self.non_admin,
                password_confirmed=True,
                typed_confirmation="RESTORE",
                dry_run=False,
            )

    def test_missing_password_confirmation_raises(self):
        job = create_routine_application_data_backup(user=self.admin)
        with self.assertRaisesMessage(Exception, "Password confirmation required."):
            restore_routine_application_data_backup(
                file_path=job.file_path,
                restored_by=self.admin,
                password_confirmed=False,
                typed_confirmation="RESTORE",
                dry_run=False,
            )

    def test_wrong_typed_confirmation_raises(self):
        job = create_routine_application_data_backup(user=self.admin)
        with self.assertRaisesMessage(Exception, "Typed confirmation 'RESTORE' required."):
            restore_routine_application_data_backup(
                file_path=job.file_path,
                restored_by=self.admin,
                password_confirmed=True,
                typed_confirmation="wrong",
                dry_run=False,
            )

    def test_dry_run_with_valid_backup_marks_validation_passed(self):
        job = create_routine_application_data_backup(user=self.admin)
        restore_job = restore_routine_application_data_backup(
            file_path=job.file_path,
            restored_by=self.admin,
            dry_run=True,
        )
        self.assertEqual(restore_job.status, "validation_passed")
        self.assertTrue(restore_job.validation_result_json["valid"])
        self.assertTrue(
            BackupAuditLog.objects.filter(
                restore_job=restore_job, action="restore_dry_run_completed"
            ).exists()
        )

    def test_dry_run_with_invalid_backup_marks_validation_failed(self):
        bogus = self.tmp_backup_dir / "bogus.pgsimsbak"
        bogus.write_text("not a zip")
        restore_job = restore_routine_application_data_backup(
            file_path=str(bogus),
            restored_by=self.admin,
            dry_run=True,
        )
        self.assertEqual(restore_job.status, "validation_failed")
        self.assertFalse(restore_job.validation_result_json["valid"])
        self.assertTrue(
            BackupAuditLog.objects.filter(
                restore_job=restore_job, action="restore_validation_failed"
            ).exists()
        )

    def test_disaster_bundle_dry_run_resolves_to_internal_routine_backup(self):
        job = create_disaster_recovery_backup(user=self.admin)
        restore_job = restore_routine_application_data_backup(
            file_path=job.file_path,
            restored_by=self.admin,
            dry_run=True,
        )
        self.assertEqual(restore_job.status, "validation_passed")

    def test_safety_backup_failure_marks_restore_failed(self):
        job = create_routine_application_data_backup(user=self.admin)

        with mock.patch(
            "sims.backup_center.services.create_routine_application_data_backup",
            side_effect=Exception("disk full"),
        ):
            with self.assertRaisesMessage(Exception, "Failed to create safety backup"):
                restore_routine_application_data_backup(
                    file_path=job.file_path,
                    restored_by=self.admin,
                    password_confirmed=True,
                    typed_confirmation="RESTORE",
                    dry_run=False,
                )

        restore_job = RestoreJob.objects.filter(restored_by=self.admin).latest("started_at")
        self.assertEqual(restore_job.status, "failed")
        self.assertIn("Failed to create safety backup", restore_job.error_message)
        self.assertTrue(
            BackupAuditLog.objects.filter(
                restore_job=restore_job, action="restore_failed"
            ).exists()
        )

    def test_full_sqlite_restore_round_trip(self):
        """
        End-to-end: back up, mutate state, restore, and confirm the pre-backup state came
        back. `connection.close()` is a no-op here only because the test sqlite database is
        ":memory:" and would otherwise be destroyed outright when closed (a test-harness
        limitation, not a change to the restore logic itself) -- the actual delete-then-
        loaddata restore body runs unmodified against the real in-memory database.
        """
        job = create_routine_application_data_backup(user=self.admin)

        # Mutate state after the backup was taken.
        extra_user = User.objects.create_user(
            username="post_backup_user", password="pass12345", role="ADMIN"
        )
        self.assertTrue(User.objects.filter(username="post_backup_user").exists())

        with mock.patch("django.db.connection.close"):
            restored_record = restore_routine_application_data_backup(
                file_path=job.file_path,
                restored_by=self.admin,
                password_confirmed=True,
                typed_confirmation="RESTORE",
                dry_run=False,
            )

        self.assertEqual(restored_record.status, "restored")
        self.assertIsNotNone(restored_record.completed_at)
        self.assertTrue(restored_record.post_restore_check_json["database_accessible"])

        # The admin present at backup time should have been restored...
        self.assertTrue(User.objects.filter(username="backup_admin").exists())
        # ...but state created strictly after the backup should be gone.
        self.assertFalse(User.objects.filter(username="post_backup_user").exists())

        self.assertTrue(
            BackupAuditLog.objects.filter(
                restore_job=restored_record, action="restore_completed"
            ).exists()
        )
