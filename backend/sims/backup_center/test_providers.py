"""Tests for sims/backup_center/providers.py — previously 0% covered.

Covers LocalBackupStorageProvider (the default, always-active provider) fully, and the
get_storage_provider() dispatcher / _get_keys() path-building logic for the GCS and S3 providers
without requiring the optional boto3/google-cloud-storage packages to be installed — those are only
imported lazily inside _get_client(), which these tests deliberately don't exercise.
"""

import os
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
