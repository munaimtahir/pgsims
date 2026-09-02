"""Tests for the DRF views in sims/backup_center/views.py.

Covers permission gating (IsSuperAdmin / IsAuthenticated) plus success and error-handling
branches for the backup/restore/Google-Drive endpoints, using APIClient + force_authenticate
against real BackupJob/RestoreJob/BackupCloudConnection/BackupCloudCopy rows. GCS/S3/Google
Drive client-SDK-level calls are deliberately not exercised (no boto3 / google-cloud-storage
installed in this environment) -- only the config-driven "disabled"/"not connected" branches
of the Google Drive endpoints are covered, since those don't require the SDK.
"""

import os
import shutil
import tempfile
import zipfile
from pathlib import Path
from unittest import mock

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from rest_framework.test import APIClient

from sims.backup_center.models import (
    BackupJob,
    RestoreJob,
    BackupAuditLog,
    BackupCloudConnection,
    BackupCloudCopy,
)
from sims.backup_center.services import create_routine_application_data_backup

User = get_user_model()


class BackupCenterViewTestBase(TestCase):
    def setUp(self):
        self.tmp_backup_dir = Path(tempfile.mkdtemp(prefix="pgsims_backup_view_test_"))
        self.addCleanup(shutil.rmtree, self.tmp_backup_dir, ignore_errors=True)
        self._settings_patch = mock.patch.dict(
            settings.SIMS_SETTINGS, {"BACKUP_LOCATION": self.tmp_backup_dir}
        )
        self._settings_patch.start()
        self.addCleanup(self._settings_patch.stop)

        # See sims/backup_center/test_services_orchestration.py docstring: an empty (but
        # existing) MEDIA_ROOT makes create_routine_application_data_backup() mark
        # media_included=True with no actual media/ zip entries, which then fails
        # validate_backup_file(). Point MEDIA_ROOT at a directory that doesn't exist so
        # these view tests get real, validating backups.
        self._media_root_patch = mock.patch.object(
            settings, "MEDIA_ROOT", str(self.tmp_backup_dir / "media_root")
        )
        self._media_root_patch.start()
        self.addCleanup(self._media_root_patch.stop)

        self.admin = User.objects.create_user(
            username="view_admin",
            password="pass12345",
            role="ADMIN",
            is_staff=True,
            is_superuser=True,
        )
        self.non_admin = User.objects.create_user(
            username="view_regular",
            password="pass12345",
            role="ADMIN",
            is_superuser=False,
        )
        self.client = APIClient()


class PermissionGatingTests(BackupCenterViewTestBase):
    def test_unauthenticated_requests_rejected(self):
        endpoints = [
            ("get", "/api/backup_center/backups/"),
            ("post", "/api/backup_center/backups/create-routine/"),
            ("get", "/api/backup_center/restores/"),
            ("get", "/api/backup_center/audit-logs/"),
        ]
        for method, url in endpoints:
            resp = getattr(self.client, method)(url)
            self.assertEqual(resp.status_code, 401, url)

    def test_non_superuser_requests_forbidden(self):
        self.client.force_authenticate(self.non_admin)
        endpoints = [
            ("get", "/api/backup_center/backups/"),
            ("post", "/api/backup_center/backups/create-routine/"),
            ("post", "/api/backup_center/backups/create-disaster/"),
            ("get", "/api/backup_center/restores/"),
            ("get", "/api/backup_center/audit-logs/"),
        ]
        for method, url in endpoints:
            resp = getattr(self.client, method)(url)
            self.assertEqual(resp.status_code, 403, url)


class CreateBackupViewTests(BackupCenterViewTestBase):
    def test_create_routine_backup_success(self):
        self.client.force_authenticate(self.admin)
        resp = self.client.post(
            "/api/backup_center/backups/create-routine/", {"notes": "via api"}, format="json"
        )
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data["status"], "completed")
        job = BackupJob.objects.get(pk=resp.data["id"])
        self.assertTrue(os.path.exists(job.file_path))

    def test_create_routine_backup_failure_returns_500(self):
        self.client.force_authenticate(self.admin)
        with mock.patch(
            "sims.backup_center.views.create_routine_application_data_backup",
            side_effect=Exception("boom"),
        ):
            resp = self.client.post("/api/backup_center/backups/create-routine/", {}, format="json")
        self.assertEqual(resp.status_code, 500)
        self.assertIn("error", resp.data)

    def test_create_disaster_backup_success(self):
        self.client.force_authenticate(self.admin)
        resp = self.client.post(
            "/api/backup_center/backups/create-disaster/", {"notes": "dr"}, format="json"
        )
        self.assertEqual(resp.status_code, 201)
        self.assertTrue(resp.data["file_name"].endswith(".pgsimsdr"))

    def test_create_disaster_backup_failure_returns_500(self):
        self.client.force_authenticate(self.admin)
        with mock.patch(
            "sims.backup_center.views.create_disaster_recovery_backup",
            side_effect=Exception("boom"),
        ):
            resp = self.client.post("/api/backup_center/backups/create-disaster/", {}, format="json")
        self.assertEqual(resp.status_code, 500)


