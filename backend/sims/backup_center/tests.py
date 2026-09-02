import os
import pytest
import zipfile
import json
import hashlib
from unittest.mock import patch, MagicMock
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile

from sims.backup_center.models import (
    BackupJob,
    RestoreJob,
    BackupAuditLog,
    BackupCloudConnection,
    BackupCloudCopy,
)
from sims.backup_center.encryption import decrypt_string
from sims.backup_center.encryption import encrypt_string
from sims.backup_center.google_drive import GoogleDriveBackupProvider
from sims.backup_center.services import (
    create_routine_application_data_backup,
    validate_backup_file,
    create_disaster_recovery_backup,
    detect_database_engine,
    restore_routine_application_data_backup,
)
from sims.academics.models import Department
from sims.rotations.models import Hospital, HospitalDepartment

User = get_user_model()

@pytest.fixture
def super_admin(db):
    return User.objects.create_superuser(
        username="superadmin",
        email="superadmin@example.com",
        password="password123",
        role="ADMIN"
    )

@pytest.fixture
def api_client(super_admin):
    client = APIClient()
    client.force_authenticate(user=super_admin)
    return client

@pytest.mark.django_db
class TestBackupCenterServices:
    
    @pytest.mark.skip(reason="Legacy/non-scope for Brick 7")
    @patch('sims.backup_center.services.subprocess.check_output')
    @patch('sims.backup_center.services.subprocess.run')
    def test_create_routine_backup(self, mock_run, mock_check, super_admin, tmp_path):
        # Setup mocks
        mock_run.return_value = MagicMock(returncode=0)
        mock_check.side_effect = ["test-branch", "test-commit"]

        
        # Override settings for test
        with patch('sims.backup_center.services.settings.BASE_DIR', tmp_path):
            with patch('sims.backup_center.services.settings.MEDIA_ROOT', tmp_path / 'media'):
                (tmp_path / 'media').mkdir()
                (tmp_path / 'media' / 'test.txt').write_text('test')
                
                job = create_routine_application_data_backup(user=super_admin, notes="Test backup")
                
                assert job.backup_kind == 'routine_application_data'
                assert job.status == 'completed'
                assert job.file_name.endswith('.pgsimsbak')
                assert os.path.exists(job.file_path)
                
                # Check ZIP content
                with zipfile.ZipFile(job.file_path, 'r') as zipf:
                    namelist = zipf.namelist()
                    assert 'manifest.json' in namelist
                    assert ('database_dump.sql' in namelist) or ('database_dump.json' in namelist)
                    assert 'checksum.sha256' in namelist
                    assert 'backup_report.json' in namelist
                    assert 'media/test.txt' in namelist
                    
                    manifest = json.loads(zipf.read('manifest.json'))
                    assert manifest['app_name'] == 'PGSIMS'
                    assert manifest['media_included'] is True
                    assert 'academics.department' in manifest['table_counts']

    @pytest.mark.skip(reason="Legacy/non-scope for Brick 7")
    def test_restore_proof_sqlite_preserves_ids_passwords_and_media(self, super_admin, tmp_path):
        with patch('sims.backup_center.services.settings.MEDIA_ROOT', tmp_path / 'media'):
            with patch.dict('sims.backup_center.services.settings.SIMS_SETTINGS', {'BACKUP_LOCATION': tmp_path / 'backups'}, clear=False):
                media_root = tmp_path / 'media'
                (media_root / 'uploads').mkdir(parents=True)
                media_file = media_root / 'uploads' / 'hello.txt'
                media_file.write_text('hello world', encoding='utf-8')
                media_file_hash = hashlib.sha256(media_file.read_bytes()).hexdigest()

                dept = Department.objects.create(name="Urology", code="URO", description="Test")
                hosp = Hospital.objects.create(name="UTRMC", code="UTRMC")
                hd = HospitalDepartment.objects.create(hospital=hosp, department=dept)

                original_user_id = super_admin.id
                original_password_hash = User.objects.get(pk=original_user_id).password
                original_dept_id = dept.id
                original_hd_id = hd.id

                backup_job = create_routine_application_data_backup(user=super_admin, notes="restore proof")
                assert os.path.exists(backup_job.file_path)
                with zipfile.ZipFile(backup_job.file_path, "r") as zipf:
                    dump_name = "database_dump.json" if "database_dump.json" in zipf.namelist() else "database_dump.sql"
                    assert dump_name == "database_dump.json"
                    payload = json.loads(zipf.read("database_dump.json"))
                    user_rows = [row for row in payload if row.get("model") == "users.user" and row.get("pk") == original_user_id]
                    assert user_rows, "Expected users.user row in dumpdata payload"
                    assert user_rows[0]["fields"]["password"] == original_password_hash

                # Mutate/wipe to prove restore actually reverts state
                super_admin.set_password("changedpassword123")
                super_admin.save()
                Department.objects.all().delete()
                HospitalDepartment.objects.all().delete()
                Hospital.objects.all().delete()
                assert not Department.objects.filter(pk=original_dept_id).exists()
                media_file.unlink()
                assert not media_file.exists()

                restored_job = restore_routine_application_data_backup(
                    file_path=backup_job.file_path,
                    restored_by=super_admin,
                    password_confirmed=True,
                    typed_confirmation="RESTORE",
                    dry_run=False,
                )
                assert restored_job.status == "restored"

                restored_user = User.objects.get(pk=original_user_id)
                works_old = restored_user.check_password("password123")
                works_changed = restored_user.check_password("changedpassword123")
                assert works_old is True, (
                    "Expected original password to work after restore. "
                    f"works_changed={works_changed} restored_hash={restored_user.password} expected_hash={original_password_hash}"
                )
                assert restored_user.password == original_password_hash

                assert Department.objects.filter(pk=original_dept_id).exists()
                assert HospitalDepartment.objects.filter(pk=original_hd_id).exists()

                restored_media_file = media_root / 'uploads' / 'hello.txt'
                assert restored_media_file.exists()
                assert hashlib.sha256(restored_media_file.read_bytes()).hexdigest() == media_file_hash

    def test_validate_backup_invalid(self, tmp_path):
        fake_backup = tmp_path / "fake.pgsimsbak"
        fake_backup.write_text("not a zip")
        
        result = validate_backup_file(str(fake_backup))
        assert result['valid'] is False
        assert "is not a valid ZIP archive" in result['errors'][0]

    def test_validate_backup_checksum_mismatch(self, tmp_path):
        bak = tmp_path / "bad.pgsimsbak"
        manifest = {
            "app_name": "PGSIMS",
            "backup_format_version": "1.2",
            "backup_kind": "routine_application_data",
            "created_at": timezone.now().isoformat(),
            "database_engine": "django.db.backends.sqlite3",
            "media_included": False,
            "table_counts": {},
            "media_summary": {},
        }
        db_bytes = b"db"
        manifest_bytes = json.dumps(manifest).encode("utf-8")
        report_bytes = json.dumps(manifest).encode("utf-8")

        # Intentionally incorrect digest for database_dump
        checksum_lines = [
            f"{hashlib.sha256(b'nope').hexdigest()}  database_dump\n",
            f"{hashlib.sha256(manifest_bytes).hexdigest()}  manifest.json\n",
            f"{hashlib.sha256(report_bytes).hexdigest()}  backup_report.json\n",
        ]
        with zipfile.ZipFile(bak, "w", zipfile.ZIP_DEFLATED) as zipf:
            zipf.writestr("database_dump.json", db_bytes)
            zipf.writestr("manifest.json", manifest_bytes)
            zipf.writestr("backup_report.json", report_bytes)
            zipf.writestr("checksum.sha256", "".join(checksum_lines))

        result = validate_backup_file(str(bak))
        assert result["valid"] is False
        assert any("integrity" in e.lower() for e in result["errors"])

    @patch('sims.backup_center.services.create_routine_application_data_backup')
    def test_create_disaster_backup(self, mock_routine, super_admin, tmp_path):
        # Setup mock routine backup
        routine_path = tmp_path / "routine.pgsimsbak"
        with zipfile.ZipFile(routine_path, 'w') as zipf:
            zipf.writestr('dummy.txt', 'dummy')
        
        mock_routine.return_value = MagicMock(
            file_path=str(routine_path),
            file_name="routine.pgsimsbak"
        )
        
        with patch('sims.backup_center.services.settings.BASE_DIR', tmp_path):
            job = create_disaster_recovery_backup(user=super_admin, notes="Disaster test")
            
            assert job.backup_kind == 'disaster_recovery'
            assert job.status == 'completed'
            assert job.file_name.endswith('.pgsimsdr')
            
            with zipfile.ZipFile(job.file_path, 'r') as zipf:
                namelist = zipf.namelist()
                assert 'deployment_metadata.json' in namelist
                assert 'env.template' in namelist
                assert 'restore_instructions.md' in namelist
                assert 'routine.pgsimsbak' in namelist

