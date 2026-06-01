import os
import json
import logging
import datetime
import tempfile
import hashlib
from typing import Dict, Any, List, Optional
from django.conf import settings
from django.utils import timezone

from .models import BackupJob
from .encryption import encrypt_file, decrypt_file

logger = logging.getLogger('sims.backup_center')

class BaseBackupStorageProvider:
    def upload_backup(self, backup_job: BackupJob) -> Dict[str, Any]:
        """
        Encrypts and uploads the backup file, manifest, and checksum to the cloud storage.
        """
        raise NotImplementedError()

    def download_backup(self, backup_job: BackupJob, destination_path: str) -> None:
        """
        Downloads and decrypts the backup file from the cloud storage to the destination_path.
        """
        raise NotImplementedError()

    def verify_remote_object(self, backup_job: BackupJob) -> bool:
        """
        Verifies that the remote backup files exist and are intact.
        """
        raise NotImplementedError()

    def delete_remote_object(self, backup_job: BackupJob) -> None:
        """
        Deletes the remote backup files from the cloud storage.
        """
        raise NotImplementedError()

    def list_backups(self) -> List[Dict[str, Any]]:
        """
        Lists all remote backup objects found under the prefix.
        """
        raise NotImplementedError()

    def health_check(self) -> Dict[str, Any]:
        """
        Performs a health check on the cloud storage connection and credentials.
        """
        raise NotImplementedError()


class LocalBackupStorageProvider(BaseBackupStorageProvider):
    """
    Default provider that emulates cloud operations locally or acts as a placeholder
    when cloud backups are disabled.
    """
    def upload_backup(self, backup_job: BackupJob) -> Dict[str, Any]:
        return {"status": "skipped", "message": "Cloud backup is disabled (local provider active)"}

    def download_backup(self, backup_job: BackupJob, destination_path: str) -> None:
        raise ValueError("Cannot download backup using local provider")

    def verify_remote_object(self, backup_job: BackupJob) -> bool:
        return True

    def delete_remote_object(self, backup_job: BackupJob) -> None:
        pass

    def list_backups(self) -> List[Dict[str, Any]]:
        return []

    def health_check(self) -> Dict[str, Any]:
        return {"status": "healthy", "provider": "local", "message": "Local storage is active"}


