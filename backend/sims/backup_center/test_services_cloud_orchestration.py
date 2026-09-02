"""Tests for the generic cloud-storage orchestration helpers in sims/backup_center/services.py
that had zero prior coverage: upload_backup_to_cloud_service, download_backup_from_cloud_service,
verify_cloud_backup_service, and enforce_cloud_retention_policy.

These functions delegate all real cloud-SDK work to sims.backup_center.providers.get_storage_provider(),
so the provider itself is mocked here (its own logic is covered directly in test_providers.py) and
these tests focus on the orchestration: BackupJob field bookkeeping, BackupAuditLog entries, and
error-handling branches when the provider raises or reports failure.
"""

import os
import shutil
import tempfile
from pathlib import Path
from unittest import mock

from django.conf import settings
from django.test import TestCase

from sims.backup_center.models import BackupAuditLog, BackupJob
from sims.backup_center.services import (
    download_backup_from_cloud_service,
    enforce_cloud_retention_policy,
    upload_backup_to_cloud_service,
    verify_cloud_backup_service,
)


class CloudOrchestrationTestBase(TestCase):
    def setUp(self):
        self.tmp_backup_dir = Path(tempfile.mkdtemp(prefix="pgsims_cloud_test_"))
        self.addCleanup(shutil.rmtree, self.tmp_backup_dir, ignore_errors=True)
        self._settings_patch = mock.patch.dict(
            settings.SIMS_SETTINGS, {"BACKUP_LOCATION": self.tmp_backup_dir}
        )
        self._settings_patch.start()
        self.addCleanup(self._settings_patch.stop)


class UploadBackupToCloudServiceTests(CloudOrchestrationTestBase):
    @mock.patch("sims.backup_center.providers.get_storage_provider")
    def test_success_updates_job_and_logs_audit(self, mock_get_provider):
        job = BackupJob.objects.create(backup_kind="routine_application_data", status="completed")

        mock_provider = mock.MagicMock()
        mock_provider.upload_backup.return_value = {
            "bucket": "my-bucket",
            "prefix": "pgsims/backups/",
            "backup_key": "backup-key",
            "manifest_key": "manifest-key",
            "checksum_key": "checksum-key",
            "checksum": "abc123",
            "size": 1024,
        }
        mock_provider.verify_remote_object.return_value = True
        mock_get_provider.return_value = mock_provider

        with mock.patch.dict(os.environ, {"BACKUP_CLOUD_PROVIDER": "gcs"}):
            result = upload_backup_to_cloud_service(job, actor=None)

        self.assertEqual(result.cloud_upload_status, "uploaded")
        self.assertEqual(result.cloud_bucket, "my-bucket")
        self.assertEqual(result.cloud_checksum, "abc123")
        self.assertEqual(result.cloud_file_size, 1024)
        self.assertIsNotNone(result.cloud_upload_completed_at)
        self.assertTrue(
            BackupAuditLog.objects.filter(backup_job=job, action="cloud_upload_started").exists()
        )
        self.assertTrue(
            BackupAuditLog.objects.filter(backup_job=job, action="cloud_upload_completed").exists()
        )

    @mock.patch("sims.backup_center.providers.get_storage_provider")
    def test_local_provider_raises_and_marks_failed(self, mock_get_provider):
        from sims.backup_center.providers import LocalBackupStorageProvider

        job = BackupJob.objects.create(backup_kind="routine_application_data", status="completed")
        mock_get_provider.return_value = LocalBackupStorageProvider()

        with self.assertRaises(ValueError):
            upload_backup_to_cloud_service(job, actor=None)

        job.refresh_from_db()
        self.assertEqual(job.cloud_upload_status, "failed")
        self.assertTrue(
            BackupAuditLog.objects.filter(backup_job=job, action="cloud_upload_failed").exists()
        )

    @mock.patch("sims.backup_center.providers.get_storage_provider")
    def test_verification_failure_marks_job_failed(self, mock_get_provider):
        job = BackupJob.objects.create(backup_kind="routine_application_data", status="completed")

        mock_provider = mock.MagicMock()
        mock_provider.upload_backup.return_value = {"bucket": "b", "size": 10}
        mock_provider.verify_remote_object.return_value = False
        mock_get_provider.return_value = mock_provider

        with mock.patch.dict(os.environ, {"BACKUP_CLOUD_PROVIDER": "gcs"}):
            with self.assertRaises(ValueError):
                upload_backup_to_cloud_service(job, actor=None)

        job.refresh_from_db()
        self.assertEqual(job.cloud_upload_status, "failed")
        self.assertIn("verification failed", job.cloud_error_message)

    @mock.patch("sims.backup_center.providers.get_storage_provider")
    def test_provider_exception_marks_job_failed_and_reraises(self, mock_get_provider):
        job = BackupJob.objects.create(backup_kind="routine_application_data", status="completed")

        mock_provider = mock.MagicMock()
        mock_provider.upload_backup.side_effect = RuntimeError("network timeout")
        mock_get_provider.return_value = mock_provider

        with mock.patch.dict(os.environ, {"BACKUP_CLOUD_PROVIDER": "s3"}):
            with self.assertRaises(RuntimeError):
                upload_backup_to_cloud_service(job, actor=None)

        job.refresh_from_db()
        self.assertEqual(job.cloud_upload_status, "failed")
        self.assertEqual(job.cloud_error_message, "network timeout")