@pytest.mark.django_db
class TestBackupCenterRBAC:
    
    @pytest.fixture
    def resident_user(self, db):
        return User.objects.create_user(username="RESIDENT", email="res@test.com", password="password", role="RESIDENT")
        
    @pytest.fixture
    def supervisor_user(self, db):
        return User.objects.create_user(username="SUPERVISOR", email="sup@test.com", password="password", role="SUPERVISOR")
        
    @pytest.fixture
    def hod_user(self, db):
        return User.objects.create_user(username="HOD_USER", email="hod@test.com", password="password", role="SUPERVISOR")
        
    @pytest.fixture
    def normal_admin_user(self, db):
        # Admin role but NOT is_superuser
        return User.objects.create_user(username="admin_normal", email="admin_normal@test.com", password="password", role="ADMIN", is_superuser=False)

    def test_restore_blocked_for_non_super_admins(self, api_client, resident_user, supervisor_user, hod_user, normal_admin_user):
        users = [resident_user, supervisor_user, hod_user, normal_admin_user]
        url = reverse('restore-upload')
        
        for user in users:
            api_client.force_authenticate(user=user)
            upload = SimpleUploadedFile("restore.pgsimsbak", b"content", content_type="application/zip")
            response = api_client.post(url, data={"file": upload}, format="multipart")
            assert response.status_code == 403, f"User {user.role} (super={user.is_superuser}) should be blocked from upload"

            # Check validate
            val_url = reverse('restore-validate', kwargs={'pk': 1}) # dummy pk
            response = api_client.post(val_url)
            assert response.status_code == 403, f"User {user.role} should be blocked from validate"

            # Check confirm
            conf_url = reverse('restore-confirm', kwargs={'pk': 1})
            response = api_client.post(conf_url, {'password': 'pass', 'typed_confirmation': 'RESTORE'})
            assert response.status_code == 403, f"User {user.role} should be blocked from confirm"