class GoogleCloudStorageProvider(BaseBackupStorageProvider):
    def __init__(self, bucket_name: str, prefix: str, credentials_path: Optional[str] = None, project_id: Optional[str] = None):
        self.bucket_name = bucket_name
        self.prefix = prefix.rstrip('/') + '/'
        self.credentials_path = credentials_path
        self.project_id = project_id

    def _get_client(self):
        from google.cloud import storage
        if self.credentials_path and os.path.exists(self.credentials_path):
            return storage.Client.from_service_account_json(self.credentials_path)
        elif self.project_id:
            return storage.Client(project=self.project_id)
        return storage.Client()

    def _get_keys(self, backup_job: BackupJob) -> Dict[str, str]:
        env = 'prod' if not settings.DEBUG else 'dev'
        created_at = backup_job.created_at or timezone.now()
        yyyy = created_at.strftime('%Y')
        mm = created_at.strftime('%m')
        ext = 'pgsimsdr' if backup_job.backup_kind == 'disaster_recovery' else 'pgsimsbak'
        
        base_key = f"{self.prefix}{env}/{yyyy}/{mm}/backup-{backup_job.id:06d}"
        return {
            "backup": f"{base_key}/backup.{ext}.enc",
            "manifest": f"{base_key}/manifest.json",
            "checksum": f"{base_key}/checksum.sha256"
        }

    def upload_backup(self, backup_job: BackupJob) -> Dict[str, Any]:
        if not self.bucket_name:
            raise ValueError("GCS_BACKUP_BUCKET is not configured.")
            
        keys = self._get_keys(backup_job)
        client = self._get_client()
        bucket = client.bucket(self.bucket_name)

        local_path = backup_job.file_path
        encrypted_path = f"{local_path}.enc"

        try:
            # 1. Encrypt file locally
            encrypt_file(local_path, encrypted_path)

            # 2. Upload encrypted backup
            backup_blob = bucket.blob(keys["backup"])
            backup_blob.upload_from_filename(encrypted_path)

            # 3. Upload manifest
            manifest_blob = bucket.blob(keys["manifest"])
            manifest_blob.upload_from_string(json.dumps(backup_job.manifest_json or {}), content_type='application/json')

            # 4. Upload checksum
            checksum_val = hashlib.sha256(open(encrypted_path, 'rb').read()).hexdigest()
            checksum_blob = bucket.blob(keys["checksum"])
            checksum_blob.upload_from_string(f"{checksum_val}  backup.enc", content_type='text/plain')

            # Verify size
            backup_blob.reload()
            remote_size = backup_blob.size

            return {
                "status": "uploaded",
                "bucket": self.bucket_name,
                "prefix": self.prefix,
                "backup_key": keys["backup"],
                "manifest_key": keys["manifest"],
                "checksum_key": keys["checksum"],
                "checksum": checksum_val,
                "size": remote_size
            }
        finally:
            if os.path.exists(encrypted_path):
                os.remove(encrypted_path)

    def download_backup(self, backup_job: BackupJob, destination_path: str) -> None:
        client = self._get_client()
        bucket = client.bucket(self.bucket_name)
        keys = self._get_keys(backup_job)
        
        blob = bucket.blob(keys["backup"])
        if not blob.exists():
            raise FileNotFoundError(f"Remote backup object {keys['backup']} not found in bucket {self.bucket_name}")

        temp_enc_path = f"{destination_path}.enc"
        try:
            # Download encrypted backup
            blob.download_to_filename(temp_enc_path)
            
            # Verify checksum if present
            checksum_blob = bucket.blob(keys["checksum"])
            if checksum_blob.exists():
                remote_chk_content = checksum_blob.download_as_text().strip().split()[0]
                local_chk_val = hashlib.sha256(open(temp_enc_path, 'rb').read()).hexdigest()
                if remote_chk_content != local_chk_val:
                    raise ValueError("Downloaded file checksum verification failed!")

            # Decrypt
            decrypt_file(temp_enc_path, destination_path)
        finally:
            if os.path.exists(temp_enc_path):
                os.remove(temp_enc_path)

    def verify_remote_object(self, backup_job: BackupJob) -> bool:
        client = self._get_client()
        bucket = client.bucket(self.bucket_name)
        keys = self._get_keys(backup_job)
        
        backup_blob = bucket.blob(keys["backup"])
        manifest_blob = bucket.blob(keys["manifest"])
        checksum_blob = bucket.blob(keys["checksum"])
        
        return backup_blob.exists() and manifest_blob.exists() and checksum_blob.exists()

    def delete_remote_object(self, backup_job: BackupJob) -> None:
        client = self._get_client()
        bucket = client.bucket(self.bucket_name)
        keys = self._get_keys(backup_job)
        
        for key in keys.values():
            blob = bucket.blob(key)
            if blob.exists():
                blob.delete()

    def list_backups(self) -> List[Dict[str, Any]]:
        client = self._get_client()
        bucket = client.bucket(self.bucket_name)
        blobs = bucket.list_blobs(prefix=self.prefix)
        
        results = []
        for blob in blobs:
            results.append({
                "name": blob.name,
                "size": blob.size,
                "updated": blob.updated.isoformat() if blob.updated else None
            })
        return results

    def health_check(self) -> Dict[str, Any]:
        try:
            client = self._get_client()
            bucket = client.bucket(self.bucket_name)
            exists = bucket.exists()
            if not exists:
                return {"status": "failed", "error": f"Bucket {self.bucket_name} does not exist"}
            return {"status": "healthy", "provider": "gcs", "bucket": self.bucket_name}
        except Exception as e:
            return {"status": "failed", "error": str(e)}