class DownloadBackupViewTests(BackupCenterViewTestBase):
    def test_download_success_writes_audit_log(self):
        self.client.force_authenticate(self.admin)
        job = create_routine_application_data_backup(user=self.admin)
        resp = self.client.get(f"/api/backup_center/backups/{job.id}/download/")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(
            BackupAuditLog.objects.filter(backup_job=job, action="backup_downloaded").exists()
        )

    def test_download_deleted_backup_returns_410(self):
        self.client.force_authenticate(self.admin)
        job = BackupJob.objects.create(status="deleted")
        resp = self.client.get(f"/api/backup_center/backups/{job.id}/download/")
        self.assertEqual(resp.status_code, 410)

    def test_download_missing_file_returns_404(self):
        self.client.force_authenticate(self.admin)
        job = BackupJob.objects.create(status="completed", file_path="/nonexistent/path.pgsimsbak")
        resp = self.client.get(f"/api/backup_center/backups/{job.id}/download/")
        self.assertEqual(resp.status_code, 404)

    def test_download_nonexistent_job_returns_404(self):
        self.client.force_authenticate(self.admin)
        resp = self.client.get("/api/backup_center/backups/999999/download/")
        self.assertEqual(resp.status_code, 404)


class DeleteBackupViewTests(BackupCenterViewTestBase):
    def test_delete_removes_file_and_marks_deleted(self):
        self.client.force_authenticate(self.admin)
        job = create_routine_application_data_backup(user=self.admin)
        self.assertTrue(os.path.exists(job.file_path))
        resp = self.client.delete(f"/api/backup_center/backups/{job.id}/delete/")
        self.assertEqual(resp.status_code, 204)
        job.refresh_from_db()
        self.assertEqual(job.status, "deleted")
        self.assertFalse(os.path.exists(job.file_path))
        self.assertTrue(
            BackupAuditLog.objects.filter(backup_job=job, action="backup_deleted").exists()
        )

    def test_delete_nonexistent_job_returns_404(self):
        self.client.force_authenticate(self.admin)
        resp = self.client.delete("/api/backup_center/backups/999999/delete/")
        self.assertEqual(resp.status_code, 404)


class ValidateBackupJobViewTests(BackupCenterViewTestBase):
    def test_validate_success(self):
        self.client.force_authenticate(self.admin)
        job = create_routine_application_data_backup(user=self.admin)
        resp = self.client.post(f"/api/backup_center/backups/{job.id}/validate/")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.data["valid"])
        self.assertTrue(
            BackupAuditLog.objects.filter(backup_job=job, action="backup_validated").exists()
        )

    def test_validate_deleted_returns_410(self):
        self.client.force_authenticate(self.admin)
        job = BackupJob.objects.create(status="deleted")
        resp = self.client.post(f"/api/backup_center/backups/{job.id}/validate/")
        self.assertEqual(resp.status_code, 410)

    def test_validate_missing_file_returns_404(self):
        self.client.force_authenticate(self.admin)
        job = BackupJob.objects.create(status="completed", file_path="")
        resp = self.client.post(f"/api/backup_center/backups/{job.id}/validate/")
        self.assertEqual(resp.status_code, 404)