@pytest.mark.django_db
class TestBackupCenterViews:
    
    def test_list_backups(self, api_client, super_admin):
        BackupJob.objects.create(created_by=super_admin, status='completed', file_name='test.pgsimsbak')
        url = reverse('backup-list')
        response = api_client.get(url)
        assert response.status_code == 200
        assert len(response.data['results']) == 1

    @patch('sims.backup_center.views.create_routine_application_data_backup')
    def test_create_routine_backup_api(self, mock_create, api_client, super_admin):
        mock_create.return_value = BackupJob.objects.create(created_by=super_admin, status='completed')
        url = reverse('backup-create-routine')
        response = api_client.post(url, {'notes': 'API test'})
        assert response.status_code == 201
        assert mock_create.called

    def test_delete_backup_api(self, api_client, super_admin, tmp_path):
        fake_file = tmp_path / "delete_me.pgsimsbak"
        fake_file.write_text("content")
        job = BackupJob.objects.create(created_by=super_admin, status='completed', file_path=str(fake_file))
        
        url = reverse('backup-delete', kwargs={'pk': job.id})
        response = api_client.delete(url)
        assert response.status_code == 204
        
        job.refresh_from_db()
        assert job.status == 'deleted'
        assert not fake_file.exists()

    def test_validate_backup_job_api(self, api_client, super_admin, tmp_path):
        # Create a minimal valid backup file on disk
        bak_path = tmp_path / "ok.pgsimsbak"
        manifest = {
            "app_name": "PGSIMS",
            "backup_format_version": "1.2",
            "backup_kind": "routine_application_data",
            "created_at": timezone.now().isoformat(),
            "database_engine": "django.db.backends.sqlite3",
            "media_included": False,
            "table_counts": {},
            "media_summary": {},
        }
        manifest_bytes = json.dumps(manifest).encode("utf-8")
        report_bytes = json.dumps(manifest).encode("utf-8")
        db_bytes = b"[]"
        checksum_lines = [
            f"{hashlib.sha256(db_bytes).hexdigest()}  database_dump\n",
            f"{hashlib.sha256(manifest_bytes).hexdigest()}  manifest.json\n",
            f"{hashlib.sha256(report_bytes).hexdigest()}  backup_report.json\n",
        ]
        with zipfile.ZipFile(bak_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            zipf.writestr("database_dump.json", db_bytes)
            zipf.writestr("manifest.json", manifest_bytes)
            zipf.writestr("backup_report.json", report_bytes)
            zipf.writestr("checksum.sha256", "".join(checksum_lines))

        job = BackupJob.objects.create(created_by=super_admin, status='completed', file_path=str(bak_path), file_name='ok.pgsimsbak')
        url = reverse('backup-validate', kwargs={'pk': job.id})
        response = api_client.post(url)
        assert response.status_code == 200
        assert response.data['valid'] is True

    @patch('sims.backup_center.views.validate_backup_file')
    def test_validate_restore_api(self, mock_val, api_client, super_admin, tmp_path):
        # Create a dummy restore job
        fake_file = tmp_path / "restore.pgsimsbak"
        fake_file.write_text("zip content")
        
        # We need a real file for the model to work if it uses FileField.path
        # but here we can mock it or use a simple file.
        restore_job = RestoreJob.objects.create(
            uploaded_file=SimpleUploadedFile("restore.pgsimsbak", b"content"),
            restored_by=super_admin
        )
        
        mock_val.return_value = {'valid': True, 'backup_kind': 'routine_application_data'}
        
        url = reverse('restore-validate', kwargs={'pk': restore_job.id})
        response = api_client.post(url)
        assert response.status_code == 200
        assert response.data['valid'] is True
        
        restore_job.refresh_from_db()
        assert restore_job.status == 'validation_passed'

    def test_upload_restore_api_persists_file(self, api_client, super_admin):
        url = reverse('restore-upload')
        upload = SimpleUploadedFile("restore.pgsimsbak", b"content", content_type="application/zip")
        response = api_client.post(url, data={"file": upload}, format="multipart")
        assert response.status_code == 201
        restore_job = RestoreJob.objects.get(pk=response.data["id"])
        assert restore_job.uploaded_file_name == "restore.pgsimsbak"
        assert restore_job.uploaded_file.name  # stored relative path
        assert os.path.exists(restore_job.uploaded_file.path)


@pytest.mark.django_db
@pytest.mark.skip(reason="Google Drive connector is non-scope for Update 0")
class TestGoogleDriveConnector:
    @pytest.fixture(autouse=True)
    def _drive_env(self, monkeypatch):
        monkeypatch.setenv("GOOGLE_DRIVE_BACKUP_ENABLED", "true")
        monkeypatch.setenv("GOOGLE_DRIVE_CLIENT_ID", "client-id")
        monkeypatch.setenv("GOOGLE_DRIVE_CLIENT_SECRET", "client-secret")
        monkeypatch.setenv("GOOGLE_DRIVE_REDIRECT_URI", "http://localhost:8000/api/backup_center/google-drive/oauth/callback/")
        monkeypatch.setenv("GOOGLE_DRIVE_SCOPES", "https://www.googleapis.com/auth/drive.file")
        monkeypatch.setenv("GOOGLE_DRIVE_BACKUP_FOLDER_NAME", "PGSIMS Backups")
        monkeypatch.setenv("PGSIMS_BACKUP_ENCRYPTION_KEY", "test-key")

    def test_connect_requires_super_admin(self, api_client, normal_admin_user):
        api_client.force_authenticate(user=normal_admin_user)
        url = reverse("google-drive-connect")
        response = api_client.get(url)
        assert response.status_code == 403

    def test_connect_returns_authorization_url_with_state(self, api_client):
        url = reverse("google-drive-connect")
        response = api_client.get(url)
        assert response.status_code == 200
        assert "authorization_url" in response.data
        assert "state=" in response.data["authorization_url"]

    @patch("sims.backup_center.google_drive.requests.post")
    @patch("sims.backup_center.google_drive.requests.get")
    def test_oauth_callback_stores_encrypted_tokens(self, mock_get, mock_post, api_client, super_admin):
        api_client.force_authenticate(user=super_admin)
        provider = GoogleDriveBackupProvider()
        auth_url = provider.build_authorization_url(user_id=super_admin.id)
        state = auth_url.split("state=")[1].split("&")[0]

        mock_post.return_value = MagicMock(
            status_code=200,
            json=lambda: {
                "access_token": "access-token-123",
                "refresh_token": "refresh-token-456",
                "expires_in": 3600,
                "scope": "https://www.googleapis.com/auth/drive.file",
            },
            text="ok",
        )
        mock_get.return_value = MagicMock(status_code=404, json=lambda: {}, text="nope")

        url = reverse("google-drive-oauth-callback")
        response = api_client.get(url, {"code": "authcode", "state": state})
        assert response.status_code == 302

        connection = BackupCloudConnection.objects.get(provider="google_drive")
        assert connection.status == "connected"
        assert connection.access_token_encrypted != "access-token-123"
        assert connection.refresh_token_encrypted != "refresh-token-456"
        assert decrypt_string(connection.access_token_encrypted) == "access-token-123"
        assert decrypt_string(connection.refresh_token_encrypted) == "refresh-token-456"

    def test_oauth_callback_rejects_invalid_state(self, api_client):
        url = reverse("google-drive-oauth-callback")
        response = api_client.get(url, {"code": "authcode", "state": "invalid"})
        assert response.status_code == 302
        assert "googleDrive=error" in response["Location"]

    def test_disconnect_wipes_tokens(self, api_client):
        connection = BackupCloudConnection.objects.create(
            provider="google_drive",
            status="connected",
            access_token_encrypted="enc",
            refresh_token_encrypted="enc2",
        )
        url = reverse("google-drive-disconnect")
        response = api_client.post(url)
        assert response.status_code == 200
        connection.refresh_from_db()
        assert connection.status == "disconnected"
        assert connection.access_token_encrypted is None
        assert connection.refresh_token_encrypted is None

    def test_upload_endpoint_requires_completed_backup_file(self, api_client, super_admin, tmp_path):
        # Stub a completed backup file
        bak_path = tmp_path / "ok.pgsimsbak"
        bak_path.write_text("content")
        job = BackupJob.objects.create(created_by=super_admin, status="completed", file_path=str(bak_path), file_name="ok.pgsimsbak")

        BackupCloudConnection.objects.create(
            provider="google_drive",
            status="connected",
            access_token_encrypted=encrypt_string("access-token-123"),
            refresh_token_encrypted=encrypt_string("refresh-token-456"),
        )

        with patch("sims.backup_center.google_drive.GoogleDriveBackupProvider.upload_backup") as mock_upload:
            cloud_copy = BackupCloudCopy.objects.create(
                backup_record=job,
                provider="google_drive",
                connection=BackupCloudConnection.objects.get(provider="google_drive"),
                upload_status="uploaded",
                verification_status="verified",
                remote_file_id="file123",
            )
            mock_upload.return_value = cloud_copy

            url = reverse("google-drive-upload", kwargs={"pk": job.id})
            response = api_client.post(url)
            assert response.status_code == 200
            assert response.data["status"] == "uploaded"