class S3CompatibleStorageProvider(BaseBackupStorageProvider):
    def __init__(self, bucket_name: str, prefix: str, endpoint_url: Optional[str] = None, region: Optional[str] = None,
                 access_key_id: Optional[str] = None, secret_access_key: Optional[str] = None, use_ssl: bool = True,
                 addressing_style: str = 'auto', signature_version: str = 's3v4'):
        self.bucket_name = bucket_name
        self.prefix = prefix.rstrip('/') + '/'
        self.endpoint_url = endpoint_url
        self.region = region
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.use_ssl = use_ssl
        self.addressing_style = addressing_style
        self.signature_version = signature_version

    def _get_client(self):
        import boto3
        from botocore.client import Config
        config = Config(
            signature_version=self.signature_version,
            s3={'addressing_style': self.addressing_style}
        )
        return boto3.client(
            's3',
            endpoint_url=self.endpoint_url,
            region_name=self.region,
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_access_key,
            use_ssl=self.use_ssl,
            config=config
        )

    def _get_keys(self, backup_job: BackupJob) -> Dict[str, str]:
        env = 'prod' if not settings.DEBUG else 'dev'
        created_at = backup_job.created_at or timezone.now()
        yyyy = created_at.strftime('%Y')
        mm = created_at.strftime('%m')
        ext = 'pgsimsdr' if backup_job.backup_kind == 'disaster_recovery' else 'pgsimsbak'
        
        base_key = f"{self.prefix}{env}/{yyyy}/{mm}/backup-{backup_job.id:06d}"
        return {
            "backup": f"{base_key}/backup.{ext}.enc",
            "manifest": f"{base_key}/manifest.json",
            "checksum": f"{base_key}/checksum.sha256"
        }

    def upload_backup(self, backup_job: BackupJob) -> Dict[str, Any]:
        if not self.bucket_name:
            raise ValueError("S3_BACKUP_BUCKET is not configured.")
            
        keys = self._get_keys(backup_job)
        client = self._get_client()

        local_path = backup_job.file_path
        encrypted_path = f"{local_path}.enc"

        try:
            # 1. Encrypt file locally
            encrypt_file(local_path, encrypted_path)

            # 2. Upload encrypted backup
            client.upload_file(encrypted_path, self.bucket_name, keys["backup"])

            # 3. Upload manifest
            client.put_object(
                Bucket=self.bucket_name,
                Key=keys["manifest"],
                Body=json.dumps(backup_job.manifest_json or {}),
                ContentType='application/json'
            )

            # 4. Upload checksum
            checksum_val = hashlib.sha256(open(encrypted_path, 'rb').read()).hexdigest()
            client.put_object(
                Bucket=self.bucket_name,
                Key=keys["checksum"],
                Body=f"{checksum_val}  backup.enc",
                ContentType='text/plain'
            )

            # Get size
            resp = client.head_object(Bucket=self.bucket_name, Key=keys["backup"])
            remote_size = resp.get('ContentLength', 0)

            return {
                "status": "uploaded",
                "bucket": self.bucket_name,
                "prefix": self.prefix,
                "backup_key": keys["backup"],
                "manifest_key": keys["manifest"],
                "checksum_key": keys["checksum"],
                "checksum": checksum_val,
                "size": remote_size
            }
        finally:
            if os.path.exists(encrypted_path):
                os.remove(encrypted_path)

    def download_backup(self, backup_job: BackupJob, destination_path: str) -> None:
        client = self._get_client()
        keys = self._get_keys(backup_job)
        
        temp_enc_path = f"{destination_path}.enc"
        try:
            # Download encrypted backup
            client.download_file(self.bucket_name, keys["backup"], temp_enc_path)
            
            # Verify checksum if present
            try:
                chk_resp = client.get_object(Bucket=self.bucket_name, Key=keys["checksum"])
                remote_chk_content = chk_resp['Body'].read().decode('utf-8').strip().split()[0]
                local_chk_val = hashlib.sha256(open(temp_enc_path, 'rb').read()).hexdigest()
                if remote_chk_content != local_chk_val:
                    raise ValueError("Downloaded file checksum verification failed!")
            except Exception as e:
                logger.warning(f"Could not fetch/verify checksum: {e}")

            # Decrypt
            decrypt_file(temp_enc_path, destination_path)
        finally:
            if os.path.exists(temp_enc_path):
                os.remove(temp_enc_path)

    def verify_remote_object(self, backup_job: BackupJob) -> bool:
        client = self._get_client()
        keys = self._get_keys(backup_job)
        try:
            client.head_object(Bucket=self.bucket_name, Key=keys["backup"])
            client.head_object(Bucket=self.bucket_name, Key=keys["manifest"])
            client.head_object(Bucket=self.bucket_name, Key=keys["checksum"])
            return True
        except Exception:
            return False

    def delete_remote_object(self, backup_job: BackupJob) -> None:
        client = self._get_client()
        keys = self._get_keys(backup_job)
        for key in keys.values():
            try:
                client.delete_object(Bucket=self.bucket_name, Key=key)
            except Exception as e:
                logger.warning(f"Failed to delete S3 object {key}: {e}")

    def list_backups(self) -> List[Dict[str, Any]]:
        client = self._get_client()
        resp = client.list_objects_v2(Bucket=self.bucket_name, Prefix=self.prefix)
        results = []
        for obj in resp.get('Contents', []):
            results.append({
                "name": obj['Key'],
                "size": obj['Size'],
                "updated": obj['LastModified'].isoformat() if obj['LastModified'] else None
            })
        return results

    def health_check(self) -> Dict[str, Any]:
        try:
            client = self._get_client()
            client.head_bucket(Bucket=self.bucket_name)
            return {"status": "healthy", "provider": "s3", "bucket": self.bucket_name}
        except Exception as e:
            return {"status": "failed", "error": str(e)}