class UploadRestoreFileViewTests(BackupCenterViewTestBase):
    def test_no_file_returns_400(self):
        self.client.force_authenticate(self.admin)
        resp = self.client.post("/api/backup_center/restores/upload/", {}, format="multipart")
        self.assertEqual(resp.status_code, 400)

    def test_invalid_extension_returns_400(self):
        self.client.force_authenticate(self.admin)
        upload = SimpleUploadedFile("notabackup.txt", b"hello")
        resp = self.client.post(
            "/api/backup_center/restores/upload/", {"file": upload}, format="multipart"
        )
        self.assertEqual(resp.status_code, 400)

    def test_valid_upload_creates_restore_job(self):
        self.client.force_authenticate(self.admin)
        buf_path = self.tmp_backup_dir / "upload_test.pgsimsbak"
        with zipfile.ZipFile(buf_path, "w") as zf:
            zf.writestr("dummy.txt", "dummy")
        upload = SimpleUploadedFile("upload_test.pgsimsbak", buf_path.read_bytes())
        resp = self.client.post(
            "/api/backup_center/restores/upload/", {"file": upload}, format="multipart"
        )
        self.assertEqual(resp.status_code, 201)
        restore_job = RestoreJob.objects.get(pk=resp.data["id"])
        self.assertTrue(
            BackupAuditLog.objects.filter(restore_job=restore_job, action="restore_uploaded").exists()
        )


class ValidateRestoreJobViewTests(BackupCenterViewTestBase):
    def _make_restore_job_with_upload(self, filename, content):
        rj = RestoreJob.objects.create(uploaded_file_name=filename, status="pending", restored_by=self.admin)
        rj.uploaded_file.save(filename, SimpleUploadedFile(filename, content), save=True)
        return rj

    def test_validate_valid_backup_marks_validation_passed(self):
        self.client.force_authenticate(self.admin)
        job = create_routine_application_data_backup(user=self.admin)
        with open(job.file_path, "rb") as f:
            content = f.read()
        rj = self._make_restore_job_with_upload("re_validate.pgsimsbak", content)

        resp = self.client.post(f"/api/backup_center/restores/{rj.id}/validate/")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.data["valid"])
        rj.refresh_from_db()
        self.assertEqual(rj.status, "validation_passed")

    def test_validate_invalid_backup_marks_validation_failed(self):
        self.client.force_authenticate(self.admin)
        rj = self._make_restore_job_with_upload("bad.pgsimsbak", b"not a zip")

        resp = self.client.post(f"/api/backup_center/restores/{rj.id}/validate/")
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(resp.data["valid"])
        rj.refresh_from_db()
        self.assertEqual(rj.status, "validation_failed")
        self.assertTrue(rj.error_message)

    def test_validate_nonexistent_restore_job_returns_404(self):
        self.client.force_authenticate(self.admin)
        resp = self.client.post("/api/backup_center/restores/999999/validate/")
        self.assertEqual(resp.status_code, 404)


