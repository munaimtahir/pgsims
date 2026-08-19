"""Tests for sims/backup_center/providers.py — previously 0% covered.

Covers LocalBackupStorageProvider (the default, always-active provider) fully, and the
get_storage_provider() dispatcher / _get_keys() path-building logic for the GCS and S3 providers
without requiring the optional boto3/google-cloud-storage packages to be installed — those are only
imported lazily inside _get_client(), which these tests deliberately don't exercise.
"""

import os
import shutil
import tempfile
from datetime import datetime, timezone
from unittest import mock

import pytest

from sims.backup_center.models import BackupJob
from sims.backup_center.providers import (
    GoogleCloudStorageProvider,
    LocalBackupStorageProvider,
    S3CompatibleStorageProvider,
    get_storage_provider,
)


@pytest.fixture
def backup_job(db):
    return BackupJob.objects.create(
        backup_kind="routine_application_data",
        backup_type="manual",
        status="pending",
    )


@pytest.fixture
def disaster_backup_job(db):
    return BackupJob.objects.create(
        backup_kind="disaster_recovery",
        backup_type="manual",
        status="pending",
    )


class TestLocalBackupStorageProvider:
    def test_upload_backup_reports_skipped(self, backup_job):
        provider = LocalBackupStorageProvider()
        result = provider.upload_backup(backup_job)
        assert result["status"] == "skipped"

    def test_download_backup_raises(self, backup_job):
        provider = LocalBackupStorageProvider()
        with pytest.raises(ValueError):
            provider.download_backup(backup_job, "/tmp/somewhere")

    def test_verify_remote_object_always_true(self, backup_job):
        assert LocalBackupStorageProvider().verify_remote_object(backup_job) is True

    def test_delete_remote_object_is_noop(self, backup_job):
        # Should not raise.
        LocalBackupStorageProvider().delete_remote_object(backup_job)

    def test_list_backups_returns_empty(self):
        assert LocalBackupStorageProvider().list_backups() == []

    def test_health_check_reports_healthy_local(self):
        result = LocalBackupStorageProvider().health_check()
        assert result["status"] == "healthy"
        assert result["provider"] == "local"


class TestGetStorageProvider:
    def test_defaults_to_local_when_cloud_disabled(self):
        with mock.patch.dict(os.environ, {"BACKUP_CLOUD_ENABLED": "false"}, clear=False):
            provider = get_storage_provider()
        assert isinstance(provider, LocalBackupStorageProvider)

    def test_defaults_to_local_when_flag_missing(self):
        env = dict(os.environ)
        env.pop("BACKUP_CLOUD_ENABLED", None)
        with mock.patch.dict(os.environ, env, clear=True):
            provider = get_storage_provider()
        assert isinstance(provider, LocalBackupStorageProvider)

    def test_explicit_local_provider(self):
        with mock.patch.dict(
            os.environ,
            {"BACKUP_CLOUD_ENABLED": "true", "BACKUP_CLOUD_PROVIDER": "local"},
            clear=False,
        ):
            provider = get_storage_provider()
        assert isinstance(provider, LocalBackupStorageProvider)

    def test_gcs_provider_configured_from_env(self):
        with mock.patch.dict(
            os.environ,
            {
                "BACKUP_CLOUD_ENABLED": "true",
                "BACKUP_CLOUD_PROVIDER": "gcs",
                "GCS_BACKUP_BUCKET": "my-bucket",
                "GCS_BACKUP_PREFIX": "pgsims/backups/",
                "GCS_PROJECT_ID": "my-project",
            },
            clear=False,
        ):
            provider = get_storage_provider()
        assert isinstance(provider, GoogleCloudStorageProvider)
        assert provider.bucket_name == "my-bucket"
        assert provider.prefix == "pgsims/backups/"
        assert provider.project_id == "my-project"

    def test_s3_provider_configured_from_env(self):
        with mock.patch.dict(
            os.environ,
            {
                "BACKUP_CLOUD_ENABLED": "true",
                "BACKUP_CLOUD_PROVIDER": "s3",
                "S3_BACKUP_BUCKET": "my-s3-bucket",
                "S3_REGION": "us-east-1",
                "S3_USE_SSL": "false",
            },
            clear=False,
        ):
            provider = get_storage_provider()
        assert isinstance(provider, S3CompatibleStorageProvider)
        assert provider.bucket_name == "my-s3-bucket"
        assert provider.region == "us-east-1"
        assert provider.use_ssl is False

    def test_unknown_provider_raises(self):
        with mock.patch.dict(
            os.environ,
            {"BACKUP_CLOUD_ENABLED": "true", "BACKUP_CLOUD_PROVIDER": "carrier-pigeon"},
            clear=False,
        ):
            with pytest.raises(ValueError):
                get_storage_provider()


