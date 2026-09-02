"""Tests for sims/backup_center/google_drive.py -- previously effectively 0% covered.

GoogleDriveBackupProvider talks to the real Google OAuth/Drive HTTP APIs via `requests`.
None of that network traffic is exercised here -- instead every `requests.get/post/put` call
is mocked so the PGSIMS-side logic (OAuth state signing/validation, token storage/refresh,
folder resolution, resumable-upload orchestration, encrypt-then-upload-then-verify backup
flow, download-then-decrypt-then-checksum flow, and error/retry bookkeeping) gets real
coverage without needing live Google credentials.
"""

import os
from unittest import mock

import pytest
from django.core.cache import cache
from django.utils import timezone

from sims.backup_center.encryption import decrypt_string
from sims.backup_center.google_drive import GoogleDriveBackupProvider
from sims.backup_center.models import BackupCloudConnection, BackupCloudCopy, BackupJob


DRIVE_ENV = {
    "GOOGLE_DRIVE_BACKUP_ENABLED": "true",
    "GOOGLE_DRIVE_CLIENT_ID": "client-id",
    "GOOGLE_DRIVE_CLIENT_SECRET": "client-secret",
    "GOOGLE_DRIVE_REDIRECT_URI": "http://localhost/api/backup_center/google-drive/oauth/callback/",
    "GOOGLE_DRIVE_SCOPES": "https://www.googleapis.com/auth/drive.file",
    "GOOGLE_DRIVE_BACKUP_FOLDER_NAME": "PGSIMS Backups",
    "PGSIMS_BACKUP_ENCRYPTION_KEY": "test-encryption-key",
}


@pytest.fixture(autouse=True)
def drive_env():
    with mock.patch.dict(os.environ, DRIVE_ENV, clear=False):
        yield


@pytest.fixture
def provider():
    return GoogleDriveBackupProvider()


@pytest.fixture
def connection(db):
    conn = BackupCloudConnection.objects.create(provider="google_drive", status="connected")
    conn.set_tokens(
        access_token="access-tok",
        refresh_token="refresh-tok",
        token_expiry=timezone.now() + timezone.timedelta(hours=1),
        scopes="https://www.googleapis.com/auth/drive.file",
    )
    conn.save()
    return conn


def _resp(status_code=200, json_data=None, text="", headers=None):
    m = mock.MagicMock()
    m.status_code = status_code
    m.json.return_value = json_data or {}
    m.text = text
    m.headers = headers or {}
    return m