class DownloadBackupFromCloudServiceTests(CloudOrchestrationTestBase):
    def test_raises_when_no_cloud_object_key(self):
        job = BackupJob.objects.create(backup_kind="routine_application_data", status="completed")
        with self.assertRaises(ValueError):
            download_backup_from_cloud_service(job, actor=None)

    @mock.patch("sims.backup_center.providers.get_storage_provider")
    def test_success_updates_file_path(self, mock_get_provider):
        job = BackupJob.objects.create(
            backup_kind="routine_application_data",
            status="completed",
            cloud_object_key="some/key",
            file_name="restored.pgsimsbak",
        )

        mock_provider = mock.MagicMock()
        mock_get_provider.return_value = mock_provider

        result = download_backup_from_cloud_service(job, actor=None)

        self.assertEqual(result.cloud_download_status, "downloaded")
        self.assertTrue(result.file_path.endswith("restored.pgsimsbak"))
        mock_provider.download_backup.assert_called_once()
        self.assertTrue(
            BackupAuditLog.objects.filter(
                backup_job=job, action="cloud_download_completed"
            ).exists()
        )

    @mock.patch("sims.backup_center.providers.get_storage_provider")
    def test_provider_exception_marks_failed(self, mock_get_provider):
        job = BackupJob.objects.create(
            backup_kind="routine_application_data",
            status="completed",
            cloud_object_key="some/key",
            file_name="restored.pgsimsbak",
        )
        mock_provider = mock.MagicMock()
        mock_provider.download_backup.side_effect = RuntimeError("not found remotely")
        mock_get_provider.return_value = mock_provider

        with self.assertRaises(RuntimeError):
            download_backup_from_cloud_service(job, actor=None)

        job.refresh_from_db()
        self.assertEqual(job.cloud_download_status, "failed")
        self.assertTrue(
            BackupAuditLog.objects.filter(backup_job=job, action="cloud_download_failed").exists()
        )