class TestGoogleCloudStorageProviderKeys:
    def test_get_keys_uses_routine_extension(self, backup_job):
        provider = GoogleCloudStorageProvider(bucket_name="b", prefix="pgsims/backups")
        keys = provider._get_keys(backup_job)
        assert keys["backup"].endswith(".pgsimsbak.enc")
        assert f"backup-{backup_job.id:06d}" in keys["backup"]
        assert keys["manifest"].endswith("manifest.json")
        assert keys["checksum"].endswith("checksum.sha256")

    def test_get_keys_uses_disaster_recovery_extension(self, disaster_backup_job):
        provider = GoogleCloudStorageProvider(bucket_name="b", prefix="pgsims/backups")
        keys = provider._get_keys(disaster_backup_job)
        assert keys["backup"].endswith(".pgsimsdr.enc")

    def test_upload_backup_requires_bucket_name(self, backup_job):
        provider = GoogleCloudStorageProvider(bucket_name="", prefix="pgsims/backups")
        with pytest.raises(ValueError):
            provider.upload_backup(backup_job)


class TestS3CompatibleStorageProviderKeys:
    def test_get_keys_uses_routine_extension(self, backup_job):
        provider = S3CompatibleStorageProvider(bucket_name="b", prefix="pgsims/backups")
        keys = provider._get_keys(backup_job)
        assert keys["backup"].endswith(".pgsimsbak.enc")
        assert f"backup-{backup_job.id:06d}" in keys["backup"]

    def test_get_keys_uses_disaster_recovery_extension(self, disaster_backup_job):
        provider = S3CompatibleStorageProvider(bucket_name="b", prefix="pgsims/backups")
        keys = provider._get_keys(disaster_backup_job)
        assert keys["backup"].endswith(".pgsimsdr.enc")

    def test_upload_backup_requires_bucket_name(self, backup_job):
        provider = S3CompatibleStorageProvider(bucket_name="", prefix="pgsims/backups")
        with pytest.raises(ValueError):
            provider.upload_backup(backup_job)


class FakeGcsBlob:
    def __init__(self, name, exists=True):
        self.name = name
        self.size = 17
        self.updated = datetime.now(timezone.utc)
        self._exists = exists

    def upload_from_filename(self, path):
        self._exists = True

    def upload_from_string(self, value, **kwargs):
        self._exists = True

    def reload(self):
        return None

    def exists(self):
        return self._exists

    def delete(self):
        self._exists = False

    def download_to_filename(self, path):
        with open(path, "wb") as handle:
            handle.write(b"encrypted")

    def download_as_text(self):
        return "bad-checksum  backup.enc"


class FakeGcsBucket:
    def __init__(self, exists=True):
        self._exists = exists
        self.blobs = {}

    def blob(self, name):
        return self.blobs.setdefault(name, FakeGcsBlob(name, self._exists))

    def exists(self):
        return self._exists

    def list_blobs(self, prefix):
        return [FakeGcsBlob(f"{prefix}one", True), FakeGcsBlob(f"{prefix}two", True)]


class FakeGcsClient:
    def __init__(self, bucket=None):
        self._bucket = bucket or FakeGcsBucket()

    def bucket(self, name):
        return self._bucket