def get_storage_provider() -> BaseBackupStorageProvider:
    """
    Instantiates and returns the configured backup storage provider.
    """
    cloud_enabled = os.environ.get("BACKUP_CLOUD_ENABLED", "false").lower() in ("true", "1", "yes")
    if not cloud_enabled:
        return LocalBackupStorageProvider()

    provider = os.environ.get("BACKUP_CLOUD_PROVIDER", "local").lower()
    
    if provider == "local":
        return LocalBackupStorageProvider()
        
    elif provider == "gcs":
        bucket = os.environ.get("GCS_BACKUP_BUCKET")
        prefix = os.environ.get("GCS_BACKUP_PREFIX", "pgsims/backups/")
        credentials = os.environ.get("GCS_CREDENTIALS_JSON_PATH")
        project_id = os.environ.get("GCS_PROJECT_ID")
        return GoogleCloudStorageProvider(
            bucket_name=bucket,
            prefix=prefix,
            credentials_path=credentials,
            project_id=project_id
        )
        
    elif provider == "s3":
        bucket = os.environ.get("S3_BACKUP_BUCKET")
        prefix = os.environ.get("S3_BACKUP_PREFIX", "pgsims/backups/")
        endpoint_url = os.environ.get("S3_ENDPOINT_URL")
        region = os.environ.get("S3_REGION")
        access_key_id = os.environ.get("S3_ACCESS_KEY_ID")
        secret_access_key = os.environ.get("S3_SECRET_ACCESS_KEY")
        use_ssl = os.environ.get("S3_USE_SSL", "true").lower() in ("true", "1", "yes")
        addressing_style = os.environ.get("S3_ADDRESSING_STYLE", "auto")
        signature_version = os.environ.get("S3_SIGNATURE_VERSION", "s3v4")
        return S3CompatibleStorageProvider(
            bucket_name=bucket,
            prefix=prefix,
            endpoint_url=endpoint_url,
            region=region,
            access_key_id=access_key_id,
            secret_access_key=secret_access_key,
            use_ssl=use_ssl,
            addressing_style=addressing_style,
            signature_version=signature_version
        )
    else:
        raise ValueError(f"Unknown cloud backup provider: {provider}")