class VerifyCloudBackupServiceTests(CloudOrchestrationTestBase):
    def test_returns_false_when_no_cloud_object_key(self):
        job = BackupJob.objects.create(backup_kind="routine_application_data", status="completed")
        self.assertFalse(verify_cloud_backup_service(job, actor=None))

    @mock.patch("sims.backup_center.providers.get_storage_provider")
    def test_returns_true_and_marks_verified(self, mock_get_provider):
        job = BackupJob.objects.create(
            backup_kind="routine_application_data",
            status="completed",
            cloud_object_key="some/key",
        )
        mock_provider = mock.MagicMock()
        mock_provider.verify_remote_object.return_value = True
        mock_get_provider.return_value = mock_provider

        result = verify_cloud_backup_service(job, actor=None)

        self.assertTrue(result)
        job.refresh_from_db()
        self.assertEqual(job.cloud_upload_status, "verified")
        self.assertTrue(
            BackupAuditLog.objects.filter(backup_job=job, action="cloud_verified").exists()
        )

    @mock.patch("sims.backup_center.providers.get_storage_provider")
    def test_returns_false_when_provider_reports_invalid(self, mock_get_provider):
        job = BackupJob.objects.create(
            backup_kind="routine_application_data",
            status="completed",
            cloud_object_key="some/key",
        )
        mock_provider = mock.MagicMock()
        mock_provider.verify_remote_object.return_value = False
        mock_get_provider.return_value = mock_provider

        result = verify_cloud_backup_service(job, actor=None)

        self.assertFalse(result)
        job.refresh_from_db()
        self.assertEqual(job.cloud_upload_status, "failed")
        self.assertTrue(
            BackupAuditLog.objects.filter(
                backup_job=job, action="cloud_verification_failed"
            ).exists()
        )

    @mock.patch("sims.backup_center.providers.get_storage_provider")
    def test_returns_false_on_provider_exception(self, mock_get_provider):
        job = BackupJob.objects.create(
            backup_kind="routine_application_data",
            status="completed",
            cloud_object_key="some/key",
        )
        mock_provider = mock.MagicMock()
        mock_provider.verify_remote_object.side_effect = RuntimeError("boom")
        mock_get_provider.return_value = mock_provider

        result = verify_cloud_backup_service(job, actor=None)

        self.assertFalse(result)
        job.refresh_from_db()
        self.assertEqual(job.cloud_upload_status, "failed")
        self.assertEqual(job.cloud_error_message, "boom")


class EnforceCloudRetentionPolicyTests(CloudOrchestrationTestBase):
    def test_disabled_by_default(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            result = enforce_cloud_retention_policy()
        self.assertEqual(result["status"], "disabled")

    @mock.patch("sims.backup_center.providers.get_storage_provider")
    def test_deletes_backups_beyond_retention_limit(self, mock_get_provider):
        mock_provider = mock.MagicMock()
        mock_get_provider.return_value = mock_provider

        jobs = [
            BackupJob.objects.create(
                backup_kind="routine_application_data",
                status="completed",
                cloud_enabled=True,
                cloud_upload_status="uploaded",
            )
            for _ in range(5)
        ]

        with mock.patch.dict(
            os.environ,
            {"BACKUP_CLOUD_RETENTION_ENFORCEMENT": "true", "BACKUP_RETENTION_DAILY": "2"},
        ):
            result = enforce_cloud_retention_policy()

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["deleted_count"], 3)
        self.assertEqual(mock_provider.delete_remote_object.call_count, 3)

        deleted_jobs = BackupJob.objects.filter(cloud_upload_status="deleted")
        self.assertEqual(deleted_jobs.count(), 3)

    @mock.patch("sims.backup_center.providers.get_storage_provider")
    def test_keeps_all_backups_within_limit(self, mock_get_provider):
        mock_provider = mock.MagicMock()
        mock_get_provider.return_value = mock_provider

        BackupJob.objects.create(
            backup_kind="routine_application_data",
            status="completed",
            cloud_enabled=True,
            cloud_upload_status="uploaded",
        )

        with mock.patch.dict(
            os.environ,
            {"BACKUP_CLOUD_RETENTION_ENFORCEMENT": "true", "BACKUP_RETENTION_DAILY": "14"},
        ):
            result = enforce_cloud_retention_policy()

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["deleted_count"], 0)
        mock_provider.delete_remote_object.assert_not_called()

    @mock.patch("sims.backup_center.providers.get_storage_provider")
    def test_continues_after_individual_delete_failure(self, mock_get_provider):
        mock_provider = mock.MagicMock()
        mock_provider.delete_remote_object.side_effect = RuntimeError("remote error")
        mock_get_provider.return_value = mock_provider

        for _ in range(3):
            BackupJob.objects.create(
                backup_kind="routine_application_data",
                status="completed",
                cloud_enabled=True,
                cloud_upload_status="uploaded",
            )

        with mock.patch.dict(
            os.environ,
            {"BACKUP_CLOUD_RETENTION_ENFORCEMENT": "true", "BACKUP_RETENTION_DAILY": "1"},
        ):
            result = enforce_cloud_retention_policy()

        # Both over-limit jobs attempted; both failed to delete remotely so neither is
        # counted nor marked deleted, but the call does not raise.
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["deleted_count"], 0)