class TestGoogleCloudStorageProviderOperations:
    def test_upload_verify_delete_list_and_health(self, backup_job):
        provider = GoogleCloudStorageProvider("bucket", "prefix")
        with tempfile.NamedTemporaryFile() as source, mock.patch.object(
            backup_job, "file_path", source.name
        ), mock.patch.object(
            provider, "_get_client", return_value=FakeGcsClient()
        ), mock.patch(
            "sims.backup_center.providers.encrypt_file",
            side_effect=lambda src, dst: shutil.copyfile(src, dst),
        ):
            uploaded = provider.upload_backup(backup_job)
            assert uploaded["status"] == "uploaded"
            assert provider.verify_remote_object(backup_job) is True
            assert len(provider.list_backups()) == 2
            provider.delete_remote_object(backup_job)
            assert provider.health_check()["status"] == "healthy"

    def test_download_missing_remote_object_raises(self, backup_job):
        provider = GoogleCloudStorageProvider("bucket", "prefix")
        bucket = FakeGcsBucket(exists=False)
        with mock.patch.object(provider, "_get_client", return_value=FakeGcsClient(bucket)):
            with pytest.raises(FileNotFoundError):
                provider.download_backup(backup_job, "/tmp/gcs-download")

    def test_health_check_reports_missing_bucket_and_client_failure(self):
        provider = GoogleCloudStorageProvider("bucket", "prefix")
        with mock.patch.object(provider, "_get_client", return_value=FakeGcsClient(FakeGcsBucket(False))):
            assert provider.health_check()["status"] == "failed"
        with mock.patch.object(provider, "_get_client", side_effect=RuntimeError("offline")):
            result = provider.health_check()
            assert result["status"] == "failed"
            assert "offline" in result["error"]


class FakeS3Client:
    def __init__(self):
        self.objects = {}

    def upload_file(self, path, bucket, key):
        self.objects[key] = b"encrypted"

    def put_object(self, Bucket, Key, Body, **kwargs):
        self.objects[Key] = Body.encode() if isinstance(Body, str) else Body

    def head_object(self, Bucket, Key):
        if Key not in self.objects:
            raise KeyError(Key)
        return {"ContentLength": len(self.objects[Key])}

    def download_file(self, bucket, key, path):
        with open(path, "wb") as handle:
            handle.write(self.objects[key])

    def get_object(self, Bucket, Key):
        from io import BytesIO
        return {"Body": BytesIO(self.objects[Key])}

    def delete_object(self, Bucket, Key):
        self.objects.pop(Key, None)

    def list_objects_v2(self, Bucket, Prefix):
        return {"Contents": [{"Key": k, "Size": len(v), "LastModified": datetime.now(timezone.utc)} for k, v in self.objects.items() if k.startswith(Prefix)]}

    def head_bucket(self, Bucket):
        return None


class TestS3CompatibleStorageProviderOperations:
    def test_upload_verify_delete_list_and_health(self, backup_job):
        provider = S3CompatibleStorageProvider("bucket", "prefix")
        client = FakeS3Client()
        with tempfile.NamedTemporaryFile() as source, mock.patch.object(
            backup_job, "file_path", source.name
        ), mock.patch.object(provider, "_get_client", return_value=client), mock.patch(
            "sims.backup_center.providers.encrypt_file",
            side_effect=lambda src, dst: shutil.copyfile(src, dst),
        ):
            uploaded = provider.upload_backup(backup_job)
            assert uploaded["status"] == "uploaded"
            assert provider.verify_remote_object(backup_job) is True
            assert provider.list_backups()
            provider.delete_remote_object(backup_job)
            assert provider.health_check()["status"] == "healthy"

    def test_download_and_failed_verification_paths(self, backup_job):
        provider = S3CompatibleStorageProvider("bucket", "prefix")
        client = FakeS3Client()
        keys = provider._get_keys(backup_job)
        client.objects[keys["backup"]] = b"encrypted"
        client.objects[keys["checksum"]] = b"wrong  backup.enc"
        with tempfile.NamedTemporaryFile() as destination, mock.patch.object(
            provider, "_get_client", return_value=client
        ), mock.patch("sims.backup_center.providers.decrypt_file") as decrypt:
            provider.download_backup(backup_job, destination.name)
            decrypt.assert_called_once()
        client.objects.clear()
        assert provider.verify_remote_object(backup_job) is False

    def test_health_check_failure_and_delete_logs(self, backup_job):
        provider = S3CompatibleStorageProvider("bucket", "prefix")
        broken = mock.Mock()
        broken.head_bucket.side_effect = RuntimeError("offline")
        broken.delete_object.side_effect = RuntimeError("delete failed")
        with mock.patch.object(provider, "_get_client", return_value=broken):
            assert provider.health_check()["status"] == "failed"
            provider.delete_remote_object(backup_job)