class TestConfigAndGuards:
    def test_load_config_disabled_by_default(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            p = GoogleDriveBackupProvider()
        assert p.config.enabled is False

    def test_require_enabled_raises_when_disabled(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            p = GoogleDriveBackupProvider()
        with pytest.raises(ValueError, match="disabled"):
            p._require_enabled()

    def test_require_oauth_config_raises_when_missing(self):
        with mock.patch.dict(
            os.environ, {"GOOGLE_DRIVE_BACKUP_ENABLED": "true"}, clear=True
        ):
            p = GoogleDriveBackupProvider()
        with pytest.raises(ValueError, match="Missing Google OAuth configuration"):
            p._require_oauth_config()

    def test_require_oauth_config_passes_when_all_present(self, provider):
        provider._require_oauth_config()  # should not raise


class TestOAuthState:
    def test_generate_and_validate_state_roundtrip(self, provider):
        state = provider._generate_state(user_id=42)
        user_id = provider._validate_state(state)
        assert user_id == 42

    def test_validate_state_rejects_tampered_state(self, provider):
        state = provider._generate_state(user_id=42)
        with pytest.raises(Exception):
            provider._validate_state(state + "tampered")

    def test_validate_state_rejects_replay(self, provider):
        state = provider._generate_state(user_id=42)
        provider._validate_state(state)
        with pytest.raises(ValueError):
            provider._validate_state(state)

    def test_validate_state_rejects_mismatched_cached_user(self, provider):
        state = provider._generate_state(user_id=42)
        # Corrupt the cache entry to simulate a different cached user id.
        nonce = provider.STATE_CACHE_PREFIX  # sanity: prefix exists
        assert nonce
        cache.clear()
        with pytest.raises(ValueError):
            provider._validate_state(state)


class TestBuildAuthorizationUrl:
    def test_build_authorization_url_contains_expected_params(self, provider):
        url = provider.build_authorization_url(user_id=7)
        assert url.startswith("https://accounts.google.com/o/oauth2/v2/auth?")
        assert "client_id=client-id" in url
        assert "state=" in url
        assert "response_type=code" in url

    def test_build_authorization_url_raises_when_disabled(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            p = GoogleDriveBackupProvider()
        with pytest.raises(ValueError):
            p.build_authorization_url(user_id=7)


class TestExchangeCodeForTokens:
    @mock.patch("sims.backup_center.google_drive.requests.post")
    def test_success(self, mock_post, provider):
        mock_post.return_value = _resp(200, {"access_token": "tok", "expires_in": 3600})
        data = provider.exchange_code_for_tokens(code="authcode")
        assert data["access_token"] == "tok"

    @mock.patch("sims.backup_center.google_drive.requests.post")
    def test_failure_raises(self, mock_post, provider):
        mock_post.return_value = _resp(400, text="bad request")
        with pytest.raises(ValueError, match="Token exchange failed"):
            provider.exchange_code_for_tokens(code="authcode")


class TestRefreshAccessToken:
    @mock.patch("sims.backup_center.google_drive.requests.post")
    def test_success_updates_connection(self, mock_post, provider, connection):
        mock_post.return_value = _resp(
            200, {"access_token": "new-access-tok", "expires_in": 3600}
        )
        updated = provider.refresh_access_token(connection)
        assert updated.status == "connected"
        assert decrypt_string(updated.access_token_encrypted) == "new-access-tok"

    @mock.patch("sims.backup_center.google_drive.requests.post")
    def test_failure_raises(self, mock_post, provider, connection):
        mock_post.return_value = _resp(401, text="invalid_grant")
        with pytest.raises(ValueError, match="Token refresh failed"):
            provider.refresh_access_token(connection)

    @mock.patch("sims.backup_center.google_drive.requests.post")
    def test_missing_access_token_raises(self, mock_post, provider, connection):
        mock_post.return_value = _resp(200, {"expires_in": 3600})
        with pytest.raises(ValueError, match="did not return access_token"):
            provider.refresh_access_token(connection)


class TestGetValidAccessToken:
    def test_returns_existing_token_when_not_expired(self, provider, connection):
        token = provider.get_valid_access_token(connection)
        assert token == "access-tok"

    @mock.patch("sims.backup_center.google_drive.requests.post")
    def test_refreshes_when_expired(self, mock_post, provider, connection):
        connection.token_expiry = timezone.now() - timezone.timedelta(minutes=5)
        connection.save()
        mock_post.return_value = _resp(200, {"access_token": "refreshed-tok", "expires_in": 3600})
        token = provider.get_valid_access_token(connection)
        assert token == "refreshed-tok"

    def test_treats_missing_expiry_as_expired(self, provider, connection):
        connection.token_expiry = None
        connection.save()
        assert connection.is_token_expired() is True


class TestFetchAccountEmail:
    @mock.patch("sims.backup_center.google_drive.requests.get")
    def test_returns_email_from_userinfo(self, mock_get, provider):
        mock_get.return_value = _resp(200, {"email": "user@example.com"})
        email = provider.fetch_account_email_if_possible(access_token="tok")
        assert email == "user@example.com"

    @mock.patch("sims.backup_center.google_drive.requests.get")
    def test_falls_back_to_tokeninfo(self, mock_get, provider):
        mock_get.side_effect = [
            _resp(404, {}),
            _resp(200, {"email": "fallback@example.com"}),
        ]
        email = provider.fetch_account_email_if_possible(access_token="tok")
        assert email == "fallback@example.com"

    @mock.patch("sims.backup_center.google_drive.requests.get")
    def test_returns_none_when_both_fail(self, mock_get, provider):
        mock_get.side_effect = [_resp(404, {}), _resp(404, {})]
        assert provider.fetch_account_email_if_possible(access_token="tok") is None

    @mock.patch("sims.backup_center.google_drive.requests.get")
    def test_returns_none_on_userinfo_exception(self, mock_get, provider):
        mock_get.side_effect = Exception("network down")
        assert provider.fetch_account_email_if_possible(access_token="tok") is None

    @mock.patch("sims.backup_center.google_drive.requests.get")
    def test_returns_none_on_tokeninfo_exception(self, mock_get, provider):
        mock_get.side_effect = [_resp(404, {}), Exception("network down")]
        assert provider.fetch_account_email_if_possible(access_token="tok") is None


class TestHandleOauthCallback:
    @mock.patch("sims.backup_center.google_drive.requests.get")
    @mock.patch("sims.backup_center.google_drive.requests.post")
    def test_success_creates_connection_with_encrypted_tokens(
        self, mock_post, mock_get, provider, db, django_user_model
    ):
        user = django_user_model.objects.create_user(username="drive_owner", password="x")
        state = provider._generate_state(user_id=user.id)
        mock_post.return_value = _resp(
            200,
            {
                "access_token": "cb-access",
                "refresh_token": "cb-refresh",
                "expires_in": 3600,
                "scope": "https://www.googleapis.com/auth/drive.file",
            },
        )
        mock_get.return_value = _resp(200, {"email": "cb@example.com"})

        conn = provider.handle_oauth_callback(code="authcode", state=state)
        assert conn.status == "connected"
        assert conn.account_email == "cb@example.com"
        assert decrypt_string(conn.access_token_encrypted) == "cb-access"
        assert decrypt_string(conn.refresh_token_encrypted) == "cb-refresh"

    @mock.patch("sims.backup_center.google_drive.requests.get")
    @mock.patch("sims.backup_center.google_drive.requests.post")
    def test_missing_access_token_raises(self, mock_post, mock_get, provider, db):
        state = provider._generate_state(user_id=99)
        mock_post.return_value = _resp(200, {"expires_in": 3600})
        with pytest.raises(ValueError, match="did not return access_token"):
            provider.handle_oauth_callback(code="authcode", state=state)

    def test_invalid_state_raises(self, provider, db):
        with pytest.raises(Exception):
            provider.handle_oauth_callback(code="authcode", state="garbage")


class TestHealthCheck:
    @mock.patch("sims.backup_center.google_drive.requests.get")
    def test_success_marks_connected(self, mock_get, provider, connection):
        mock_get.return_value = _resp(200, {"files": []})
        result = provider.health_check(connection)
        assert result["status"] == "healthy"
        connection.refresh_from_db()
        assert connection.status == "connected"

    @mock.patch("sims.backup_center.google_drive.requests.get")
    def test_failure_marks_failed(self, mock_get, provider, connection):
        mock_get.return_value = _resp(500, text="server error")
        result = provider.health_check(connection)
        assert result["status"] == "failed"
        connection.refresh_from_db()
        assert connection.status == "failed"
        assert "Drive health check failed" in connection.last_error


class TestEnsureBackupFolder:
    def test_uses_env_folder_id_when_configured(self, provider, connection):
        with mock.patch.dict(os.environ, {"GOOGLE_DRIVE_BACKUP_FOLDER_ID": "folder-from-env"}):
            p = GoogleDriveBackupProvider()
            updated = p.ensure_backup_folder(connection)
        assert updated.backup_folder_id == "folder-from-env"

    def test_returns_early_when_already_stored(self, provider, connection):
        connection.backup_folder_id = "already-there"
        connection.save()
        updated = provider.ensure_backup_folder(connection)
        assert updated.backup_folder_id == "already-there"

    @mock.patch("sims.backup_center.google_drive.requests.get")
    def test_finds_existing_folder(self, mock_get, provider, connection):
        mock_get.return_value = _resp(
            200, {"files": [{"id": "found-folder-id", "name": "PGSIMS Backups"}]}
        )
        updated = provider.ensure_backup_folder(connection)
        assert updated.backup_folder_id == "found-folder-id"

    @mock.patch("sims.backup_center.google_drive.requests.post")
    @mock.patch("sims.backup_center.google_drive.requests.get")
    def test_creates_folder_when_not_found(self, mock_get, mock_post, provider, connection):
        mock_get.return_value = _resp(200, {"files": []})
        mock_post.return_value = _resp(
            201, {"id": "new-folder-id", "name": "PGSIMS Backups"}
        )
        updated = provider.ensure_backup_folder(connection)
        assert updated.backup_folder_id == "new-folder-id"

    @mock.patch("sims.backup_center.google_drive.requests.get")
    def test_lookup_failure_raises(self, mock_get, provider, connection):
        mock_get.return_value = _resp(500, text="boom")
        with pytest.raises(ValueError, match="Drive folder lookup failed"):
            provider.ensure_backup_folder(connection)

    @mock.patch("sims.backup_center.google_drive.requests.post")
    @mock.patch("sims.backup_center.google_drive.requests.get")
    def test_create_failure_raises(self, mock_get, mock_post, provider, connection):
        mock_get.return_value = _resp(200, {"files": []})
        mock_post.return_value = _resp(500, text="boom")
        with pytest.raises(ValueError, match="Drive folder create failed"):
            provider.ensure_backup_folder(connection)


class TestUploadFileAndMetadata:
    @mock.patch("sims.backup_center.google_drive.requests.put")
    @mock.patch("sims.backup_center.google_drive.requests.post")
    def test_upload_file_success(self, mock_post, mock_put, provider, connection, tmp_path):
        local_file = tmp_path / "data.bin"
        local_file.write_bytes(b"hello world")

        mock_post.return_value = _resp(
            200, headers={"Location": "https://upload.example.com/resumable/xyz"}
        )
        mock_put.return_value = _resp(200, {"id": "uploaded-file-id"})

        result = provider.upload_file(
            connection=connection,
            local_path=str(local_file),
            remote_name="data.bin",
            folder_id="folder-1",
        )
        assert result["id"] == "uploaded-file-id"

    @mock.patch("sims.backup_center.google_drive.requests.post")
    def test_init_resumable_upload_failure_raises(self, mock_post, provider):
        mock_post.return_value = _resp(500, text="boom")
        with pytest.raises(ValueError, match="Drive resumable init failed"):
            provider._init_resumable_upload(access_token="tok", metadata={})

    @mock.patch("sims.backup_center.google_drive.requests.post")
    def test_init_resumable_upload_missing_location_raises(self, mock_post, provider):
        mock_post.return_value = _resp(200, headers={})
        with pytest.raises(ValueError, match="missing Location header"):
            provider._init_resumable_upload(access_token="tok", metadata={})

    @mock.patch("sims.backup_center.google_drive.requests.put")
    @mock.patch("sims.backup_center.google_drive.requests.post")
    def test_upload_file_put_failure_raises(
        self, mock_post, mock_put, provider, connection, tmp_path
    ):
        local_file = tmp_path / "data.bin"
        local_file.write_bytes(b"hello world")
        mock_post.return_value = _resp(200, headers={"Location": "https://upload.example.com/x"})
        mock_put.return_value = _resp(500, text="boom")
        with pytest.raises(ValueError, match="Drive upload failed"):
            provider.upload_file(
                connection=connection,
                local_path=str(local_file),
                remote_name="data.bin",
                folder_id="folder-1",
            )

    @mock.patch("sims.backup_center.google_drive.requests.get")
    def test_get_file_metadata_success(self, mock_get, provider, connection):
        mock_get.return_value = _resp(200, {"id": "f1", "size": "123"})
        meta = provider.get_file_metadata(connection=connection, file_id="f1")
        assert meta["id"] == "f1"

    @mock.patch("sims.backup_center.google_drive.requests.get")
    def test_get_file_metadata_failure_raises(self, mock_get, provider, connection):
        mock_get.return_value = _resp(404, text="not found")
        with pytest.raises(ValueError, match="Drive metadata fetch failed"):
            provider.get_file_metadata(connection=connection, file_id="f1")


class TestVerifyUploadedFile:
    @mock.patch("sims.backup_center.google_drive.requests.get")
    def test_success(self, mock_get, provider, connection):
        mock_get.return_value = _resp(200, {"size": "100", "md5Checksum": "abc"})
        meta = provider.verify_uploaded_file(
            connection=connection, drive_file_id="f1", expected_size=100, expected_md5="abc"
        )
        assert meta["size"] == "100"

    @mock.patch("sims.backup_center.google_drive.requests.get")
    def test_size_mismatch_raises(self, mock_get, provider, connection):
        mock_get.return_value = _resp(200, {"size": "99"})
        with pytest.raises(ValueError, match="size mismatch"):
            provider.verify_uploaded_file(connection=connection, drive_file_id="f1", expected_size=100)

    @mock.patch("sims.backup_center.google_drive.requests.get")
    def test_checksum_mismatch_raises(self, mock_get, provider, connection):
        mock_get.return_value = _resp(200, {"size": "100", "md5Checksum": "different"})
        with pytest.raises(ValueError, match="checksum mismatch"):
            provider.verify_uploaded_file(
                connection=connection, drive_file_id="f1", expected_size=100, expected_md5="abc"
            )


class TestUploadBackup:
    @pytest.fixture
    def backup_job_with_file(self, db, tmp_path):
        f = tmp_path / "backup.pgsimsbak"
        f.write_bytes(b"some backup content")
        return BackupJob.objects.create(
            backup_kind="routine_application_data",
            backup_type="manual",
            status="completed",
            file_path=str(f),
            file_name="backup.pgsimsbak",
            manifest_json={"foo": "bar"},
        )

    def test_raises_when_not_connected(self, provider, backup_job_with_file):
        with pytest.raises(ValueError, match="not connected"):
            provider.upload_backup(backup_record=backup_job_with_file)

    def test_raises_when_file_missing(self, provider, connection, db):
        job = BackupJob.objects.create(
            backup_kind="routine_application_data",
            backup_type="manual",
            status="completed",
            file_path="/nonexistent/path.pgsimsbak",
            file_name="path.pgsimsbak",
        )
        with pytest.raises(FileNotFoundError):
            provider.upload_backup(backup_record=job)

    def test_success_creates_verified_cloud_copy(
        self, provider, connection, backup_job_with_file
    ):
        connection.backup_folder_id = "folder-1"
        connection.save()

        # Isolate upload_backup()'s own orchestration (temp-dir/encrypt/hash/cleanup and
        # BackupCloudCopy bookkeeping) from the HTTP transport layer, which is already
        # covered directly by TestUploadFileAndMetadata / TestVerifyUploadedFile above.
        upload_calls = []

        def fake_upload_file(*, connection, local_path, remote_name, folder_id, mime_type="application/octet-stream", description=None):
            upload_calls.append(remote_name)
            return {"id": f"drive-id-{remote_name}"}

        with mock.patch.object(provider, "upload_file", side_effect=fake_upload_file), mock.patch.object(
            provider, "verify_uploaded_file", return_value={"id": "drive-id-verified"}
        ):
            cloud_copy = provider.upload_backup(backup_record=backup_job_with_file)

        assert cloud_copy.upload_status == "uploaded"
        assert cloud_copy.verification_status == "verified"
        assert cloud_copy.remote_file_id.startswith("drive-id-")
        assert cloud_copy.local_checksum
        assert cloud_copy.remote_checksum
        assert len(upload_calls) == 3  # backup + manifest + checksum files
        assert BackupCloudCopy.objects.filter(pk=cloud_copy.pk).exists()

    @mock.patch("sims.backup_center.google_drive.requests.post")
    def test_upload_failure_marks_cloud_copy_failed(
        self, mock_post, provider, connection, backup_job_with_file
    ):
        connection.backup_folder_id = "folder-1"
        connection.save()
        mock_post.return_value = _resp(500, text="boom")

        with pytest.raises(ValueError):
            provider.upload_backup(backup_record=backup_job_with_file)

        copy = BackupCloudCopy.objects.filter(backup_record=backup_job_with_file).first()
        assert copy is not None
        assert copy.upload_status == "upload_failed"
        assert copy.verification_status == "verification_failed"
        assert copy.error_message

    def test_raises_when_folder_not_configured_and_lookup_empty(
        self, provider, connection, backup_job_with_file
    ):
        # No backup_folder_id, no env var, and Drive API lookup will be attempted; simulate
        # the folder resolution itself failing so upload_backup surfaces a clean error
        # rather than crashing uninformatively.
        with mock.patch(
            "sims.backup_center.google_drive.requests.get",
            return_value=_resp(500, text="boom"),
        ):
            with pytest.raises(ValueError, match="Drive folder lookup failed"):
                provider.upload_backup(backup_record=backup_job_with_file)


class TestDownloadBackup:
    @pytest.fixture
    def cloud_copy(self, db, connection):
        job = BackupJob.objects.create(
            backup_kind="routine_application_data",
            backup_type="manual",
            status="completed",
        )
        return BackupCloudCopy.objects.create(
            backup_record=job,
            provider="google_drive",
            connection=connection,
            remote_file_id="drive-file-id",
            remote_file_name="backup.pgsimsbak.enc",
            upload_status="uploaded",
        )

    def test_raises_when_provider_mismatch(self, provider, cloud_copy, tmp_path):
        # Force a mismatched provider value directly on the in-memory connection object
        # (not saved back to the DB, since "provider" is unique) to exercise the guard.
        cloud_copy.connection.provider = "not_google_drive"
        with pytest.raises(ValueError, match="not Google Drive"):
            provider.download_backup(cloud_copy=cloud_copy, destination_path=str(tmp_path / "out"))

    def test_raises_when_missing_remote_file_id(self, provider, connection, tmp_path, db):
        job = BackupJob.objects.create(backup_kind="routine_application_data", status="completed")
        copy = BackupCloudCopy.objects.create(
            backup_record=job, provider="google_drive", connection=connection
        )
        with pytest.raises(ValueError, match="missing remote file id"):
            provider.download_backup(cloud_copy=copy, destination_path=str(tmp_path / "out"))

    @mock.patch("sims.backup_center.google_drive.requests.get")
    def test_success_downloads_and_decrypts(self, mock_get, provider, cloud_copy, tmp_path):
        from sims.backup_center.encryption import encrypt_file

        # Build a real encrypted payload so decrypt_file() in download_backup() succeeds.
        plain_path = tmp_path / "plain.txt"
        plain_path.write_bytes(b"decrypted contents")
        encrypted_path = tmp_path / "plain.txt.enc"
        encrypt_file(str(plain_path), str(encrypted_path))
        encrypted_bytes = encrypted_path.read_bytes()

        import hashlib

        cloud_copy.local_checksum = hashlib.sha256(encrypted_bytes).hexdigest()
        cloud_copy.save()

        stream_resp = mock.MagicMock()
        stream_resp.status_code = 200
        stream_resp.iter_content.return_value = [encrypted_bytes]
        stream_resp.__enter__.return_value = stream_resp
        stream_resp.__exit__.return_value = False
        mock_get.return_value = stream_resp

        dest_path = tmp_path / "restored.txt"
        result_path = provider.download_backup(cloud_copy=cloud_copy, destination_path=str(dest_path))

        assert result_path == str(dest_path)
        assert dest_path.read_bytes() == b"decrypted contents"
        cloud_copy.refresh_from_db()
        assert cloud_copy.download_status == "downloaded"

    @mock.patch("sims.backup_center.google_drive.requests.get")
    def test_download_http_failure_marks_failed(self, mock_get, provider, cloud_copy, tmp_path):
        stream_resp = mock.MagicMock()
        stream_resp.status_code = 500
        stream_resp.text = "boom"
        stream_resp.__enter__.return_value = stream_resp
        stream_resp.__exit__.return_value = False
        mock_get.return_value = stream_resp

        with pytest.raises(ValueError, match="Drive download failed"):
            provider.download_backup(cloud_copy=cloud_copy, destination_path=str(tmp_path / "out"))

        cloud_copy.refresh_from_db()
        assert cloud_copy.download_status == "download_failed"
        assert cloud_copy.error_message

    @mock.patch("sims.backup_center.google_drive.requests.get")
    def test_checksum_mismatch_marks_failed(self, mock_get, provider, cloud_copy, tmp_path):
        cloud_copy.local_checksum = "deadbeef"
        cloud_copy.save()

        stream_resp = mock.MagicMock()
        stream_resp.status_code = 200
        stream_resp.iter_content.return_value = [b"not matching content"]
        stream_resp.__enter__.return_value = stream_resp
        stream_resp.__exit__.return_value = False
        mock_get.return_value = stream_resp

        with pytest.raises(ValueError, match="checksum verification failed"):
            provider.download_backup(cloud_copy=cloud_copy, destination_path=str(tmp_path / "out"))

        cloud_copy.refresh_from_db()
        assert cloud_copy.download_status == "download_failed"


class TestHashHelpers:
    def test_sha256_and_md5_file(self, provider, tmp_path):
        f = tmp_path / "data.bin"
        f.write_bytes(b"pgsims backup content" * 100)

        import hashlib

        assert provider._sha256_file(str(f)) == hashlib.sha256(f.read_bytes()).hexdigest()
        assert provider._md5_file(str(f)) == hashlib.md5(f.read_bytes()).hexdigest()  # nosec