class DryRunRestoreViewTests(BackupCenterViewTestBase):
    def test_dry_run_success(self):
        self.client.force_authenticate(self.admin)
        job = create_routine_application_data_backup(user=self.admin)
        with open(job.file_path, "rb") as f:
            content = f.read()
        rj = RestoreJob.objects.create(uploaded_file_name="dr.pgsimsbak", status="pending", restored_by=self.admin)
        rj.uploaded_file.save("dr.pgsimsbak", SimpleUploadedFile("dr.pgsimsbak", content), save=True)

        resp = self.client.post(f"/api/backup_center/restores/{rj.id}/dry-run/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["status"], "validation_passed")

    def test_dry_run_nonexistent_restore_job_returns_404(self):
        self.client.force_authenticate(self.admin)
        resp = self.client.post("/api/backup_center/restores/999999/dry-run/")
        self.assertEqual(resp.status_code, 404)

    def test_dry_run_service_error_returns_400(self):
        self.client.force_authenticate(self.admin)
        rj = RestoreJob.objects.create(uploaded_file_name="x.pgsimsbak", status="pending", restored_by=self.admin)
        rj.uploaded_file.save("x.pgsimsbak", SimpleUploadedFile("x.pgsimsbak", b"zzz"), save=True)
        with mock.patch(
            "sims.backup_center.views.restore_routine_application_data_backup",
            side_effect=Exception("kaboom"),
        ):
            resp = self.client.post(f"/api/backup_center/restores/{rj.id}/dry-run/")
        self.assertEqual(resp.status_code, 400)


class ConfirmRestoreViewTests(BackupCenterViewTestBase):
    def test_missing_password_or_confirmation_returns_400(self):
        self.client.force_authenticate(self.admin)
        rj = RestoreJob.objects.create(uploaded_file_name="x.pgsimsbak", status="pending", restored_by=self.admin)
        resp = self.client.post(f"/api/backup_center/restores/{rj.id}/confirm/", {}, format="json")
        self.assertEqual(resp.status_code, 400)

    def test_invalid_password_returns_401(self):
        self.client.force_authenticate(self.admin)
        rj = RestoreJob.objects.create(uploaded_file_name="x.pgsimsbak", status="pending", restored_by=self.admin)
        resp = self.client.post(
            f"/api/backup_center/restores/{rj.id}/confirm/",
            {"password": "wrongpassword", "typed_confirmation": "RESTORE"},
            format="json",
        )
        self.assertEqual(resp.status_code, 401)

    def test_valid_password_but_restore_job_missing_returns_404(self):
        self.client.force_authenticate(self.admin)
        resp = self.client.post(
            "/api/backup_center/restores/999999/confirm/",
            {"password": "pass12345", "typed_confirmation": "RESTORE"},
            format="json",
        )
        self.assertEqual(resp.status_code, 404)

    def test_valid_password_wrong_typed_confirmation_returns_400(self):
        self.client.force_authenticate(self.admin)
        job = create_routine_application_data_backup(user=self.admin)
        with open(job.file_path, "rb") as f:
            content = f.read()
        rj = RestoreJob.objects.create(uploaded_file_name="c.pgsimsbak", status="pending", restored_by=self.admin)
        rj.uploaded_file.save("c.pgsimsbak", SimpleUploadedFile("c.pgsimsbak", content), save=True)

        resp = self.client.post(
            f"/api/backup_center/restores/{rj.id}/confirm/",
            {"password": "pass12345", "typed_confirmation": "WRONG"},
            format="json",
        )
        self.assertEqual(resp.status_code, 400)
        self.assertIn("error", resp.data)


class GoogleDriveStatusAndConfigViewTests(BackupCenterViewTestBase):
    def test_status_reports_not_connected_when_no_connection_row(self):
        self.client.force_authenticate(self.admin)
        resp = self.client.get("/api/backup_center/google-drive/status/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["status"], "not_connected")
        self.assertFalse(resp.data["enabled"])

    def test_status_reports_existing_connection(self):
        self.client.force_authenticate(self.admin)
        BackupCloudConnection.objects.create(
            provider="google_drive", status="connected", account_email="ops@example.com"
        )
        resp = self.client.get("/api/backup_center/google-drive/status/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["status"], "connected")
        self.assertEqual(resp.data["connected_account"], "ops@example.com")

    def test_connect_returns_400_when_disabled(self):
        self.client.force_authenticate(self.admin)
        resp = self.client.get("/api/backup_center/google-drive/connect/")
        self.assertEqual(resp.status_code, 400)
        self.assertIn("error", resp.data)

    def test_disconnect_when_no_connection(self):
        self.client.force_authenticate(self.admin)
        resp = self.client.post("/api/backup_center/google-drive/disconnect/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["status"], "not_connected")

    def test_disconnect_clears_existing_connection(self):
        self.client.force_authenticate(self.admin)
        BackupCloudConnection.objects.create(
            provider="google_drive", status="connected", account_email="ops@example.com"
        )
        resp = self.client.post("/api/backup_center/google-drive/disconnect/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["status"], "disconnected")
        self.assertTrue(
            BackupAuditLog.objects.filter(action="google_drive_disconnected").exists()
        )

    def test_health_check_returns_400_when_not_connected(self):
        self.client.force_authenticate(self.admin)
        resp = self.client.post("/api/backup_center/google-drive/health-check/")
        self.assertEqual(resp.status_code, 400)

    def test_create_folder_returns_400_when_not_connected(self):
        self.client.force_authenticate(self.admin)
        resp = self.client.post("/api/backup_center/google-drive/create-folder/")
        self.assertEqual(resp.status_code, 400)

    def test_oauth_callback_with_error_param_redirects(self):
        resp = self.client.get("/api/backup_center/google-drive/oauth/callback/?error=access_denied")
        self.assertEqual(resp.status_code, 302)
        self.assertIn("googleDrive=error", resp.url)

    def test_oauth_callback_missing_code_or_state_redirects(self):
        resp = self.client.get("/api/backup_center/google-drive/oauth/callback/")
        self.assertEqual(resp.status_code, 302)
        self.assertIn("missing_code_or_state", resp.url)

    def test_oauth_callback_failure_redirects_with_error(self):
        resp = self.client.get(
            "/api/backup_center/google-drive/oauth/callback/?code=abc&state=xyz"
        )
        self.assertEqual(resp.status_code, 302)
        self.assertIn("googleDrive=error", resp.url)


class GoogleDriveBackupJobViewTests(BackupCenterViewTestBase):
    def test_upload_backup_job_not_found_returns_404(self):
        self.client.force_authenticate(self.admin)
        resp = self.client.post("/api/backup_center/backups/999999/google-drive/upload/")
        self.assertEqual(resp.status_code, 404)

    def test_upload_backup_fails_when_drive_disabled(self):
        self.client.force_authenticate(self.admin)
        job = create_routine_application_data_backup(user=self.admin)
        resp = self.client.post(f"/api/backup_center/backups/{job.id}/google-drive/upload/")
        self.assertEqual(resp.status_code, 400)
        self.assertTrue(
            BackupAuditLog.objects.filter(
                backup_job=job, action="google_drive_upload_failed"
            ).exists()
        )

    def test_verify_backup_job_not_found_returns_404(self):
        self.client.force_authenticate(self.admin)
        resp = self.client.post("/api/backup_center/backups/999999/google-drive/verify/")
        self.assertEqual(resp.status_code, 404)

    def test_verify_no_cloud_copy_returns_404(self):
        self.client.force_authenticate(self.admin)
        job = create_routine_application_data_backup(user=self.admin)
        resp = self.client.post(f"/api/backup_center/backups/{job.id}/google-drive/verify/")
        self.assertEqual(resp.status_code, 404)

    def test_download_backup_job_not_found_returns_404(self):
        self.client.force_authenticate(self.admin)
        resp = self.client.post("/api/backup_center/backups/999999/google-drive/download/")
        self.assertEqual(resp.status_code, 404)

    def test_download_no_verified_cloud_copy_returns_404(self):
        self.client.force_authenticate(self.admin)
        job = create_routine_application_data_backup(user=self.admin)
        resp = self.client.post(f"/api/backup_center/backups/{job.id}/google-drive/download/")
        self.assertEqual(resp.status_code, 404)

    def test_list_returns_cloud_copies(self):
        self.client.force_authenticate(self.admin)
        job = create_routine_application_data_backup(user=self.admin)
        connection = BackupCloudConnection.objects.create(provider="google_drive", status="connected")
        BackupCloudCopy.objects.create(
            backup_record=job,
            provider="google_drive",
            connection=connection,
            remote_file_id="file123",
            remote_file_name="backup.enc",
            upload_status="uploaded",
        )
        resp = self.client.get("/api/backup_center/google-drive/list/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data["results"]), 1)
        self.assertEqual(resp.data["results"][0]["remote_file_id"], "file123")


class ListDetailViewTests(BackupCenterViewTestBase):
    def test_backup_job_list_and_detail(self):
        self.client.force_authenticate(self.admin)
        job = create_routine_application_data_backup(user=self.admin)
        deleted_job = BackupJob.objects.create(status="deleted")

        list_resp = self.client.get("/api/backup_center/backups/")
        self.assertEqual(list_resp.status_code, 200)
        results = list_resp.data.get("results", list_resp.data)
        ids = [row["id"] for row in results]
        self.assertIn(job.id, ids)
        self.assertNotIn(deleted_job.id, ids)

        detail_resp = self.client.get(f"/api/backup_center/backups/{job.id}/")
        self.assertEqual(detail_resp.status_code, 200)
        self.assertEqual(detail_resp.data["id"], job.id)

    def test_restore_and_audit_log_lists(self):
        self.client.force_authenticate(self.admin)
        RestoreJob.objects.create(uploaded_file_name="a.pgsimsbak", restored_by=self.admin)
        BackupAuditLog.objects.create(action="restore_uploaded", actor=self.admin)

        resp = self.client.get("/api/backup_center/restores/")
        self.assertEqual(resp.status_code, 200)
        self.assertGreaterEqual(len(resp.data.get("results", resp.data)), 1)

        resp2 = self.client.get("/api/backup_center/audit-logs/")
        self.assertEqual(resp2.status_code, 200)
        self.assertGreaterEqual(len(resp2.data.get("results", resp2.data)), 1)
